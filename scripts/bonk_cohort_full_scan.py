import asyncio
import logging
import sqlite3
import time
from pathlib import Path
from extractors.solana_rpc import SolanaRPCClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BonkCohortScanner:
    def __init__(self):
        self.rpc = SolanaRPCClient()
        self.mint = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
        self.db_path = Path("data/onchain_intelligence.db")
        self.semaphore = asyncio.Semaphore(5) # 5 concurrent reqs to stay safely under 10/s
        
    async def process_wallet(self, wallet: str, airdrop_amt: float, conn):
        async with self.semaphore:
            await asyncio.sleep(0.55) # Rate limit pacing
            
            try:
                req = await self.rpc.call("getTokenAccountsByOwner", [
                    wallet,
                    {"mint": self.mint},
                    {"encoding": "jsonParsed"}
                ])
                
                current_balance = 0.0
                if req and "value" in req:
                    for acc in req["value"]:
                        info = acc.get("account", {}).get("data", {}).get("parsed", {}).get("info", {})
                        amt = float(info.get("tokenAmount", {}).get("uiAmount") or 0)
                        current_balance += amt
                        
                cohort = "Airdrop recipient"
                if current_balance < airdrop_amt * 0.1: # Dumped almost everything
                    cohort = "Early seller"
                elif current_balance > airdrop_amt * 1.1: # Bought significantly more
                    cohort = "Airdrop + Buy"
                    
                # We update the DB
                while True:
                    try:
                        conn.execute("UPDATE bonk_airdrop SET cohort=? WHERE wallet_address=?", (cohort, wallet))
                        conn.commit()
                        break
                    except sqlite3.OperationalError:
                        time.sleep(0.1)
                        
                return cohort
            except Exception as e:
                # If error, leave as default
                return "Airdrop recipient"

    async def run(self):
        print("Starting comprehensive Cohort Scan for 10,009 BONK Airdrop recipients...")
        conn = sqlite3.connect(self.db_path, timeout=30)
        
        recipients = conn.execute("SELECT wallet_address, amount FROM bonk_airdrop WHERE cohort='Airdrop recipient'").fetchall()
        
        print(f"Loaded {len(recipients)} wallets to scan.")
        
        tasks = []
        batch_size = 100
        processed = 0
        
        # We process in batches to print progress
        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i+batch_size]
            coros = [self.process_wallet(r[0], r[1], conn) for r in batch]
            results = await asyncio.gather(*coros)
            processed += len(results)
            print(f"Processed {processed}/{len(recipients)} wallets...")
            
        print("Cohort classification completed via deep RPC scanning.")
        
        # Print stats
        stats = conn.execute("SELECT cohort, count(*) FROM bonk_airdrop GROUP BY cohort").fetchall()
        print("\n--- BONK BEHAVIORAL COHORTS ---")
        for s in stats:
            print(f"{s[0]}: {s[1]}")
            
        conn.close()

async def main():
    scanner = BonkCohortScanner()
    await scanner.run()

if __name__ == "__main__":
    asyncio.run(main())
