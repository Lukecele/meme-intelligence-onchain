"""Birdeye client for first buyers, funding provenance and holder distribution."""
import aiohttp, logging
from typing import Dict, Any, List, Optional
from config.settings import BIRDEYE_API_KEY
logger=logging.getLogger(__name__)

class BirdeyeClient:
    def __init__(self, api_key: str = BIRDEYE_API_KEY):
        self.api_key=api_key; self.base_url="https://public-api.birdeye.so"; self.session=None
    def _require_key(self):
        if not self.api_key: raise RuntimeError("BIRDEYE_API_KEY not configured")
    async def _get_session(self):
        self._require_key()
        if self.session is None or self.session.closed:
            self.session=aiohttp.ClientSession(headers={"X-API-KEY":self.api_key,"accept":"application/json","x-chain":"solana"}, timeout=aiohttp.ClientTimeout(total=30))
        return self.session
    async def get_token_first_buyers(self, token_address: str, limit: int=1000) -> List[Dict[str,Any]]:
        session=await self._get_session(); out=[]; wanted=min(max(limit,1),1000)
        for offset in range(0,wanted,100):
            page_limit=min(100,wanted-offset)
            async with session.get(f"{self.base_url}/token/v1/first-buyers", params={"token_address":token_address,"offset":offset,"limit":page_limit}) as resp:
                if resp.status != 200:
                    logger.warning("Birdeye first-buyers HTTP %s", resp.status); break
                payload=await resp.json(); data=payload.get("data") or {}; items=data.get("items") or data.get("list") or []
                if not items: break
                for idx,item in enumerate(items):
                    out.append({
                        "wallet_address": item.get("wallet") or item.get("wallet_address") or item.get("owner") or item.get("address"),
                        "rank": item.get("rank") or offset+idx+1,
                        "first_buy_time": item.get("first_buy_time") or item.get("block_time") or item.get("blockTime"),
                        "first_buy_volume": item.get("first_buy_volume"),
                        "first_buy_volume_usd": item.get("first_buy_volume_usd"),
                        "initial_holding": item.get("initial_holding"),
                        "current_holding": item.get("current_holding"),
                        "position_status": item.get("position_status"),
                        "tags": item.get("tags") or [],
                        "raw": item,
                        "source_type":"API", "source_name":"BIRDEYE_FIRST_BUYERS"
                    })
                if len(items)<page_limit: break
            import asyncio; await asyncio.sleep(1.1)
        return [x for x in out if x.get("wallet_address")]
    async def get_wallets_first_funded(self, wallets: List[str], token_address: Optional[str]=None) -> List[Dict[str,Any]]:
        session=await self._get_session(); out=[]
        for i in range(0,len(wallets),50):
            body={"wallets":wallets[i:i+50]}
            if token_address: body["token_address"]=token_address
            async with session.post(f"{self.base_url}/wallet/v2/tx/first-funded", json=body) as resp:
                if resp.status!=200:
                    logger.warning("Birdeye first-funded HTTP %s",resp.status); continue
                payload=await resp.json(); data=payload.get("data") or []
                if isinstance(data,dict): data=data.get("items") or data.get("list") or [data]
                out.extend(data)
        return out
    async def get_wallet_first_funded_tx(self, wallet_address: str):
        rows=await self.get_wallets_first_funded([wallet_address]); return rows[0] if rows else None
    async def get_holder_distribution(self, token_address: str, top_n: int=10):
        session=await self._get_session()
        params={"token_address":token_address,"address_type":"wallet","mode":"top","top_n":min(max(top_n,1),10000),"include_list":"true","offset":0,"limit":min(top_n,50)}
        async with session.get(f"{self.base_url}/holder/v1/distribution",params=params) as resp:
            if resp.status!=200: return {}
            return (await resp.json()).get("data") or {}
    async def close(self):
        if self.session and not self.session.closed: await self.session.close()
