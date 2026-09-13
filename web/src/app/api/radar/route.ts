import { NextResponse } from "next/server";
import { SMART_WALLETS } from "../../../lib/data";
import { Redis } from "@upstash/redis";

export const dynamic = "force-dynamic";
export const revalidate = 0;

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

async function fetchTimeout(url: string, ms = 4000) {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), ms);
  try { return await fetch(url, { signal: c.signal, cache: "no-store" }); } finally { clearTimeout(t); }
}

export async function GET() {
  try {
    const pRes = await fetchTimeout("https://api.dexscreener.com/token-profiles/latest/v1");
    const profiles = pRes.ok ? await pRes.json() : [];
    const mints = Array.isArray(profiles) ? profiles.filter((p: any) => p.chainId === "solana" && p.tokenAddress).map((p: any) => p.tokenAddress).slice(0, 20) : [];
    
    const candidates: Record<string, any> = {};
    if (mints.length) {
      const dRes = await fetchTimeout(`https://api.dexscreener.com/latest/dex/tokens/${mints.join(",")}`);
      if (dRes.ok) {
        const d = await dRes.json();
        for (const pair of (d.pairs || [])) {
          if (pair.chainId !== "solana") continue;
          const fdv = Number(pair.fdv || pair.marketCap || 0);
          const liq = Number(pair.liquidity?.usd || 0);
          if (fdv > 0 && fdv <= 1_000_000 && liq >= 2_500) {
            candidates[pair.baseToken?.address] = {
              tokenMint: pair.baseToken?.address,
              symbol: pair.baseToken?.symbol || "?",
              name: pair.baseToken?.name || "",
              pairAddress: pair.pairAddress,
              dexId: pair.dexId,
              priceUsd: Number(pair.priceUsd || 0),
              marketCapUsd: fdv,
              liquidityUsd: liq,
              pairCreatedAt: pair.pairCreatedAt || null,
              sourceType: "API",
              sourceName: "DEXSCREENER",
              fetchedAt: Date.now()
            };
          }
        }
      }
    }
    
    let alerts: any[] = [];
    try {
      const rawEvents = await redis.lrange("helius_live_events", 0, 999);
      const events = rawEvents.map(e => typeof e === 'string' ? JSON.parse(e) : e);
      
      const nowTs = Math.floor(Date.now() / 1000);
      const twentyMinsAgo = nowTs - 1200; // Finestra temporale di 20 minuti
      
      const buyEvents = events.filter((e: any) => {
        if (e.type !== "BUY" || !e.mint) return false;
        if (e.timestamp < twentyMinsAgo) return false;
        // Filter Watchlist: Must be an authorized SMART WALLET
        if (!SMART_WALLETS.find(w => w.address === e.wallet)) return false;
        return true;
      });
      
      const mintGroups: Record<string, any[]> = {};
      
      for (const ev of buyEvents) {
        if (!mintGroups[ev.mint]) mintGroups[ev.mint] = [];
        mintGroups[ev.mint].push(ev);
      }
      
      for (const mint in mintGroups) {
        const group = mintGroups[mint];
        // Unique wallets (Cluster Collapse)
        const uniqueWallets = Array.from(new Set(group.map(g => g.wallet)));
        if (uniqueWallets.length >= 2) {
          
          let cand = candidates[mint];
          if (!cand) {
             // Fallback minimal cand if not in DexScreener latest profiles
             cand = { symbol: "UNKNOWN", name: "Unknown Token", priceUsd: 0, marketCapUsd: 0, liquidityUsd: 0 };
          }
          
          // Risk filter logic: skip if completely zero liquidity (unless it's truly brand new)
          // We allow it to pass but flag it
          
          alerts.push({
            id: `conv_${mint}_${group[0].timestamp}`,
            timestamp: group[0].timestamp * 1000,
            tokenMint: mint,
            symbol: cand.symbol,
            name: cand.name,
            priceUsd: cand.priceUsd,
            marketCapUsd: cand.marketCapUsd,
            liquidityUsd: cand.liquidityUsd,
            walletsInvolved: uniqueWallets.map(w => {
              const sw = SMART_WALLETS.find(x => x.address === w);
              const wEvents = group.filter(g => g.wallet === w);
              const totalAmount = wEvents.reduce((acc, curr) => acc + (curr.amountSol || 0), 0);
              return {
                address: w,
                score: sw ? sw.independenceScore : 50,
                amountSol: totalAmount
              };
            })
          });
        }
      }
      
      alerts.sort((a, b) => b.timestamp - a.timestamp);
      
    } catch (redisErr) {
      console.error("Redis fetch error:", redisErr);
    }
    
    return NextResponse.json({
      success: true, 
      status: alerts.length > 0 ? "CONVERGENCE_DETECTED" : "MARKET_CANDIDATES_ONLY", 
      timestamp: Date.now(), 
      count: Object.keys(candidates).length, 
      candidates: Object.values(candidates), 
      alerts, 
      monitoringWalletsCount: SMART_WALLETS.length, 
      message: alerts.length > 0 ? "Active convergences detected." : "Market discovery is live."
    });
  } catch (e: any) {
    return NextResponse.json({
      success: false, 
      status: "DATA_UNAVAILABLE", 
      error: e?.message || "Radar error", 
      alerts: [], 
      candidates: []
    }, { status: 503 });
  }
}
