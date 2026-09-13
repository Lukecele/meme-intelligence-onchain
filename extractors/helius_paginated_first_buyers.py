"""Helius archival transaction helper for launch-window verification.
This module does not classify every transaction as a buyer. It only exports raw chronological
transactions; semantic BUY classification must use pre/post token/quote balance deltas.
"""
import asyncio,json
from extractors.solana_rpc import SolanaRPCClient
async def fetch_launch_window(address:str,start_ts:int,end_ts:int,limit_pages:int=20):
    c=SolanaRPCClient();out=[];token=None
    try:
        for _ in range(limit_pages):
            page=await c.get_transactions_for_address(address,limit=100,sort_order='asc',block_time_gte=start_ts,block_time_lte=end_ts,pagination_token=token,transaction_details='full')
            rows=page.get('data') or [];out.extend(rows);token=page.get('paginationToken')
            if not token or not rows: break
        return out
    finally: await c.close()
if __name__=='__main__':
    raise SystemExit('Import fetch_launch_window() from this module with a verified launch window.')
