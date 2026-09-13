import httpx
import asyncio
import time
import json

async def test():
    now_ms = int(time.time() * 1000)
    day_ago_ms = now_ms - (24 * 3600 * 1000)
    
    queries = ['pump', 'sol', 'cat', 'dog', 'pepe', 'ai', 'trump', 'moon', 'alpha', 'degen', 'inu', 'meme', 'coin', 'shib', 'chad', 'wojak', 'frog']
    tokens_by_age = {}
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        for q in queries:
            try:
                r = await client.get(f'https://api.dexscreener.com/latest/dex/search?q={q}')
                if r.status_code == 200:
                    pairs = r.json().get('pairs', [])
                    for p in pairs:
                        if p.get('chainId') == 'solana':
                            created = p.get('pairCreatedAt') or 0
                            mint = (p.get('baseToken') or {}).get('address')
                            fdv = p.get('fdv') or p.get('marketCap') or 0
                            liq = (p.get('liquidity') or {}).get('usd', 0)
                            price = float(p.get('priceUsd') or 0)
                            
                            # Truly in the 24h window (between 0.5h and 24h)
                            if day_ago_ms <= created <= (now_ms - 1800 * 1000) and 4000 <= fdv <= 800000 and liq >= 2000 and price > 0 and mint:
                                age_h = (now_ms - created) / (3600 * 1000)
                                if mint not in tokens_by_age:
                                    tokens_by_age[mint] = {
                                        'symbol': (p.get('baseToken') or {}).get('symbol'),
                                        'name': (p.get('baseToken') or {}).get('name'),
                                        'mint': mint,
                                        'age_hours': round(age_h, 1),
                                        'fdv': fdv,
                                        'liq': liq,
                                        'price': price,
                                        'created_ms': created
                                    }
            except Exception:
                pass
            await asyncio.sleep(0.05)
            
    sorted_tokens = sorted(tokens_by_age.values(), key=lambda x: x['age_hours'])
    print(f"Total genuine Solana microcaps across the 24h spectrum: {len(sorted_tokens)}")
    for t in sorted_tokens:
        print(f"* ${t['symbol']} ({t['mint'][:10]}...) - Age: {t['age_hours']}h fa - FDV: ${t['fdv']:,.0f} - Liq: ${t['liq']:,.0f} - Price: ${t['price']:.8f}")

    with open('web/src/lib/true_24h_spectrum.json', 'w') as f:
        json.dump(sorted_tokens, f, indent=2)

if __name__ == '__main__':
    asyncio.run(test())
