"""Blind out-of-sample validator. Train/test symbols must be frozen before running."""
import sqlite3
from pathlib import Path
from typing import Sequence
class OutOfSampleValidator:
    def __init__(self,db_path:Path,train_symbols:Sequence[str]=('BONK','WIF'),test_symbols:Sequence[str]=('POPCAT','MEW')):
        self.db_path=db_path;self.train_symbols=tuple(train_symbols);self.test_symbols=tuple(test_symbols)
    def run_blind_test(self):
        conn=sqlite3.connect(self.db_path);conn.row_factory=sqlite3.Row
        try:
            qmarks=','.join('?'*len(self.train_symbols))
            rows=conn.execute(f"""SELECT t.wallet_address,COUNT(DISTINCT t.token_mint) hits FROM trades t JOIN tokens tk ON tk.mint=t.token_mint WHERE tk.symbol IN ({qmarks}) AND t.side='BUY' AND t.is_first_buyer=1 AND t.source_type IN ('ONCHAIN','API') GROUP BY t.wallet_address HAVING hits>=2""",self.train_symbols).fetchall()
            trained={r['wallet_address'] for r in rows}
            if not trained:return {'status':'DATA_INCOMPLETE','trained_wallets_count':0,'is_validated':False}
            hits={};
            for sym in self.test_symbols:
                ws={r['wallet_address'] for r in conn.execute("""SELECT DISTINCT t.wallet_address FROM trades t JOIN tokens tk ON tk.mint=t.token_mint WHERE tk.symbol=? AND t.side='BUY' AND t.is_first_buyer=1 AND t.source_type IN ('ONCHAIN','API')""",(sym,)).fetchall()}
                hits[sym]=len(trained & ws)
            token_hit_rate=100*sum(1 for v in hits.values() if v>0)/max(1,len(self.test_symbols))
            return {'status':'PASSED' if token_hit_rate>=70 else 'FAILED','trained_wallets_count':len(trained),'test_tokens_evaluated':list(self.test_symbols),'hits_by_token':hits,'token_hit_rate_pct':round(token_hit_rate,1),'is_validated':token_hit_rate>=70}
        finally:conn.close()
