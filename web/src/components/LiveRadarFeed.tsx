"use client";

import React, { useState, useEffect, useRef } from "react";
import { Radio, ShieldCheck, RefreshCw, Loader2, ArrowUpRight, ChevronRight, CheckCircle2, LogOut, ListChecks, Users, Zap, Search, TrendingUp, TrendingDown, Coins, ExternalLink, Flame, Clock } from "lucide-react";
import { ConvergenceAlert } from "../types";
import { CopyButton } from "./CopyButton";

export const LiveRadarFeed: React.FC = () => {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
  const [monitoredCount, setMonitoredCount] = useState<number>(0);
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
  const detailRef = useRef<HTMLDivElement>(null);

  const fetchLiveRadar = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/radar", { cache: "no-store" });
      const data = await res.json();
      if (data.success) {
        setAlerts(data.alerts || []);
        if (data.monitoringWalletsCount) {
          setMonitoredCount(data.monitoringWalletsCount);
        }
        if (data.solPriceUsd) {
          setSolPrice(data.solPriceUsd);
        }
        if (data.alerts && data.alerts.length > 0) {
          if (!selectedAlert) {
            setSelectedAlert(data.alerts[0]);
          } else {
            const current = data.alerts.find((a: any) => a.tokenMint === selectedAlert.tokenMint);
            if (current) setSelectedAlert(current);
          }
        } else {
          setSelectedAlert(null);
        }
        setLastUpdated(new Date());
      }
    } catch (err) {
      console.error("Failed to fetch live radar:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLiveRadar();
    const interval = setInterval(fetchLiveRadar, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-4 sm:space-y-6">
      
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 sm:p-5 rounded-2xl bg-gradient-to-r from-emerald-950/30 via-zinc-900/60 to-zinc-900/60 border border-emerald-500/20">
        <div className="flex items-center gap-3">
          <div className="relative shrink-0">
            <div className="w-3 h-3 rounded-full bg-emerald-400 animate-ping"></div>
            <div className="w-3 h-3 rounded-full bg-emerald-500 absolute top-0 left-0"></div>
          </div>
          <div>
            <h2 className="text-sm sm:text-base font-bold text-white flex items-center gap-1.5 flex-wrap">
              <span>Radar Live Feed Solana</span>
              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                LIVE ORA &bull; {monitoredCount} SMART WALLET MONITORATI
              </span>
            </h2>
            <p className="text-[11px] sm:text-xs text-zinc-400" suppressHydrationWarning>
              Scansione continua convergenze on-chain &bull; SOL: ${solPrice.toFixed(2)} (Sync: {lastUpdated.toLocaleTimeString()})
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between sm:justify-end gap-2">
          <span className="text-[10px] sm:text-xs font-mono px-2 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 border border-zinc-700">
            Filtro: <b className="text-emerald-400">&ge; 2 Wallet Indipendenti</b>
          </span>
          <button
            onClick={fetchLiveRadar}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 active:scale-95 text-xs font-mono text-zinc-300 border border-zinc-700 transition-all touch-manipulation"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-emerald-400" : "text-zinc-400"}`} />
            <span>Scansiona Mempool</span>
          </button>
        </div>
      </div>

      {loading && alerts.length === 0 ? (
        <div className="p-8 sm:p-12 text-center rounded-2xl bg-zinc-900/60 border border-zinc-800 flex flex-col items-center justify-center space-y-3">
          <Loader2 className="w-8 h-8 text-emerald-400 animate-spin" />
          <span className="text-xs sm:text-sm font-mono text-zinc-400">Scansione mempool Solana in tempo reale...</span>
        </div>
      ) : alerts.length === 0 ? (
        <div className="p-8 sm:p-12 rounded-2xl bg-zinc-900/50 border border-zinc-800 text-center space-y-4 max-w-2xl mx-auto">
          <div className="w-16 h-16 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto animate-pulse">
            <Radio className="w-8 h-8" />
          </div>
          <div>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-zinc-800 text-emerald-400 border border-emerald-500/30">
              RADAR ATTIVO &bull; ZERO RUMORE
            </span>
            <h3 className="text-lg sm:text-xl font-bold text-white mt-2">
              In Attesa di Nuova Convergenza On-Chain
            </h3>
            <p className="text-xs sm:text-sm text-zinc-400 mt-1 max-w-lg mx-auto leading-relaxed">
              Il sistema monitora i <b>{monitoredCount} Smart Wallet Qualificati</b>. Mostra un allarme solo quando &ge; 2 wallet acquistano un micro-cap conforme ($FDV &le; $1M).
            </p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6">
          
          {/* Left Column: Alerts List */}
          <div className="lg:col-span-5 space-y-2.5 sm:space-y-3">
            <div className="text-xs font-bold uppercase tracking-wider text-zinc-400 px-1 flex justify-between items-center">
              <span>Token Rilevati Live & 24h ({alerts.length})</span>
              <span className="text-emerald-400 font-mono text-[11px]">Score & Convergenza</span>
            </div>

            {alerts.map((alert) => {
              const isSelected = selectedAlert?.tokenMint === alert.tokenMint;
              const isLive = alert.tokenAgeMinutes < 15;
              const timeLabel = isLive ? `${alert.tokenAgeMinutes}m fa` : `${(alert.tokenAgeMinutes / 60).toFixed(1)}h fa`;
              const isPositive = alert.priceChangePct >= 0;

              return (
                <div
                  key={alert.id || alert.tokenMint}
                  onClick={() => setSelectedAlert(alert)}
                  className={`p-3.5 sm:p-4 rounded-xl cursor-pointer transition-all duration-150 border active:scale-[0.99] touch-manipulation ${
                    isSelected
                      ? "bg-zinc-800/95 border-emerald-500/60 shadow-lg shadow-emerald-950/30"
                      : "bg-zinc-900/70 border-zinc-800/80 hover:bg-zinc-800/50 hover:border-zinc-700"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-black text-sm sm:text-base text-white">${alert.symbol}</span>
                      {isLive ? (
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded-full font-black bg-red-500/20 text-red-400 border border-red-500/40 animate-pulse flex items-center gap-1">
                          <Flame className="w-3 h-3 inline text-red-400" />
                          LIVE ORA
                        </span>
                      ) : (
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded-full font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                          {alert.signalLevel} ({alert.score}/100)
                        </span>
                      )}
                    </div>
                    <span className="text-[11px] font-mono text-zinc-400 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {timeLabel}
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-2 mt-2.5 text-xs font-mono">
                    <div>
                      <span className="text-zinc-500 text-[10px] block">MCAP ENTRATA &rarr; LIVE</span>
                      <span className="text-zinc-200 font-bold text-[11px] truncate block">
                        ${(alert.marketCapUsd/1000).toFixed(1)}k &rarr; <b className={isPositive ? "text-emerald-400" : "text-red-400"}>${(alert.currentMarketCapUsd/1000).toFixed(1)}k</b>
                      </span>
                    </div>
                    <div>
                      <span className="text-zinc-500 text-[10px] block">PREZZO LIVE</span>
                      <span className="text-zinc-200 font-bold text-[11px] truncate block">
                        ${alert.priceUsd ? alert.priceUsd.toFixed(7) : "0.000165"}
                      </span>
                    </div>
                    <div>
                      <span className="text-zinc-500 text-[10px] block">VARIAZIONE</span>
                      <span className={`${isPositive ? "text-emerald-400" : "text-red-400"} font-bold text-[11px] truncate block flex items-center gap-0.5`}>
                        {isPositive ? <TrendingUp className="w-3 h-3 inline" /> : <TrendingDown className="w-3 h-3 inline" />}
                        {isPositive ? "+" : ""}{alert.priceChangePct}%
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right Column: Alert Detail Inspector */}
          <div ref={detailRef} className="lg:col-span-7">
            {selectedAlert && (
              <div className="p-4 sm:p-6 rounded-2xl bg-zinc-900/90 border border-zinc-800 space-y-4 sm:space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 sm:pb-4 border-b border-zinc-800 gap-2">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-lg sm:text-2xl font-black text-white font-mono">${selectedAlert.symbol}</h3>
                      <span className="text-xs text-zinc-400">{selectedAlert.name}</span>
                    </div>
                    <div className="text-[11px] font-mono text-zinc-400 mt-1 flex items-center gap-2 flex-wrap">
                      <span>Mint: {selectedAlert.tokenMint}</span>
                      <CopyButton text={selectedAlert.tokenMint} label="Copia Contratto" />
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] text-zinc-500 font-mono block">SCORE & CONVERGENZA</span>
                    <span className="text-xl sm:text-2xl font-black text-emerald-400 font-mono">{selectedAlert.score}/100</span>
                  </div>
                </div>

                {/* Market Cap & Price Comparison */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-3.5 rounded-xl bg-zinc-950/60 border border-zinc-800 text-xs font-mono">
                  <div>
                    <span className="text-[10px] text-zinc-500 block">MCAP all&apos;Ingresso</span>
                    <span className="text-zinc-300 font-bold">${selectedAlert.marketCapUsd.toLocaleString()}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-zinc-500 block">MCAP Attuale Live</span>
                    <span className={`${selectedAlert.priceChangePct >= 0 ? "text-emerald-400" : "text-red-400"} font-bold`}>
                      ${selectedAlert.currentMarketCapUsd.toLocaleString()}
                    </span>
                  </div>
                  <div>
                    <span className="text-[10px] text-zinc-500 block">Prezzo Attuale Sub-Sec</span>
                    <span className="text-white font-bold">${selectedAlert.priceUsd.toFixed(8)}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-zinc-500 block">Liquidità DEX</span>
                    <span className="text-zinc-300 font-bold">${selectedAlert.liquidityUsd.toLocaleString()}</span>
                  </div>
                </div>

                {/* Smart Wallets Breakdown with Positions, Holdings & Sells */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-zinc-300 mb-2.5 flex items-center justify-between">
                    <span className="flex items-center gap-1.5">
                      <Users className="w-4 h-4 text-emerald-400" />
                      Smart Wallet Qualificati Coinvolti ({selectedAlert.walletsInvolved.length})
                    </span>
                    <span className="text-[11px] font-mono text-zinc-500">Stato Holding & Uscite On-Chain</span>
                  </h4>
                  
                  <div className="space-y-3">
                    {selectedAlert.walletsInvolved.map((w: any, idx: number) => {
                      const soldPct = w.tokensBought > 0 ? ((w.tokensSold / w.tokensBought) * 100).toFixed(0) : "0";
                      const isFullExit = w.positionStatus === "FULL_EXIT" || (w.tokensBought > 0 && w.tokensSold >= w.tokensBought);
                      const isDeRisked = w.positionStatus === "PARTIAL_EXIT" || (w.tokensSold > 0 && !isFullExit);

                      return (
                        <div key={idx} className="p-3.5 rounded-xl bg-zinc-950/80 border border-zinc-800 space-y-2 text-xs font-mono">
                          <div className="flex items-center justify-between flex-wrap gap-2">
                            <div>
                              <div className="text-white font-bold flex items-center gap-2">
                                <span>{w.label}</span>
                                <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${
                                  isDeRisked
                                    ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                                    : isFullExit
                                    ? "bg-red-500/20 text-red-400 border border-red-500/30"
                                    : "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                                }`}>
                                  {isDeRisked ? `🛡️ DE-RISKED ${soldPct}%` : isFullExit ? "🔴 LIQUIDATO 100%" : "🟢 IN HOLDING 100%"}
                                </span>
                              </div>
                              <div className="text-[10px] text-zinc-500 flex items-center gap-1.5 mt-0.5">
                                <span>{w.address}</span>
                                <a
                                  href={`https://solscan.io/account/${w.address}`}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="text-zinc-400 hover:text-emerald-400"
                                >
                                  <ExternalLink className="w-3 h-3 inline" />
                                </a>
                              </div>
                            </div>

                            <div className="text-right">
                              <span className="text-emerald-400 font-bold text-xs block">Smart Score: {w.score}/100</span>
                              <span className="text-[10px] text-zinc-400">Entrato con: <b>{w.amountSol} SOL</b> (${(w.amountSol * solPrice).toFixed(2)})</span>
                            </div>
                          </div>

                          {/* Token Balances Row */}
                          <div className="grid grid-cols-3 gap-2 pt-2 border-t border-zinc-800/60 text-[11px]">
                            <div>
                              <span className="text-zinc-500 text-[10px] block">Token Acquistati</span>
                              <span className="text-zinc-300 font-bold">{w.tokensBought.toLocaleString()}</span>
                            </div>
                            <div>
                              <span className="text-zinc-500 text-[10px] block">Token Venduti ({soldPct}%)</span>
                              <span className="text-emerald-400 font-bold">{w.tokensSold.toLocaleString()} ({soldPct}%)</span>
                            </div>
                            <div>
                              <span className="text-zinc-500 text-[10px] block">Token Residui Detenuti</span>
                              <span className="text-amber-400 font-bold">{w.currentHoldingTokens.toLocaleString()}</span>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

              </div>
            )}
          </div>

        </div>
      )}

    </div>
  );
};
