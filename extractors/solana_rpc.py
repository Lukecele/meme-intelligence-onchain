"""Async Solana/Helius RPC client with safe fallback and archival helpers."""
import asyncio
import aiohttp
import logging
from typing import Dict, Any, List, Optional
from config.settings import RPC_ENDPOINTS, HELIUS_API_KEY

logger = logging.getLogger(__name__)

class SolanaRPCClient:
    def __init__(self, endpoints: Optional[List[str]] = None, helius_api_key: str = HELIUS_API_KEY):
        self.endpoints = endpoints or RPC_ENDPOINTS
        self.helius_api_key = helius_api_key
        self.current_endpoint_idx = 0
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60))
        return self.session

    @property
    def current_endpoint(self):
        return self.endpoints[self.current_endpoint_idx % len(self.endpoints)]

    def _rotate_endpoint(self):
        self.current_endpoint_idx = (self.current_endpoint_idx + 1) % len(self.endpoints)

    async def call(self, method: str, params: List[Any], max_retries: int = 15, endpoint: Optional[str] = None):
        session = await self._get_session()
        payload = {"jsonrpc":"2.0","id":"1","method":method,"params":params}
        for attempt in range(max_retries):
            target = endpoint or self.current_endpoint
            try:
                async with session.post(target, json=payload) as resp:
                    if resp.status == 429:
                        if endpoint is None: self._rotate_endpoint()
                        # Very slow backoff for 429
                        await asyncio.sleep(2 + attempt * 2)
                        continue
                    if resp.status != 200:
                        if endpoint is None: self._rotate_endpoint()
                        logger.warning("RPC HTTP %s for %s", resp.status, method)
                        await asyncio.sleep(1 + attempt)
                        continue
                    data = await resp.json()
                    if data.get("error"):
                        logger.warning("RPC error %s for %s", data["error"], method)
                        return None
                    return data.get("result")
            except Exception as exc:
                logger.warning("RPC exception for %s: %s", method, exc)
                if endpoint is None: self._rotate_endpoint()
                await asyncio.sleep(1 + attempt)
        return None

    async def get_signatures_for_address(self, address: str, limit: int = 100, before: Optional[str] = None):
        opts: Dict[str,Any] = {"limit": min(max(limit,1),1000)}
        if before: opts["before"] = before
        return await self.call("getSignaturesForAddress", [address, opts]) or []

    async def get_transaction(self, signature: str, encoding: str = "jsonParsed"):
        return await self.call("getTransaction", [signature, {"maxSupportedTransactionVersion":0, "encoding":encoding, "commitment":"finalized"}])

    async def get_parsed_transaction(self, signature: str):
        return await self.get_transaction(signature, "jsonParsed")

    async def get_transactions_for_address(self, address: str, *, limit: int = 100, sort_order: str = "asc",
                                           block_time_gte: Optional[int] = None, block_time_lte: Optional[int] = None,
                                           pagination_token: Optional[str] = None, transaction_details: str = "full",
                                           token_accounts: str = "balanceChanged") -> Dict[str,Any]:
        if not self.helius_api_key:
            raise RuntimeError("HELIUS_API_KEY required for getTransactionsForAddress")
        opts: Dict[str,Any] = {"transactionDetails": transaction_details, "sortOrder": sort_order,
                              "limit": min(limit, 100 if transaction_details == "full" else 1000),
                              "filters": {"status":"succeeded", "tokenAccounts": token_accounts}}
        bt = {}
        if block_time_gte is not None: bt["gte"] = int(block_time_gte)
        if block_time_lte is not None: bt["lte"] = int(block_time_lte)
        if bt: opts["filters"]["blockTime"] = bt
        if pagination_token: opts["paginationToken"] = pagination_token
        endpoint = f"https://mainnet.helius-rpc.com/?api-key={self.helius_api_key}"
        return await self.call("getTransactionsForAddress", [address, opts], endpoint=endpoint) or {"data":[],"paginationToken":None}

    async def get_account_info(self, address: str):
        return await self.call("getAccountInfo", [address, {"encoding":"jsonParsed"}])

    async def get_token_largest_accounts(self, mint: str):
        result = await self.call("getTokenLargestAccounts", [mint])
        return result.get("value",[]) if result else []

    async def get_token_supply(self, mint: str):
        result = await self.call("getTokenSupply", [mint])
        return result.get("value") if result else None

    async def close(self):
        if self.session and not self.session.closed: await self.session.close()
