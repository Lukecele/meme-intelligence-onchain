import urllib.request
import json

def rpc_call(method, params):
    url = "https://api.mainnet-beta.solana.com"
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode()).get("result")
    except: return None

sigs = rpc_call("getSignaturesForAddress", ["Fgy66m7yjq776WTErRNkGgfrPF7fCMfDyMcC8vDMpump", {"limit": 10}])
if sigs:
    for s in sigs:
        print(s.get("blockTime"), s.get("signature"))
