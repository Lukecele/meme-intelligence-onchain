"use client";

import React from "react";
import { BookOpen, Target, ShieldCheck, Zap, HelpCircle, CheckCircle2, AlertTriangle, ArrowRight, Copy } from "lucide-react";
import { CopyButton } from "./CopyButton";

export const SimpleGuideView: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      
      {/* Hero Guide Banner */}
      <div className="p-5 sm:p-7 rounded-2xl bg-gradient-to-r from-emerald-950/40 via-zinc-900/90 to-zinc-900/90 border border-emerald-500/30 space-y-2">
        <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs sm:text-sm uppercase tracking-wider font-mono">
          <BookOpen className="w-4 h-4" />
          <span>Guida Rapida & Istruzioni Semplificate</span>
        </div>
        <h2 className="text-xl sm:text-3xl font-black text-white">
          Come usare il Radar On-Chain in 3 Passi
        </h2>
        <p className="text-xs sm:text-sm text-zinc-300">
          Tutto quello che c&apos;è da sapere spiegato in modo semplice e diretto, per comprendere gli allarmi e analizzare i token senza perdersi nel gergo tecnico.
        </p>
      </div>

      {/* 3 Simple Steps */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <div className="p-5 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-3">
          <div className="w-8 h-8 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-mono font-bold text-sm border border-emerald-500/30">
            1
          </div>
          <h3 className="font-bold text-sm text-white">Guarda il Live Radar</h3>
          <p className="text-xs text-zinc-400 leading-relaxed">
            Il Radar monitora i nuovi lanci su Solana. Quando vedi un segnale con badge <b className="text-emerald-400">ALTO</b>, significa che più wallet esperti sono entrati nello stesso token entro pochi minuti.
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-3">
          <div className="w-8 h-8 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-mono font-bold text-sm border border-cyan-500/30">
            2
          </div>
          <h3 className="font-bold text-sm text-white">Copia il Mint Address</h3>
          <p className="text-xs text-zinc-400 leading-relaxed">
            Su ogni token o alert c&apos;è il pulsante <b className="text-white font-mono">Copia</b>. Cliccandolo copi l&apos;indirizzo di contratto univoco di 44 caratteri per incollarlo su DEX o wallet.
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-3">
          <div className="w-8 h-8 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center font-mono font-bold text-sm border border-amber-500/30">
            3
          </div>
          <h3 className="font-bold text-sm text-white">Verifica con lo Scanner</h3>
          <p className="text-xs text-zinc-400 leading-relaxed">
            Nella scheda <b className="text-white">Scanner</b> puoi incollare qualsiasi contratto per verificare all&apos;istante se è sicuro (Honeypot, Freeze Authority revocata, liquidità reale).
          </p>
        </div>

      </div>

      {/* Deep-Dive: Come Funziona il Punteggio (Score) */}
      <div className="p-5 sm:p-6 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Target className="w-5 h-5 text-emerald-400" />
          Come interpretare i Punteggi (Score)
        </h3>

        <div className="space-y-3 text-xs">
          
          <div className="p-3.5 rounded-xl bg-zinc-800/40 border border-zinc-800 space-y-1">
            <div className="flex items-center justify-between font-mono">
              <span className="font-bold text-white">Smart Score Wallet (da 0 a 100)</span>
              <span className="text-emerald-400 font-bold">&ge; 70 = Qualificato</span>
            </div>
            <p className="text-zinc-400">
              Misura la bravura reale di un wallet. <b>Regola chiave:</b> se un bot compra 2.000 meme coin alla cieca per trovarne 1 buona, il suo score viene azzerato a 0. Solo i wallet selettivi che comprano pochi token con alto tasso di successo ottengono score &ge; 80.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-zinc-800/40 border border-zinc-800 space-y-1">
            <div className="flex items-center justify-between font-mono">
              <span className="font-bold text-white">Safety Score Token (da 0 a 100)</span>
              <span className="text-emerald-400 font-bold">&ge; 75 = Sicuro</span>
            </div>
            <p className="text-zinc-400">
              Verifica i parametri del contratto su Solana. Controlla che il creatore non possa congelare i fondi (Freeze Authority) o stampare supply infinita (Mint Authority).
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-zinc-800/40 border border-zinc-800 space-y-1">
            <div className="flex items-center justify-between font-mono">
              <span className="font-bold text-white">Livello del Segnale</span>
              <span className="text-amber-400 font-bold">ALTO / MEDIO / BASSO</span>
            </div>
            <p className="text-zinc-400">
              • <b className="text-emerald-400">ALTO:</b> Almeno 2 smart wallet indipendenti sono entrati entro 30 minuti con Safety Score elevato.<br />
              • <b className="text-amber-400">MEDIO:</b> Segnale buono ma liquidità ancora in consolidamento o solo 1 smart wallet primario.<br />
              • <b className="text-zinc-500">BASSO:</b> Rischio elevato o semplice rumore di mercato.
            </p>
          </div>

        </div>
      </div>

      {/* Differenza Pump.fun vs Raydium */}
      <div className="p-5 sm:p-6 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-3">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Zap className="w-5 h-5 text-purple-400" />
          Differenza tra Token su Pump.fun e Raydium
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          <div className="p-3.5 rounded-xl bg-purple-950/20 border border-purple-500/30 space-y-1.5">
            <span className="font-bold text-purple-300 font-mono block">Token Pump.fun (Bonding Curve)</span>
            <p className="text-zinc-400">
              I token appena nati su Pump.fun non hanno una pool normale ma una riserva interna di SOL. Quando la Market Cap raggiunge ~69.000$, la bonding curve si completa e il token migra automaticamente su Raydium con liquidità bloccata.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-1.5">
            <span className="font-bold text-emerald-300 font-mono block">Token Raydium (AMM Pool)</span>
            <p className="text-zinc-400">
              Hanno una pool di liquidità tradizionale aperta al trading globale su Solana. Il radar controlla sempre che la liquidità sia &ge; 5.000$ per evitare slippage eccessivo.
            </p>
          </div>
        </div>
      </div>

      {/* Contratti Verificati di Esempio pronti da copiare */}
      <div className="p-5 sm:p-6 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-3">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          Contratti Storici Verificati da Testare
        </h3>
        <p className="text-xs text-zinc-400">
          Clicca su &quot;Copia&quot; per copiare il contratto e incollarlo subito nella scheda Scanner:
        </p>

        <div className="space-y-2">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-xl bg-zinc-800/50 border border-zinc-700/60 text-xs gap-2">
            <div>
              <b className="text-white font-mono">$WIF (dogwifhat)</b>
              <div className="font-mono text-zinc-400 text-[11px] break-all">
                EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm
              </div>
            </div>
            <CopyButton text="EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm" label="Copia Mint $WIF" />
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-xl bg-zinc-800/50 border border-zinc-700/60 text-xs gap-2">
            <div>
              <b className="text-white font-mono">$BONK (Bonk)</b>
              <div className="font-mono text-zinc-400 text-[11px] break-all">
                DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263
              </div>
            </div>
            <CopyButton text="DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263" label="Copia Mint $BONK" />
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-xl bg-zinc-800/50 border border-zinc-700/60 text-xs gap-2">
            <div>
              <b className="text-white font-mono">$POPCAT (Popcat)</b>
              <div className="font-mono text-zinc-400 text-[11px] break-all">
                7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr
              </div>
            </div>
            <CopyButton text="7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr" label="Copia Mint $POPCAT" />
          </div>
        </div>
      </div>

    </div>
  );
};
