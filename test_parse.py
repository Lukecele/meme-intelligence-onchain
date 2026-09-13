import asyncio
from typing import Dict, Any
from extractors.solana_rpc import SolanaRPCClient

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

async def main():
    rpc = SolanaRPCClient()
    # Test WIF
    mint = "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm"
    page = await rpc.get_transactions_for_address(mint, limit=50, sort_order="asc", transaction_details="full")
    txs = page.get("data", [])
    print(f"Got {len(txs)} txs")
    
    for tx in txs:
        meta = tx.get("meta", {})
        if not meta or meta.get("err"): continue
        
        pre_tb = meta.get("preTokenBalances", [])
        post_tb = meta.get("postTokenBalances", [])
        
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
        
        if not buyers: continue
        
        print("Found token increase for:", buyers)
        
        tx_msg = tx.get("transaction", {}).get("message", {})
        accounts = tx_msg.get("accountKeys", [])
        if isinstance(accounts, list) and len(accounts) > 0 and isinstance(accounts[0], dict):
            account_pubkeys = [a.get("pubkey") for a in accounts]
        else:
            account_pubkeys = accounts
            
        fee_payer = account_pubkeys[0] if account_pubkeys else None
        print("Fee payer:", fee_payer)
        
        valid_buyer = None
        for owner, delta in buyers:
            if owner in BLACKLIST:
                continue
            if owner == fee_payer:
                valid_buyer = owner
                break
                
        if not valid_buyer:
            for owner, delta in buyers:
                if owner not in BLACKLIST:
                    valid_buyer = owner
                    break
        
        print("Valid buyer:", valid_buyer)
        if not valid_buyer: continue
        
        pre_bal = meta.get("preBalances", [])
        post_bal = meta.get("postBalances", [])
        fee_payer_idx = account_pubkeys.index(fee_payer)
        sol_spent = 0
        if fee_payer_idx < len(pre_bal) and fee_payer_idx < len(post_bal):
            diff = pre_bal[fee_payer_idx] - post_bal[fee_payer_idx]
            print(f"Fee payer SOL diff: {diff}")
            if diff > 0:
                sol_spent = diff / 1e9
        
        print("SOL Spent:", sol_spent)
        
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
                        print(f"Lost quote token {t.get('mint')}")
                        quote_lost = True
                        break
            if not quote_lost:
                print("REJECTED: No SOL spent and no quote token lost")
                
    await rpc.close()

asyncio.run(main())
