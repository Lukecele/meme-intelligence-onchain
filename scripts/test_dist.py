import asyncio
from extractors.solana_rpc import SolanaRPCClient
async def main():
    rpc = SolanaRPCClient()
    distributor = "9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw"
    page = await rpc.get_transactions_for_address(distributor, limit=2, sort_order="asc", transaction_details="full")
    txs = page.get("data", [])
    print("Found txs for distributor:", len(txs))
if __name__ == "__main__":
    asyncio.run(main())
