import httpx
import asyncio
import time
import json

async def test():
    now_ms = int(time.time() * 1000)
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get('https://api.dexscreener.com/token-profiles/latest/v1')
        profiles = r.json() if r.status_code == 200 else []
        sol_mints = [p.get('tokenAddress') for p in profiles if p.get('chainId') == 'solana' and p.get('tokenAddress')]
        
        # Batch fetch in chunks
        chunk_size = 20
        all_pairs = []
        for i in range(0, min(60, len(sol_mints)), chunk_size):
            chunk = sol_mints[i:i+chunk_size]
            mints_str = ','.join(chunk)
            r2 = await client.get(f'https://api.dexscreener.com/latest/dex/tokens/{mints_str}')
            if r2.status_code == 200:
                all_pairs.extend(r2.json().get('pairs', []))
            await asyncio.sleep(0.2)
        
        valid_24h = []
        seen = set()
        for p in all_pairs:
            if p.get('chainId') == 'solana':
                mint = (p.get('baseToken') or {}).get('address')
                if not mint or mint in seen:
                    continue
                created = p.get('pairCreatedAt') or 0
                age_h = (now_ms - created) / (3600 * 1000) if created else 0
                fdv = p.get('fdv') or p.get('marketCap') or 0
                liq = (p.get('liquidity') or {}).get('usd', 0)
                price = float(p.get('priceUsd') or 0)
                base = p.get('baseToken', {})
                
                # Check 24h span
                if 0.1 <= age_h <= 24.0 and 5000 <= fdv <= 600000 and liq >= 2000 and price > 0:
                    seen.add(mint)
                    valid_24h.append({
                        'symbol': base.get('symbol'),
                        'name': base.get('name'),
                        'mint': mint,
                        'age_hours': round(age_h, 1),
                        'fdv': fdv,
                        'liq': liq,
                        'price': price
                    })
        
        valid_24h.sort(key=lambda x: x['age_hours'])
        print(f"Found {len(valid_24h)} real microcaps covering the 24h window:")
        for v in valid_24h:
            print(f"* ${v['symbol']} ({v['mint'][:10]}...) - Age: {v['age_hours']}h - FDV: ${v['fdv']:,.0f} - Liq: ${v['liq']:,.0f} - Price: ${v['price']:.8f}")

        with open('web/src/lib/full_24h_tokens.json', 'w') as f:
            json.dump(valid_24h, f, indent=2)

if __name__ == '__main__':
    asyncio.run(test())
