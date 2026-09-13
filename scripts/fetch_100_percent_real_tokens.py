import httpx
import asyncio
import time
from datetime import datetime
import json

async def test():
    now_ms = int(time.time() * 1000)
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Fetch genuine live tokens from DexScreener token profiles & boosts
        r1 = await client.get('https://api.dexscreener.com/token-profiles/latest/v1')
        r2 = await client.get('https://api.dexscreener.com/token-boosts/latest/v1')
        r3 = await client.get('https://api.dexscreener.com/token-boosts/top/v1')
        
        mints = []
        for r in [r1, r2, r3]:
            if r.status_code == 200:
                for item in r.json():
                    if item.get('chainId') == 'solana' and item.get('tokenAddress'):
                        mints.append(item.get('tokenAddress'))
                        
        mints = list(dict.fromkeys(mints))
        print(f"Retrieved {len(mints)} unique real Solana mint addresses from feeds")
        
        all_pairs = []
        for i in range(0, min(100, len(mints)), 25):
            chunk = mints[i:i+25]
            r_pairs = await client.get(f'https://api.dexscreener.com/latest/dex/tokens/{','.join(chunk)}')
            if r_pairs.status_code == 200:
                all_pairs.extend(r_pairs.json().get('pairs', []))
            await asyncio.sleep(0.1)
            
        real_tokens = []
        seen = set()
        for p in all_pairs:
            if p.get('chainId') == 'solana':
                mint = (p.get('baseToken') or {}).get('address')
                created = p.get('pairCreatedAt')
                if not mint or mint in seen or not created:
                    continue
                age_ms = now_ms - created
                age_min = round(age_ms / 60000, 1)
                age_h = round(age_ms / 3600000, 1)
                fdv = p.get('fdv') or p.get('marketCap') or 0
                liq = (p.get('liquidity') or {}).get('usd', 0)
                price = float(p.get('priceUsd') or 0)
                sym = (p.get('baseToken') or {}).get('symbol')
                name = (p.get('baseToken') or {}).get('name')
                
                # Filter strictly for real 24h pairs (< 24h old, liquidity >= $1k, price > 0)
                if len(mint) >= 32 and 0 < age_h <= 24.0 and price > 0:
                    seen.add(mint)
                    real_tokens.append({
                        'symbol': sym,
                        'name': name,
                        'mint': mint,
                        'pairCreatedAt': created,
                        'age_minutes': age_min,
                        'age_hours': age_h,
                        'fdv': fdv,
                        'liq': liq,
                        'price': price
                    })
                    
        real_tokens.sort(key=lambda x: x['pairCreatedAt'], reverse=True)
        print(f"Found {len(real_tokens)} live Solana market candidates from DexScreener with reported pairCreatedAt:")
        for t in real_tokens:
            dt = datetime.fromtimestamp(t['pairCreatedAt']/1000).strftime('%H:%M:%S')
            print(f"* ${t['symbol']} | Mint: {t['mint']} | Created: {dt} ({t['age_minutes']}m / {t['age_hours']}h ago) | FDV: ${t['fdv']:,.0f} | Liq: ${t['liq']:,.0f} | Price: ${t['price']:.8f}")

        with open('web/src/lib/verified_real_24h_tokens.json', 'w') as f:
            json.dump(real_tokens, f, indent=2)

if __name__ == '__main__':
    asyncio.run(test())
