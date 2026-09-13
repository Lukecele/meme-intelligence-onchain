import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from extractors.dex_screener import DexScreenerClient

async def get_fresh():
    client = DexScreenerClient()
    profiles = await client.get_latest_token_profiles()
    print("Fresh live tokens on Solana right now:")
    for p in profiles[:5]:
        addr = p.get("tokenAddress")
        if addr:
            summary = await client.get_token_summary(addr)
            if summary:
                print(f"• Symbol: ${summary.get('symbol')} | Mint: {addr} | Mcap: ${summary.get('market_cap_usd'):,.0f} | Liq: ${summary.get('liquidity_usd'):,.0f}")
    await client.close()

if __name__ == "__main__":
    asyncio.run(get_fresh())
