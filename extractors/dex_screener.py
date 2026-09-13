"""
DexScreener and Free Market Data API Extractor for Solana Meme Coins
"""
import aiohttp
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DexScreenerClient:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex"
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))
        return self.session

    async def get_token_pairs(self, token_address: str) -> List[Dict[str, Any]]:
        session = await self._get_session()
        url = f"{self.base_url}/tokens/{token_address}"
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    pairs = data.get("pairs") or []
                    # Filter for Solana pairs only
                    return [p for p in pairs if p.get("chainId") == "solana"]
                else:
                    logger.warning(f"DexScreener HTTP {resp.status} for {token_address}")
        except Exception as e:
            logger.error(f"DexScreener API error for {token_address}: {e}")
        return []

    async def get_latest_token_profiles(self) -> List[Dict[str, Any]]:
        session = await self._get_session()
        url = "https://api.dexscreener.com/token-profiles/latest/v1"
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        return [t for t in data if t.get("chainId") == "solana"]
        except Exception as e:
            logger.error(f"DexScreener latest profiles error: {e}")
        return []

    async def get_latest_boosted_tokens(self) -> List[Dict[str, Any]]:
        session = await self._get_session()
        url = "https://api.dexscreener.com/token-boosts/latest/v1"
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        return [t for t in data if t.get("chainId") == "solana"]
        except Exception as e:
            logger.error(f"DexScreener latest boosts error: {e}")
        return []

    async def get_token_summary(self, token_address: str) -> Optional[Dict[str, Any]]:
        pairs = await self.get_token_pairs(token_address)
        if not pairs:
            return None
        
        # Sort by liquidity descending to pick the main pool
        pairs.sort(key=lambda p: float((p.get("liquidity") or {}).get("usd") or 0.0), reverse=True)
        main_pair = pairs[0]

        liq_usd = float((main_pair.get("liquidity") or {}).get("usd") or 0.0)
        fdv = float(main_pair.get("fdv") or main_pair.get("marketCap") or 0.0)
        price_usd = float(main_pair.get("priceUsd") or 0.0)
        pair_created_at = main_pair.get("pairCreatedAt", 0) # ms timestamp
        dex_id = main_pair.get("dexId", "unknown")
        pair_address = main_pair.get("pairAddress", "")

        txns = main_pair.get("txns", {})
        volume = main_pair.get("volume", {})

        return {
            "mint": token_address,
            "symbol": main_pair.get("baseToken", {}).get("symbol", ""),
            "name": main_pair.get("baseToken", {}).get("name", ""),
            "price_usd": price_usd,
            "liquidity_usd": liq_usd,
            "fdv_usd": fdv,
            "market_cap_usd": fdv,
            "dex_id": dex_id,
            "pair_address": pair_address,
            "created_timestamp_ms": pair_created_at,
            "created_timestamp_sec": pair_created_at // 1000 if pair_created_at else 0,
            "txns_24h": (txns.get("h24") or {}),
            "volume_24h": volume.get("h24", 0.0),
            "price_change_24h": (main_pair.get("priceChange") or {}).get("h24", 0.0)
        }

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
