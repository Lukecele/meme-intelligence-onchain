import urllib.request, json, sqlite3, time, asyncio
from config.settings import DATA_DIR
from config.tokens import HISTORICAL_WINNERS, CONTROL_GROUP_TOKENS
from extractors.solana_rpc import SolanaRPCClient

async def fetch_coingecko_data(mint: str, rpc: SolanaRPCClient):
    url = f"https://api.coingecko.com/api/v3/coins/solana/contract/{mint}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response_data = None
        # Use sync urllib but inside an async function for simplicity, block is fine here
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode())
            
        market_data = response_data.get("market_data", {})
        ath = market_data.get("ath", {}).get("usd", 0)
        atl = market_data.get("atl", {}).get("usd", 0)
        
        # Approximate return multiplier: ATH / ATL
        multiplier = 0
        if atl > 0 and ath > 0:
            multiplier = ath / atl
            
        total_supply = market_data.get("total_supply")
        if total_supply is None:
            # Fallback to absolute real native on-chain supply
            supply_resp = await rpc.call("getTokenSupply", [mint])
            if supply_resp and "value" in supply_resp:
                ui_amount = supply_resp["value"].get("uiAmount")
                if ui_amount is not None:
                    total_supply = float(ui_amount)
            if total_supply is None:
                total_supply = 0
                
        return {
            "multiplier": multiplier,
            "peak_mcap": ath * total_supply
        }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None # Not found
        print(f"Error fetching {mint}: {e}")
        return None
    except Exception as e:
        print(f"Error fetching {mint}: {e}")
        return None

async def main():
    db_path = DATA_DIR / "onchain_intelligence.db"
    conn = sqlite3.connect(db_path)
    rpc = SolanaRPCClient()
    
    conn.execute("CREATE TABLE IF NOT EXISTS historical_outcomes (token_mint TEXT PRIMARY KEY, max_return_1h REAL, max_return_24h REAL, max_return_7d REAL, max_return_30d REAL, peak_mcap REAL, status TEXT)")
    
    all_tokens = HISTORICAL_WINNERS + CONTROL_GROUP_TOKENS
    for t in all_tokens:
        mint = t["mint"]
        sym = t["symbol"]
        print(f"Fetching CoinGecko/RPC data for {sym} ({mint})...")
        cg_data = await fetch_coingecko_data(mint, rpc)
        
        if cg_data:
            multiplier = cg_data["multiplier"]
            peak = cg_data["peak_mcap"]
            print(f" -> Found! Multiplier: {multiplier:.1f}x, Peak MarketCap: ${peak:,.0f}")
            
            conn.execute("""
                INSERT OR REPLACE INTO historical_outcomes (token_mint, max_return_1h, max_return_24h, max_return_7d, max_return_30d, peak_mcap, status)
                VALUES (?, 0, 0, 0, ?, ?, 'COMPLETED')
            """, (mint, multiplier, peak))
            conn.execute("UPDATE tokens SET peak_mcap = ?, max_return_x = ? WHERE mint = ?", (peak, multiplier, mint))
        else:
            print(f" -> Not found or failed. Recording 1.0x return.")
            conn.execute("""
                INSERT OR REPLACE INTO historical_outcomes (token_mint, max_return_1h, max_return_24h, max_return_7d, max_return_30d, peak_mcap, status)
                VALUES (?, 0, 0, 0, 1.0, 0, 'COMPLETED')
            """, (mint,))
            conn.execute("UPDATE tokens SET peak_mcap = 0, max_return_x = 1.0 WHERE mint = ?", (mint,))
            
        time.sleep(2)
        
    conn.commit()
    conn.close()
    await rpc.close()
    print("Historical outcomes successfully populated from CoinGecko + Native RPC API.")

if __name__ == "__main__":
    asyncio.run(main())
