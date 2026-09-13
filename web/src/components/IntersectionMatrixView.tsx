"use client";

import React from "react";
import { FileSpreadsheet, CheckCircle2, Minus, ArrowRight } from "lucide-react";
import { SMART_WALLETS, HISTORICAL_TOKENS } from "../lib/data";
import { WalletProfile } from "../types";

export const IntersectionMatrixView: React.FC = () => {
  const winnerTokens = HISTORICAL_TOKENS.filter((t) => t.isWinner);
  const controlTokens = HISTORICAL_TOKENS.filter((t) => t.isControl);

  return (
    <div className="space-y-4 sm:space-y-6">
      
      <div className="p-4 sm:p-5 rounded-2xl bg-zinc-900/70 border border-zinc-800 space-y-1.5 sm:space-y-2">
        <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs sm:text-sm">
          <FileSpreadsheet className="w-4 h-4 shrink-0" />
          <span>Matrice di Intersezione Wallet &times; Token (Sezione 4.3 & 10.2)</span>
        </div>
        <p className="text-[11px] sm:text-xs text-zinc-400">
          Misurazione della ricorrenza precoce nei vincitori rispetto al gruppo di controllo. Esclude il survivorship bias dimostrando che gli smart wallet non comprano indiscriminatamente i token falliti.
        </p>
      </div>

      <div className="md:hidden flex items-center justify-between text-[11px] font-mono text-zinc-500 px-1">
        <span>← Scorri orizzontalmente la tabella →</span>
      </div>

      <div className="rounded-2xl bg-zinc-900/80 border border-zinc-800 overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left min-w-[650px]">
            <thead>
              <tr className="border-b border-zinc-800 bg-zinc-950/60 text-xs">
                <th className="py-3 px-3.5 text-xs font-semibold text-zinc-400 uppercase tracking-wider sticky left-0 bg-zinc-950 z-10">
                  Wallet Profilato
                </th>
                
                {winnerTokens.map((t) => (
                  <th key={t.mint} className="py-3 px-2.5 text-center text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                    {t.symbol}
                    <span className="block text-[9px] text-zinc-500 font-normal">Winner</span>
                  </th>
                ))}

                {controlTokens.map((t) => (
                  <th key={t.mint} className="py-3 px-2.5 text-center text-xs font-semibold text-red-400 uppercase tracking-wider">
                    {t.symbol.replace("_FAIL", "")}
                    <span className="block text-[9px] text-zinc-500 font-normal">Controllo</span>
                  </th>
                ))}

                <th className="py-3 px-3 text-center text-xs font-semibold text-zinc-300 uppercase tracking-wider">
                  Hit Rate
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-zinc-800/60">
              {SMART_WALLETS.slice(0, 35).map((w: WalletProfile) => {
                const hits = w.totalWinnersEntered;
                const total = w.totalTokensBought;
                const hitRate = total > 0 ? ((hits / total) * 100).toFixed(1) : "0";

                return (
                  <tr key={w.address} className="hover:bg-zinc-800/30 transition-colors text-xs">
                    <td className="py-3 px-3.5 sticky left-0 bg-zinc-900/95 z-10">
                      <div className="font-semibold text-white truncate max-w-[140px] sm:max-w-none">{w.label}</div>
                      <div className="font-mono text-[10px] text-zinc-400">
                        {w.address.slice(0, 6)}...{w.address.slice(-4)}
                      </div>
                    </td>

                    {winnerTokens.map((t) => {
                      const present = (w.hitTokens || []).includes(t.symbol);
                      return (
                        <td key={t.mint} className="py-3 px-2.5 text-center">
                          {present ? (
                            <span className="inline-flex items-center justify-center w-5 h-5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold text-xs">
                              ✓
                            </span>
                          ) : (
                            <span className="text-zinc-700 text-xs">-</span>
                          )}
                        </td>
                      );
                    })}

                    {controlTokens.map((t) => {
                      const presentInControl = (w.controlTokens || []).includes(t.symbol);
                      return (
                        <td key={t.mint} className="py-3 px-2.5 text-center">
                          {presentInControl ? (
                            <span className="inline-flex items-center justify-center w-5 h-5 rounded bg-red-500/20 text-red-400 border border-red-500/30 font-bold text-xs">
                              ✗
                            </span>
                          ) : (
                            <span className="text-zinc-700 text-xs">-</span>
                          )}
                        </td>
                      );
                    })}

                    <td className="py-3 px-3 text-center font-mono text-xs font-bold text-emerald-400">
                      {`${hitRate}%`}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
