import asyncio
import sys
from extractors.solana_rpc import SolanaRPCClient
import logging
logging.basicConfig(level=logging.INFO)

async def main():
    rpc = SolanaRPCClient()
    mint = "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm"
    pagination = None
    for i in range(5):
        print(f"Requesting page {i}...")
        sys.stdout.flush()
        page = await rpc.get_transactions_for_address(mint, limit=100, sort_order="asc", transaction_details="full", pagination_token=pagination)
        if not page:
            print("Failed page", i)
            break
        txs = page.get("data", [])
        pagination = page.get("paginationToken")
        print(f"Page {i}: Got {len(txs)} txs")
        sys.stdout.flush()
        if not pagination: break
        await asyncio.sleep(3)
    await rpc.close()

asyncio.run(main())
