"use client";

import React, { useState } from "react";
import { Header } from "../components/Header";
import { MetricCards } from "../components/MetricCards";
import { LiveRadarFeed } from "../components/LiveRadarFeed";
import { SmartWalletLeaderboard } from "../components/SmartWalletLeaderboard";
import { WalletDetailModal } from "../components/WalletDetailModal";
import { ClusterGraphViewer } from "../components/ClusterGraphViewer";
import { IntersectionMatrixView } from "../components/IntersectionMatrixView";
import { BacktestReportView } from "../components/BacktestReportView";
import { TokenScannerWidget } from "../components/TokenScannerWidget";
import { SimpleGuideView } from "../components/SimpleGuideView";
import { InvestmentSimulator } from "../components/InvestmentSimulator";
import { WalletProfile } from "../types";

export default function Home() {
  const [activeTab, setActiveTab] = useState("radar");
  const [selectedWallet, setSelectedWallet] = useState<WalletProfile | null>(null);

  return (
    <div className="min-h-screen bg-[#08090d] text-zinc-100 flex flex-col selection:bg-emerald-500/30 selection:text-emerald-300">
      
      {/* Top Navbar */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* KPI Metrics Strip */}
        <MetricCards />

        {/* Dynamic Tab Views */}
        <div className="transition-all duration-150">
          {activeTab === "radar" && <LiveRadarFeed />}
          {activeTab === "simulator" && <InvestmentSimulator />}
          {activeTab === "wallets" && <SmartWalletLeaderboard onSelectWallet={setSelectedWallet} />}
          {activeTab === "scanner" && <TokenScannerWidget />}
          {activeTab === "clusters" && <ClusterGraphViewer />}
          {activeTab === "matrix" && <IntersectionMatrixView />}
          {activeTab === "backtest" && <BacktestReportView />}
          {activeTab === "guide" && <SimpleGuideView />}
        </div>

      </main>

      {/* Wallet Inspector Modal */}
      {selectedWallet && (
        <WalletDetailModal
          wallet={selectedWallet}
          onClose={() => setSelectedWallet(null)}
        />
      )}

      {/* Footer */}
      <footer className="border-t border-zinc-800/60 bg-[#090b10] py-6 text-center text-xs text-zinc-500 font-mono">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>Solana On-Chain Intelligence System • Production Radar v1.0</span>
          <span>Vercel Compatible • Helius, Birdeye & Pyth Integrated</span>
        </div>
      </footer>

    </div>
  );
}
