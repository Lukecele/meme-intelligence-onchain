"""Pyth Hermes price client. Authentication is required from 2026-08-18."""
import aiohttp, logging
from typing import Dict, Any, Optional
from config.settings import PYTH_API_KEY
logger=logging.getLogger(__name__)
PYTH_FEED_IDS={
 "SOL_USD":"ef0d8b6fda2ceba41da15d4095d1da392a0d2f8ed0c6c7bc0f4cfac8c280b56d",
 "BONK_USD":"72b021217ca3fe68922a19aaf990109cb9d84e9ad004b4d20e8c4155b8613717",
 "BTC_USD":"e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43",
 "ETH_USD":"ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace"}
class PythBenchmarkClient:
    def __init__(self, api_key: str=PYTH_API_KEY):
        self.api_key=api_key; self.base_url="https://pyth.dourolabs.app/hermes/api/latest_price_feeds"; self.session=None
    async def _get_session(self):
        if not self.api_key: raise RuntimeError("PYTH_API_KEY not configured")
        if self.session is None or self.session.closed:
            self.session=aiohttp.ClientSession(headers={"Authorization":f"Bearer {self.api_key}"},timeout=aiohttp.ClientTimeout(total=15))
        return self.session
    async def get_price(self, feed_symbol: str="SOL_USD") -> Optional[Dict[str,Any]]:
        feed_id=PYTH_FEED_IDS.get(feed_symbol,feed_symbol); session=await self._get_session()
        async with session.get(self.base_url,params=[("ids[]",feed_id)]) as resp:
            if resp.status!=200:
                logger.warning("Pyth Hermes HTTP %s",resp.status); return None
            data=await resp.json(); row=(data[0] if isinstance(data,list) and data else None)
            if not row: return None
            p=row.get("price",{}); raw=int(p.get("price",0)); expo=int(p.get("expo",0)); conf=int(p.get("conf",0))
            return {"symbol":feed_symbol,"price_usd":raw*(10**expo),"confidence_usd":conf*(10**expo),"publish_timestamp":int(p.get("publish_time",0)),"source_type":"API","source_name":"PYTH_HERMES"}
    async def close(self):
        if self.session and not self.session.closed: await self.session.close()
