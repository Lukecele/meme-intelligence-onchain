"use client";

import React from "react";
import { Network, ShieldAlert, Users, ArrowRight, ArrowDown } from "lucide-react";
import { CLUSTERS } from "../lib/data";

export const ClusterGraphViewer: React.FC = () => {
  const cluster = CLUSTERS && CLUSTERS.length > 0 ? CLUSTERS[0] : null;

  return (
    <div className="space-y-4 sm:space-y-6">
      
      <div className="p-4 sm:p-5 rounded-2xl bg-zinc-900/70 border border-purple-500/20 space-y-1.5 sm:space-y-2">
        <div className="flex items-center gap-2 text-purple-400 font-bold text-xs sm:text-sm">
          <Network className="w-4 h-4 shrink-0" />
          <span>Analisi Grafi di Funding & Rilevamento Sybil (Sezione 4)</span>
        </div>
        <p className="text-[11px] sm:text-xs text-zinc-400">
          Un singolo indirizzo non equivale a una persona: il motore ricostruisce l&apos;albero dei trasferimenti SOL per accorpare wallet coordinati ed eliminare falsi segnali indipendenti.
        </p>
      </div>

      {!cluster ? (
        <div className="p-10 rounded-2xl bg-zinc-900/80 border border-zinc-800 text-center">
          <Network className="w-10 h-10 text-zinc-600 mx-auto mb-4 animate-pulse" />
          <h3 className="text-white font-bold mb-2">Generazione Cluster in corso...</h3>
          <p className="text-xs text-zinc-400">Il motore di graph analysis sta elaborando le relazioni di funding on-chain sui nuovi portafogli importati.</p>
        </div>
      ) : (
        <div className="p-4 sm:p-6 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-4 sm:space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 sm:pb-4 border-b border-zinc-800">
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono font-bold text-sm sm:text-base text-white">{cluster.clusterId}</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
                  Confidenza: {(cluster.confidence * 100).toFixed(0)}%
                </span>
              </div>
              <span className="text-[11px] sm:text-xs text-zinc-400 font-mono">Tipo Relazione: {cluster.relationType}</span>
            </div>

            <div className="flex items-center gap-3 text-xs font-mono">
              <div>
                <span className="text-zinc-500 text-[10px] block">NODI</span>
                <span className="text-white font-bold">{cluster.members.length} wallet</span>
              </div>
              <div>
                <span className="text-zinc-500 text-[10px] block">AVG SMART SCORE</span>
                <span className="text-emerald-400 font-bold">{cluster.avgScore}/100</span>
              </div>
            </div>
          </div>

          <div className="p-4 sm:p-6 rounded-xl bg-zinc-950/60 border border-zinc-800 flex flex-col md:flex-row items-center justify-center gap-4 sm:gap-6">
            
            <div className="p-3 sm:p-4 rounded-xl bg-purple-950/40 border border-purple-500/40 text-center w-full md:w-auto min-w-[180px] shadow-lg shadow-purple-950/30">
              <span className="text-[9px] font-mono font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                ROOT PARENT FUNDER
              </span>
              <div className="font-mono text-xs font-bold text-white mt-1.5">
                {cluster.rootAddress.slice(0, 6)}...{cluster.rootAddress.slice(-4)}
              </div>
              <span className="text-[10px] text-zinc-400 block mt-0.5">Emette 2.5 SOL per nodo</span>
            </div>

            <div className="flex md:hidden items-center justify-center text-purple-400">
              <ArrowDown className="w-5 h-5 animate-bounce" />
            </div>
            <div className="hidden md:flex flex-col items-center text-zinc-600 font-mono text-xs">
              <span>Trasferimento Diretto</span>
              <ArrowRight className="w-5 h-5 text-purple-400" />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 w-full md:w-auto">
              {cluster.members.slice(1).map((addr: string, idx: number) => (
                <div key={idx} className="p-3 rounded-xl bg-zinc-900 border border-zinc-700 text-center">
                  <span className="text-[9px] font-mono text-zinc-400 block">CHILD SUB-WALLET {idx + 1}</span>
                  <div className="font-mono text-xs font-semibold text-emerald-400 mt-0.5">
                    {addr.slice(0, 6)}...{addr.slice(-4)}
                  </div>
                  <span className="text-[10px] text-zinc-500 block mt-0.5">Acquisto &le; 24s dal pool</span>
                </div>
              ))}
            </div>

          </div>

          <div className="p-3 sm:p-4 rounded-xl bg-zinc-800/30 border border-zinc-800 text-[11px] sm:text-xs text-zinc-400 flex items-start gap-2.5">
            <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <b className="text-zinc-200">Perché è essenziale (Sez. 4.1):</b> Tre wallet coordinati dallo stesso genitore sembrano tre segnali indipendenti. Il radar li comprime in un&apos;unica entità di segnale reale, evitando falsi allarmi.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
