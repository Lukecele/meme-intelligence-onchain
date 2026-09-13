import asyncio
import logging
from extractors.solana_rpc import SolanaRPCClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    rpc = SolanaRPCClient()
    mint = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    
    # We want to find the very first transactions.
    # By using sort_order="asc", we can get the oldest ones!
    page = await rpc.get_transactions_for_address(mint, limit=10, sort_order="asc", transaction_details="full")
    txs = page.get("data", [])
    
    if not txs:
        print("No txs found.")
        return
        
    for tx in txs:
        sig = tx.get("signature")
        meta = tx.get("meta", {})
        pre = meta.get("preTokenBalances", [])
        post = meta.get("postTokenBalances", [])
        
        print(f"Tx: {sig}")
        for pre_b in pre:
            for post_b in post:
                if pre_b.get("owner") == post_b.get("owner") and pre_b.get("mint") == mint:
                    owner = pre_b.get("owner")
                    pre_amt = float(pre_b.get("uiTokenAmount", {}).get("uiAmount") or 0)
                    post_amt = float(post_b.get("uiTokenAmount", {}).get("uiAmount") or 0)
                    if pre_amt > post_amt:
                        print(f"  {owner} sent {pre_amt - post_amt} BONK")
                    elif post_amt > pre_amt:
                        print(f"  {owner} received {post_amt - pre_amt} BONK")

if __name__ == "__main__":
    asyncio.run(main())
