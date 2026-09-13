import sqlite3
import pandas as pd
from pathlib import Path

def main():
    db_path = Path("data/onchain_intelligence.db")
    conn = sqlite3.connect(db_path)
    
    print("Running BONK Cohort Analysis...")
    
    # Get Airdrop recipients
    airdrop = pd.read_sql("SELECT wallet_address, amount FROM bonk_airdrop", conn)
    
    if len(airdrop) == 0:
        print("No airdrop data found yet.")
        return
        
    print(f"Total Airdrop Recipients: {len(airdrop)}")
    
    # Find their trades on BONK
    trades = pd.read_sql("SELECT wallet_address, side, amount_tokens FROM trades WHERE token_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'", conn)
    
    cohorts = {
        "Airdrop recipient": 0,
        "Early buyer": 0,
        "Airdrop + Buy": 0,
        "Early seller": 0
    }
    
    airdrop_set = set(airdrop["wallet_address"])
    
    for idx, row in airdrop.iterrows():
        wallet = row["wallet_address"]
        w_trades = trades[trades["wallet_address"] == wallet]
        
        if len(w_trades) == 0:
            cohorts["Airdrop recipient"] += 1
            conn.execute("UPDATE bonk_airdrop SET cohort='Airdrop recipient' WHERE wallet_address=?", (wallet,))
        else:
            has_buy = len(w_trades[w_trades["side"] == "BUY"]) > 0
            has_sell = len(w_trades[w_trades["side"] == "SELL"]) > 0
            
            if has_buy and not has_sell:
                cohorts["Airdrop + Buy"] += 1
                conn.execute("UPDATE bonk_airdrop SET cohort='Airdrop + Buy' WHERE wallet_address=?", (wallet,))
            elif has_sell:
                cohorts["Early seller"] += 1
                conn.execute("UPDATE bonk_airdrop SET cohort='Early seller' WHERE wallet_address=?", (wallet,))
            else:
                cohorts["Airdrop recipient"] += 1
                
    # Also find Early Buyers (people who bought but didn't get Airdrop)
    all_buyers = set(trades[trades["side"] == "BUY"]["wallet_address"])
    non_airdrop_buyers = all_buyers - airdrop_set
    cohorts["Early buyer"] = len(non_airdrop_buyers)
    
    for w in non_airdrop_buyers:
        conn.execute("INSERT OR IGNORE INTO bonk_airdrop (wallet_address, amount, timestamp, cohort) VALUES (?, 0, 0, 'Early buyer')", (w,))
        
    conn.commit()
    conn.close()
    
    print("\n--- BONK BEHAVIORAL COHORTS ---")
    for k, v in cohorts.items():
        print(f"{k}: {v}")
        
if __name__ == "__main__":
    main()
