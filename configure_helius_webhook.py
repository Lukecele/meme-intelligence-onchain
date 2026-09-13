#!/usr/bin/env python3
import json
import re
import os
import urllib.request
import urllib.error

def load_env():
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    key, val = line.split("=", 1)
                    os.environ[key] = val.replace('"', '').replace("'", "")
                except:
                    pass

load_env()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
WEBHOOK_URL = "https://web-lovat-eight-11.vercel.app/api/webhook"

def get_smart_wallets():
    with open("web/src/lib/data.ts", "r") as f:
        content = f.read()
    
    matches = set(re.findall(r'"address":\s*["\']([1-9A-HJ-NP-Za-km-z]{32,44})["\']', content))
    return list(matches)

def do_request(url, method="GET", payload=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.read().decode()}")
        return None

def main():
    wallets = get_smart_wallets()
    if not wallets:
        print("No wallets found.")
        return
        
    print(f"Found {len(wallets)} smart wallets.")
    
    get_url = f"https://api.helius.xyz/v0/webhooks?api-key={HELIUS_API_KEY}"
    existing_webhooks = do_request(get_url) or []
    
    payload = {
        "webhookURL": WEBHOOK_URL,
        "transactionTypes": ["SWAP", "ANY"],
        "accountAddresses": wallets,
        "webhookType": "enhanced"
    }
    
    my_webhook_id = None
    for wh in existing_webhooks:
        if wh.get("webhookURL") == WEBHOOK_URL:
            my_webhook_id = wh.get("webhookID")
            break
            
    if my_webhook_id:
        print(f"Updating existing webhook {my_webhook_id}...")
        put_url = f"https://api.helius.xyz/v0/webhooks/{my_webhook_id}?api-key={HELIUS_API_KEY}"
        res = do_request(put_url, "PUT", payload)
        print("Updated successfully!" if res else "Failed to update.")
    else:
        print("Creating new webhook...")
        post_url = f"https://api.helius.xyz/v0/webhooks?api-key={HELIUS_API_KEY}"
        res = do_request(post_url, "POST", payload)
        print("Created successfully!" if res else "Failed to create.")

if __name__ == "__main__":
    main()
