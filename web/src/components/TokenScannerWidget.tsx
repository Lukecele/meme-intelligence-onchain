"use client";

import React, { useState } from "react";
import { Search, Loader2, ShieldCheck, ShieldAlert, ArrowUpRight, Zap, CheckCircle2, AlertCircle } from "lucide-react";
import { CopyButton } from "./CopyButton";

export const TokenScannerWidget: React.FC = () => {
  const [mintInput, setMintInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleScan = async (mintToScan?: string) => {
    const target = (mintToScan || mintInput).trim();
    if (!target) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const resp = await fetch(`/api/scan?mint=${encodeURIComponent(target)}`);
      const data = await resp.json();
      if (!resp.ok || !data.success) {
        setError(data.error || "Impossibile analizzare questo mint address.");
      } else {
        setResult(data.data);
      }
    } catch (e: any) {
      setError(e.message || "Errore di connessione con il nodo RPC Solana.");
    } finally {
      setLoading(false);
    }
  };

  const presetMints = [
    { label: "WIF", mint: "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm" },
    { label: "BONK", mint: "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263" },
    { label: "POPCAT", mint: "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr" },
  ];

  return (
    <div className="space-y-4 sm:space-y-6">
      
      {/* Scanner Input Box */}
      <div className="p-4 sm:p-6 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-3.5 sm:space-y-4">
        <div>
          <h2 className="text-sm sm:text-base font-bold text-white flex items-center gap-2">
            <Zap className="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400" />
            Scanner On-Chain Token Solana (Live Helius RPC)
          </h2>
          <p className="text-[11px] sm:text-xs text-zinc-400 mt-0.5">
            Analizza un Mint Solana verificando authority on-chain e, quando disponibili, dati di mercato e concentrazione holder. Non costituisce una verifica completa anti-rug/honeypot.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-2.5">
          <div className="relative flex-1">
            <input
              type="text"
              placeholder="Incolla Mint Solana (es. EKpQGSJtjMFqKZ9...)"
              value={mintInput}
              onChange={(e) => setMintInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleScan()}
              className="w-full px-3.5 py-3 rounded-xl bg-zinc-800/70 border border-zinc-700/70 text-xs font-mono text-white placeholder-zinc-500 focus:outline-none focus:border-emerald-500/50"
            />
          </div>
          <button
            onClick={() => handleScan()}
            disabled={loading || !mintInput.trim()}
            className="w-full sm:w-auto px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 active:scale-95 disabled:opacity-50 text-black font-bold text-xs font-mono flex items-center justify-center gap-2 transition-all touch-manipulation"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
            <span>Analizza On-Chain</span>
          </button>
        </div>

        {/* Presets */}
        <div className="flex items-center gap-2 text-xs text-zinc-400 overflow-x-auto pb-1 no-scrollbar">
          <span className="shrink-0 text-[11px]">Prova rapida:</span>
          {presetMints.map((p) => (
            <button
              key={p.label}
              onClick={() => {
                setMintInput(p.mint);
                handleScan(p.mint);
              }}
              className="px-2.5 py-1 rounded-lg bg-zinc-800 hover:bg-zinc-700 active:scale-95 font-mono text-[11px] text-zinc-300 border border-zinc-700 shrink-0 transition-all touch-manipulation"
            >
              ${p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-3.5 rounded-xl bg-red-950/40 border border-red-500/30 text-xs text-red-300 flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 shrink-0 text-red-400" />
          <span className="text-[11px] sm:text-xs">{error}</span>
        </div>
      )}

      {/* Scan Results Card */}
      {result && (
        <div className="p-4 sm:p-6 rounded-2xl bg-zinc-900/90 border border-zinc-800 space-y-4 sm:space-y-6">
          
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 sm:pb-4 border-b border-zinc-800">
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-lg sm:text-2xl font-black font-mono text-white">${result.symbol}</span>
                <span className="text-xs text-zinc-400 font-mono">({result.name})</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full font-bold bg-zinc-800 text-emerald-400 border border-zinc-700">
                  {result.dexId}
                </span>
              </div>
              <div className="text-[11px] font-mono text-zinc-400 mt-1 flex items-center gap-2 flex-wrap break-all">
                <span>Mint: {result.mint}</span>
                <CopyButton text={result.mint} label="Copia Contratto" />
                <a
                  href={`https://dexscreener.com/solana/${result.mint}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-emerald-400 hover:underline flex items-center gap-0.5"
                >
                  DexScreener <ArrowUpRight className="w-3 h-3" />
                </a>
              </div>
            </div>

            <div className="flex items-center justify-between sm:justify-end sm:text-right pt-2 sm:pt-0 border-t sm:border-0 border-zinc-800">
              <div>
                <span className="text-[9px] font-mono text-cyan-400 font-bold px-1.5 py-0.2 rounded bg-cyan-500/10 border border-cyan-500/20 block mb-0.5">
                  MINT RPC + MARKET API
                </span>
                <span className="text-[10px] text-zinc-400 font-mono block">SAFETY & MICROCAP SCORE</span>
                <span className="text-xl sm:text-2xl font-black text-emerald-400 font-mono">{result.safetyMicrocapScore == null ? "N/D" : `${result.safetyMicrocapScore}/100`}</span>
              </div>
            </div>
          </div>

          {/* Metric Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-3 text-xs font-mono">
            <div className="p-2.5 sm:p-3.5 rounded-xl bg-zinc-800/40 border border-zinc-800">
              <span className="text-zinc-400 text-[10px] block">PREZZO USD</span>
              <span className="text-xs sm:text-sm font-bold text-white truncate block">${result.priceUsd.toFixed(6)}</span>
            </div>
            <div className="p-2.5 sm:p-3.5 rounded-xl bg-zinc-800/40 border border-zinc-800">
              <span className="text-zinc-400 text-[10px] block">MARKET CAP / FDV</span>
              <span className="text-xs sm:text-sm font-bold text-white truncate block">${result.marketCapUsd.toLocaleString()}</span>
            </div>
            <div className="p-2.5 sm:p-3.5 rounded-xl bg-zinc-800/40 border border-zinc-800">
              <span className="text-zinc-400 text-[10px] block">LIQUIDITÀ USD</span>
              <span className="text-xs sm:text-sm font-bold text-emerald-400 truncate block">${result.liquidityUsd.toLocaleString()}</span>
            </div>
            <div className="p-2.5 sm:p-3.5 rounded-xl bg-zinc-800/40 border border-zinc-800">
              <span className="text-zinc-400 text-[10px] block">VOLUME 24H</span>
              <span className="text-xs sm:text-sm font-bold text-zinc-200 truncate block">${result.volume24h.toLocaleString()}</span>
            </div>
          </div>

          {/* Safety & Risk Flags */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-zinc-300 mb-2 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Verifica authority e rischi osservabili
            </h4>
            <div className="p-3.5 rounded-xl bg-zinc-800/30 border border-zinc-800 space-y-1.5">
              {result.riskFlags.map((flag: string, idx: number) => (
                <div key={idx} className="flex items-start gap-2 text-[11px] sm:text-xs text-zinc-300">
                  <span className="text-emerald-400 mt-0.5">•</span>
                  <span>{flag}</span>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
};
