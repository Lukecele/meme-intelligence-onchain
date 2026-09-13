import asyncio
from extractors.solana_rpc import SolanaRPCClient
from extractors.real_bonk_airdrop_fetcher import RealBonkAirdropFetcher
async def main():
    f = RealBonkAirdropFetcher(["9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw"])
    page = await f.rpc.get_transactions_for_address("9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw", limit=10, sort_order="asc", transaction_details="full")
    txs = page.get("data", [])
    for tx in txs:
        evs = f._parse_airdrop_events(tx)
        print("Sig:", tx.get("signature"), "Events:", evs)
if __name__ == "__main__":
    asyncio.run(main())
