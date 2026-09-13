import asyncio
import logging
import sqlite3
from typing import Dict, Any, Optional
from config.settings import DATA_DIR
from extractors.solana_rpc import SolanaRPCClient

logger = logging.getLogger(__name__)

class SellsTracker:
    def __init__(self):
        self.db_path = DATA_DIR / "onchain_intelligence.db"
        self.rpc = SolanaRPCClient()
        
    async def close(self):
        await self.rpc.close()
        
    def _parse_sell_event(self, tx: Dict[str, Any], target_wallet: str, target_mint: str) -> Optional[Dict[str, Any]]:
        try:
            meta = tx.get("meta", {})
            if meta.get("err"): return None
            
            pre_tb = meta.get("preTokenBalances", [])
            post_tb = meta.get("postTokenBalances", [])
            pre_b = meta.get("preBalances", [])
            post_b = meta.get("postBalances", [])
            
            accounts = tx.get("transaction", {}).get("message", {}).get("accountKeys", [])
            if accounts and isinstance(accounts[0], dict):
                accounts = [a.get("pubkey") for a in accounts]
                
            # SELL condition: Token decreased AND SOL/Quote increased
            # Since we are querying the ATA, target_wallet might not be the direct owner in accountKeys if it's the ATA address,
            # but preTokenBalances has "owner" field!
            
            pre_token = 0.0
            for t in pre_tb:
                if t.get("mint") == target_mint and t.get("owner") == target_wallet:
                    pre_token += float(t.get("uiTokenAmount", {}).get("uiAmount") or 0)
                    
            post_token = 0.0
            for t in post_tb:
                if t.get("mint") == target_mint and t.get("owner") == target_wallet:
                    post_token += float(t.get("uiTokenAmount", {}).get("uiAmount") or 0)
                    
            token_delta = post_token - pre_token
            
            sol_delta = 0.0
            if target_wallet in accounts:
                wallet_idx = accounts.index(target_wallet)
                sol_delta = (post_b[wallet_idx] - pre_b[wallet_idx]) / 1e9 if wallet_idx < len(pre_b) else 0
            
            if token_delta < -0.01 and sol_delta > 0.001:
                return {
                    "amount_tokens": abs(token_delta),
                    "amount_sol": sol_delta
                }
            return None
        except Exception as e:
            return None

    async def run(self):
        print("Starting comprehensive SELL tracking via O(1) ATA targeting...")
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        buys = conn.execute("""
            SELECT t.wallet_address, t.token_mint, t.timestamp, tk.symbol 
            FROM trades t 
            JOIN tokens tk ON tk.mint = t.token_mint
            WHERE t.side='BUY' AND t.is_first_buyer=1 AND t.source_type IN ('ONCHAIN','API') AND tk.is_winner=1
            AND t.wallet_address IN (
                SELECT t2.wallet_address FROM trades t2 JOIN tokens tk2 ON tk2.mint=t2.token_mint 
                WHERE t2.side='BUY' AND t2.is_first_buyer=1 AND tk2.is_winner=1 
                GROUP BY t2.wallet_address HAVING COUNT(DISTINCT t2.token_mint) >= 2
            )
        """).fetchall()
        
        updates = 0
        
        for buy in buys:
            wallet = buy["wallet_address"]
            mint = buy["token_mint"]
            buy_ts = buy["timestamp"]
            
            print(f"Tracking exact exits for wallet {wallet} on token {buy['symbol']}...")
            
            # 1. Get the exact ATA for this wallet + mint
            # We use getParsedTokenAccountsByOwner or getTokenAccountsByOwner
            req = await self.rpc.call("getTokenAccountsByOwner", [
                wallet,
                {"mint": mint},
                {"encoding": "jsonParsed"}
            ])
            
            ata_address = None
            if req and "value" in req and len(req["value"]) > 0:
                ata_address = req["value"][0]["pubkey"]
                
            if not ata_address:
                print(f"  -> No ATA found, wallet must have closed it (sold all). Will search main wallet, limit 10.")
                search_address = wallet
                limit = 10
            else:
                search_address = ata_address
                limit = 1000 # ATA has very few transactions, we can get ALL of them instantly!
                
            # 2. Get transactions for the ATA
            page = await self.rpc.get_transactions_for_address(
                search_address, limit=limit, transaction_details="full"
            )
            txs = page.get("data", [])
            
            for tx in txs:
                tx_hash = tx.get("signature")
                ts = int(tx.get("blockTime") or 0)
                if ts <= buy_ts: continue # Sell must happen after buy
                
                sell_data = self._parse_sell_event(tx, wallet, mint)
                if sell_data:
                    conn.execute("""
                        INSERT OR IGNORE INTO trades (
                            event_key, tx_hash, wallet_address, token_mint, timestamp, 
                            side, amount_tokens, amount_sol, source_type, source_name
                        ) VALUES (?, ?, ?, ?, ?, 'SELL', ?, ?, 'ONCHAIN', 'HELIUS_RPC_ATA')
                    """, (f"HELIUS_SELL_ATA:{mint}:{tx_hash}:{wallet}", tx_hash, wallet, mint, ts, sell_data["amount_tokens"], sell_data["amount_sol"]))
                    
                    if conn.total_changes > 0:
                        updates += 1
                        
            await asyncio.sleep(0.3)
                
        print(f"Successfully recorded {updates} REAL on-chain SELL events using Deep ATA indexing.")
        
        conn.execute("""
            UPDATE wallets SET exit_efficiency = (
                SELECT 
                    CASE 
                        WHEN COUNT(t_sell.id) > 0 THEN 0.9 
                        ELSE 0.3 
                    END
                FROM trades t_buy 
                LEFT JOIN trades t_sell ON t_buy.wallet_address = t_sell.wallet_address 
                    AND t_buy.token_mint = t_sell.token_mint AND t_sell.side = 'SELL'
                WHERE t_buy.wallet_address = wallets.address AND t_buy.side = 'BUY'
            )
            WHERE address IN (SELECT wallet_address FROM trades WHERE side='BUY' GROUP BY wallet_address HAVING COUNT(DISTINCT token_mint) >= 2)
        """)
        conn.commit()
        conn.close()

async def main():
    tracker = SellsTracker()
    try:
        await tracker.run()
    finally:
        await tracker.close()

if __name__ == "__main__":
    asyncio.run(main())
