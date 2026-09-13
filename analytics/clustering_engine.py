"""
On-Chain Graph Clustering & Syndicate Detection Engine (Section 4)
"""
import networkx as nx
import logging
from typing import Dict, Any, List, Set, Tuple, Optional
from config.settings import KNOWN_EXCHANGES

logger = logging.getLogger(__name__)

class ClusteringEngine:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_funding_relation(self, funder: str, recipient: str, amount_sol: float, tx_hash: str, timestamp: int):
        """
        Adds a funding edge from parent wallet to child wallet
        """
        # If funder is a known CEX, do not cluster as a private syndicate
        is_funder_cex = funder in KNOWN_EXCHANGES
        
        self.graph.add_node(funder, is_cex=is_funder_cex, label=KNOWN_EXCHANGES.get(funder, "Wallet"))
        self.graph.add_node(recipient, is_cex=False, label="Wallet")
        
        self.graph.add_edge(
            funder,
            recipient,
            amount_sol=amount_sol,
            tx_hash=tx_hash,
            timestamp=timestamp,
            relation="FUNDING",
            is_cex_funding=is_funder_cex
        )

    def detect_syndicate_clusters(self) -> List[Dict[str, Any]]:
        """
        Detects connected components where wallets share the same non-CEX parent funder
        or exhibit structural ties
        """
        clusters = []
        cluster_counter = 1

        # Find weakly connected components on subgraph excluding CEX nodes
        non_cex_nodes = [n for n, d in self.graph.nodes(data=True) if not d.get("is_cex", False)]
        subgraph = self.graph.subgraph(non_cex_nodes)

        for comp in nx.weakly_connected_components(subgraph):
            if len(comp) > 1:
                # Find root funder if exists (in-degree == 0 within component)
                comp_sub = subgraph.subgraph(comp)
                roots = [n for n, d in comp_sub.in_degree() if d == 0]
                parent = roots[0] if roots else list(comp)[0]

                cluster_id = f"CLUST_{cluster_counter:04d}"
                cluster_counter += 1

                for member in comp:
                    relation_type = "CLUSTER_ROOT" if member == parent else "DIRECT_FUNDING"
                    confidence = 0.95 if relation_type == "DIRECT_FUNDING" else 0.85

                    clusters.append({
                        "cluster_id": cluster_id,
                        "wallet_address": member,
                        "parent_wallet": parent if member != parent else None,
                        "confidence": confidence,
                        "relation_type": relation_type,
                        "size": len(comp),
                        "members": list(comp)
                    })

        return clusters

    @staticmethod
    def detect_temporal_coordination(trades: List[Dict[str, Any]], window_seconds: int = 30) -> List[Dict[str, Any]]:
        """
        Detects multiple distinct wallets executing buys within tight seconds window (Section 4.1)
        """
        coordinated_events = []
        sorted_trades = sorted([t for t in trades if t.get("side") == "BUY"], key=lambda x: x["timestamp"])

        for i in range(len(sorted_trades)):
            current = sorted_trades[i]
            batch = [current]
            for j in range(i + 1, len(sorted_trades)):
                nxt = sorted_trades[j]
                if nxt["timestamp"] - current["timestamp"] <= window_seconds:
                    if nxt["wallet_address"] != current["wallet_address"]:
                        batch.append(nxt)
                else:
                    break
            
            if len(batch) >= 2:
                wallets_in_batch = list({b["wallet_address"] for b in batch})
                if len(wallets_in_batch) >= 2:
                    coordinated_events.append({
                        "timestamp": current["timestamp"],
                        "token_mint": current["token_mint"],
                        "wallets": wallets_in_batch,
                        "count": len(wallets_in_batch),
                        "window_sec": batch[-1]["timestamp"] - batch[0]["timestamp"]
                    })

        return coordinated_events
