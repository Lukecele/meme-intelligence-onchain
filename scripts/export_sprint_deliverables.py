import sqlite3
import pandas as pd
import json
from config.settings import DATA_DIR
import os

def main():
    db_path = DATA_DIR / "onchain_intelligence.db"
    out_dir = DATA_DIR / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        # 1. Lista airdrop BONK
        try:
            airdrop = pd.read_sql("SELECT * FROM airdrop_claims", conn)
            airdrop.to_csv(out_dir / "Lista_airdrop_BONK.csv", index=False)
            print("Exported Lista_airdrop_BONK.csv")
        except Exception as e:
            print(f"Skipped airdrop: {e}")

        # 2. Lista first buyers BONK/WIF/POPCAT
        try:
            fb = pd.read_sql("SELECT * FROM trades WHERE side='BUY'", conn)
            fb.to_csv(out_dir / "Lista_first_buyers_BONK_WIF_POPCAT.csv", index=False)
            print("Exported Lista_first_buyers_BONK_WIF_POPCAT.csv")
        except Exception as e:
            print(f"Skipped first buyers: {e}")

        # 3. Wallet intersection matrix
        try:
            # Pivot table: wallet vs token
            matrix = pd.read_sql("""
                SELECT wallet_address, token_mint, COUNT(*) as buy_count 
                FROM trades WHERE side='BUY' GROUP BY wallet_address, token_mint
            """, conn)
            if not matrix.empty:
                pivot = matrix.pivot(index='wallet_address', columns='token_mint', values='buy_count').fillna(0)
                pivot.to_csv(out_dir / "Wallet_intersection_matrix.csv")
                print("Exported Wallet_intersection_matrix.csv")
        except Exception as e:
            print(f"Skipped matrix: {e}")

        # 4. Wallet score preliminare
        try:
            scores = pd.read_sql("SELECT * FROM wallets", conn)
            scores.to_csv(out_dir / "Wallet_score_preliminare.csv", index=False)
            print("Exported Wallet_score_preliminare.csv")
        except Exception as e:
            print(f"Skipped scores: {e}")

        # 5. Cluster sospetti (JSON)
        try:
            clusters = pd.read_sql("SELECT * FROM clusters", conn)
            clusters_dict = clusters.to_dict(orient='records')
            with open(out_dir / "Cluster_sospetti.json", "w") as f:
                json.dump(clusters_dict, f, indent=2)
            print("Exported Cluster_sospetti.json")
        except Exception as e:
            print(f"Skipped clusters: {e}")

if __name__ == "__main__":
    main()
