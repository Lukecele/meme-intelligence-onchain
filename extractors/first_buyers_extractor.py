import asyncio, logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from config.settings import DATA_DIR
from config.tokens import HISTORICAL_WINNERS, CONTROL_GROUP_TOKENS
from db.database import Database
from extractors.solana_rpc import SolanaRPCClient

logger = logging.getLogger(__name__)

BLACKLIST = {
    "5Q544fK1y8T1pU2L1s1t7GqL1v2m4j1R5o3P8x9M4j1", 
    "srmqPvymEx5CGtwrqsq6Qq62WNuU7MTgUzhqjL2JNA1", 
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", 
    "11111111111111111111111111111111", 
    "JUP6LkbZbjS1jKKwapdH67yUe35c24aXEMH4VbH6E2yR", 
    "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN", 
    "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8", 
    "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C", 
    "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc",  
    "LBUZKhRxPF3XUpBCjp4BNC5wCKSvq6MNCq6YV6B2w4A",  
}

class FirstBuyersExtractor:
    def __init__(self, db_path: Optional[Path] = None):
        self.db = Database(db_path or DATA_DIR / "onchain_intelligence.db")
        self.rpc = SolanaRPCClient()

    async def close(self):
        await self.rpc.close()

    def _parse_buy_event(self, tx: Dict[str, Any], mint: str) -> Optional[Dict[str, Any]]:
        try:
            meta = tx.get("meta", {})
            if not meta or meta.get("err"): return None
            
            pre_tb = meta.get("preTokenBalances", [])
            post_tb = meta.get("postTokenBalances", [])
            pre_bal = meta.get("preBalances", [])
            post_bal = meta.get("postBalances", [])
            
            tx_msg = tx.get("transaction", {}).get("message", {})
            accounts = tx_msg.get("accountKeys", [])
            if isinstance(accounts, list) and len(accounts) > 0 and isinstance(accounts[0], dict):
                account_pubkeys = [a.get("pubkey") for a in accounts]
            else:
                account_pubkeys = accounts
                
            fee_payer = account_pubkeys[0] if account_pubkeys else None
            if not fee_payer: return None

            pre_tokens = {}
            for t in pre_tb:
                if t.get("mint") == mint:
                    pre_tokens[t.get("owner")] = float(t.get("uiTokenAmount", {}).get("uiAmount") or 0)
            
            post_tokens = {}
            for t in post_tb:
                if t.get("mint") == mint:
                    post_tokens[t.get("owner")] = float(t.get("uiTokenAmount", {}).get("uiAmount") or 0)
            
            buyers = []
            for owner, post_amt in post_tokens.items():
                pre_amt = pre_tokens.get(owner, 0.0)
                if post_amt > pre_amt:
                    buyers.append((owner, post_amt - pre_amt))
            
            if not buyers: return None
            
            valid_buyer = None
            token_delta = 0
            
            for owner, delta in buyers:
                if owner in BLACKLIST:
                    continue
                if owner == fee_payer:
                    valid_buyer = owner
                    token_delta = delta
                    break
                    
            if not valid_buyer:
                for owner, delta in buyers:
                    if owner not in BLACKLIST:
                        valid_buyer = owner
                        token_delta = delta
                        break
                        
            if not valid_buyer: return None
            
            sol_spent = 0
            fee_payer_idx = account_pubkeys.index(fee_payer)
            if fee_payer_idx < len(pre_bal) and fee_payer_idx < len(post_bal):
                diff = pre_bal[fee_payer_idx] - post_bal[fee_payer_idx]
                if diff > 0:
                    sol_spent = diff / 1e9
                    
            if sol_spent <= 0:
                quote_lost = False
                for t in pre_tb:
                    if t.get("owner") == valid_buyer and t.get("mint") != mint:
                        pre_q = float(t.get("uiTokenAmount", {}).get("uiAmount") or 0)
                        post_q = 0
                        for pt in post_tb:
                            if pt.get("owner") == valid_buyer and pt.get("mint") == t.get("mint"):
                                post_q = float(pt.get("uiTokenAmount", {}).get("uiAmount") or 0)
                                break
                        if pre_q > post_q:
                            quote_lost = True
                            break
                if not quote_lost:
                    return None
            
            return {
                "wallet": valid_buyer,
                "amount_tokens": token_delta,
                "amount_sol": sol_spent if sol_spent > 0 else 0
            }
        except Exception as e:
            logger.debug(f"Parse error: {e}")
            return None

    async def process_token(self, token_def: Dict[str, Any], is_winner: bool, limit: int = 1000) -> int:
        mint = token_def["mint"]
        symbol = token_def["symbol"]
        self.db.upsert_token({**token_def, "is_winner": is_winner, "is_control": not is_winner, "source_type": "ONCHAIN", "source_name": "HELIUS_RPC"})
        
        inserted = 0
        launch_ts = int(token_def.get("launch_timestamp") or 0)
        pagination = None
        
        print(f"Fetching Helius RPC for {symbol}...")
        
        max_pages = 50 # Avoid infinite loops on tokens with millions of non-swap early txs (like BONK airdrops)
        pages_fetched = 0
        
        while inserted < limit and pages_fetched < max_pages:
            page = await self.rpc.get_transactions_for_address(mint, limit=100, sort_order="asc", transaction_details="full", pagination_token=pagination)
            pages_fetched += 1
            
            txs = page.get("data", [])
            pagination = page.get("paginationToken")
            
            if not txs:
                break
                
            for row in txs:
                if inserted >= limit: break
                tx_hash = row.get("signature")
                ts = int(row.get("blockTime") or 0)
                
                buy_data = self._parse_buy_event(row, mint)
                if buy_data:
                    wallet = buy_data["wallet"]
                    
                    self.db.upsert_wallet({"address": wallet, "label": None, "first_seen_timestamp": ts, "notes": "Helius verified first buyer"})
                    event_key = f"HELIUS_FIRST_BUYERS:{mint}:{tx_hash}:{wallet}"
                    
                    self.db.insert_trade({
                        "event_key": event_key,
                        "tx_hash": tx_hash,
                        "wallet_address": wallet,
                        "token_mint": mint,
                        "timestamp": ts,
                        "side": "BUY",
                        "amount_tokens": buy_data["amount_tokens"],
                        "amount_sol": buy_data["amount_sol"],
                        "price_usd": 0, 
                        "is_first_buyer": 1,
                        "entry_delay_seconds": max(0, ts - launch_ts) if launch_ts else 0,
                        "source_type": "ONCHAIN",
                        "source_name": "HELIUS_RPC",
                        "source_ref": str(inserted + 1),
                        "raw_json": "{}"
                    })
                    inserted += 1
                    
            if not pagination:
                break
                
            await asyncio.sleep(0.5)
            
        print(f"{symbol}: {inserted} first buyers imported from Helius RPC (Pages: {pages_fetched})")
        return inserted

    async def run(self, limit: int = 1000):
        total = 0
        for token in HISTORICAL_WINNERS:
            total += await self.process_token(token, True, limit)
        for token in CONTROL_GROUP_TOKENS:
            total += await self.process_token(token, False, limit)
        return total

async def main():
    import sys
    limit = 1000
    if len(sys.argv) > 1 and sys.argv[1] == '--limit':
        limit = int(sys.argv[2])
    ext = FirstBuyersExtractor()
    try:
        print(f"Imported {await ext.run(limit)} verified ONCHAIN first-buyer rows")
    finally:
        await ext.close()

if __name__ == "__main__":
    asyncio.run(main())
