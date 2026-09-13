"""
Real-time Convergence Detector & Candidate Signal Generator (Section 5.1 & 5.3)
"""
import time
import logging
from typing import Dict, Any, List, Optional
from db.database import Database
from config.settings import (
    MIN_QUALIFIED_WALLET_SCORE, CONVERGENCE_TIME_WINDOW_SEC, MIN_CONVERGENT_WALLETS
)

logger = logging.getLogger(__name__)

class ConvergenceDetector:
    def __init__(self, db: Database):
        self.db = db

    def evaluate_token_convergence(self, token_mint: str, trades: List[Dict[str, Any]], token_meta: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyzes early trades on a token to detect multi-wallet smart convergence
        """
        if not trades:
            return None

        # Filter only BUY trades within the convergence window
        earliest_trade_ts = min(t.get("timestamp", 0) for t in trades)
        window_trades = [
            t for t in trades
            if t.get("side") == "BUY" and (t.get("timestamp", 0) - earliest_trade_ts) <= CONVERGENCE_TIME_WINDOW_SEC
        ]

        if not window_trades:
            return None

        # Lookup wallet scores and clusters
        qualified_wallets = []
        seen_addresses = set()
        cluster_map = {} # cluster_id -> list of member wallets

        for trade in window_trades:
            addr = trade.get("wallet_address")
            if not addr or addr in seen_addresses:
                continue
            seen_addresses.add(addr)

            wallet_data = self.db.get_wallet(addr)
            if not wallet_data:
                continue

            score = float(wallet_data.get("score", 0.0))
            insider_score = float(wallet_data.get("insider_score", 0.0))

            if score >= MIN_QUALIFIED_WALLET_SCORE or insider_score >= 70.0:
                clusters = self.db.get_clusters_for_wallet(addr)
                cluster_id = clusters[0]["cluster_id"] if clusters else None
                relation_type = clusters[0]["relation_type"] if clusters else "INDEPENDENT"

                wallet_info = {
                    "address": addr,
                    "label": wallet_data.get("label", "Smart Wallet"),
                    "score": score,
                    "insider_score": insider_score,
                    "entry_delay_seconds": trade.get("entry_delay_seconds", 0),
                    "amount_sol": trade.get("amount_sol", 0.0),
                    "cluster_id": cluster_id,
                    "relation_type": relation_type
                }
                qualified_wallets.append(wallet_info)

                if cluster_id:
                    if cluster_id not in cluster_map:
                        cluster_map[cluster_id] = []
                    cluster_map[cluster_id].append(wallet_info)

        # Count independent signal units
        independent_count = 0
        counted_clusters = set()
        
        for w in qualified_wallets:
            cid = w.get("cluster_id")
            if cid:
                if cid not in counted_clusters:
                    counted_clusters.add(cid)
                    independent_count += 1
            else:
                independent_count += 1

        if independent_count < MIN_CONVERGENT_WALLETS:
            return None

        # Calculate Aggregate Convergence Score
        avg_score = sum(w["score"] for w in qualified_wallets) / len(qualified_wallets)
        time_span_minutes = (max(t.get("timestamp", 0) for t in window_trades) - earliest_trade_ts) / 60.0

        # Determine Signal Level (Section 5.3)
        if len(qualified_wallets) >= 3 and independent_count >= 2 and avg_score >= 80.0:
            signal_level = "ALTO"
        elif independent_count >= 2 and avg_score >= 70.0:
            signal_level = "MEDIO"
        else:
            signal_level = "BASSO"

        return {
            "token_mint": token_mint,
            "symbol": token_meta.get("symbol", "UNKNOWN"),
            "name": token_meta.get("name", "Unknown Token"),
            "timestamp": int(time.time()),
            "score": round(avg_score, 1),
            "confidence": min(0.98, round(0.50 + (independent_count * 0.15) + (avg_score / 300.0), 2)),
            "signal_level": signal_level,
            "wallets_count": len(qualified_wallets),
            "independent_wallets_count": independent_count,
            "time_span_minutes": round(time_span_minutes, 1),
            "wallets_involved": qualified_wallets,
            "market_cap_usd": token_meta.get("market_cap_usd", 0.0),
            "liquidity_usd": token_meta.get("liquidity_usd", 0.0),
            "token_age_minutes": round(token_meta.get("token_age_minutes", 0.0), 1),
            "creator_concentration_pct": token_meta.get("creator_concentration_pct", 0.0)
        }
