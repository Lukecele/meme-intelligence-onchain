"""Statistical validation engine. Uses only verified early BUY rows and matched winner/control tokens."""
import math
from dataclasses import dataclass
from typing import Dict,Any,Tuple
@dataclass
class ContingencyTable2x2: a:int; b:int; c:int; d:int
def calculate_fisher_exact_p_value(t):
    a,b,c,d=t.a,t.b,t.c,t.d; n=a+b+c+d
    if n==0:return 1.0
    lf=lambda k: math.lgamma(k+1)
    def hp(x):
        k=a+c;m=a+b
        return math.exp(lf(m)+lf(n-m)+lf(k)+lf(n-k)-lf(n)-lf(x)-lf(m-x)-lf(k-x)-lf(n-m-k+x))
    obs=hp(a); lo=max(0,(a+b)+(a+c)-n); hi=min(a+b,a+c)
    return min(1.0,sum(p for x in range(lo,hi+1) if (p:=hp(x))<=obs+1e-12))
def calculate_odds_ratio(t)->Tuple[float,Tuple[float,float]]:
    a,b,c,d=map(float,(t.a,t.b,t.c,t.d))
    if 0 in (a,b,c,d): a,b,c,d=a+.5,b+.5,c+.5,d+.5
    orr=(a*d)/(b*c); se=math.sqrt(1/a+1/b+1/c+1/d)
    return orr,(math.exp(math.log(orr)-1.96*se),math.exp(math.log(orr)+1.96*se))
class EmpiricalBacktestValidator:
    def __init__(self,table): self.table=table
    def evaluate(self):
        orr,ci=calculate_odds_ratio(self.table); p=calculate_fisher_exact_p_value(self.table)
        verdict='GO' if p<.05 and orr>=3 else 'INSUFFICIENT_DATA_OR_NO_GO'
        return {'verdict':verdict,'provenance':'DERIVED_STATISTICAL_TEST','contingency_table':{'early_in_winners':self.table.a,'late_in_winners':self.table.b,'early_in_control':self.table.c,'late_in_control':self.table.d},'odds_ratio':round(orr,3),'confidence_interval_95':[round(ci[0],3),round(ci[1],3)],'fisher_exact_p_value':round(p,6),'is_statistically_significant':p<.05,'is_asymmetric_signal':orr>=3}
class BacktestValidator:
    def __init__(self,db): self.db=db
    def run_full_validation(self):
        with self.db.get_connection() as conn:
            # Only API/on-chain observed first BUY rows are admissible.
            rows=conn.execute("""SELECT t.wallet_address, tk.is_winner, tk.is_control FROM trades t JOIN tokens tk ON tk.mint=t.token_mint WHERE t.side='BUY' AND t.is_first_buyer=1 AND t.source_type IN ('ONCHAIN','API')""").fetchall()
            winners={r['wallet_address'] for r in rows if r['is_winner']}; controls={r['wallet_address'] for r in rows if r['is_control']}
            # Candidate smart cohort: repeated across >=2 winner tokens, computed only from verified early buys.
            multi={r['wallet_address'] for r in conn.execute("""SELECT t.wallet_address, COUNT(DISTINCT t.token_mint) hits FROM trades t JOIN tokens tk ON tk.mint=t.token_mint WHERE t.side='BUY' AND t.is_first_buyer=1 AND t.source_type IN ('ONCHAIN','API') AND tk.is_winner=1 GROUP BY t.wallet_address HAVING hits>=2""").fetchall()}
            n_wtokens=conn.execute("SELECT COUNT(*) FROM tokens WHERE is_winner=1").fetchone()[0]; n_ctokens=conn.execute("SELECT COUNT(*) FROM tokens WHERE is_control=1").fetchone()[0]
        if not rows or n_wtokens<2 or n_ctokens<2:
            return {'decision':'DATA_INCOMPLETE','interpretation':'Dataset empirico insufficiente: servono first buyers verificati per winner e controlli matched.','recommendation':'Completare ingestione e congelare il dataset prima del test.','metrics':{'winner_tokens_count':n_wtokens,'control_tokens_count':n_ctokens,'verified_first_buy_rows':len(rows),'multi_winner_wallets_count':len(multi)}}
        universe=winners|controls; a=len(multi & winners); c=len(multi & controls); b=max(0,len(winners)-a); d=max(0,len(controls)-c)
        stats=EmpiricalBacktestValidator(ContingencyTable2x2(a,b,c,d)).evaluate()
        return {'decision':stats['verdict'],'interpretation':'Fisher exact test su coorti wallet verificate; nessuna metrica OOS/lead-time viene inventata.','recommendation':'Eseguire OOS separato su test set congelato.','statistics':stats,'metrics':{'winner_tokens_count':n_wtokens,'control_tokens_count':n_ctokens,'verified_first_buy_rows':len(rows),'multi_winner_wallets_count':len(multi),'odds_ratio_vs_control':stats['odds_ratio'],'fisher_exact_p_value':stats['fisher_exact_p_value']}}
