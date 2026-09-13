import httpx
import asyncio
import time

async def test():
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get('https://api.dexscreener.com/token-profiles/latest/v1')
        if r.status_code == 200:
            profiles = r.json()
            sol_mints = [p.get('tokenAddress') for p in profiles if p.get('chainId') == 'solana'][:15]
            mints_str = ','.join(sol_mints)
            
            r2 = await client.get(f'https://api.dexscreener.com/latest/dex/tokens/{mints_str}')
            if r2.status_code == 200:
                pairs = r2.json().get('pairs', [])
                now_ms = int(time.time() * 1000)
                print(f"Retrieved {len(pairs)} live pairs for freshly launched Solana tokens:")
                for p in pairs:
                    base = p.get('baseToken', {})
                    created = p.get('pairCreatedAt') or now_ms
                    age_min = round((now_ms - created) / 60000, 1)
                    fdv = p.get('fdv') or p.get('marketCap') or 0
                    liq = (p.get('liquidity') or {}).get('usd', 0)
                    price = float(p.get('priceUsd') or 0)
                    print(f"* ${base.get('symbol')} ({base.get('address')}) - Age: {age_min}m - FDV: ${fdv:,.0f} - Liq: ${liq:,.0f} - Price: ${price:.8f}")

if __name__ == '__main__':
    asyncio.run(test())
