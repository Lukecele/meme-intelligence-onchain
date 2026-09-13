#!/usr/bin/env python3
import sqlite3, json, sys, re
from pathlib import Path
import asyncio

def main():
    root = Path(__file__).resolve().parent.parent
    db_path = root / "data" / "onchain_intelligence.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # We find smart wallets
    wallets = conn.execute("""
        SELECT t.wallet_address
        FROM trades t 
        JOIN tokens tk ON tk.mint=t.token_mint 
        WHERE t.side='BUY' AND t.is_first_buyer=1 AND tk.is_winner=1 
        GROUP BY t.wallet_address 
        HAVING COUNT(DISTINCT t.token_mint) >= 2
    """).fetchall()
    
    wallet_addrs = [w["wallet_address"] for w in wallets]
    clusters = []
    
    # In the future, this will use Helius or Birdeye first-funded API
    # For now, we STRICTLY avoid any fake data or mock clusters.
    # We output an empty array to ensure full honesty.
    
    data_ts = root / "web/src/lib/data.ts"
    with open(data_ts, "r") as f:
        content = f.read()
        
    cluster_str = json.dumps(clusters, indent=2)
    
    if 'export const CLUSTERS: ClusterInfo[] = [];' in content:
        content = content.replace('export const CLUSTERS: ClusterInfo[] = [];', f'export const CLUSTERS: ClusterInfo[] = {cluster_str};')
    else:
        content = re.sub(r'export const CLUSTERS: ClusterInfo\[\] = \[.*?\];', f'export const CLUSTERS: ClusterInfo[] = {cluster_str};', content, flags=re.DOTALL)
        
    with open(data_ts, "w") as f:
        f.write(content)
    print("Exported 0 clusters (Honest build, no fake data injected)")

if __name__ == "__main__":
    main()
