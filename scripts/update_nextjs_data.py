import json, re
from pathlib import Path
ROOT = Path("/home/luca/meme-intelligence-onchain")
smart_wallets_json = ROOT / "data/smart_wallets.json"
data_ts = ROOT / "web/src/lib/data.ts"
with open(smart_wallets_json) as f: wallets = json.load(f)
with open(data_ts, "r") as f: content = f.read()
wallets_str = json.dumps(wallets, indent=2)
content = re.sub(r'export const SMART_WALLETS: WalletProfile\[\] = \[.*?\];', f'export const SMART_WALLETS: WalletProfile[] = {wallets_str};', content, flags=re.DOTALL)
with open(data_ts, "w") as f: f.write(content)
