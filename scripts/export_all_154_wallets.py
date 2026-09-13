#!/usr/bin/env python3
import sqlite3, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import DATA_DIR
from analytics.scoring_engine import ScoringEngine

def main():
    db_path = DATA_DIR / "onchain_intelligence.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    rows = conn.execute("""
        SELECT t.wallet_address, COUNT(DISTINCT t.token_mint) hits 
        FROM trades t 
        JOIN tokens tk ON tk.mint=t.token_mint 
        WHERE t.side='BUY' AND t.is_first_buyer=1 AND t.source_type IN ('ONCHAIN','API') AND tk.is_winner=1 
        GROUP BY t.wallet_address 
        HAVING hits >= 2
    """).fetchall()
    
    smart_wallets = []
    
    for row in rows:
        wallet = row["wallet_address"]
        hits = row["hits"]
        
        w_stats = conn.execute("""
            SELECT 
                COUNT(*) as total_tokens_bought,
                AVG(t.entry_delay_seconds) as avg_entry_delay_seconds,
                AVG(tk.max_return_x) as avg_max_return_x
            FROM trades t
            JOIN tokens tk ON t.token_mint = tk.mint
            WHERE t.wallet_address = ? AND t.side='BUY'
        """, (wallet,)).fetchone()
        
        wallet_data = conn.execute("SELECT exit_efficiency FROM wallets WHERE address = ?", (wallet,)).fetchone()
        real_exit = wallet_data["exit_efficiency"] if wallet_data and wallet_data["exit_efficiency"] is not None else 0.5
        
        token_rows = conn.execute("""
            SELECT DISTINCT tk.symbol, tk.is_winner 
            FROM trades t 
            JOIN tokens tk ON tk.mint=t.token_mint 
            WHERE t.wallet_address = ? AND t.side='BUY' AND t.is_first_buyer=1
        """, (wallet,)).fetchall()
        
        hit_tokens = [r["symbol"] for r in token_rows if r["is_winner"]]
        control_tokens_hit = [r["symbol"] for r in token_rows if not r["is_winner"]]
        
        metrics = {
            "winners_entered": hits,
            "total_tokens_bought": w_stats["total_tokens_bought"],
            "avg_entry_delay_seconds": w_stats["avg_entry_delay_seconds"] or 3600,
            "avg_max_return_x": w_stats["avg_max_return_x"] or 1.0,
            "exit_efficiency": real_exit,
            "cluster_size": 1,
            "is_cluster_root": True,
            "is_exchange_funded": False
        }
        
        score_data = ScoringEngine.compute_smart_wallet_score(metrics)
        c = score_data["components"]
        
        smart_wallets.append({
            "address": wallet,
            "label": f"Smart Wallet {wallet[:4]}",
            "smartScore": score_data["score"],
            "independenceScore": c.get("independence", 0),
            "selectivityScore": c.get("selectivity", 0),
            "precocityAvgSec": w_stats["avg_entry_delay_seconds"] or 0,
            "avgPostEntryReturn": w_stats["avg_max_return_x"] or 0,
            "exitEfficiency": real_exit * 100,
            "totalTokensBought": w_stats["total_tokens_bought"],
            "totalWinnersEntered": hits,
            "fundingSource": "ONCHAIN",
            "hitTokens": hit_tokens,
            "controlTokens": control_tokens_hit,
            "scoreBreakdown": {
                "earlyBigWins": c.get("early_big_wins", 0),
                "precocity": c.get("precocity", 0),
                "selectivity": c.get("selectivity", 0),
                "postEntryReturn": c.get("post_entry_return", 0),
                "exitManagement": c.get("exit_management", 0),
                "independence": c.get("independence", 0)
            }
        })
        
    smart_wallets.sort(key=lambda x: x["smartScore"], reverse=True)
    
    with open(DATA_DIR / "smart_wallets.json", "w") as f:
        json.dump(smart_wallets, f, indent=2)
        
    print(f"Exported {len(smart_wallets)} empirically validated smart wallets to data/smart_wallets.json")
    conn.close()

if __name__ == "__main__":
    main()
