import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Solana On-Chain Intelligence System | Radar & Wallet Convergence",
  description: "Early detection of high-potential meme coins on Solana via smart wallet selectivity, on-chain clustering, and real-time multi-wallet convergence monitoring.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="it" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen bg-[#08090d] text-zinc-100 antialiased selection:bg-emerald-500/30 selection:text-emerald-300">
        {children}
      </body>
    </html>
  );
}
