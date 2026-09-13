"""
Wallet Scoring Engine: Smart Wallet Score & Insider Score (Sections 3.2 & 3.3)
"""
import math
import logging
from typing import Dict, Any, List, Optional
from config.settings import SCORE_WEIGHTS

logger = logging.getLogger(__name__)

class ScoringEngine:
    """
    Computes mathematical intelligence scores for observed Solana wallets.
    """

    @staticmethod
    def calculate_early_wins_score(winners_entered: int, total_winners_available: int = 5) -> float:
        """
        Grandi successi precoci (30% peso):
        Premia la partecipazione a molteplici grandi vincitori storici (BONK, WIF, POPCAT, BOME, MEW)
        """
        if winners_entered == 0:
            return 0.0
        elif winners_entered == 1:
            return 50.0
        elif winners_entered == 2:
            return 80.0
        elif winners_entered == 3:
            return 95.0
        else:
            return 100.0

    @staticmethod
    def calculate_selectivity_score(winners_entered: int, total_tokens_bought: int) -> float:
        """
        Selettività (20% peso):
        Regola fondamentale: un wallet che compra 2000 meme coin per trovare 2 winner ha score quasi zero.
        Un wallet che ha comprato 10 token totali e 3 sono stati x100+ ha massima selettività.
        """
        if total_tokens_bought <= 0:
            return 0.0
        
        hit_rate = winners_entered / total_tokens_bought
        
        # Penalizzazione logaritmica per iperattività incontrollata (bot sniper indiscriminati)
        if total_tokens_bought > 1000:
            penalty = 0.05
        elif total_tokens_bought > 300:
            penalty = 0.20
        elif total_tokens_bought > 100:
            penalty = 0.50
        elif total_tokens_bought > 30:
            penalty = 0.80
        else:
            penalty = 1.0

        raw_score = min(100.0, (hit_rate * 100.0) * 4.0) # Se 25% hit rate -> 100 score
        return round(raw_score * penalty, 2)

    @staticmethod
    def calculate_precocity_score(avg_entry_delay_seconds: float) -> float:
        """
        Precocità (15% peso):
        Quanto presto entra rispetto al primo pool liquido.
        < 30 sec: 100 (Sniper/Ultra-early)
        < 180 sec (3 min): 90
        < 600 sec (10 min): 75
        < 1800 sec (30 min): 55
        < 3600 sec (1h): 35
        > 1h: 15
        """
        if avg_entry_delay_seconds <= 30:
            return 100.0
        elif avg_entry_delay_seconds <= 180:
            return 90.0
        elif avg_entry_delay_seconds <= 600:
            return 75.0
        elif avg_entry_delay_seconds <= 1800:
            return 55.0
        elif avg_entry_delay_seconds <= 3600:
            return 35.0
        else:
            return 15.0

    @staticmethod
    def calculate_post_entry_return_score(avg_max_return_x: float) -> float:
        """
        Rendimento post-ingresso (15% peso):
        Performance massima moltiplicatore raggiunta dai token dopo l'ingresso
        """
        if avg_max_return_x >= 500:
            return 100.0
        elif avg_max_return_x >= 100:
            return 90.0
        elif avg_max_return_x >= 20:
            return 70.0
        elif avg_max_return_x >= 5:
            return 45.0
        elif avg_max_return_x >= 2:
            return 25.0
        else:
            return 10.0

    @staticmethod
    def calculate_exit_management_score(exit_efficiency: float) -> float:
        """
        Gestione dell'uscita (10% peso):
        Misura la capacità di monetizzare il profitto rispetto a mantenere fino al crollo (round-trip)
        exit_efficiency tra 0.0 e 1.0 (percentuale di profitto potenziale effettivamente realizzata)
        """
        return min(100.0, max(0.0, exit_efficiency * 100.0))

    @staticmethod
    def calculate_independence_score(cluster_size: int, is_root: bool, is_exchange_funded: bool) -> float:
        """
        Indipendenza (10% peso):
        Se il wallet fa parte di un cluster di 10 wallet sybil, il suo score di indipendenza è basso.
        Se è un wallet autonomo o root con funding chiaro, score elevato.
        """
        if is_exchange_funded:
            return 85.0
        if cluster_size <= 1:
            return 100.0
        elif cluster_size <= 3:
            return 70.0 if is_root else 50.0
        elif cluster_size <= 8:
            return 40.0 if is_root else 25.0
        else:
            return 15.0

    @classmethod
    def compute_smart_wallet_score(cls, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes the complete Smart Wallet Score (0 - 100) using the 6 weighted components
        """
        s_wins = cls.calculate_early_wins_score(metrics.get("winners_entered", 0))
        s_selectivity = cls.calculate_selectivity_score(metrics.get("winners_entered", 0), metrics.get("total_tokens_bought", 1))
        s_precocity = cls.calculate_precocity_score(metrics.get("avg_entry_delay_seconds", 3600))
        s_return = cls.calculate_post_entry_return_score(metrics.get("avg_max_return_x", 1.0))
        s_exit = cls.calculate_exit_management_score(metrics.get("exit_efficiency", 0.5))
        s_indep = cls.calculate_independence_score(
            metrics.get("cluster_size", 1),
            metrics.get("is_cluster_root", True),
            metrics.get("is_exchange_funded", False)
        )

        final_score = (
            s_wins * SCORE_WEIGHTS["early_big_wins"] +
            s_selectivity * SCORE_WEIGHTS["selectivity"] +
            s_precocity * SCORE_WEIGHTS["precocity"] +
            s_return * SCORE_WEIGHTS["post_entry_return"] +
            s_exit * SCORE_WEIGHTS["exit_management"] +
            s_indep * SCORE_WEIGHTS["independence"]
        )

        final_score = round(min(100.0, max(0.0, final_score)), 2)

        return {
            "score": final_score,
            "components": {
                "early_big_wins": round(s_wins, 2),
                "selectivity": round(s_selectivity, 2),
                "precocity": round(s_precocity, 2),
                "post_entry_return": round(s_return, 2),
                "exit_management": round(s_exit, 2),
                "independence": round(s_indep, 2)
            }
        }

    @staticmethod
    def compute_insider_score(metrics: Dict[str, Any]) -> float:
        """
        Computes the separate Insider Score (Section 3.3):
        Identifies entities with systematic structural/deployer privilege
        """
        score = 0.0
        if metrics.get("is_creator_linked", False):
            score += 45.0
        if metrics.get("is_deployer_funded", False):
            score += 30.0
        if metrics.get("has_pre_mint_transfer", False):
            score += 25.0
        if metrics.get("systematic_pre_pump_entry", False):
            score += 20.0
        return min(100.0, round(score, 2))
