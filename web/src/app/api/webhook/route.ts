import { NextResponse } from "next/server";
import { Redis } from "@upstash/redis";

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

function parseSwapEvent(tx: any) {
  if (!tx.meta || tx.meta.err) return null;
  
  const preTokenBalances = tx.meta.preTokenBalances || [];
  const postTokenBalances = tx.meta.postTokenBalances || [];
  const preBalances = tx.meta.preBalances || [];
  const postBalances = tx.meta.postBalances || [];
  
  const accounts = tx.transaction?.message?.accountKeys || [];
  const accountKeys = accounts.map((a: any) => typeof a === 'string' ? a : a.pubkey);
  
  const tokenDeltas: Record<string, { tokenDelta: number, owner: string, mint: string }> = {};
  
  for (const t of preTokenBalances) {
    const key = `${t.owner}-${t.mint}`;
    if (!tokenDeltas[key]) tokenDeltas[key] = { tokenDelta: 0, owner: t.owner, mint: t.mint };
    tokenDeltas[key].tokenDelta -= Number(t.uiTokenAmount?.uiAmount || 0);
  }
  for (const t of postTokenBalances) {
    const key = `${t.owner}-${t.mint}`;
    if (!tokenDeltas[key]) tokenDeltas[key] = { tokenDelta: 0, owner: t.owner, mint: t.mint };
    tokenDeltas[key].tokenDelta += Number(t.uiTokenAmount?.uiAmount || 0);
  }
  
  const swapper = accountKeys[0];
  if (!swapper) return null;
  
  const swapperIdx = accountKeys.indexOf(swapper);
  let solDelta = 0;
  if (swapperIdx >= 0 && swapperIdx < preBalances.length) {
    solDelta = (postBalances[swapperIdx] - preBalances[swapperIdx]) / 1e9;
  }
  
  let swappedMint = null;
  let swappedAmount = 0;
  
  for (const key in tokenDeltas) {
    if (tokenDeltas[key].owner === swapper && Math.abs(tokenDeltas[key].tokenDelta) > 0.01) {
      swappedMint = tokenDeltas[key].mint;
      swappedAmount = tokenDeltas[key].tokenDelta;
      break;
    }
  }
  
  if (swappedMint) {
    return {
      type: swappedAmount > 0 ? "BUY" : "SELL",
      mint: swappedMint,
      wallet: swapper,
      amountTokens: Math.abs(swappedAmount),
      amountSol: Math.abs(solDelta)
    };
  }
  
  return null;
}

export async function POST(req: Request) {
  try {
    const authHeader = req.headers.get("Authorization");
    if (process.env.HELIUS_WEBHOOK_SECRET && authHeader !== process.env.HELIUS_WEBHOOK_SECRET) {
      return new NextResponse("Unauthorized", { status: 401 });
    }

    const payload = await req.json();
    const txs = Array.isArray(payload) ? payload : [payload];
    
    let processed = 0;
    for (const tx of txs) {
      if (!tx.signature) continue;
      
      // Implement Deduplication using Redis SETNX with a 10-minute TTL
      const isNew = await redis.setnx(`dedupe_tx_${tx.signature}`, "1");
      if (!isNew) {
         console.log(`Skipping duplicate webhook event: ${tx.signature}`);
         continue; // Helius retry duplicate
      }
      await redis.expire(`dedupe_tx_${tx.signature}`, 600);
      
      const parsedSwap = parseSwapEvent(tx);
      
      const alertEvent = {
        signature: tx.signature,
        type: parsedSwap ? parsedSwap.type : (tx.type || "UNKNOWN"),
        timestamp: tx.timestamp || Math.floor(Date.now() / 1000),
        wallet: parsedSwap ? parsedSwap.wallet : tx.feePayer,
        mint: parsedSwap ? parsedSwap.mint : null,
        amountTokens: parsedSwap ? parsedSwap.amountTokens : null,
        amountSol: parsedSwap ? parsedSwap.amountSol : null,
        description: tx.description || `Transaction ${tx.signature}`,
        raw: tx 
      };
      
      await redis.lpush("helius_live_events", JSON.stringify(alertEvent));
      await redis.ltrim("helius_live_events", 0, 999);
      processed++;
    }
    
    return NextResponse.json({ success: true, processed });
  } catch (error: any) {
    console.error("Webhook error:", error);
    return new NextResponse("Internal Server Error", { status: 500 });
  }
}
