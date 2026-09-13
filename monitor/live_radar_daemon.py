#!/usr/bin/env python3
"""Production live radar worker. Does not fabricate alerts/trades.
The persistent version should be fed by Helius webhooks or a long-running worker that observes watchlist transactions.
"""
import asyncio, logging
from db.database import Database
from monitor.live_scanner import LiveScanner
logging.basicConfig(level=logging.INFO); logger=logging.getLogger(__name__)
async def main():
    db=Database(); scanner=LiveScanner(db)
    try:
        logger.info("Live scanner started. Only observed/API data may be persisted.")
        await scanner.run_live_loop(poll_interval_sec=30, max_iterations=10**9)
    finally: await scanner.close()
if __name__=="__main__": asyncio.run(main())
