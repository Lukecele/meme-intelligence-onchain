import asyncio
from extractors.solana_rpc import SolanaRPCClient
from extractors.real_bonk_airdrop_fetcher import RealBonkAirdropFetcher
async def main():
    f = RealBonkAirdropFetcher(["9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw"])
    page = await f.rpc.get_transactions_for_address("9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw", limit=2, sort_order="asc", transaction_details="full")
    txs = page.get("data", [])
    tx = txs[1]
    
    meta=tx.get("meta") or {}
    pre=f._map(meta.get("preTokenBalances") or [])
    post=f._map(meta.get("postTokenBalances") or [])
    dist_loss = sum(max(0.0,pre.get((d,f.BONK_MINT),0.0)-post.get((d,f.BONK_MINT),0.0)) for d in f.distributors)
    print("Distributors set:", f.distributors)
    print("Loss:", dist_loss)
    owners={o for o,m in set(pre)|set(post) if m==f.BONK_MINT and o not in f.distributors}
    print("Owners:", owners)
    events=[]
    for owner in owners:
        delta=post.get((owner,f.BONK_MINT),0.0)-pre.get((owner,f.BONK_MINT),0.0)
        print("Delta for", owner, ":", delta)
        if delta>0:events.append({"wallet":owner,"amount_tokens":delta})
    print("Sum:", sum(e["amount_tokens"] for e in events))
    print("Events:", events)
if __name__ == "__main__":
    asyncio.run(main())
