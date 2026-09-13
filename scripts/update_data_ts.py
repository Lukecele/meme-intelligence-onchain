#!/usr/bin/env python3
"""Production-safe UI state exporter.
Writes only backend validation status. It never invents smart-wallet metrics or wallet addresses.
"""
import json
from pathlib import Path
from db.database import Database
from analytics.backtest_validator import BacktestValidator
ROOT=Path(__file__).resolve().parent.parent
result=BacktestValidator(Database()).run_full_validation()
metrics=result.get('metrics',{})
out={
 'status':'PASSED' if result.get('decision')=='GO' else result.get('decision','NOT_RUN'),
 'dataset_type':'PRODUCTION_ONLY','decision':result.get('decision'),
 'metrics':{'verified_first_buy_rows':metrics.get('verified_first_buy_rows',0),'smart_wallets':metrics.get('multi_winner_wallets_count',0),'odds_ratio':metrics.get('odds_ratio_vs_control'),'fisher_p':metrics.get('fisher_exact_p_value'),'oos':None,'bonk_airdrop_verified':0}
}
(ROOT/'web/src/lib/validation_result.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('Updated validation_result.json from backend state.')
