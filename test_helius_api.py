import os
import requests
import json

def load_env():
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                try:
                    k, v = line.strip().split("=", 1)
                    os.environ[k] = v.strip('"\'')
                except: pass
load_env()
api_key = os.environ.get("HELIUS_API_KEY")

wallet = "7cnvQ77FDhVo8PZ8NqDn51qo5YJ4NLzR8zkiYH8DouZN"
url = f"https://api.helius.xyz/v0/addresses/{wallet}/transactions?api-key={api_key}&type=SWAP&limit=1"

res = requests.get(url)
if res.ok:
    data = res.json()
    if data:
        print(json.dumps(data[0], indent=2))
else:
    print(res.text)
