"""Honest report generator: it reports database state and validation status without hardcoded claims."""
import csv,json,hashlib
from pathlib import Path
from config.settings import REPORTS_DIR
from analytics.backtest_validator import BacktestValidator
class ReportGenerator:
 def __init__(self,db): self.db=db
 def _rows(self,q,args=()):
  with self.db.get_connection() as c:return [dict(r) for r in c.execute(q,args).fetchall()]
 def _csv(self,name,rows):
  p=REPORTS_DIR/name
  if not rows:p.write_text('',encoding='utf-8');return p
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
  return p
 def export_bonk_airdrop_csv(self): return self._csv('bonk_airdrop_list.csv',self._rows("SELECT * FROM airdrop_claims WHERE source_type IN ('ONCHAIN','API')"))
 def export_first_buyers_csv(self): return self._csv('first_buyers_bonk_wif_popcat.csv',self._rows("SELECT * FROM trades WHERE side='BUY' AND is_first_buyer=1 AND source_type IN ('ONCHAIN','API') ORDER BY timestamp"))
 def export_wallet_intersection_matrix_csv(self): return self._csv('wallet_intersection_matrix.csv',self._rows("SELECT wallet_address,COUNT(DISTINCT token_mint) token_count FROM trades WHERE side='BUY' AND is_first_buyer=1 AND source_type IN ('ONCHAIN','API') GROUP BY wallet_address"))
 def export_wallet_scores_csv(self): return self._csv('wallet_scores_preliminary.csv',self._rows('SELECT * FROM wallets WHERE score>0 ORDER BY score DESC'))
 def export_clusters_json(self):
  p=REPORTS_DIR/'clusters_suspicious.json';p.write_text(json.dumps(self._rows('SELECT * FROM clusters'),indent=2),encoding='utf-8');return p
 def generate_gonogo_report(self):
  result=BacktestValidator(self.db).run_full_validation();raw=json.dumps(result,sort_keys=True).encode();dh=hashlib.sha256(raw).hexdigest();p=REPORTS_DIR/'REPORT_GO_NOGO_SPRINT1.md'
  p.write_text(f"# GO / NO-GO Sprint 1\n\n**Status:** {result['decision']}\n\n**Validation result hash:** `{dh}`\n\n```json\n{json.dumps(result,indent=2)}\n```\n",encoding='utf-8');return p
