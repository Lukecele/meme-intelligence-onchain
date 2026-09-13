import asyncio
from extractors.solana_rpc import SolanaRPCClient

async def main():
    rpc = SolanaRPCClient()
    mint = "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm"
    pagination = None
    for i in range(5):
        page = await rpc.get_transactions_for_address(mint, limit=5, sort_order="asc", transaction_details="full", pagination_token=pagination)
        txs = page.get("data", [])
        pagination = page.get("paginationToken")
        print(f"Page {i}: Got {len(txs)} txs, Next token: {pagination}")
        if not pagination: break
        await asyncio.sleep(0.5)
    await rpc.close()

asyncio.run(main())
