import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const revalidate = 0;

const BIRDEYE_API_KEY = process.env.BIRDEYE_API_KEY || "";

export async function GET(request: NextRequest) {
  const mint = request.nextUrl.searchParams.get("mint");
  if (!mint) {
    return NextResponse.json({ error: "Missing mint" }, { status: 400 });
  }

  try {
    // 1. Try Birdeye real-time price API first (fastest sub-second)
    try {
      const bResp = await fetch(`https://public-api.birdeye.so/defi/price?address=${mint}`, {
        headers: {
          "X-API-KEY": BIRDEYE_API_KEY,
          "Accept": "application/json"
        },
        cache: "no-store"
      });
      if (bResp.ok) {
        const bJson = await bResp.json();
        if (bJson.data?.value) {
          return NextResponse.json({
            success: true,
            source: "birdeye_live",
            priceUsd: bJson.data.value,
            liquidityUsd: bJson.data.liquidity || 0,
            timestamp: Date.now()
          });
        }
      }
    } catch (e) {
      // fallback
    }

    // 2. Try Jupiter Price API v2
    try {
      const jupResp = await fetch(`https://api.jup.ag/price/v2?ids=${mint}`, {
        headers: { "Accept": "application/json" },
        cache: "no-store"
      });
      if (jupResp.ok) {
        const jupJson = await jupResp.json();
        const pData = jupJson.data?.[mint];
        if (pData?.price) {
          return NextResponse.json({
            success: true,
            source: "jupiter_v2_live",
            priceUsd: parseFloat(pData.price),
            timestamp: Date.now()
          });
        }
      }
    } catch (e) {
      // fallback
    }

    // 3. Fallback DexScreener specific pair (no-store)
    const dexResp = await fetch(`https://api.dexscreener.com/latest/dex/tokens/${mint}`, {
      headers: { "Accept": "application/json" },
      cache: "no-store"
    });
    if (dexResp.ok) {
      const dexJson = await dexResp.json();
      const pair = (dexJson.pairs || []).find((p: any) => p.chainId === "solana");
      if (pair) {
        return NextResponse.json({
          success: true,
          source: "dexscreener_live_pair",
          priceUsd: parseFloat(pair.priceUsd || "0"),
          marketCapUsd: pair.marketCap || pair.fdv || 0,
          liquidityUsd: pair.liquidity?.usd || 0,
          timestamp: Date.now()
        });
      }
    }

    return NextResponse.json({ error: "Price not found" }, { status: 404 });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
