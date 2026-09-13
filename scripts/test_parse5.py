import asyncio
from extractors.solana_rpc import SolanaRPCClient
async def main():
    rpc = SolanaRPCClient()
    page = await rpc.get_transactions_for_address("9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw", limit=1, sort_order="asc", transaction_details="full")
    tx = page.get("data", [])[0]
    print(tx.keys())
    print(tx.get("signature"))
    print(tx.get("transaction", {}).get("signatures"))
if __name__ == "__main__":
    asyncio.run(main())
