"""
Wallet x Token Intersection Matrix & Multi-Winner Recurrence Engine (Section 4.3 & 10.2)
"""
import pandas as pd
import logging
from typing import Dict, Any, List, Set, Tuple
from db.database import Database

logger = logging.getLogger(__name__)

class MatrixIntersectionEngine:
    def __init__(self, db: Database):
        self.db = db

    def build_wallet_token_matrix(self) -> Tuple[pd.DataFrame, pd.DataFrame, List[Dict[str, Any]]]:
        """
        Builds the binary intersection matrix (Wallets x Tokens) and Token Overlap Correlation Matrix
        """
        with self.db.get_connection() as conn:
            query = """
            SELECT DISTINCT t.wallet_address, t.token_mint, tk.symbol, tk.is_winner, tk.is_control
            FROM trades t
            JOIN tokens tk ON t.token_mint = tk.mint
            WHERE ((t.side = 'BUY' AND t.is_first_buyer = 1) OR t.is_airdrop = 1)
              AND t.source_type IN ('ONCHAIN','API')
            """
            df_trades = pd.read_sql_query(query, conn)

        if df_trades.empty:
            return pd.DataFrame(), pd.DataFrame(), []

        # Pivot into binary matrix: Index = wallet_address, Columns = symbol
        matrix = pd.crosstab(df_trades["wallet_address"], df_trades["symbol"])
        matrix = (matrix > 0).astype(int)

        # Token x Token Overlap Matrix (Co-occurrence of early wallets)
        token_overlap = matrix.T.dot(matrix)

        # Identify multi-winner recurring wallets
        winner_tokens = [r["symbol"] for r in self.db.get_tokens(is_winner=True) if r["symbol"] in matrix.columns]
        control_tokens = [r["symbol"] for r in self.db.get_tokens(is_control=True) if r["symbol"] in matrix.columns]

        recurring_wallets = []
        for wallet, row in matrix.iterrows():
            winners_count = int(sum(row[col] for col in winner_tokens if col in row))
            control_count = int(sum(row[col] for col in control_tokens if col in row))
            
            if winners_count >= 2:
                recurring_wallets.append({
                    "wallet_address": str(wallet),
                    "winners_count": winners_count,
                    "control_count": control_count,
                    "tokens": [col for col in matrix.columns if row[col] == 1]
                })

        recurring_wallets.sort(key=lambda x: (x["winners_count"], -x["control_count"]), reverse=True)

        return matrix, token_overlap, recurring_wallets
