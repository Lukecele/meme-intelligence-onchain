-- Solana On-Chain Meme Coin Intelligence Database Schema (Section 6.3)

CREATE TABLE IF NOT EXISTS tokens (
    mint TEXT PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT,
    creator TEXT,
    launch_time TEXT,
    launch_timestamp INTEGER,
    first_pool TEXT,
    initial_liquidity REAL DEFAULT 0.0,
    chain TEXT DEFAULT 'solana',
    peak_mcap REAL DEFAULT 0.0,
    max_return_x REAL DEFAULT 1.0,
    is_winner INTEGER DEFAULT 0,
    is_control INTEGER DEFAULT 0,
    has_airdrop INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wallets (
    address TEXT PRIMARY KEY,
    label TEXT,
    first_seen TEXT,
    first_seen_timestamp INTEGER,
    score REAL DEFAULT 0.0,
    insider_score REAL DEFAULT 0.0,
    activity_rate REAL DEFAULT 0.0,
    total_tokens_bought INTEGER DEFAULT 0,
    total_winners_entered INTEGER DEFAULT 0,
    total_control_entered INTEGER DEFAULT 0,
    selectivity_score REAL DEFAULT 0.0,
    precocity_avg_sec REAL DEFAULT 0.0,
    avg_post_entry_return REAL DEFAULT 1.0,
    exit_efficiency REAL DEFAULT 0.0,
    funding_source TEXT,
    funding_tx TEXT,
    is_exchange_funded INTEGER DEFAULT 0,
    is_bot_sniper INTEGER DEFAULT 0,
    is_creator_insider INTEGER DEFAULT 0,
    notes TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_key TEXT NOT NULL,
    tx_hash TEXT,
    wallet_address TEXT NOT NULL,
    token_mint TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    date_str TEXT,
    side TEXT NOT NULL, -- 'BUY', 'SELL', 'AIRDROP', 'LP_ADD', 'LP_REMOVE'
    amount_tokens REAL DEFAULT 0.0,
    amount_sol REAL DEFAULT 0.0,
    amount_usd REAL DEFAULT 0.0,
    price_usd REAL DEFAULT 0.0,
    is_airdrop INTEGER DEFAULT 0,
    is_first_buyer INTEGER DEFAULT 0,
    entry_delay_seconds INTEGER DEFAULT 0,
    program_id TEXT,
    source_type TEXT NOT NULL DEFAULT 'ONCHAIN' CHECK(source_type IN ('ONCHAIN','API','DERIVED','SIMULATED','REFERENCE')),
    source_name TEXT,
    source_ref TEXT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_json TEXT,
    FOREIGN KEY(wallet_address) REFERENCES wallets(address),
    FOREIGN KEY(token_mint) REFERENCES tokens(mint),
    CHECK(is_first_buyer = 0 OR side = 'BUY'),
    UNIQUE(event_key)
);

CREATE TABLE IF NOT EXISTS clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cluster_id TEXT NOT NULL,
    wallet_address TEXT NOT NULL,
    parent_wallet TEXT,
    confidence REAL DEFAULT 1.0,
    relation_type TEXT NOT NULL, -- 'DIRECT_FUNDING', 'COORDINATED_TIMING', 'SHARED_CREATOR', 'SHARED_SIGNER'
    first_detected_at INTEGER,
    UNIQUE(cluster_id, wallet_address)
);

CREATE TABLE IF NOT EXISTS historical_outcomes (
    token_mint TEXT PRIMARY KEY,
    max_return_1h REAL DEFAULT 1.0,
    max_return_24h REAL DEFAULT 1.0,
    max_return_7d REAL DEFAULT 1.0,
    max_return_30d REAL DEFAULT 1.0,
    peak_mcap REAL DEFAULT 0.0,
    status TEXT DEFAULT 'COMPLETED',
    FOREIGN KEY(token_mint) REFERENCES tokens(mint)
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_mint TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    score REAL NOT NULL,
    confidence REAL NOT NULL,
    signal_level TEXT NOT NULL, -- 'ALTO', 'MEDIO', 'BASSO'
    wallets_count INTEGER DEFAULT 0,
    independent_wallets_count INTEGER DEFAULT 0,
    wallets_involved TEXT, -- JSON Array of addresses and scores
    risks_json TEXT, -- JSON Array of risk factors
    market_cap_usd REAL DEFAULT 0.0,
    liquidity_usd REAL DEFAULT 0.0,
    token_age_minutes REAL DEFAULT 0.0,
    alert_text TEXT NOT NULL,
    dispatched INTEGER DEFAULT 0,
    FOREIGN KEY(token_mint) REFERENCES tokens(mint)
);

CREATE TABLE IF NOT EXISTS simulated_trades (
    id TEXT PRIMARY KEY,
    token_mint TEXT NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT,
    entry_timestamp INTEGER NOT NULL,
    entry_price_usd REAL NOT NULL,
    entry_mcap_usd REAL NOT NULL,
    amount_invested_usd REAL DEFAULT 100.0,
    amount_invested_sol REAL DEFAULT 0.0,
    initial_tokens REAL NOT NULL,
    current_tokens REAL NOT NULL,
    current_price_usd REAL NOT NULL,
    current_mcap_usd REAL NOT NULL,
    current_position_value_usd REAL DEFAULT 0.0,
    total_cash_extracted_usd REAL DEFAULT 0.0,
    total_net_pnl_usd REAL DEFAULT 0.0,
    total_net_pnl_pct REAL DEFAULT 0.0,
    status TEXT NOT NULL, -- 'OPEN_FULL', 'OPEN_PARTIAL_EXITED', 'CLOSED_FULL_EXIT', 'CLOSED_MANUAL'
    partial_sells_count INTEGER DEFAULT 0,
    copy_trade_logs_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(token_mint) REFERENCES tokens(mint)
);

-- Indexes for high-speed queries during backtest and real-time monitoring
CREATE INDEX IF NOT EXISTS idx_trades_wallet ON trades(wallet_address);
CREATE INDEX IF NOT EXISTS idx_trades_token ON trades(token_mint);
CREATE INDEX IF NOT EXISTS idx_trades_timestamp ON trades(timestamp);
CREATE INDEX IF NOT EXISTS idx_trades_wallet_token ON trades(wallet_address, token_mint);
CREATE INDEX IF NOT EXISTS idx_clusters_wallet ON clusters(wallet_address);
CREATE INDEX IF NOT EXISTS idx_clusters_id ON clusters(cluster_id);
CREATE INDEX IF NOT EXISTS idx_wallets_score ON wallets(score);
CREATE INDEX IF NOT EXISTS idx_wallets_insider_score ON wallets(insider_score);
CREATE INDEX IF NOT EXISTS idx_simulated_trades_mint ON simulated_trades(token_mint);


CREATE TABLE IF NOT EXISTS airdrop_claims (
 id INTEGER PRIMARY KEY AUTOINCREMENT, wallet_address TEXT NOT NULL, token_mint TEXT NOT NULL, amount_claimed REAL NOT NULL,
 claim_timestamp INTEGER NOT NULL, cohort TEXT, reinvested_in_subsequent_winners INTEGER DEFAULT 0, sol_spent_reinvesting REAL DEFAULT 0.0,
 source_type TEXT NOT NULL CHECK(source_type IN ('ONCHAIN','API')), source_name TEXT NOT NULL, source_ref TEXT, fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, notes TEXT,
 UNIQUE(wallet_address, token_mint, source_ref)
);
