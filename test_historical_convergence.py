import sqlite3
from collections import defaultdict
from datetime import datetime
import json

conn = sqlite3.connect('data/onchain_intelligence.db')
conn.row_factory = sqlite3.Row

# Get the 33 smart wallets from JSON or DB
with open("web/src/lib/data.ts", "r") as f:
    import re
    matches = set(re.findall(r'"address":\s*["\']([1-9A-HJ-NP-Za-km-z]{32,44})["\']', f.read()))
    smart_wallets = list(matches)

query = f"""
    SELECT t.wallet_address, t.token_mint, t.timestamp, tk.symbol, tk.is_winner, tk.max_return_x
    FROM trades t
    LEFT JOIN tokens tk ON t.token_mint = tk.mint
    WHERE t.side = 'BUY' AND t.wallet_address IN ({','.join(['?']*len(smart_wallets))})
    ORDER BY t.timestamp ASC
"""
trades = conn.execute(query, smart_wallets).fetchall()

token_buys = defaultdict(list)
for t in trades:
    token_buys[t["token_mint"]].append(t)

convergences = []

for mint, buys in token_buys.items():
    buys.sort(key=lambda x: x["timestamp"])
    unique_wallets = set([b["wallet_address"] for b in buys])
    
    if len(unique_wallets) >= 2:
        symbol = buys[0]["symbol"] or "UNKNOWN"
        is_winner = buys[0]["is_winner"]
        max_x = buys[0]["max_return_x"]
        first_buy_ts = buys[0]["timestamp"]
        
        convergences.append({
            "mint": mint,
            "symbol": symbol,
            "wallets_count": len(unique_wallets),
            "is_winner": is_winner,
            "max_x": max_x,
            "date": datetime.utcfromtimestamp(first_buy_ts).strftime('%Y-%m-%d')
        })

print(f"Total tokens bought by smart wallets: {len(token_buys)}")
print(f"Total convergences (>= 2 smart wallets): {len(convergences)}")

winners = [c for c in convergences if c["is_winner"] == 1]
losers = [c for c in convergences if c["is_winner"] == 0]
unknown = [c for c in convergences if c["is_winner"] is None]

print(f"Converged Winners: {len(winners)}")
print(f"Converged Losers: {len(losers)}")
print(f"Converged Unknown (Not in DB winners list): {len(unknown)}")
print("\n--- TOP CONVERGENCES ---")

for c in sorted(convergences, key=lambda x: x["wallets_count"], reverse=True)[:20]:
    status = "🏆 WINNER" if c["is_winner"] == 1 else ("🔴 LOSER" if c["is_winner"] == 0 else "❓ UNKNOWN")
    max_ret = f"{c['max_x']}x" if c['max_x'] else "?"
    print(f"[{c['date']}] {c['symbol']} ({c['mint'][:6]}...): {c['wallets_count']} wallets | {status} ({max_ret})")

