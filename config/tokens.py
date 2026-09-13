"""Research cohort configuration.
Only token mint identities are preconfigured here. Launch slot/time, first pool,
initial liquidity and historical returns must be populated from verifiable data
before they are used by scoring or validation.
"""
HISTORICAL_WINNERS = [
    {"symbol":"BONK","name":"Bonk","mint":"DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263","launch_time":"","launch_timestamp":1670531612,"first_pool":"","initial_liquidity_usd":0.0,"peak_mcap_usd":0.0,"max_return_x":0.0,"has_airdrop":True,"metadata_status":"REQUIRES_VERIFICATION"},
    {"symbol":"WIF","name":"dogwifhat","mint":"EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm","launch_time":"","launch_timestamp":1700508163,"first_pool":"","initial_liquidity_usd":0.0,"peak_mcap_usd":0.0,"max_return_x":0.0,"has_airdrop":False,"metadata_status":"REQUIRES_VERIFICATION"},
    {"symbol":"POPCAT","name":"Popcat","mint":"7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr","launch_time":"","launch_timestamp":1702413767,"first_pool":"","initial_liquidity_usd":0.0,"peak_mcap_usd":0.0,"max_return_x":0.0,"has_airdrop":False,"metadata_status":"REQUIRES_VERIFICATION"},
    {"symbol":"BOME","name":"BOOK OF MEME","mint":"ukHH6c7mMyPWCf1b9pnWe25TSpkDDt3H5pQZgZ74J82","launch_time":"","launch_timestamp":1710403337,"first_pool":"","initial_liquidity_usd":0.0,"peak_mcap_usd":0.0,"max_return_x":0.0,"has_airdrop":False,"metadata_status":"REQUIRES_VERIFICATION"},
    {"symbol":"MEW","name":"cat in a dogs world","mint":"MEW1gQWJ3nEXg2qgERiKu7FAFj79PHvQVREQUzScPP5","launch_time":"","launch_timestamp":1711430139,"first_pool":"","initial_liquidity_usd":0.0,"peak_mcap_usd":0.0,"max_return_x":0.0,"has_airdrop":False,"metadata_status":"REQUIRES_VERIFICATION"},
]

# IMPORTANT: matched controls must be selected and frozen ex ante from real Solana tokens.
CONTROL_GROUP_TOKENS = [
    {"symbol":"GLIN","name":"Glin Meme","mint":"BPuNpj7eqg8R2z8jGxJqWZqxqoVritGsFpHTsNLHpump","launch_timestamp":1787115611},
    {"symbol":"GROKB","name":"Grok Butt","mint":"A4GoNqSZTvX4sSnRE1wFjEkemWm8jmbHhLgyCBAkpump","launch_timestamp":1787115185},
    {"symbol":"AZ007","name":"Agent Z007","mint":"3LH7pDMG6maRkpHfQdN6hV36D6geFckDp7vTNDYTpump","launch_timestamp":1787114906},
    {"symbol":"TRUMPCLUG","name":"Trump Clug","mint":"5E8ifewWjdGPDCRdmvbua3YvV1QzjiZs63qJYwuFpump","launch_timestamp":1787112398},
    {"symbol":"QBULL","name":"Qbull Meme","mint":"8sxdRtLdtaYdHis1VSkCJoZUNVZXiaEKEUomzPRTpump","launch_timestamp":1787088036}
]

PROGRAMS = {
    "SYSTEM_PROGRAM":"11111111111111111111111111111111",
    "TOKEN_PROGRAM":"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "ASSOCIATED_TOKEN_PROGRAM":"ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
}
