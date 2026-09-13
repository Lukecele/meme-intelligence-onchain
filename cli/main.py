"""CLI - production-safe commands."""
import argparse, asyncio, json, sys
from pathlib import Path
PROJECT_ROOT=Path(__file__).resolve().parent.parent; sys.path.insert(0,str(PROJECT_ROOT))
from db.database import Database
from extractors.first_buyers_extractor import FirstBuyersExtractor
from analytics.backtest_validator import BacktestValidator
from analytics.out_of_sample_tester import OutOfSampleValidator
from config.settings import DATA_DIR
def init_db(): Database(); print('Production database initialized (empty; no synthetic seed).')
async def ingest(limit):
    e=FirstBuyersExtractor()
    try: print('Imported rows:',await e.run(limit))
    finally: await e.close()
def backtest(): print(json.dumps(BacktestValidator(Database()).run_full_validation(),indent=2))
def oos(): print(json.dumps(OutOfSampleValidator(DATA_DIR/'onchain_intelligence.db').run_blind_test(),indent=2))
def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    sp.add_parser('init-db'); ing=sp.add_parser('ingest-first-buyers');ing.add_argument('--limit',type=int,default=1000);sp.add_parser('backtest');sp.add_parser('oos')
    a=p.parse_args();
    if a.cmd=='init-db':init_db()
    elif a.cmd=='ingest-first-buyers':asyncio.run(ingest(a.limit))
    elif a.cmd=='backtest':backtest()
    elif a.cmd=='oos':oos()
if __name__=='__main__':main()
