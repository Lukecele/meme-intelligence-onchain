"""
Configuration Settings for Solana On-Chain Intelligence System
"""
import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
DB_PATH = DATA_DIR / "onchain_intelligence.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Load .env file manually if exists
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

# API Keys (Loaded strictly from .env)
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", "")
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY", "")
DUNE_API_KEY = os.getenv("DUNE_API_KEY", "")
SOLANA_TRACKER_API_KEY = os.getenv("SOLANA_TRACKER_API_KEY", "")
PYTH_API_KEY = os.getenv("PYTH_API_KEY", "")

# Solana RPC Endpoints (with fallback array)
RPC_ENDPOINTS = [
    f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}" if HELIUS_API_KEY else None,
    os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"),
    "https://rpc.ankr.com/solana",
    "https://solana-mainnet.rpc.extrnode.com",
    "https://mainnet.solanaspaces.com",
    "https://solana-api.projectserum.com",
]
# Filter out None and empty strings
RPC_ENDPOINTS = [rpc for rpc in RPC_ENDPOINTS if rpc and not rpc.endswith("api-key=")]
if not RPC_ENDPOINTS:
    RPC_ENDPOINTS = ["https://api.mainnet-beta.solana.com"]

# Telegram Alert Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Scoring Weights (Section 3.2 of Concept Specification)
SCORE_WEIGHTS = {
    "early_big_wins": 0.30,   # Numero e qualità ingressi anticipati in vincitori storici
    "selectivity": 0.20,      # Capacità di non comprare indiscriminatamente tutto
    "precocity": 0.15,        # Quanto presto entra rispetto al lancio reale
    "post_entry_return": 0.15,# Rendimento massimo successivo all'acquisto
    "exit_management": 0.10,  # Capacità di monetizzare / realizzare profitto
    "independence": 0.10,     # Riduzione del rischio insider/cluster mascherato
}

# Detection & Convergence Thresholds
MIN_QUALIFIED_WALLET_SCORE = 70.0    # Wallet con score >= 70 è considerato qualificato
HIGH_QUALIFIED_WALLET_SCORE = 85.0   # Wallet con score >= 85 è considerato tier-1 smart
CONVERGENCE_TIME_WINDOW_SEC = 1800   # 30 minuti di convergenza
MIN_CONVERGENT_WALLETS = 2          # Almeno 2 wallet qualificati indipendenti
MAX_INITIAL_MCAP_USD = 1_000_000    # Considera solo micro-cap <= 1M$
MIN_INITIAL_LIQUIDITY_USD = 5_000   # Esclude scam a liquidità zero
MAX_TOP10_SUPPLY_PCT = 35.0         # Filtro rischio supply concentration
MAX_CREATOR_SUPPLY_PCT = 10.0       # Filtro rischio concentrazione creator

# Known CEX Hot Wallets (to avoid false clustering)
KNOWN_EXCHANGES = {
    "5tzFkiKscBizbkHGXYbx52nAn23pmUorBQCSUxwK922W": "Binance 1",
    "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM": "Binance 2",
    "2AQdpHJ2JpcEgBtATUXjqwJEXMeWhUKzkjoBXQSp534R": "Binance 3",
    "AC5RDfQFmDS1deWZos921qqvw3xEmbKeC8CcdeLE3xED": "Kraken 1",
    "2ojv9BAiHUrvsm9gxDe7fJSzbNZSJcxZvf8dqmWGHG8S": "Coinbase 1",
    "H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS": "Coinbase 2",
    "5VCwKtCXgCJ6kit5FybXjvmsWnG6HXVGyA1SVdP6PBQ4": "OKX 1",
    "6Q3Kz2s49zP8P3YmZ9n69zXz2W88Y1ZqW5tV6tW3v7xQ": "Bybit 1",
    "CuieVDEDtLo7FypA9SbLM9saXFdb1dsshveFiuvbUeq5": "KuCoin 1",
    "ASTyfSima4LLAdDddFGkgbm3GLTqasxWNTBXBSqdaQTq": "Gate.io 1",
}
