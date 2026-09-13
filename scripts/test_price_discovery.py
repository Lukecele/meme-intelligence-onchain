import asyncio
from extractors.solana_rpc import SolanaRPCClient

async def test_price():
    rpc = SolanaRPCClient()
    mint = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263" # BONK
    launch_ts = 1670531612
    target_ts = launch_ts + 86400 * 7 # 7 days later
    
    page = await rpc.get_transactions_for_address(
        mint, limit=20, sort_order="asc", block_time_gte=target_ts, transaction_details="full"
    )
    
    for tx in page.get("data", []):
        meta = tx.get("meta", {})
        if meta.get("err"): continue
        
        pre_tb = meta.get("preTokenBalances", [])
        post_tb = meta.get("postTokenBalances", [])
        pre_b = meta.get("preBalances", [])
        post_b = meta.get("postBalances", [])
        
        accounts = tx.get("transaction", {}).get("message", {}).get("accountKeys", [])
        if accounts and isinstance(accounts[0], dict):
            accounts = [a.get("pubkey") for a in accounts]
            
        deltas = {}
        for t in pre_tb:
            owner = t.get("owner")
            m = t.get("mint")
            if owner not in deltas: deltas[owner] = {"tokens": {}}
            deltas[owner]["tokens"][m] = -float(t.get("uiTokenAmount", {}).get("uiAmount") or 0)
            
        for t in post_tb:
            owner = t.get("owner")
            m = t.get("mint")
            if owner not in deltas: deltas[owner] = {"tokens": {}}
            if m not in deltas[owner]["tokens"]: deltas[owner]["tokens"][m] = 0
            deltas[owner]["tokens"][m] += float(t.get("uiTokenAmount", {}).get("uiAmount") or 0)
            
        for i, acc in enumerate(accounts):
            if acc not in deltas: deltas[acc] = {"tokens": {}}
            sol_delta = (post_b[i] - pre_b[i]) / 1e9 if i < len(pre_b) else 0
            deltas[acc]["sol"] = sol_delta
            
        WSOL = "So11111111111111111111111111111111111111112"
        USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        
        for owner, data in deltas.items():
            bonk_delta = data["tokens"].get(mint, 0)
            wsol_delta = data["tokens"].get(WSOL, 0)
            usdc_delta = data["tokens"].get(USDC, 0)
            sol_delta = data.get("sol", 0)
            
            if bonk_delta > 0:
                cost_sol = abs(wsol_delta) if wsol_delta < -0.001 else (abs(sol_delta) if sol_delta < -0.001 else 0)
                cost_usdc = abs(usdc_delta) if usdc_delta < -0.01 else 0
                
                if cost_sol > 0:
                    price_in_sol = cost_sol / bonk_delta
                    print(f"Found Swap at {tx.get('blockTime')}: Bought {bonk_delta} BONK for {cost_sol} SOL. Price: {price_in_sol:.12f} SOL/BONK")
                    await rpc.close()
                    return
                elif cost_usdc > 0:
                    price_in_usdc = cost_usdc / bonk_delta
                    print(f"Found Swap at {tx.get('blockTime')}: Bought {bonk_delta} BONK for {cost_usdc} USDC. Price: {price_in_usdc:.12f} USDC/BONK")
                    await rpc.close()
                    return

    await rpc.close()
    print("No clear swap found.")

if __name__ == "__main__":
    asyncio.run(test_price())
