"use client";

import React, { useState } from "react";
import { Copy, Check } from "lucide-react";

interface CopyButtonProps {
  text: string;
  label?: string;
  className?: string;
}

export const CopyButton: React.FC<CopyButtonProps> = ({ text, label, className = "" }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async (e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  return (
    <button
      onClick={handleCopy}
      type="button"
      className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-zinc-800 hover:bg-zinc-700 active:scale-90 text-[11px] font-mono text-zinc-300 border border-zinc-700 transition-all touch-manipulation cursor-pointer ${
        copied ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/40" : ""
      } ${className}`}
      title="Copia negli appunti"
    >
      {copied ? (
        <>
          <Check className="w-3 h-3 text-emerald-400" />
          <span className="text-emerald-400 font-bold">Copiato!</span>
        </>
      ) : (
        <>
          <Copy className="w-3 h-3 text-zinc-400" />
          <span>{label || "Copia"}</span>
        </>
      )}
    </button>
  );
};
