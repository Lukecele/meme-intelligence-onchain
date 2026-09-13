import httpx
import asyncio
import json

async def test():
    async with httpx.AsyncClient(timeout=15.0) as client:
        queries = ['pump', 'sol', 'cat', 'dog', 'pepe', 'ai', 'trump']
        results = {}
        for q in queries:
            try:
                r = await client.get(f'https://api.dexscreener.com/latest/dex/search?q={q}')
                if r.status_code == 200:
                    pairs = r.json().get('pairs', [])
                    for p in pairs:
                        if p.get('chainId') == 'solana':
                            fdv = p.get('fdv') or p.get('marketCap') or 0
                            liq = (p.get('liquidity') or {}).get('usd', 0)
                            price = float(p.get('priceUsd') or 0)
                            mint = (p.get('baseToken') or {}).get('address')
                            sym = (p.get('baseToken') or {}).get('symbol')
                            name = (p.get('baseToken') or {}).get('name')
                            created = p.get('pairCreatedAt') or 0
                            if 8000 <= fdv <= 500000 and liq >= 3500 and price > 0 and mint:
                                if mint not in results:
                                    results[mint] = {
                                        'symbol': sym,
                                        'name': name,
                                        'mint': mint,
                                        'fdv': fdv,
                                        'liq': liq,
                                        'price': price,
                                        'pairCreatedAt': created
                                    }
            except Exception as e:
                pass
            await asyncio.sleep(0.1)

        print(f"Found {len(results)} distinct Solana microcaps:")
        microcaps_list = list(results.values())[:6]
        for m in microcaps_list:
            print(f"* ${m['symbol']} ({m['mint'][:10]}...) FDV: ${m['fdv']:,.0f} Liq: ${m['liq']:,.0f} Price: ${m['price']:.8f}")

        with open('..//web/src/lib/live_microcaps_sample.json', 'w') as f:
            json.dump(microcaps_list, f, indent=2)

if __name__ == "__main__":
    asyncio.run(test())
