import asyncio
from extractors.solana_rpc import SolanaRPCClient
from extractors.real_bonk_airdrop_fetcher import RealBonkAirdropFetcher
async def main():
    f = RealBonkAirdropFetcher(["9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw"])
    page = await f.rpc.get_transactions_for_address("9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw", limit=2, sort_order="asc", transaction_details="full")
    tx = page.get("data", [])[1]
    
    meta=tx.get("meta") or {}
    pre=f._map(meta.get("preTokenBalances") or [])
    print("Pre:", pre)
if __name__ == "__main__":
    asyncio.run(main())
