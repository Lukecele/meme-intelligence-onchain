"""Disabled in production: the 25k BONK generator produced synthetic addresses.
A real BONK airdrop reconstruction must ingest on-chain transfer records from the verified distributor(s).
"""
def main():
    raise RuntimeError("Synthetic BONK airdrop generation is disabled. Provide verified distributor address(es) and ingest on-chain transfers.")
if __name__ == "__main__": main()
