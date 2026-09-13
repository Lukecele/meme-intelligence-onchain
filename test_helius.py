import asyncio
import os
import aiohttp

def load_env():
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ[k] = v.strip('"\'')
load_env()
api_key = os.environ.get("HELIUS_API_KEY")

async def main():
    async with aiohttp.ClientSession() as session:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransactionsForAddress",
            "params": [
                "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",
                {"limit": 50, "sortOrder": "asc"}
            ]
        }
        async with session.post(f"https://mainnet.helius-rpc.com/?api-key={api_key}", json=payload) as res:
            print("Status:", res.status)
            data = await res.json()
            if "error" in data:
                print("Error:", data["error"])
            else:
                print("Result type:", type(data.get("result")))
                if isinstance(data.get("result"), dict):
                    print("Keys:", data.get("result").keys())
                    print("Number of txs:", len(data.get("result").get("data", [])))

asyncio.run(main())
