"""
Token Risk Filter Pipeline (Section 5.2)
"""
import logging
from typing import Dict, Any, List, Tuple
from config.settings import (
    MAX_TOP10_SUPPLY_PCT, MAX_CREATOR_SUPPLY_PCT,
    MIN_INITIAL_LIQUIDITY_USD, MAX_INITIAL_MCAP_USD
)

logger = logging.getLogger(__name__)

class RiskFilter:
    """
    Evaluates token risk parameters to eliminate rugs, honeypots, and toxic distributions
    """

    @classmethod
    def evaluate_token_risk(cls, token_meta: Dict[str, Any], top_holders: List[Dict[str, Any]] = None) -> Tuple[bool, List[str], float]:
        """
        Returns: (is_safe: bool, risk_flags: List[str], safety_score: float)
        """
        risk_flags = []
        safety_score = 100.0

        mcap = float(token_meta.get("market_cap_usd") or token_meta.get("fdv_usd") or 0.0)
        liq = float(token_meta.get("liquidity_usd") or 0.0)
        mint_authority = token_meta.get("mint_authority")
        freeze_authority = token_meta.get("freeze_authority")
        creator_pct = float(token_meta.get("creator_concentration_pct") or 0.0)

        # 1. Liquidity Depth Check
        if liq < MIN_INITIAL_LIQUIDITY_USD:
            risk_flags.append(f"LIQUIDITA_CRITICA: ${liq:,.0f} < ${MIN_INITIAL_LIQUIDITY_USD:,.0f}")
            safety_score -= 30.0

        # 2. Market Cap Ceiling for Early Microcap
        if mcap > MAX_INITIAL_MCAP_USD:
            risk_flags.append(f"MCAP_TROPPO_ELEVATA: ${mcap:,.0f} > ${MAX_INITIAL_MCAP_USD:,.0f} (Non più micro-cap)")
            safety_score -= 15.0

        # 3. Mint Authority Check
        if mint_authority is not None and mint_authority != "" and mint_authority != "11111111111111111111111111111111":
            risk_flags.append("MINT_AUTHORITY_ATTIVA: Il creator può mintare supply illimitata")
            safety_score -= 40.0

        # 4. Freeze Authority Check
        if freeze_authority is not None and freeze_authority != "":
            risk_flags.append("FREEZE_AUTHORITY_ATTIVA: Possibile Honeypot / blocco trasferimenti")
            safety_score -= 40.0

        # 5. Creator Concentration Check
        if creator_pct > MAX_CREATOR_SUPPLY_PCT:
            risk_flags.append(f"CONCENTRAZIONE_CREATOR_ELEVATA: {creator_pct:.1f}% > {MAX_CREATOR_SUPPLY_PCT}%")
            safety_score -= 25.0

        # 6. Top 10 Holders Concentration Check
        if top_holders:
            top10_sum = sum(float(h.get("uiAmount", 0.0) or h.get("pct", 0.0)) for h in top_holders[:10])
            if top10_sum > MAX_TOP10_SUPPLY_PCT:
                risk_flags.append(f"TOP10_SUPPLY_CONCENTRATION: {top10_sum:.1f}% > {MAX_TOP10_SUPPLY_PCT}%")
                safety_score -= 20.0

        safety_score = max(0.0, safety_score)
        is_safe = safety_score >= 50.0 and not any(flag.startswith("FREEZE_AUTHORITY_ATTIVA") for flag in risk_flags)

        return is_safe, risk_flags, safety_score
