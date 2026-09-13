import asyncio
from extractors.solana_rpc import SolanaRPCClient

async def main():
    rpc = SolanaRPCClient()
    mint = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    page = await rpc.get_transactions_for_address(mint, limit=2, sort_order="asc", transaction_details="full")
    tx = page.get("data", [])[1]
    
    meta = tx.get("meta") or {}
    pre = meta.get("preTokenBalances") or []
    post = meta.get("postTokenBalances") or []
    
    print("Pre:", pre)
    print("Post:", post)

if __name__ == "__main__":
    asyncio.run(main())
