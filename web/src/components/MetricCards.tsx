import React from "react";
import { TrendingUp, ShieldCheck, Database, Users } from "lucide-react";
import validation from "../lib/validation_result.json";
export const MetricCards:React.FC=()=>{
  const m:any=(validation as any).backtest?.metrics||{};
  const stats:any=(validation as any).backtest?.statistics||{};
  const metrics=[
    {title:"Odds Ratio",value:m.odds_ratio_vs_control==null?"N/D":`${m.odds_ratio_vs_control.toFixed(1)}x`,sub:"Solo dopo Fisher su dataset verificato",icon:TrendingUp},
    {title:"Smart Wallets",value:String(m.multi_winner_wallets_count||0),sub:"Qualificati su dati verificati",icon:ShieldCheck},
    {title:"First Buyers",value:String(m.verified_first_buy_rows||0),sub:"BUY early con provenance API/on-chain",icon:Users},
    {title:"Fisher p-value",value:String(stats.fisher_exact_p_value||0),sub:"Significatività statistica",icon:Database}
  ];
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-4">
      {metrics.map((x,i)=>{
        const I=x.icon;
        return (
          <div key={i} className="p-3.5 sm:p-5 rounded-xl sm:rounded-2xl bg-zinc-900/70 border border-zinc-800">
            <div className="flex justify-between">
              <span className="text-[10px] sm:text-xs text-zinc-400 uppercase">{x.title}</span>
              <I className="w-4 h-4 text-amber-400"/>
            </div>
            <div className="text-xl sm:text-3xl font-black font-mono mt-2 text-amber-400">{x.value}</div>
            <p className="text-[10px] sm:text-xs text-zinc-500 mt-1">{x.sub}</p>
          </div>
        );
      })}
    </div>
  );
};
