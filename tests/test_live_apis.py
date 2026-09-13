"""Manual smoke test for configured live providers.

No credentials are embedded.  Missing keys are reported as SKIP, not as success.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import HELIUS_API_KEY, BIRDEYE_API_KEY, PYTH_API_KEY
from extractors.helius_api import HeliusClient
from extractors.birdeye_api import BirdeyeClient
from extractors.pyth_client import PythBenchmarkClient

BONK_MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
WIF_MINT = "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm"


async def test_live() -> None:
    print("Live provider smoke test")

    if HELIUS_API_KEY:
        h = HeliusClient()
        txs = await h.get_address_transactions(BONK_MINT, limit=2, sort_order="desc")
        print(f"Helius: OK ({len(txs)} transactions)")
        await h.close()
    else:
        print("Helius: SKIP (HELIUS_API_KEY missing)")

    if BIRDEYE_API_KEY:
        b = BirdeyeClient()
        buyers = await b.get_token_first_buyers(WIF_MINT, limit=3)
        print(f"Birdeye: OK ({len(buyers)} first buyers)")
        await b.close()
    else:
        print("Birdeye: SKIP (BIRDEYE_API_KEY missing)")

    if PYTH_API_KEY:
        p = PythBenchmarkClient()
        sol_price = await p.get_price("SOL_USD")
        print(f"Pyth: {'OK' if sol_price else 'NO DATA'}")
        await p.close()
    else:
        print("Pyth: SKIP (PYTH_API_KEY missing)")


if __name__ == "__main__":
    asyncio.run(test_live())
