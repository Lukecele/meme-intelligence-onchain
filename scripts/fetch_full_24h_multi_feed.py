import httpx
import asyncio
import time
import json

async def test():
    now_ms = int(time.time() * 1000)
    async with httpx.AsyncClient(timeout=15.0) as client:
        # 1. Fetch from token-boosts/latest/v1
        r1 = await client.get('https://api.dexscreener.com/token-boosts/latest/v1')
        # 2. Fetch from token-boosts/top/v1
        r2 = await client.get('https://api.dexscreener.com/token-boosts/top/v1')
        # 3. Fetch from token-profiles/latest/v1
        r3 = await client.get('https://api.dexscreener.com/token-profiles/latest/v1')
        
        all_sol_mints = []
        for r in [r1, r2, r3]:
            if r.status_code == 200:
                for item in r.json():
                    if item.get('chainId') == 'solana' and item.get('tokenAddress'):
                        all_sol_mints.append(item.get('tokenAddress'))
                        
        distinct_mints = list(set(all_sol_mints))
        print(f"Total distinct Solana mints from live feeds: {len(distinct_mints)}")
        
        # Batch query pairs in chunks of 20
        all_pairs = []
        for i in range(0, min(80, len(distinct_mints)), 20):
            chunk = distinct_mints[i:i+20]
            mints_str = ','.join(chunk)
            r_pairs = await client.get(f'https://api.dexscreener.com/latest/dex/tokens/{mints_str}')
            if r_pairs.status_code == 200:
                all_pairs.extend(r_pairs.json().get('pairs', []))
            await asyncio.sleep(0.1)
            
        valid_24h = []
        seen = set()
        for p in all_pairs:
            mint = (p.get('baseToken') or {}).get('address')
            if not mint or mint in seen:
                continue
            created = p.get('pairCreatedAt')
            if not created:
                continue
            age_h = (now_ms - created) / (3600 * 1000)
            fdv = p.get('fdv') or p.get('marketCap') or 0
            liq = (p.get('liquidity') or {}).get('usd', 0)
            price = float(p.get('priceUsd') or 0)
            sym = (p.get('baseToken') or {}).get('symbol')
            name = (p.get('baseToken') or {}).get('name')
            
            # Between 0.2h and 24h
            if 0.2 <= age_h <= 24.0 and 4000 <= fdv <= 1000000 and liq >= 2000 and price > 0:
                seen.add(mint)
                valid_24h.append({
                    'symbol': sym,
                    'name': name,
                    'mint': mint,
                    'age_hours': round(age_h, 1),
                    'fdv': fdv,
                    'liq': liq,
                    'price': price,
                    'created_ms': created
                })
                
        valid_24h.sort(key=lambda x: x['age_hours'])
        print(f"Found {len(valid_24h)} real microcaps covering the 24h span:")
        for v in valid_24h:
            print(f"* ${v['symbol']} ({v['mint'][:10]}...) - Age: {v['age_hours']}h fa - FDV: ${v['fdv']:,.0f} - Liq: ${v['liq']:,.0f} - Price: ${v['price']:.8f}")

        with open('web/src/lib/multi_feed_24h.json', 'w') as f:
            json.dump(valid_24h, f, indent=2)

if __name__ == '__main__':
    asyncio.run(test())
