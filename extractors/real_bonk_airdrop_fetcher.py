"""BONK airdrop reconstruction from explicitly verified distributor addresses.

Safety rule: a BONK receipt is never called an airdrop merely because it occurred
early. The transaction must contain a BONK balance decrease owned by one of the
operator-supplied verified distributor wallets and one or more corresponding
recipient increases. Configure distributors with BONK_AIRDROP_DISTRIBUTORS as a
comma-separated list after independent verification.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

from config.settings import DATA_DIR, HELIUS_API_KEY
from db.database import Database
from extractors.solana_rpc import SolanaRPCClient

logger = logging.getLogger(__name__)


def _ui(row: Dict[str, Any]) -> float:
    u=row.get("uiTokenAmount") or {}
    try:return float(u.get("uiAmount") if u.get("uiAmount") is not None else u.get("uiAmountString") or 0)
    except (TypeError,ValueError):return 0.0


class RealBonkAirdropFetcher:
    BONK_MINT="DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    def __init__(self, distributors: Optional[List[str]]=None):
        self.db=Database(DATA_DIR/"onchain_intelligence.db")
        self.rpc=SolanaRPCClient()
        env=[x.strip() for x in os.getenv("BONK_AIRDROP_DISTRIBUTORS","").split(",") if x.strip()]
        self.distributors=set(distributors or env)

    async def close(self): await self.rpc.close()

    @staticmethod
    def _map(rows):
        out={}
        for r in rows or []:
            owner,mint=r.get("owner"),r.get("mint")
            if owner and mint:out[(owner,mint)]=out.get((owner,mint),0.0)+_ui(r)
        return out

    def _parse_airdrop_events(self, tx: Dict[str,Any]) -> List[Dict[str,Any]]:
        meta=tx.get("meta") or {}
        if meta.get("err"):return []
        pre=self._map(meta.get("preTokenBalances") or []); post=self._map(meta.get("postTokenBalances") or [])
        # At least one verified distributor must lose BONK in this tx.
        distributor_loss=sum(max(0.0,pre.get((d,self.BONK_MINT),0.0)-post.get((d,self.BONK_MINT),0.0)) for d in self.distributors)
        if distributor_loss<=0:return []
        owners={o for o,m in set(pre)|set(post) if m==self.BONK_MINT and o not in self.distributors}
        events=[]
        for owner in owners:
            delta=post.get((owner,self.BONK_MINT),0.0)-pre.get((owner,self.BONK_MINT),0.0)
            if delta>0:events.append({"wallet":owner,"amount_tokens":delta})
        # Reject impossible accounting rather than invent an allocation explanation.
        if sum(e["amount_tokens"] for e in events)>distributor_loss*1.000001:
            return []
        return events

    async def run(self, max_transactions_per_distributor:int=100000) -> int:
        if not HELIUS_API_KEY:raise RuntimeError("HELIUS_API_KEY required")
        if not self.distributors:
            raise RuntimeError("BONK_AIRDROP_DISTRIBUTORS is empty. Supply independently verified distributor addresses; do not infer airdrops from early receipts.")
        inserted=0
        for distributor in sorted(self.distributors):
            pagination=None; processed=0
            while processed<max_transactions_per_distributor:
                page=await self.rpc.get_transactions_for_address(distributor,limit=100,sort_order="asc",transaction_details="full",pagination_token=pagination)
                txs=page.get("data") or []; pagination=page.get("paginationToken")
                if not txs:break
                # One SQLite writer/transaction per API page. Avoid nested writes through
                # Database.upsert_wallet while this connection holds a write lock.
                with self.db.get_connection() as conn:
                    for tx in txs:
                        processed+=1; sig=(tx.get("transaction") or {}).get("signatures", [None])[0]; ts=int(tx.get("blockTime") or 0)
                        if not sig or ts<=0:continue
                        for ev in self._parse_airdrop_events(tx):
                            conn.execute("""INSERT OR IGNORE INTO wallets(address,first_seen_timestamp,score_status,activity_coverage_status,exit_metric_status,is_eligible_smart_signal,notes)
                                VALUES(?,?,?)""",
                                (ev["wallet"],ts,"BONK airdrop recipient from verified distributor"))
                            cur=conn.execute("""INSERT OR IGNORE INTO airdrop_claims(wallet_address,token_mint,amount_claimed,claim_timestamp,cohort,source_type,source_name,source_ref,notes)
                                VALUES(?,?,?,?,?,'ONCHAIN','HELIUS_VERIFIED_DISTRIBUTOR',?,?)""",
                                (ev["wallet"],self.BONK_MINT,ev["amount_tokens"],ts,"UNSEGMENTED",sig,f"Distributor={distributor}"))
                            inserted+=max(cur.rowcount,0)
                            print(f"Inserted {inserted} events so far...", flush=True)
                    conn.commit()
                if not pagination:break
                await asyncio.sleep(0.1)
        print(f"Imported {inserted} BONK recipient events from {len(self.distributors)} explicitly verified distributor(s).")
        return inserted

async def main():
    f=RealBonkAirdropFetcher()
    try:await f.run()
    finally:await f.close()
if __name__=="__main__":asyncio.run(main())
