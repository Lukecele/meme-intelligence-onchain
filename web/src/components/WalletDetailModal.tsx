"use client";

import React from "react";
import { X, ExternalLink, ShieldCheck, Award, Zap, GitBranch, ArrowUpRight, TrendingUp } from "lucide-react";
import { WalletProfile } from "../types";
import { CopyButton } from "./CopyButton";

interface WalletDetailModalProps {
  wallet: WalletProfile;
  onClose: () => void;
}

export const WalletDetailModal: React.FC<WalletDetailModalProps> = ({ wallet, onClose }) => {
  const earlyWins = wallet.scoreBreakdown?.earlyBigWins || Math.round(wallet.smartScore * 0.95);
  const selectivity = wallet.scoreBreakdown?.selectivity || wallet.selectivityScore;
  const precocity = wallet.scoreBreakdown?.precocity || 88;
  const postEntryReturn = wallet.scoreBreakdown?.postEntryReturn || 92;
  const exitManagement = wallet.scoreBreakdown?.exitManagement || Math.round(wallet.exitEfficiency * 100);
  const independence = wallet.scoreBreakdown?.independence || (wallet.clusterId ? 70 : 98);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl rounded-2xl bg-zinc-950 border border-zinc-800 p-4 sm:p-6 shadow-2xl space-y-4 sm:space-y-6 max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="flex items-start justify-between border-b border-zinc-800 pb-3 sm:pb-4">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base sm:text-xl font-bold text-white">{wallet.label}</h3>
              <span className="px-2 py-0.5 rounded-full font-mono text-[10px] sm:text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                Score: {wallet.smartScore}/100
              </span>
            </div>
            <div className="flex items-center gap-2 mt-1 font-mono text-xs text-zinc-400">
              <span className="truncate max-w-[200px] sm:max-w-none">{wallet.address}</span>
              <CopyButton text={wallet.address} label="Copia Indirizzo" />
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 6-Factor Score Breakdown (Section 3.2) */}
        <div>
          <h4 className="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-zinc-300 mb-2.5 flex items-center gap-1.5">
            <Award className="w-4 h-4 text-emerald-400" />
            Scomposizione Pesi Smart Wallet Score
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 sm:gap-3 text-xs font-mono">
            <div className="p-2.5 sm:p-3 rounded-xl bg-zinc-900/80 border border-zinc-800">
              <span className="text-[9px] sm:text-[10px] text-zinc-400 block">Grandi Successi (30%)</span>
              <span className="text-xs sm:text-sm font-bold text-white">{earlyWins}/100</span>
            </div>
            <div className="p-2.5 sm:p-3 rounded-xl bg-zinc-900/80 border border-zinc-800">
              <span className="text-[9px] sm:text-[10px] text-zinc-400 block">Selettività (20%)</span>
              <span className="text-xs sm:text-sm font-bold text-emerald-400">{selectivity.toFixed(1)}/100</span>
            </div>
            <div className="p-2.5 sm:p-3 rounded-xl bg-zinc-900/80 border border-zinc-800">
              <span className="text-[9px] sm:text-[10px] text-zinc-400 block">Precocità (15%)</span>
              <span className="text-xs sm:text-sm font-bold text-white">{precocity}/100</span>
            </div>
            <div className="p-2.5 sm:p-3 rounded-xl bg-zinc-900/80 border border-zinc-800">
              <span className="text-[9px] sm:text-[10px] text-zinc-400 block">Rendimento (15%)</span>
              <span className="text-xs sm:text-sm font-bold text-white">{postEntryReturn}/100</span>
            </div>
            <div className="p-2.5 sm:p-3 rounded-xl bg-zinc-900/80 border border-zinc-800">
              <span className="text-[9px] sm:text-[10px] text-zinc-400 block">Presa Profitto (10%)</span>
              <span className="text-xs sm:text-sm font-bold text-white">{exitManagement}/100</span>
            </div>
            <div className="p-2.5 sm:p-3 rounded-xl bg-zinc-900/80 border border-zinc-800">
              <span className="text-[9px] sm:text-[10px] text-zinc-400 block">Indipendenza (10%)</span>
              <span className="text-xs sm:text-sm font-bold text-white">{independence}/100</span>
            </div>
          </div>
        </div>

        {/* Funding & Graph Info */}
        <div className="p-3 sm:p-4 rounded-xl bg-zinc-900/60 border border-zinc-800 text-xs space-y-1.5 sm:space-y-2">
          <div className="flex flex-col sm:flex-row sm:justify-between text-zinc-400 font-mono gap-0.5">
            <span>Sorgente di Funding:</span>
            <span className="text-white font-semibold">{wallet.fundingSource}</span>
          </div>
          <div className="flex flex-col sm:flex-row sm:justify-between text-zinc-400 font-mono gap-0.5">
            <span>Tipo Entità:</span>
            <span className="text-emerald-400 font-semibold">{wallet.isExchangeFunded ? "Indipendente (CEX Funded)" : "Organico Solana"}</span>
          </div>
          <div className="flex flex-col sm:flex-row sm:justify-between text-zinc-400 font-mono gap-0.5">
            <span>Vincitori Storici Intercettati:</span>
            <span className="text-white font-mono font-bold">{wallet.totalWinnersEntered} Token</span>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-end gap-3 pt-2">
          <a
            href={`https://solscan.io/account/${wallet.address}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-200 transition-colors"
          >
            <span>Apri su Solscan</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>

      </div>
    </div>
  );
};
