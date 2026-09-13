import os
import json
import sqlite3
import urllib.request
import urllib.error
from collections import defaultdict

def load_env():
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                try:
                    k, v = line.strip().split("=", 1)
                    os.environ[k] = v.strip('"\'')
                except: pass
load_env()
rpc_url = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

def rpc_call(method, params):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(rpc_url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode()).get("result")
    except Exception as e:
        print(f"RPC Error: {e}")
        return None

def get_smart_wallets():
    with open("web/src/lib/data.ts", "r") as f:
        import re
        matches = set(re.findall(r'"address":\s*["\']([1-9A-HJ-NP-Za-km-z]{32,44})["\']', f.read()))
        return list(matches)

def parse_swap(tx_info, wallet):
    meta = tx_info.get("meta", {})
    if not meta or meta.get("err"): return None
    
    pre = meta.get("preTokenBalances", [])
    post = meta.get("postTokenBalances", [])
    
    deltas = defaultdict(float)
    for t in pre:
        deltas[f"{t['owner']}_{t['mint']}"] -= float(t.get("uiTokenAmount", {}).get("uiAmount") or 0)
    for t in post:
        deltas[f"{t['owner']}_{t['mint']}"] += float(t.get("uiTokenAmount", {}).get("uiAmount") or 0)
        
    bought_mint = None
    bought_amt = 0
    for k, v in deltas.items():
        owner, mint = k.split("_")
        if owner == wallet and v > 0 and mint != "So11111111111111111111111111111111111111112":
            bought_mint = mint
            bought_amt = v
            
    if bought_mint:
        return bought_mint
    return None

def main():
    wallets = get_smart_wallets()
    print(f"Scanning {len(wallets)} smart wallets...")
    
    # To avoid rate limits and taking 1 hour, we just scan 50 recent txs per wallet
    token_buys = defaultdict(list)
    
    for w in wallets:
        sigs = rpc_call("getSignaturesForAddress", [w, {"limit": 50}])
        if not sigs: continue
        
        # Batch get transactions
        # Since standard RPC doesn't support batch getTransaction easily without a wrapper, 
        # we just get them one by one. But limit to recent 10 to speed up.
        sigs = [s["signature"] for s in sigs[:20]]
        for sig in sigs:
            tx = rpc_call("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
            if tx:
                mint = parse_swap(tx, w)
                if mint:
                    token_buys[mint].append({"wallet": w, "sig": sig})

    convergences = []
    for mint, buys in token_buys.items():
        unique_wallets = set(b["wallet"] for b in buys)
        if len(unique_wallets) >= 2:
            convergences.append({
                "mint": mint,
                "wallets": list(unique_wallets)
            })
            
    print(f"Found {len(convergences)} recent convergences.")
    if convergences:
        for c in convergences:
            print(f"Mint: {c['mint']}, Wallets: {len(c['wallets'])}")
    else:
        print("No convergences found in the very recent blocks.")

if __name__ == "__main__":
    main()
