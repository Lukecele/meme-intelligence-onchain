import pytest
from analytics.scoring_engine import ScoringEngine
from extractors.first_buyers_extractor import FirstBuyersExtractor

def test_scoring_engine_early_wins():
    assert ScoringEngine.calculate_early_wins_score(0) == 0.0
    assert ScoringEngine.calculate_early_wins_score(2) == 80.0
    assert ScoringEngine.calculate_early_wins_score(5) == 100.0

def test_scoring_engine_selectivity():
    # 2 winners out of 10 buys = 20% hit rate => 80 raw score. Penalty = 1.0 (<= 30)
    assert ScoringEngine.calculate_selectivity_score(2, 10) == 80.0
    # 2 winners out of 2000 buys = 0.1% hit rate => 0.4 raw score. Penalty = 0.05
    assert ScoringEngine.calculate_selectivity_score(2, 2000) == 0.02

def test_scoring_engine_full():
    metrics = {
        "winners_entered": 2,
        "total_tokens_bought": 5,
        "avg_entry_delay_seconds": 25, # <30s => 100
        "avg_max_return_x": 1000, # >=500 => 100
        "exit_efficiency": 0.9, # => 90
        "cluster_size": 1,
        "is_cluster_root": True,
        "is_exchange_funded": False
    }
    res = ScoringEngine.compute_smart_wallet_score(metrics)
    assert res["score"] > 80.0
    assert res["components"]["precocity"] == 100.0

@pytest.mark.asyncio
async def test_semantic_parser_buy_fixture():
    extractor = FirstBuyersExtractor()
    
    # Fake Solana RPC transaction response simulating a BUY
    # Wallet spends 1 SOL, receives 1000 BONK
    tx = {
        "meta": {
            "err": None,
            "preBalances": [2000000000], # 2 SOL
            "postBalances": [1000000000], # 1 SOL (cost 1 SOL)
            "preTokenBalances": [], # 0 BONK
            "postTokenBalances": [{
                "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                "owner": "WalletA",
                "uiTokenAmount": {"uiAmount": 1000}
            }]
        },
        "transaction": {
            "message": {
                "accountKeys": [{"pubkey": "WalletA"}]
            }
        }
    }
    
    parsed = extractor._parse_buy_event(tx, "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263")
    assert parsed is not None
    assert parsed["wallet"] == "WalletA"
    assert parsed["amount_tokens"] == 1000.0
    
    await extractor.close()

def test_semantic_parser_not_buy():
    extractor = FirstBuyersExtractor()
    # Token balance DECREASES (this is a sell, not a buy)
    tx = {
        "meta": {
            "err": None,
            "preBalances": [1000000000],
            "postBalances": [2000000000],
            "preTokenBalances": [{
                "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                "owner": "WalletA",
                "uiTokenAmount": {"uiAmount": 1000}
            }],
            "postTokenBalances": []
        },
        "transaction": {
            "message": {
                "accountKeys": [{"pubkey": "WalletA"}]
            }
        }
    }
    
    parsed = extractor._parse_buy_event(tx, "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263")
    # Our extractor currently specifically looks for BUYS for first-buyers.
    assert parsed is None
