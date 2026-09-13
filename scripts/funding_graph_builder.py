import asyncio
import logging
import sqlite3
import json
import re
from pathlib import Path
from extractors.solana_rpc import SolanaRPCClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FundingGraphBuilder:
    def __init__(self):
        self.rpc = SolanaRPCClient()
        self.db_path = Path("data/onchain_intelligence.db")
        self.data_ts_path = Path("web/src/lib/data.ts")
        
    async def run(self):
        print("Building REAL Funding Graph for Smart Wallets...")
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Get smart wallets
        wallets = conn.execute("""
            SELECT address, score FROM wallets
        """).fetchall()
        
        clusters = {}
        for w in wallets:
            wallet_addr = w["address"]
            print(f"Fetching funding tx for {wallet_addr}...")
            
            # Fetch very first transaction (oldest) using Helius before/until is hard, 
            # we just get the oldest page by sorting asc (if supported) or fetching last page
            page = await self.rpc.get_transactions_for_address(
                wallet_addr, limit=100, sort_order="asc", transaction_details="full"
            )
            
            txs = page.get("data", [])
            if not txs:
                continue
                
            first_tx = txs[0] # Very first transaction
            
            meta = first_tx.get("meta", {})
            if meta.get("err"): continue
            
            pre_b = meta.get("preBalances", [])
            post_b = meta.get("postBalances", [])
            accounts = first_tx.get("transaction", {}).get("message", {}).get("accountKeys", [])
            if accounts and isinstance(accounts[0], dict):
                accounts = [a.get("pubkey") for a in accounts]
                
            wallet_idx = -1
            if wallet_addr in accounts:
                wallet_idx = accounts.index(wallet_addr)
                
            funder = None
            funder_amount = 0
            
            if wallet_idx >= 0 and wallet_idx < len(post_b):
                # Look for who lost SOL
                for i, account in enumerate(accounts):
                    if i == wallet_idx: continue
                    if i < len(pre_b) and i < len(post_b):
                        sol_delta = (post_b[i] - pre_b[i]) / 1e9
                        if sol_delta < -0.01: # Lost SOL
                            funder = account
                            funder_amount = abs(sol_delta)
                            break
                            
            # Some txs are just SystemProgram transfer, let's identify standard funders
            if funder:
                # E.g. Coinbase, Binance hot wallets, or another user
                known_exchanges = {
                    "5JQ8MhdpXwvND6462M1n1Z1rB6ZJgU5X5U": "Binance Hot Wallet",
                    "A77HErqNJAEDzJ2c75aWfX23o3o9pZ4P": "Coinbase Hot Wallet"
                }
                funder_label = known_exchanges.get(funder, funder)
                if funder not in clusters:
                    clusters[funder] = {
                        "clusterId": f"CLUST_{funder[:6]}",
                        "rootAddress": funder_label,
                        "members": [],
                        "relationType": "DIRECT_FUNDING",
                        "avgScore": 0,
                        "confidence": 1.0,
                        "totalVolumeSol": 0
                    }
                clusters[funder]["members"].append(wallet_addr)
                clusters[funder]["totalVolumeSol"] += funder_amount
                clusters[funder]["avgScore"] += w["score"]
                
            await asyncio.sleep(0.3)
            
        conn.close()
        
        final_clusters = []
        for funder, data in clusters.items():
            if len(data["members"]) >= 2: # Only keep clusters with 2+ smart wallets!
                data["avgScore"] = data["avgScore"] / len(data["members"])
                final_clusters.append(data)
                
        # Export to data.ts
        with open(self.data_ts_path, "r") as f:
            content = f.read()
            
        cluster_str = json.dumps(final_clusters, indent=2)
        
        if 'export const CLUSTERS: ClusterInfo[] = [];' in content:
            content = content.replace('export const CLUSTERS: ClusterInfo[] = [];', f'export const CLUSTERS: ClusterInfo[] = {cluster_str};')
        else:
            content = re.sub(r'export const CLUSTERS: ClusterInfo\[\] = \[.*?\];', f'export const CLUSTERS: ClusterInfo[] = {cluster_str};', content, flags=re.DOTALL)
            
        with open(self.data_ts_path, "w") as f:
            f.write(content)
            
        print(f"Exported {len(final_clusters)} REAL funding clusters to data.ts")

async def main():
    builder = FundingGraphBuilder()
    await builder.run()

if __name__ == "__main__":
    asyncio.run(main())
