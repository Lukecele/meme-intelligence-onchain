"use client";

import React, { useState, useEffect } from "react";
import { Search, Filter, ArrowUpDown, ExternalLink, ShieldCheck, Eye, RefreshCw, Loader2, ArrowUpRight } from "lucide-react";
import { WalletProfile } from "../types";

interface SmartWalletLeaderboardProps {
  onSelectWallet: (wallet: WalletProfile) => void;
}

export const SmartWalletLeaderboard: React.FC<SmartWalletLeaderboardProps> = ({ onSelectWallet }) => {
  const [wallets, setWallets] = useState<WalletProfile[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState<"smartScore" | "selectivityScore" | "precocityAvgSec" | "totalWinnersEntered">("smartScore");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  const fetchWallets = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/wallets");
      const data = await res.json();
      if (data.success && Array.isArray(data.wallets)) {
        setWallets(data.wallets);
      }
    } catch (err) {
      console.error("Failed to fetch wallets:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWallets();
  }, []);

  const filteredWallets = wallets.filter((w) => {
    const term = searchTerm.toLowerCase();
    return (
      w.address.toLowerCase().includes(term) ||
      w.label.toLowerCase().includes(term) ||
      w.fundingSource.toLowerCase().includes(term)
    );
  }).sort((a, b) => {
    const valA = a[sortBy];
    const valB = b[sortBy];
    return sortOrder === "desc" ? (valB > valA ? 1 : -1) : (valA > valB ? 1 : -1);
  });

  const handleSort = (field: typeof sortBy) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === "desc" ? "asc" : "desc");
    } else {
      setSortBy(field);
      setSortOrder("desc");
    }
  };

  return (
    <div className="space-y-4 sm:space-y-6">
      
      {/* Controls Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3.5 sm:p-4 rounded-2xl bg-zinc-900/70 border border-zinc-800">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Cerca per indirizzo, label o funding..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-zinc-800/60 border border-zinc-700/60 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-emerald-500/50"
          />
        </div>

        <div className="flex items-center justify-between sm:justify-end gap-2">
          <button
            onClick={fetchWallets}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 active:scale-95 text-xs font-mono text-zinc-300 border border-zinc-700 transition-all touch-manipulation"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-emerald-400" : "text-zinc-400"}`} />
            <span>Ricarica</span>
          </button>
          <div className="text-xs font-mono text-zinc-400">
            <span>Totale:</span> <b className="text-emerald-400">{filteredWallets.length}</b>
          </div>
        </div>
      </div>

      {loading && wallets.length === 0 ? (
        <div className="p-8 sm:p-12 text-center rounded-2xl bg-zinc-900/60 border border-zinc-800 flex flex-col items-center justify-center space-y-3">
          <Loader2 className="w-8 h-8 text-emerald-400 animate-spin" />
          <span className="text-xs sm:text-sm font-mono text-zinc-400">Estrazione transazioni e scoring wallet in corso via Helius...</span>
        </div>
      ) : (
        <>
          {/* MOBILE CARDS VIEW (< md breakpoint) */}
          <div className="md:hidden space-y-3">
            {filteredWallets.map((wallet) => {
              const isTopTier = wallet.smartScore >= 85;
              return (
                <div
                  key={wallet.address}
                  className="p-4 rounded-xl bg-zinc-900/90 border border-zinc-800 space-y-3"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="font-semibold text-xs text-white flex items-center gap-1.5">
                        <span>{wallet.label}</span>
                        <a
                          href={`https://solscan.io/account/${wallet.address}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-zinc-500 hover:text-emerald-400"
                        >
                          <ArrowUpRight className="w-3 h-3" />
                        </a>
                      </div>
                      <div className="font-mono text-[11px] text-zinc-400 mt-0.5">
                        {wallet.address.slice(0, 8)}...{wallet.address.slice(-6)}
                      </div>
                    </div>

                    <span className={`px-2.5 py-1 rounded-full text-xs font-mono font-bold ${
                      isTopTier
                        ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                        : wallet.smartScore >= 70
                        ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                        : "bg-zinc-800 text-zinc-400 border border-zinc-700"
                    }`}>
                      {wallet.smartScore.toFixed(1)}
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-2 text-xs font-mono bg-zinc-950/40 p-2.5 rounded-lg border border-zinc-800/80">
                    <div>
                      <span className="text-[10px] text-zinc-500 block">SELETTIVITÀ</span>
                      <span className="text-emerald-400 font-bold">{wallet.selectivityScore.toFixed(1)}%</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-zinc-500 block">PRECOCITÀ</span>
                      <span className="text-zinc-300 font-bold">+{wallet.precocityAvgSec}s</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-zinc-500 block">WINNERS</span>
                      <span className="text-amber-400 font-bold">{wallet.totalWinnersEntered}</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <span className="text-[11px] font-mono text-zinc-400 truncate mr-2">
                      {wallet.fundingSource}
                    </span>
                    <button
                      onClick={() => onSelectWallet(wallet)}
                      className="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-emerald-500/20 hover:text-emerald-400 text-zinc-300 border border-zinc-700 text-xs font-mono flex items-center gap-1 shrink-0"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>Dettagli</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          {/* DESKTOP TABLE VIEW (>= md breakpoint) */}
          <div className="hidden md:block rounded-2xl bg-zinc-900/80 border border-zinc-800 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-zinc-800 bg-zinc-950/40 text-xs font-semibold text-zinc-400 uppercase tracking-wider">
                    <th className="py-3.5 px-4">Solana Wallet Address</th>
                    <th className="py-3.5 px-4 cursor-pointer hover:text-white" onClick={() => handleSort("smartScore")}>
                      <div className="flex items-center gap-1">
                        Smart Score <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                    <th className="py-3.5 px-4">Indipendenza</th>
                    <th className="py-3.5 px-4 cursor-pointer hover:text-white" onClick={() => handleSort("selectivityScore")}>
                      <div className="flex items-center gap-1">
                        Selettività <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                    <th className="py-3.5 px-4 cursor-pointer hover:text-white" onClick={() => handleSort("precocityAvgSec")}>
                      <div className="flex items-center gap-1">
                        Precocità Media <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                    <th className="py-3.5 px-4 cursor-pointer hover:text-white" onClick={() => handleSort("totalWinnersEntered")}>
                      <div className="flex items-center gap-1">
                        Winner Entrati <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                    <th className="py-3.5 px-4">Sorgente Funding</th>
                    <th className="py-3.5 px-4 text-center">Ispezione</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60">
                  {filteredWallets.map((wallet) => {
                    const isTopTier = wallet.smartScore >= 85;
                    return (
                      <tr
                        key={wallet.address}
                        className="hover:bg-zinc-800/40 transition-colors duration-100 group"
                      >
                        <td className="py-3.5 px-4">
                          <div className="flex items-center gap-2.5">
                            <div className="p-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-300 font-mono text-xs">
                              👤
                            </div>
                            <div>
                              <div className="font-semibold text-xs text-white flex items-center gap-1.5">
                                <span>{wallet.label}</span>
                                <a
                                  href={`https://solscan.io/account/${wallet.address}`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-zinc-500 hover:text-emerald-400 transition-colors"
                                >
                                  <ArrowUpRight className="w-3 h-3" />
                                </a>
                              </div>
                              <div className="font-mono text-xs text-zinc-400">
                                {wallet.address.slice(0, 8)}...{wallet.address.slice(-6)}
                              </div>
                            </div>
                          </div>
                        </td>

                        <td className="py-3.5 px-4">
                          <span className={`inline-block px-2.5 py-1 rounded-full text-xs font-mono font-bold ${
                            isTopTier
                              ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                              : wallet.smartScore >= 70
                              ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                              : "bg-zinc-800 text-zinc-400 border border-zinc-700"
                          }`}>
                            {wallet.smartScore.toFixed(1)}
                          </span>
                        </td>

                        <td className="py-3.5 px-4 font-mono text-xs text-zinc-300">
                          {wallet.independenceScore > 0 ? (
                            <span className="text-purple-400 font-semibold">{wallet.independenceScore.toFixed(0)}</span>
                          ) : (
                            <span className="text-zinc-600">-</span>
                          )}
                        </td>

                        <td className="py-3.5 px-4 font-mono text-xs">
                          <span className="font-semibold text-emerald-400">
                            {wallet.selectivityScore.toFixed(1)}%
                          </span>
                        </td>

                        <td className="py-3.5 px-4 font-mono text-xs text-zinc-300">
                          +{wallet.precocityAvgSec}s
                        </td>

                        <td className="py-3.5 px-4 font-mono text-xs text-zinc-300">
                          <span className="text-emerald-400 font-bold">{wallet.totalWinnersEntered}</span>
                          <span className="text-zinc-600"> / </span>
                          <span className="text-zinc-400">{wallet.totalTokensBought}</span>
                        </td>

                        <td className="py-3.5 px-4 font-mono text-[11px] text-zinc-400">
                          {wallet.fundingSource}
                        </td>

                        <td className="py-3.5 px-4 text-center">
                          <button
                            onClick={() => onSelectWallet(wallet)}
                            className="p-2 rounded-lg bg-zinc-800 hover:bg-emerald-500/20 hover:text-emerald-400 text-zinc-400 border border-zinc-700 transition-colors"
                            title="Ispeziona Wallet On-Chain"
                          >
                            <Eye className="w-3.5 h-3.5" />
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

    </div>
  );
};
