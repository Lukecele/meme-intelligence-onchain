"""Live market candidate scanner.

Production note: this scanner discovers new Solana tokens and applies market-data
availability checks. Smart-wallet convergence is intentionally NOT inferred here.
It must be fed by observed watchlist transactions (webhook/worker) before alerts
can be generated.
"""
import asyncio
import logging
from db.database import Database
from extractors.dex_screener import DexScreenerClient

logger = logging.getLogger(__name__)

class LiveScanner:
    def __init__(self, db: Database):
        self.db = db
        self.dex_client = DexScreenerClient()
        self.processed_tokens = set()

    async def scan_candidate_token(self, token_address: str) -> bool:
        if token_address in self.processed_tokens:
            return False
        token_meta = await self.dex_client.get_token_summary(token_address)
        self.processed_tokens.add(token_address)
        if not token_meta:
            logger.info("Market data unavailable for %s; skipped.", token_address)
            return False
        logger.info(
            "Market candidate %s: mcap=%s liquidity=%s. No smart-wallet alert emitted without observed watchlist events.",
            token_meta.get("symbol", token_address[:8]),
            token_meta.get("market_cap_usd"),
            token_meta.get("liquidity_usd"),
        )
        return False

    async def run_live_loop(self, poll_interval_sec: int = 15, max_iterations: int = 10):
        logger.info("Starting market discovery scanner (alert generation disabled until watchlist validation).")
        for iteration in range(max_iterations):
            try:
                latest_tokens = await self.dex_client.get_latest_token_profiles()
                logger.info("[Poll %d/%d] discovered %d candidates", iteration + 1, max_iterations, len(latest_tokens))
                for t in latest_tokens[:10]:
                    mint = t.get("tokenAddress")
                    if mint:
                        await self.scan_candidate_token(mint)
                await asyncio.sleep(poll_interval_sec)
            except Exception as exc:
                logger.error("Live scanner cycle error: %s", exc)
                await asyncio.sleep(5)

    async def close(self):
        await self.dex_client.close()
