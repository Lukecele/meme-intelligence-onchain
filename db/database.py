"""
Database connection and repository for Solana On-Chain Intelligence System
"""
import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional
from config.settings import DB_PATH

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        schema_path = DB_PATH.parent.parent / "db" / "schema.sql"
        if not schema_path.exists():
            return
        with self.get_connection() as conn:
            with open(schema_path, "r") as f:
                conn.executescript(f.read())
            conn.commit()

    # --- Token Methods ---
    def upsert_token(self, token_data: Dict[str, Any]):
        query = """
        INSERT INTO tokens (
            mint, symbol, name, creator, launch_time, launch_timestamp,
            first_pool, initial_liquidity, chain, peak_mcap, max_return_x,
            is_winner, is_control, has_airdrop
        ) VALUES (
            :mint, :symbol, :name, :creator, :launch_time, :launch_timestamp,
            :first_pool, :initial_liquidity, :chain, :peak_mcap, :max_return_x,
            :is_winner, :is_control, :has_airdrop
        )
        ON CONFLICT(mint) DO UPDATE SET
            symbol=excluded.symbol,
            name=excluded.name,
            creator=coalesce(excluded.creator, tokens.creator),
            peak_mcap=excluded.peak_mcap,
            max_return_x=excluded.max_return_x,
            initial_liquidity=excluded.initial_liquidity,
            is_winner=excluded.is_winner,
            is_control=excluded.is_control
        """
        with self.get_connection() as conn:
            conn.execute(query, {
                "mint": token_data["mint"],
                "symbol": token_data.get("symbol", ""),
                "name": token_data.get("name", ""),
                "creator": token_data.get("creator", None),
                "launch_time": token_data.get("launch_time", ""),
                "launch_timestamp": token_data.get("launch_timestamp", 0),
                "first_pool": token_data.get("first_pool", ""),
                "initial_liquidity": token_data.get("initial_liquidity", token_data.get("initial_liquidity_usd", 0.0)),
                "chain": token_data.get("chain", "solana"),
                "peak_mcap": token_data.get("peak_mcap", token_data.get("peak_mcap_usd", 0.0)),
                "max_return_x": token_data.get("max_return_x", 1.0),
                "is_winner": 1 if token_data.get("is_winner", False) else 0,
                "is_control": 1 if token_data.get("is_control", False) else 0,
                "has_airdrop": 1 if token_data.get("has_airdrop", False) else 0,
            })
            conn.commit()

    def get_tokens(self, is_winner: Optional[bool] = None, is_control: Optional[bool] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM tokens WHERE 1=1"
        params = []
        if is_winner is not None:
            query += " AND is_winner = ?"
            params.append(1 if is_winner else 0)
        if is_control is not None:
            query += " AND is_control = ?"
            params.append(1 if is_control else 0)
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_token(self, mint: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM tokens WHERE mint = ?", (mint,))
            row = cursor.fetchone()
            return dict(row) if row else None

    # --- Wallet Methods ---
    def upsert_wallet(self, wallet_data: Dict[str, Any]):
        query = """
        INSERT INTO wallets (
            address, label, first_seen, first_seen_timestamp, score, insider_score,
            activity_rate, total_tokens_bought, total_winners_entered, total_control_entered,
            selectivity_score, precocity_avg_sec, avg_post_entry_return, exit_efficiency,
            funding_source, funding_tx, is_exchange_funded, is_bot_sniper, is_creator_insider, notes
        ) VALUES (
            :address, :label, :first_seen, :first_seen_timestamp, :score, :insider_score,
            :activity_rate, :total_tokens_bought, :total_winners_entered, :total_control_entered,
            :selectivity_score, :precocity_avg_sec, :avg_post_entry_return, :exit_efficiency,
            :funding_source, :funding_tx, :is_exchange_funded, :is_bot_sniper, :is_creator_insider, :notes
        )
        ON CONFLICT(address) DO UPDATE SET
            label=coalesce(excluded.label, wallets.label),
            score=excluded.score,
            insider_score=excluded.insider_score,
            activity_rate=excluded.activity_rate,
            total_tokens_bought=excluded.total_tokens_bought,
            total_winners_entered=excluded.total_winners_entered,
            total_control_entered=excluded.total_control_entered,
            selectivity_score=excluded.selectivity_score,
            precocity_avg_sec=excluded.precocity_avg_sec,
            avg_post_entry_return=excluded.avg_post_entry_return,
            exit_efficiency=excluded.exit_efficiency,
            funding_source=coalesce(excluded.funding_source, wallets.funding_source),
            funding_tx=coalesce(excluded.funding_tx, wallets.funding_tx),
            is_exchange_funded=coalesce(excluded.is_exchange_funded, wallets.is_exchange_funded),
            is_bot_sniper=excluded.is_bot_sniper,
            is_creator_insider=excluded.is_creator_insider,
            notes=coalesce(excluded.notes, wallets.notes),
            updated_at=CURRENT_TIMESTAMP
        """
        defaults = {
            "label": None, "first_seen": None, "first_seen_timestamp": 0,
            "score": 0.0, "insider_score": 0.0, "activity_rate": 0.0,
            "total_tokens_bought": 0, "total_winners_entered": 0, "total_control_entered": 0,
            "selectivity_score": 0.0, "precocity_avg_sec": 0.0, "avg_post_entry_return": 1.0,
            "exit_efficiency": 0.0, "funding_source": None, "funding_tx": None,
            "is_exchange_funded": 0, "is_bot_sniper": 0, "is_creator_insider": 0, "notes": None
        }
        for k, v in defaults.items():
            if k not in wallet_data:
                wallet_data[k] = v
        with self.get_connection() as conn:
            conn.execute(query, wallet_data)
            conn.commit()

    def get_wallets(self, min_score: float = 0.0, limit: int = 100) -> List[Dict[str, Any]]:
        query = "SELECT * FROM wallets WHERE score >= ? ORDER BY score DESC LIMIT ?"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (min_score, limit))
            return [dict(row) for row in cursor.fetchall()]

    def get_wallet(self, address: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM wallets WHERE address = ?", (address,))
            row = cursor.fetchone()
            return dict(row) if row else None

    # --- Trades Methods ---
    def insert_trade(self, trade_data: Dict[str, Any]):
        query = """
        INSERT INTO trades (
            event_key, tx_hash, wallet_address, token_mint, timestamp, date_str, side,
            amount_tokens, amount_sol, amount_usd, price_usd, is_airdrop,
            is_first_buyer, entry_delay_seconds, program_id, source_type, source_name, source_ref, raw_json
        ) VALUES (
            :event_key, :tx_hash, :wallet_address, :token_mint, :timestamp, :date_str, :side,
            :amount_tokens, :amount_sol, :amount_usd, :price_usd, :is_airdrop,
            :is_first_buyer, :entry_delay_seconds, :program_id, :source_type, :source_name, :source_ref, :raw_json
        )
        ON CONFLICT(event_key) DO NOTHING
        """
        with self.get_connection() as conn:
            event_key = trade_data.get("event_key") or trade_data.get("tx_hash")
            if not event_key:
                event_key = f"{trade_data.get('source_name','EVENT')}:{trade_data.get('token_mint','')}:{trade_data.get('source_ref','')}:{trade_data.get('wallet_address','')}:{trade_data.get('side','')}"
            conn.execute(query, {
                "event_key": event_key,
                "tx_hash": trade_data.get("tx_hash"),
                "wallet_address": trade_data["wallet_address"],
                "token_mint": trade_data["token_mint"],
                "timestamp": trade_data.get("timestamp", 0),
                "date_str": trade_data.get("date_str", ""),
                "side": trade_data.get("side", "BUY"),
                "amount_tokens": trade_data.get("amount_tokens", 0.0),
                "amount_sol": trade_data.get("amount_sol", 0.0),
                "amount_usd": trade_data.get("amount_usd", 0.0),
                "price_usd": trade_data.get("price_usd", 0.0),
                "is_airdrop": 1 if trade_data.get("is_airdrop", False) else 0,
                "is_first_buyer": 1 if trade_data.get("is_first_buyer", False) else 0,
                "entry_delay_seconds": trade_data.get("entry_delay_seconds", 0),
                "program_id": trade_data.get("program_id", None),
                "source_type": trade_data.get("source_type", "ONCHAIN"),
                "source_name": trade_data.get("source_name"),
                "source_ref": trade_data.get("source_ref"),
                "raw_json": json.dumps(trade_data.get("raw_json")) if trade_data.get("raw_json") is not None else None
            })
            conn.commit()

    def get_trades_for_token(self, token_mint: str, limit: int = 500) -> List[Dict[str, Any]]:
        query = "SELECT * FROM trades WHERE token_mint = ? ORDER BY timestamp ASC LIMIT ?"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (token_mint, limit))
            return [dict(row) for row in cursor.fetchall()]

    def get_trades_for_wallet(self, wallet_address: str) -> List[Dict[str, Any]]:
        query = """
        SELECT t.*, tk.symbol, tk.is_winner, tk.is_control, tk.max_return_x
        FROM trades t
        JOIN tokens tk ON t.token_mint = tk.mint
        WHERE t.wallet_address = ?
        ORDER BY t.timestamp ASC
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (wallet_address,))
            return [dict(row) for row in cursor.fetchall()]

    # --- Clusters Methods ---
    def upsert_cluster(self, cluster_id: str, wallet_address: str, parent_wallet: Optional[str],
                       confidence: float, relation_type: str, first_detected_at: int):
        query = """
        INSERT INTO clusters (cluster_id, wallet_address, parent_wallet, confidence, relation_type, first_detected_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(cluster_id, wallet_address) DO UPDATE SET
            parent_wallet=coalesce(excluded.parent_wallet, clusters.parent_wallet),
            confidence=excluded.confidence,
            relation_type=excluded.relation_type
        """
        with self.get_connection() as conn:
            conn.execute(query, (cluster_id, wallet_address, parent_wallet, confidence, relation_type, first_detected_at))
            conn.commit()

    def get_clusters_for_wallet(self, wallet_address: str) -> List[Dict[str, Any]]:
        query = "SELECT * FROM clusters WHERE wallet_address = ?"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (wallet_address,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_clusters(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM clusters"
        with self.get_connection() as conn:
            cursor = conn.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # --- Alerts Methods ---
    def insert_alert(self, alert_data: Dict[str, Any]) -> int:
        token_mint = alert_data["token_mint"]
        # Ensure token entry exists
        existing = self.get_token(token_mint)
        if not existing:
            self.upsert_token({
                "mint": token_mint,
                "symbol": alert_data.get("symbol", "ALERT_TOKEN"),
                "name": alert_data.get("name", "Alert Token Candidate"),
                "initial_liquidity": alert_data.get("liquidity_usd", 0.0),
                "peak_mcap": alert_data.get("market_cap_usd", 0.0),
                "chain": "solana"
            })

        query = """
        INSERT INTO alerts (
            token_mint, timestamp, score, confidence, signal_level,
            wallets_count, independent_wallets_count, wallets_involved,
            risks_json, market_cap_usd, liquidity_usd, token_age_minutes, alert_text, dispatched
        ) VALUES (
            :token_mint, :timestamp, :score, :confidence, :signal_level,
            :wallets_count, :independent_wallets_count, :wallets_involved,
            :risks_json, :market_cap_usd, :liquidity_usd, :token_age_minutes, :alert_text, :dispatched
        )
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, {
                "token_mint": alert_data["token_mint"],
                "timestamp": alert_data.get("timestamp", 0),
                "score": alert_data.get("score", 0.0),
                "confidence": alert_data.get("confidence", 0.0),
                "signal_level": alert_data.get("signal_level", "MEDIO"),
                "wallets_count": alert_data.get("wallets_count", 0),
                "independent_wallets_count": alert_data.get("independent_wallets_count", 0),
                "wallets_involved": json.dumps(alert_data.get("wallets_involved", [])),
                "risks_json": json.dumps(alert_data.get("risks_json", [])),
                "market_cap_usd": alert_data.get("market_cap_usd", 0.0),
                "liquidity_usd": alert_data.get("liquidity_usd", 0.0),
                "token_age_minutes": alert_data.get("token_age_minutes", 0.0),
                "alert_text": alert_data.get("alert_text", ""),
                "dispatched": 1 if alert_data.get("dispatched", False) else 0
            })
            conn.commit()
            return cursor.lastrowid

    def get_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        query = """
        SELECT a.*, t.symbol, t.name
        FROM alerts a
        LEFT JOIN tokens t ON a.token_mint = t.mint
        ORDER BY a.timestamp DESC LIMIT ?
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, (limit,))
            return [dict(row) for row in cursor.fetchall()]
