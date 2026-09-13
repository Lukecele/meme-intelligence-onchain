import urllib.request
import json
import time

def rpc_call(method, params):
    url = "https://api.mainnet-beta.solana.com"
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode()).get("result")
    except Exception as e: 
        print(e)
        return None

tx = rpc_call("getTransaction", ["2JZrpnoy8h2zrgcrGSkqqdFgUh8rUprgK2g3EbJ16owAwPEbRM31kfXikmhGY9hyPxFUwktKPENaybN1qcc6bWp9", {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
if tx:
    meta = tx.get("meta", {})
    pre_b = meta.get("preBalances", [])
    post_b = meta.get("postBalances", [])
    account_keys = [a["pubkey"] if isinstance(a, dict) else a for a in tx["transaction"]["message"]["accountKeys"]]
    
    print("Fee payer:", account_keys[0])
    for i, acc in enumerate(account_keys):
        delta = (post_b[i] - pre_b[i]) / 1e9
        if abs(delta) > 0.001:
            print(f"Account {acc} changed by {delta} SOL")
            
    print("Log messages:")
    for log in meta.get("logMessages", []):
        print(" ", log)
