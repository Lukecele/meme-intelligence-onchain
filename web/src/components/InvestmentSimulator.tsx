"use client";

import React, { useState, useEffect } from "react";
import { DollarSign, TrendingUp, TrendingDown, Clock, ShieldCheck, ShieldAlert, CheckCircle2, RefreshCw, Play, RotateCcw, AlertTriangle, ArrowUpRight, Zap, ChevronDown, ChevronUp, History, Coins, ArrowRightLeft, Layers, UserCheck } from "lucide-react";
import { SimulatedTrade, ConvergenceAlert, CopyTradeLogEvent } from "../types";
import { CopyButton } from "./CopyButton";

export const InvestmentSimulator: React.FC = () => {
  const [trades, setTrades] = useState<any[]>([]);
  const [expandedTradeId, setExpandedTradeId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [lastSync, setLastSync] = useState<Date>(new Date());
  const [solPrice, setSolPrice] = useState<number>(145.5);

  useEffect(() => {
    fetch("/api/price?mint=So11111111111111111111111111111111111111112")
      .then(res => res.json())
      .then(data => {
        if (data.success && data.priceUsd) {
          setSolPrice(data.priceUsd);
        }
      })
      .catch(() => {});
  }, []);

  // Real-time consequential sync with 24h radar & on-chain wallet actions
  const syncConsequentialTrading = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/radar", { cache: "no-store" });
      const data = await res.json();
      if (data.success && Array.isArray(data.alerts)) {
        const alerts = data.alerts;
        const currentSolPrice = data.solPriceUsd || solPrice;
        setSolPrice(currentSolPrice);

        const updated: any[] = [];

        for (const alert of alerts) {
          if (alert.signalLevel === "ALTO" && alert.score >= 80) {
            const currentPrice = (alert.priceUsd && alert.priceUsd > 0) ? alert.priceUsd : 0.000007;
            const entryPrice = (alert.entryPriceUsd && alert.entryPriceUsd > 0) ? alert.entryPriceUsd : 0.000007;
            const entryMcap = alert.marketCapUsd || 15000;
            const currentMcap = alert.currentMarketCapUsd || entryMcap;
            
            const entryTimestamp = alert.timestamp || (Date.now() - 3600 * 1000 * 3.5);
            const initialSol = parseFloat((100 / currentSolPrice).toFixed(4));
            const initialTokens = 100 / entryPrice;

            // Check primary Smart Wallet involved in this alert
            const leadWallet = alert.walletsInvolved?.[0] || { label: "Smart Wallet Scout", address: "Solana Scout", tokensBought: 1000, tokensSold: 0 };
            
            // Calculate EXACT on-chain percentage sold by the Smart Wallet
            const exactSoldPct = (leadWallet.tokensBought && leadWallet.tokensBought > 0)
              ? Math.min(1.0, Math.max(0.0, leadWallet.tokensSold / leadWallet.tokensBought))
              : 0;

            const entryLog: CopyTradeLogEvent = {
              timestamp: entryTimestamp,
              actionType: "ENTRY_COPY",
              walletAddress: leadWallet.address,
              description: `🎯 INGRESSO CONSEGUENZIALE: Rilevata convergenza (${alert.walletsCount} Smart Wallets: ${leadWallet.label}) &rarr; Acquistati 100.00$ (${initialSol} SOL) pari a ${initialTokens.toLocaleString(undefined, { maximumFractionDigits: 0 })} token al prezzo di convergenza $${entryPrice.toFixed(8)} (MCAP $${entryMcap.toLocaleString()})`,
              cashAmountUsd: -100,
              tokensAmount: initialTokens,
              priceUsd: entryPrice
            };

            const logs: CopyTradeLogEvent[] = [entryLog];
            let currentTokens = initialTokens;
            let cashExtracted = 0;
            let partialCount = 0;
            let status = "HOLDING_100";

            // STRICT COPY OF THE EXACT PERCENTAGE SOLD BY THE SMART WALLET
            if (exactSoldPct >= 0.99) {
              // Smart wallet sold 100% (Full Exit)
              const exitPrice = currentPrice;
              const soldTokens = initialTokens;
              const cashFromExit = soldTokens * exitPrice;
              cashExtracted = cashFromExit;
              currentTokens = 0;
              status = "CLOSED_FULL_EXIT";

              logs.push({
                timestamp: entryTimestamp + (3600 * 1000),
                actionType: "FULL_EXIT_COPY",
                walletAddress: leadWallet.address,
                description: `🔴 COPIA LIQUIDAZIONE TOTALE (100%): Lo smart wallet ${leadWallet.label} ha venduto il 100% dei token &rarr; Simulatore vende tutti i ${soldTokens.toLocaleString(undefined, { maximumFractionDigits: 0 })} token a $${exitPrice.toFixed(8)} incassando $${cashFromExit.toFixed(2)} (${parseFloat((cashFromExit / currentSolPrice).toFixed(4))} SOL) in cash. Posizione chiusa.`,
                cashAmountUsd: cashFromExit,
                tokensAmount: soldTokens,
                priceUsd: exitPrice
              });
            } else if (exactSoldPct > 0) {
              // Smart wallet sold a partial percentage (e.g. 25%, 35%, 40%, 50%, 65%, 70%, 75%, 80%)
              const exitPrice = currentPrice;
              const soldTokens = initialTokens * exactSoldPct;
              const cashFromExit = soldTokens * exitPrice;
              cashExtracted = cashFromExit;
              currentTokens = initialTokens - soldTokens;
              partialCount = 1;
              status = "OPEN_PARTIAL_EXITED";

              logs.push({
                timestamp: entryTimestamp + (1800 * 1000),
                actionType: "PARTIAL_EXIT_COPY",
                walletAddress: leadWallet.address,
                description: `🛡️ COPIA USCITA PARZIALE (${(exactSoldPct * 100).toFixed(0)}%): Lo smart wallet ${leadWallet.label} ha venduto il ${(exactSoldPct * 100).toFixed(0)}% dei suoi token &rarr; Simulatore vende esattamente ${soldTokens.toLocaleString(undefined, { maximumFractionDigits: 0 })} token a $${exitPrice.toFixed(8)} incassando $${cashFromExit.toFixed(2)} (${parseFloat((cashFromExit / currentSolPrice).toFixed(4))} SOL) in cash. Posizione de-risked con ${( (1 - exactSoldPct) * 100 ).toFixed(0)}% residuo a mercato.`,
                cashAmountUsd: cashFromExit,
                tokensAmount: soldTokens,
                priceUsd: exitPrice
              });
            } else {
              // Smart wallet is holding 100%
              status = currentMcap >= entryMcap ? "HOLDING_100" : "HOLDING_IN_LOSS";
            }

            const currentPositionValue = currentTokens * currentPrice;
            const totalNetPnl = (cashExtracted + currentPositionValue) - 100;
            const totalNetPnlPct = (totalNetPnl / 100) * 100;

            updated.push({
              id: `trade_${alert.tokenMint.slice(0, 8)}`,
              tokenMint: alert.tokenMint,
              symbol: alert.symbol,
              name: alert.name,
              leadWallet: leadWallet,
              exactSoldPct: exactSoldPct,
              entryTimestamp: entryTimestamp,
              tokenAgeMinutes: alert.tokenAgeMinutes,
              isLiveNow: alert.isLiveNow,
              entryPriceUsd: entryPrice,
              entryMcapUsd: entryMcap,
              currentMcapUsd: currentMcap,
              amountInvestedUsd: 100,
              amountInvestedSol: initialSol,
              initialTokensAcquired: initialTokens,
              currentTokensHeld: currentTokens,
              currentPriceUsd: currentPrice,
              currentPositionValueUsd: parseFloat(currentPositionValue.toFixed(2)),
              totalCashExtractedUsd: parseFloat(cashExtracted.toFixed(2)),
              totalNetPnlUsd: parseFloat(totalNetPnl.toFixed(2)),
              totalNetPnlPct: parseFloat(totalNetPnlPct.toFixed(1)),
              status: status,
              partialSellsCount: partialCount,
              copyTradeLogs: logs
            });
          }
        }

        setTrades(updated);
        setLastSync(new Date());
      }
    } catch (err) {
      console.error("Simulator sync failed:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    syncConsequentialTrading();
    const interval = setInterval(syncConsequentialTrading, 15000);
    return () => clearInterval(interval);
  }, []);

  // Accounting Totals
  const totalInvested = trades.length * 100;
  const currentOpenValue = trades.reduce((acc, t) => acc + t.currentPositionValueUsd, 0);
  const totalCashExtracted = trades.reduce((acc, t) => acc + t.totalCashExtractedUsd, 0);
  const totalCombinedNetPnl = (totalCashExtracted + currentOpenValue) - totalInvested;

  const partialExitCount = trades.filter((t) => t.status === "OPEN_PARTIAL_EXITED").length;
  const holdingLossCount = trades.filter((t) => t.status === "HOLDING_IN_LOSS").length;
  const fullExitCount = trades.filter((t) => t.status === "CLOSED_FULL_EXIT").length;

  return (
    <div className="space-y-4 sm:space-y-6">
      
      {/* Top Banner */}
      <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-r from-amber-950/40 via-zinc-900/90 to-zinc-900/90 border border-amber-500/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2 sm:p-2.5 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/30 shrink-0">
            <Zap className="w-5 h-5 sm:w-6 sm:h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-[10px] sm:text-xs font-mono font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                COPIA RIGIDA % SMART WALLETS &bull; $100 FISSI
              </span>
              <span className="text-[10px] font-mono text-zinc-400 border border-zinc-700 px-1.5 py-0.2 rounded">
                LIVE & STORICO 24H &bull; SOL: ${solPrice.toFixed(2)}
              </span>
            </div>
            <h2 className="text-sm sm:text-base font-bold text-white mt-1">
              Trading Conseguenziale Retroattivo e Live ($100 per Token)
            </h2>
            <p className="text-[11px] sm:text-xs text-zinc-300 mt-0.5">
              Ingresso al Market Cap di convergenza. Le vendite copiano esattamente le percentuali di vendita on-chain eseguite dagli Smart Wallets.
            </p>
          </div>
        </div>

        <button
          onClick={syncConsequentialTrading}
          disabled={loading}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700 transition-all self-end sm:self-center"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-amber-400" : "text-zinc-400"}`} />
          <span>Aggiorna Prezzi Live</span>
        </button>
      </div>

      {/* Financial Summary Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        
        {/* Total Capital Deployed */}
        <div className="p-4 sm:p-5 rounded-2xl bg-zinc-900/80 border border-zinc-800">
          <span className="text-[10px] sm:text-xs font-bold text-zinc-400 uppercase tracking-wider block">Capitale Impiegato</span>
          <div className="text-xl sm:text-2xl font-black text-white font-mono mt-1">
            ${totalInvested.toLocaleString()}
          </div>
          <span className="text-[10px] text-zinc-500 font-mono mt-0.5 block">
            {trades.length} Trade eseguiti da $100
          </span>
        </div>

        {/* Total Cash Recovered */}
        <div className="p-4 sm:p-5 rounded-2xl bg-zinc-900/80 border border-zinc-800">
          <span className="text-[10px] sm:text-xs font-bold text-zinc-400 uppercase tracking-wider block">Cash Incassato (Uscite Smart Wallets)</span>
          <div className="text-xl sm:text-2xl font-black text-emerald-400 font-mono mt-1">
            ${totalCashExtracted.toFixed(2)}
          </div>
          <span className="text-[10px] text-zinc-500 font-mono mt-0.5 block">
            Da {partialExitCount} uscite parziali & {fullExitCount} totali
          </span>
        </div>

        {/* Current Active Holdings Value */}
        <div className="p-4 sm:p-5 rounded-2xl bg-zinc-900/80 border border-zinc-800">
          <span className="text-[10px] sm:text-xs font-bold text-zinc-400 uppercase tracking-wider block">Valore Attuale Token a Mercato</span>
          <div className="text-xl sm:text-2xl font-black text-amber-400 font-mono mt-1">
            ${currentOpenValue.toFixed(2)}
          </div>
          <span className="text-[10px] text-zinc-500 font-mono mt-0.5 block">
            {partialExitCount} in De-risking &bull; {holdingLossCount} in Calo
          </span>
        </div>

        {/* Net Absolute Profit */}
        <div className="p-4 sm:p-5 rounded-2xl bg-zinc-900/80 border border-zinc-800">
          <span className="text-[10px] sm:text-xs font-bold text-zinc-400 uppercase tracking-wider block">Bilancio Netto Cumulativo</span>
          <div className={`text-xl sm:text-2xl font-black font-mono mt-1 flex items-center gap-1 ${totalCombinedNetPnl >= 0 ? "text-emerald-400" : "text-red-400"}`}>
            {totalCombinedNetPnl >= 0 ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
            <span>{totalCombinedNetPnl >= 0 ? "+" : ""}${totalCombinedNetPnl.toFixed(2)}</span>
          </div>
          <span className="text-[10px] text-zinc-500 font-mono mt-0.5 block">
            (Cash + Token) - Impiegato
          </span>
        </div>

      </div>

      {/* Individual Trades Cards */}
      <div className="space-y-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-400 flex items-center justify-between px-1">
          <span>Rendimento Dettagliato Singoli Trade ({trades.length})</span>
          <span className="text-amber-400 font-mono text-[11px]">Sync Live DexScreener</span>
        </h3>

        {trades.map((trade) => {
          const isExpanded = expandedTradeId === trade.id;
          const pnlPositive = trade.totalNetPnlUsd >= 0;
          const isDeRisked = trade.status === "OPEN_PARTIAL_EXITED";
          const isFullExit = trade.status === "CLOSED_FULL_EXIT";
          const isLoss = trade.status === "HOLDING_IN_LOSS";
          const timeLabel = trade.isLiveNow ? `${trade.tokenAgeMinutes}m fa` : `${(trade.tokenAgeMinutes / 60).toFixed(1)}h fa`;
          const soldPctLabel = (trade.exactSoldPct * 100).toFixed(0);

          return (
            <div
              key={trade.id}
              className="p-4 sm:p-5 rounded-2xl bg-zinc-900/90 border border-zinc-800 hover:border-zinc-700 transition-all space-y-3.5"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-base sm:text-lg font-black text-white font-mono">${trade.symbol}</span>
                    <span className="text-xs text-zinc-400">{trade.name}</span>
                    <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded ${
                      isDeRisked
                        ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                        : isFullExit
                        ? "bg-red-500/20 text-red-400 border border-red-500/30"
                        : isLoss
                        ? "bg-red-500/20 text-red-400 border border-red-500/30"
                        : "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                    }`}>
                      {isDeRisked
                        ? `🛡️ VENDUTO ${soldPctLabel}% (SEGUITO SMART WALLET)`
                        : isFullExit
                        ? "🔴 CHIUSO 100% (FULL EXIT SMART WALLET)"
                        : isLoss
                        ? "🔴 HOLDING 100% (IN CALO)"
                        : "🟢 HOLDING 100%"}
                    </span>
                  </div>
                  <div className="text-[11px] font-mono text-zinc-500 mt-0.5 flex items-center gap-2 flex-wrap">
                    <span>Lanciato: {timeLabel} ({new Date(trade.entryTimestamp).toLocaleTimeString()})</span>
                    <span>&bull;</span>
                    <span>Seguito: <b>{trade.leadWallet?.label}</b></span>
                    <span>&bull;</span>
                    <span>Mint: {trade.tokenMint}</span>
                    <CopyButton text={trade.tokenMint} label="Copia Mint" />
                  </div>
                </div>

                <div className="text-right flex sm:flex-col justify-between items-center sm:items-end">
                  <div className="text-[10px] text-zinc-500 font-mono">Bilancio Netto Posizione</div>
                  <div className={`text-base sm:text-lg font-black font-mono ${pnlPositive ? "text-emerald-400" : "text-red-400"}`}>
                    {pnlPositive ? "+" : ""}${trade.totalNetPnlUsd.toFixed(2)} ({pnlPositive ? "+" : ""}{trade.totalNetPnlPct.toFixed(1)}%)
                  </div>
                </div>
              </div>

              {/* Detailed Financial Metrics Grid for this single trade */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 p-3 rounded-xl bg-zinc-950/70 border border-zinc-800 text-xs font-mono">
                <div>
                  <span className="text-[10px] text-zinc-500 block">Capitale Investito</span>
                  <span className="text-zinc-200 font-bold">$100.00 ({trade.amountInvestedSol} SOL)</span>
                  <span className="text-[10px] text-zinc-500 block truncate">{trade.initialTokensAcquired.toLocaleString(undefined, { maximumFractionDigits: 0 })} TOKENS</span>
                </div>
                <div>
                  <span className="text-[10px] text-zinc-500 block">Prezzo Ingresso &rarr; MCAP</span>
                  <span className="text-zinc-300 font-bold">${trade.entryPriceUsd.toFixed(8)}</span>
                  <span className="text-[10px] text-zinc-500 block">MCAP: ${trade.entryMcapUsd.toLocaleString()}</span>
                </div>
                <div>
                  <span className="text-[10px] text-zinc-500 block">Cash Incassato ({soldPctLabel}%)</span>
                  <span className={`${trade.totalCashExtractedUsd > 0 ? "text-emerald-400" : "text-zinc-500"} font-bold`}>
                    ${trade.totalCashExtractedUsd.toFixed(2)}
                  </span>
                  <span className="text-[10px] text-zinc-500 block">{trade.exactSoldPct > 0 ? `Venduto ${soldPctLabel}% on-chain` : "Nessuna vendita"}</span>
                </div>
                <div>
                  <span className="text-[10px] text-zinc-500 block">Valore Token Residui</span>
                  <span className={`${isLoss ? "text-red-400" : "text-amber-400"} font-bold`}>
                    ${trade.currentPositionValueUsd.toFixed(2)}
                  </span>
                  <span className="text-[10px] text-zinc-400 block">MCAP Live: ${trade.currentMcapUsd.toLocaleString()}</span>
                </div>
              </div>

              {/* Remaining Tokens Status Row */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between text-xs font-mono p-2.5 rounded-lg bg-zinc-800/40 border border-zinc-700/40 gap-2">
                <div className="flex items-center gap-2">
                  <Coins className="w-4 h-4 text-amber-400 shrink-0" />
                  <span>
                    Token Detenuti nel Wallet: <b className="text-white">{trade.currentTokensHeld.toLocaleString(undefined, { maximumFractionDigits: 0 })} TOKENS</b> ({( (1 - trade.exactSoldPct) * 100 ).toFixed(0)}% residuo)
                  </span>
                </div>
                <div className={`${pnlPositive ? "text-emerald-400" : "text-red-400"} font-bold`}>
                  Valore Attuale: ${trade.currentPositionValueUsd.toFixed(2)} {trade.totalCashExtractedUsd > 0 && `(+ $${trade.totalCashExtractedUsd.toFixed(2)} Cash)`} (Totale: ${(trade.totalCashExtractedUsd + trade.currentPositionValueUsd).toFixed(2)})
                </div>
              </div>

              {/* Expand Action Logs */}
              <button
                onClick={() => setExpandedTradeId(isExpanded ? null : trade.id)}
                className="w-full pt-2 flex items-center justify-between text-[11px] font-mono text-zinc-400 hover:text-white transition-colors border-t border-zinc-800/60"
              >
                <span>Vedi Registro Transazioni Copiate dallo Smart Wallet ({trade.copyTradeLogs.length} eventi)</span>
                {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>

              {isExpanded && (
                <div className="p-3 rounded-xl bg-zinc-950/90 border border-zinc-800 space-y-2.5 text-xs font-mono">
                  {trade.copyTradeLogs.map((log: any, idx: number) => (
                    <div key={idx} className="flex items-start gap-2 text-[11px] text-zinc-300 pb-2 border-b border-zinc-800/60 last:border-0 last:pb-0">
                      <span className="text-zinc-500 shrink-0" suppressHydrationWarning>{new Date(log.timestamp).toLocaleTimeString()}</span>
                      <span className="text-zinc-200" dangerouslySetInnerHTML={{ __html: log.description }}></span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

    </div>
  );
};
