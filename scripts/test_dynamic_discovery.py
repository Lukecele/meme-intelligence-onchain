import httpx
import asyncio
import time
from datetime import datetime

async def test():
    now_ms = int(time.time() * 1000)
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Dynamic feed of newest token profiles
        r = await client.get('https://api.dexscreener.com/token-profiles/latest/v1')
        if r.status_code == 200:
            profiles = r.json()
            sol_mints = [p.get('tokenAddress') for p in profiles if p.get('chainId') == 'solana' and p.get('tokenAddress')][:15]
            
            r2 = await client.get(f'https://api.dexscreener.com/latest/dex/tokens/{','.join(sol_mints)}')
            if r2.status_code == 200:
                pairs = r2.json().get('pairs', [])
                fresh_tokens = []
                seen = set()
                for p in pairs:
                    if p.get('chainId') == 'solana':
                        mint = (p.get('baseToken') or {}).get('address')
                        created = p.get('pairCreatedAt')
                        if not mint or mint in seen or not created:
                            continue
                        seen.add(mint)
                        age_min = round((now_ms - created) / 60000, 1)
                        sym = (p.get('baseToken') or {}).get('symbol')
                        name = (p.get('baseToken') or {}).get('name')
                        fdv = p.get('fdv') or p.get('marketCap') or 0
                        liq = (p.get('liquidity') or {}).get('usd', 0)
                        price = float(p.get('priceUsd') or 0)
                        
                        fresh_tokens.append({
                            'symbol': sym,
                            'name': name,
                            'mint': mint,
                            'pairCreatedAt': created,
                            'age_min': age_min,
                            'fdv': fdv,
                            'liq': liq,
                            'price': price
                        })
                        
                fresh_tokens.sort(key=lambda x: x['pairCreatedAt'], reverse=True)
                print(f"Dynamic discovery retrieved {len(fresh_tokens)} live tokens created in the latest minutes:")
                for t in fresh_tokens[:8]:
                    dt = datetime.fromtimestamp(t['pairCreatedAt']/1000).strftime('%H:%M:%S')
                    print(f"* ${t['symbol']} | Mint: {t['mint']} | Created at {dt} ({t['age_min']}m ago) | FDV: ${t['fdv']:,.0f} | Price: ${t['price']:.8f}")

if __name__ == '__main__':
    asyncio.run(test())
