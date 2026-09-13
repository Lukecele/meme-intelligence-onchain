"""Helius client used by the production pipeline.

Historical address scans use the current Helius `getTransactionsForAddress` RPC via
:class:`SolanaRPCClient`.  The legacy Enhanced Transactions REST endpoint is not used
for new historical ingestion.  Webhook registration remains isolated here for the
future live-watch phase.
"""
from __future__ import annotations

import aiohttp
import logging
from typing import Any, Dict, List, Optional

from config.settings import HELIUS_API_KEY
from extractors.solana_rpc import SolanaRPCClient

logger = logging.getLogger(__name__)


class HeliusClient:
    def __init__(self, api_key: str = HELIUS_API_KEY):
        self.api_key = api_key
        self.rpc = SolanaRPCClient(api_key=api_key)
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20))
        return self.session

    async def get_address_transactions(
        self,
        address: str,
        limit: int = 100,
        *,
        sort_order: str = "desc",
        pagination_token: Optional[str] = None,
        block_time_gte: Optional[int] = None,
        block_time_lte: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        if not self.api_key:
            logger.info("Helius API key not configured; address history unavailable.")
            return []
        return await self.rpc.get_transactions_for_address(
            address,
            limit=limit,
            sort_order=sort_order,
            pagination_token=pagination_token,
            block_time_gte=block_time_gte,
            block_time_lte=block_time_lte,
        )

    async def get_enhanced_transactions(
        self, address: str, limit: int = 50, before_signature: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Backward-compatible alias. `before_signature` is retained only for call compatibility.

        Helius getTransactionsForAddress uses its own pagination token; callers that require
        deterministic pagination should use get_address_transactions(..., pagination_token=...).
        """
        return await self.get_address_transactions(
            address,
            limit=limit,
            sort_order="desc",
            pagination_token=None,
        )

    async def register_webhook_for_wallets(
        self, webhook_url: str, wallet_addresses: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Register an Enhanced Helius webhook for an already validated watchlist."""
        if not self.api_key or not webhook_url or not wallet_addresses:
            return None

        session = await self._get_session()
        url = f"https://api.helius.xyz/v0/webhooks?api-key={self.api_key}"
        payload = {
            "webhookURL": webhook_url,
            "transactionTypes": ["SWAP", "TRANSFER"],
            "accountAddresses": wallet_addresses,
            "webhookType": "enhanced",
        }
        try:
            async with session.post(url, json=payload) as resp:
                if resp.status in (200, 201):
                    return await resp.json()
                logger.warning("Helius webhook registration HTTP %s", resp.status)
        except Exception as exc:
            logger.error("Helius webhook registration error: %s", exc)
        return None

    async def close(self) -> None:
        await self.rpc.close()
        if self.session and not self.session.closed:
            await self.session.close()
