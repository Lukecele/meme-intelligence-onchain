"use client";

import React, { useState } from "react";
import { Radio, ShieldCheck, Database, Zap, FileSpreadsheet, Award, Wifi, ChevronDown } from "lucide-react";
import validation from "../lib/validation_result.json";
import { SMART_WALLETS } from "../lib/data";

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab }) => {
  const [showApiStatus, setShowApiStatus] = useState(false);
  const v = validation as any;
  const isVal = v.status === "VALIDATED";

  const tabs = [
    { id: "radar", label: "Radar Live", icon: Radio, badge: "LIVE", badgeColor: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
    { id: "simulator", label: "Simulatore $100", icon: Zap, badge: "DEMO", badgeColor: "bg-amber-500/20 text-amber-400 border-amber-500/30" },
    { id: "wallets", label: "Smart Wallets", icon: ShieldCheck, count: String(SMART_WALLETS.length) },
    { id: "scanner", label: "Scanner", icon: Zap, badge: "ON-CHAIN", badgeColor: "bg-cyan-500/20 text-cyan-400 border-cyan-500/30" },
    { id: "clusters", label: "Cluster", icon: Database },
    { id: "matrix", label: "Matrice", icon: FileSpreadsheet },
    { id: "backtest", label: "Sprint 1", icon: Award, badge: isVal ? "VALIDATO" : "NON VALIDATO", badgeColor: isVal ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" : "bg-amber-500/20 text-amber-400 border-amber-500/30" },
    { id: "guide", label: "Guida", icon: FileSpreadsheet, badge: "INFO", badgeColor: "bg-zinc-700 text-zinc-300 border-zinc-600" },
  ];

  return (
    <header className="border-b border-zinc-800/80 bg-[#0c0e15]/95 sticky top-0 z-40 backdrop-blur-xl transition-all">
      {/* Global Status Banner */}
      <div className="bg-amber-500/10 border-b border-amber-500/20 px-3 py-1.5 text-center text-[11px] sm:text-xs font-mono text-amber-300/90">
        ⚠️ <strong>Research Baseline v8</strong>: Framework sperimentale on-chain. L&apos;ingestione completa richiede chiavi Helius e Birdeye configurate. Dati sintetici rimossi.
      </div>
      <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        
        {/* Top brand row */}
        <div className="flex items-center justify-between py-3 sm:py-4 border-b border-zinc-800/40 gap-2">
          
          {/* Logo & Title */}
          <div className="flex items-center space-x-2.5 sm:space-x-3.5 min-w-0">
            <div className="relative flex items-center justify-center w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-tr from-emerald-600/30 to-teal-500/20 border border-emerald-500/30 shadow-lg shadow-emerald-950/40 shrink-0">
              <span className="text-base sm:text-xl">🎯</span>
              <div className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></div>
              <div className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
            </div>
            
            <div className="min-w-0">
              <div className="flex items-center gap-1.5 flex-wrap">
                <h1 className="text-sm sm:text-lg font-black tracking-tight text-white truncate">
                  SOLANA ON-CHAIN RADAR
                </h1>
                <span className="hidden xs:inline-block text-[9px] sm:text-[10px] font-mono font-bold px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  v1.0
                </span>
              </div>
              <p className="text-[11px] sm:text-xs text-zinc-400 truncate">
                Meme Coin Intelligence & Smart Convergence
              </p>
            </div>
          </div>

          {/* Desktop Status Chips / Mobile Toggle */}
          <div className="hidden lg:flex items-center gap-2 text-xs font-mono">
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-zinc-900/80 border border-zinc-800 text-zinc-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span>Helius:</span>
              <span className="text-emerald-400 font-semibold">Active</span>
            </div>
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-zinc-900/80 border border-zinc-800 text-zinc-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span>Birdeye:</span>
              <span className="text-emerald-400 font-semibold">Active</span>
            </div>
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-zinc-900/80 border border-zinc-800 text-zinc-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span>Pyth:</span>
              <span className="text-emerald-400 font-semibold">Live</span>
            </div>
          </div>

          {/* Mobile Status Button */}
          <button
            onClick={() => setShowApiStatus(!showApiStatus)}
            className="lg:hidden flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-[11px] font-mono text-emerald-400 shrink-0"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>API Online</span>
            <ChevronDown className={`w-3 h-3 text-zinc-400 transition-transform ${showApiStatus ? "rotate-180" : ""}`} />
          </button>
        </div>

        {/* Mobile Expandable API Status Bar */}
        {showApiStatus && (
          <div className="lg:hidden py-2 px-3 bg-zinc-900/90 rounded-xl border border-zinc-800 my-2 grid grid-cols-3 gap-2 text-[10px] font-mono text-center">
            <div className="p-1.5 rounded bg-zinc-800/60 text-zinc-300">
              <span className="block text-zinc-500">Helius RPC</span>
              <span className="text-emerald-400 font-bold">● Active</span>
            </div>
            <div className="p-1.5 rounded bg-zinc-800/60 text-zinc-300">
              <span className="block text-zinc-500">Birdeye</span>
              <span className="text-emerald-400 font-bold">● Active</span>
            </div>
            <div className="p-1.5 rounded bg-zinc-800/60 text-zinc-300">
              <span className="block text-zinc-500">Pyth Hermes</span>
              <span className="text-emerald-400 font-bold">● Live</span>
            </div>
          </div>
        )}

        {/* Touch-optimized Navigation Tabs */}
        <nav className="flex space-x-1 sm:space-x-2 overflow-x-auto py-2 sm:py-2.5 no-scrollbar scroll-smooth">
          {tabs.map((tab) => {
            const Icon = tab.icon as React.ElementType;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setShowApiStatus(false);
                }}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-150 whitespace-nowrap touch-manipulation active:scale-95 ${
                  isActive
                    ? "bg-zinc-800 text-emerald-400 border border-emerald-500/40 shadow-sm"
                    : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40 border border-transparent"
                }`}
              >
                {Icon && <Icon className={`w-3.5 h-3.5 sm:w-4 sm:h-4 ${isActive ? "text-emerald-400" : "text-zinc-500"}`} />}
                <span>{tab.label}</span>
                {tab.badge && (
                  <span className={`text-[9px] font-mono px-1 py-0.2 rounded font-bold border ${tab.badgeColor || "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"}`}>
                    {tab.badge}
                  </span>
                )}
                {tab.count && (
                  <span className="text-[9px] font-mono px-1.5 py-0.2 rounded font-bold bg-zinc-800 text-zinc-300 border border-zinc-700">
                    {tab.count}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

      </div>
    </header>
  );
};
