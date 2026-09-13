import { NextRequest, NextResponse } from "next/server";
export const dynamic="force-dynamic";export const revalidate=0;
const HELIUS_API_KEY=process.env.HELIUS_API_KEY||"";const BIRDEYE_API_KEY=process.env.BIRDEYE_API_KEY||"";
const RPC_URL=HELIUS_API_KEY?`https://mainnet.helius-rpc.com/?api-key=${HELIUS_API_KEY}`:(process.env.SOLANA_RPC_URL||"https://api.mainnet-beta.solana.com");
const BASE58=/^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
export async function GET(request:NextRequest){
 const cleanMint=(request.nextUrl.searchParams.get("mint")||"").trim();
 if(!BASE58.test(cleanMint)) return NextResponse.json({error:"Mint Solana non valido: atteso Base58 (32-44 caratteri)."},{status:400});
 try{
  const [dexResp,rpcResp]=await Promise.all([
   fetch(`https://api.dexscreener.com/latest/dex/tokens/${cleanMint}`,{headers:{Accept:"application/json"},cache:"no-store"}),
   fetch(RPC_URL,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({jsonrpc:"2.0",id:1,method:"getAccountInfo",params:[cleanMint,{encoding:"jsonParsed"}]}),cache:"no-store"})
  ]);
  const dexData=dexResp.ok?await dexResp.json():{};const pairs=(dexData.pairs||[]).filter((p:any)=>p.chainId==="solana").sort((a:any,b:any)=>(b.liquidity?.usd||0)-(a.liquidity?.usd||0));const pair=pairs[0]||null;
  const rpcJson=rpcResp.ok?await rpcResp.json():{};const info=rpcJson.result?.value?.data?.parsed?.info;
  if(!info) return NextResponse.json({error:"Mint non trovato o account non interpretabile come SPL mint.",source:"SOLANA_RPC"},{status:404});
  const mintAuthority=info.mintAuthority||null,freezeAuthority=info.freezeAuthority||null,decimals=Number(info.decimals??0),supply=info.supply?Number(info.supply)/Math.pow(10,decimals):0;
  let topHoldersPct:number|null=null;let holderSource="UNAVAILABLE";
  if(BIRDEYE_API_KEY){try{const h=await fetch(`https://public-api.birdeye.so/holder/v1/distribution?token_address=${cleanMint}&address_type=wallet&mode=top&top_n=10&include_list=false`,{headers:{"X-API-KEY":BIRDEYE_API_KEY,"x-chain":"solana",Accept:"application/json"},cache:"no-store"});if(h.ok){const j=await h.json();const pct=j.data?.summary?.percent_of_supply;if(pct!=null){topHoldersPct=Number(pct);holderSource="BIRDEYE_WALLET_DISTRIBUTION"}}}catch{}}
  const marketDataAvailable=!!pair;const liquidityUsd=Number(pair?.liquidity?.usd||0),marketCapUsd=Number(pair?.marketCap||pair?.fdv||0),priceUsd=Number(pair?.priceUsd||0);const pairCreatedAt=pair?.pairCreatedAt||null;const ageMinutes=pairCreatedAt?Math.max(0,Math.round((Date.now()-pairCreatedAt)/60000)):null;
  const riskFlags:string[]=[];let safetyScore=100;
  if(freezeAuthority){riskFlags.push("FREEZE_AUTHORITY_ATTIVA: il mint conserva la capacità di congelare token account");safetyScore-=40}else riskFlags.push("Freeze authority assente: questo specifico rischio non risulta attivo.");
  if(mintAuthority){riskFlags.push("MINT_AUTHORITY_ATTIVA: può essere emessa ulteriore supply");safetyScore-=35}else riskFlags.push("Mint authority assente: non risulta possibile aumentare la supply tramite la mint authority standard.");
  if(!marketDataAvailable){riskFlags.push("MARKET_DATA_UNAVAILABLE: nessun pair Solana disponibile su DexScreener; market cap, liquidità ed età non vengono stimati.");safetyScore=Math.min(safetyScore,50)}else if(liquidityUsd<5000){riskFlags.push(`LIQUIDITA_CRITICA: $${liquidityUsd.toLocaleString()} < $5.000`);safetyScore-=25}
  if(topHoldersPct!=null&&topHoldersPct>35){riskFlags.push(`TOP10_WALLET_CONCENTRATION: ${topHoldersPct.toFixed(1)}%`);safetyScore-=20}
  safetyScore=Math.max(0,safetyScore);const isMicroCap=marketDataAvailable&&marketCapUsd>0&&marketCapUsd<=1_000_000;const safetyMicrocapScore=marketDataAvailable?Math.max(0,Math.min(100,safetyScore+(isMicroCap?0:-10))):null;
  return NextResponse.json({success:true,data:{mint:cleanMint,symbol:pair?.baseToken?.symbol||"UNKNOWN",name:pair?.baseToken?.name||"SPL Token",dexId:pair?.dexId||null,pairAddress:pair?.pairAddress||null,priceUsd,liquidityUsd,marketCapUsd,ageMinutes,decimals,supply,topHoldersPct,holderSource,mintAuthority,freezeAuthority,txns24h:pair?.txns?.h24||null,volume24h:Number(pair?.volume?.h24||0),priceChange24h:Number(pair?.priceChange?.h24||0),marketDataAvailable,safetyMicrocapScore,riskFlags,provenance:{mint:"SOLANA_RPC",market:"DEXSCREENER",holders:holderSource,fetchedAt:Date.now()},convergenceScore:null,signalLevel:null,isQualifiedRadar:false}});
 }catch(e:any){return NextResponse.json({error:e?.message||"Internal server error"},{status:500})}
}
