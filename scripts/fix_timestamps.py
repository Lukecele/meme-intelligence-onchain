import sqlite3, json
from config.settings import DATA_DIR

db_path = DATA_DIR / "onchain_intelligence.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Get earliest timestamp for each token
earliest = {}
for row in c.execute("SELECT token_mint, MIN(timestamp) FROM trades GROUP BY token_mint"):
    earliest[row[0]] = row[1]

print("Earliest timestamps found:", earliest)

# Update the tokens table
for mint, ts in earliest.items():
    c.execute("UPDATE tokens SET launch_timestamp = ? WHERE mint = ?", (ts, mint))

# Now recalculate entry_delay_seconds for all trades
c.execute("""
    UPDATE trades 
    SET entry_delay_seconds = timestamp - (
        SELECT launch_timestamp FROM tokens WHERE tokens.mint = trades.token_mint
    )
""")
conn.commit()
print("Fixed entry_delay_seconds for all trades.")
conn.close()
