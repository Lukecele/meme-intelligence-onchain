import { WalletProfile, ClusterInfo, TokenMeta } from "../types";
// Historical token metadata is reference metadata only; it is not validation evidence.
export const HISTORICAL_TOKENS: TokenMeta[] = [
 {mint:"DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",symbol:"BONK",name:"Bonk",launchTime:"2022-12-25",initialLiquidityUsd:0,peakMcapUsd:0,maxReturnX:0,isWinner:true,isControl:false,hasAirdrop:true},
 {mint:"EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",symbol:"WIF",name:"dogwifhat",launchTime:"2023-11-20",initialLiquidityUsd:0,peakMcapUsd:0,maxReturnX:0,isWinner:true,isControl:false,hasAirdrop:false},
 {mint:"7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr",symbol:"POPCAT",name:"Popcat",launchTime:"2023-12-13",initialLiquidityUsd:0,peakMcapUsd:0,maxReturnX:0,isWinner:true,isControl:false,hasAirdrop:false},
];
export const SMART_WALLETS: WalletProfile[] = [
  {
    "address": "7cnvQ77FDhVo8PZ8NqDn51qo5YJ4NLzR8zkiYH8DouZN",
    "label": "Smart Wallet 7cnv",
    "smartScore": 86.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 1683.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 55.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "7gxMAbLoNgaNp9nrTbzZXbHRHzd1j4cyZf88KA3NxLRL",
    "label": "Smart Wallet 7gxM",
    "smartScore": 86.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 1683.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 55.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "GnZfegAFEPbgrhX1Z7uK4cQbwps7Rn5xMaecTToLn1WW",
    "label": "Smart Wallet GnZf",
    "smartScore": 86.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 1710.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 55.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "3DNKTCDRqaWQ99P1ugE9v5ApedSPZR7XK8YtqYJ7wHpf",
    "label": "Smart Wallet 3DNK",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2593.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "3rifrbSvsd2YMydAD9sg4yuGsPPVrW8KZLVnFg64tQNr",
    "label": "Smart Wallet 3rif",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2891.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "6CxLREB6VbQarG9LgorHuJTTb8xZLHpBqrQPGHUkb4J1",
    "label": "Smart Wallet 6CxL",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2677.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "8PR9KLjM8ugQXnghBRbEpJCRk9SFD9SoZu32d4rNdzqr",
    "label": "Smart Wallet 8PR9",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 3540.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "9q667SDd7s5rLWRWaySH6Qx7fiPi1keXtH7mZdHWJZVB",
    "label": "Smart Wallet 9q66",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 3533.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "ALmfCk6AtsMTpfoCp11mjcGnDyJcVayux5EURRAaTjDd",
    "label": "Smart Wallet ALmf",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2820.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "BMtsc9tnawZMEwH7iMtYmz4sBmY1KVmCGFWXB7xDj2Z",
    "label": "Smart Wallet BMts",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 1866.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "BzVMozq6s3uHXfRrRcFYxbdFf65q1r9nUbK9B45RDVhc",
    "label": "Smart Wallet BzVM",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2513.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "C1Y95WKh2UGt3Q8162XiQ2ak2FdM31NWbLwpw3LHUEYQ",
    "label": "Smart Wallet C1Y9",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2591.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "DMMuujNm4NgvbVdywJaSY1VmeowvbAeZt2YyQBUZQBuk",
    "label": "Smart Wallet DMMu",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2554.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "EdAFyo6v5uGxinTrzN1BBFUxMfnVDME883VnwmwquJS",
    "label": "Smart Wallet EdAF",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 1809.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "G2scoC5Ey3UyGdrfmtRsdvLHTacfH4yaSwGKs1tSEFxw",
    "label": "Smart Wallet G2sc",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2676.0,
    "avgPostEntryReturn": 1574.0710143216045,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "MEW"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "HZkjpXnvXCtMgoZJubzvksG2GstaUNWXoBTSt5sA6x5e",
    "label": "Smart Wallet HZkj",
    "smartScore": 83.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 3539.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1",
    "label": "Smart Wallet 5Q54",
    "smartScore": 80.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 357848.25,
    "avgPostEntryReturn": 1091.052797302747,
    "exitEfficiency": 30.0,
    "totalTokensBought": 4,
    "totalWinnersEntered": 4,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "POPCAT",
      "MEW",
      "BONK",
      "WIF"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 100.0,
      "precocity": 15.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "5Re17wLyFS8wQQN4mVpaWqSTPHfS5fGF4vEWmSVQ5cDE",
    "label": "Smart Wallet 5Re1",
    "smartScore": 80.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 730334.0,
    "avgPostEntryReturn": 608.0345802838895,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "BONK",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 15.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "AcBvyRVZJduyASUhhtyFzEuvSxSfAMBeRdW9t3Ajjdug",
    "label": "Smart Wallet AcBv",
    "smartScore": 80.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 1595.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 55.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "Dmv8iWkSozgM61UBpVEkkdwfgwEeKdubVHuEAGdBKBFm",
    "label": "Smart Wallet Dmv8",
    "smartScore": 80.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 729637.0,
    "avgPostEntryReturn": 1891.5188203574162,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "BONK",
      "WIF"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 15.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "EckLsguuHRGcwbbxwzjf97VEiWousakMvUH3cYmdc2XK",
    "label": "Smart Wallet EckL",
    "smartScore": 80.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 1152.0,
    "avgPostEntryReturn": 1574.0710143216045,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "MEW"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 55.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "F9zBzytuqdra4ajHZeZY3sJoVTSoApPeyA5LyYiwLN3P",
    "label": "Smart Wallet F9zB",
    "smartScore": 80.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 759429.0,
    "avgPostEntryReturn": 1891.5188203574162,
    "exitEfficiency": 90.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "BONK",
      "WIF"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 15.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 90.0,
      "independence": 100.0
    }
  },
  {
    "address": "J4WuTaRot2cXd87jykjHFQ95zofYhwQ3RLCxHKwhJCUM",
    "label": "Smart Wallet J4Wu",
    "smartScore": 80.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 1600.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "POPCAT",
      "WIF"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 55.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "REDBUt2A3xz2jpncmJ4LyvEVHZYwRGPwyLAhtiskKSk",
    "label": "Smart Wallet REDB",
    "smartScore": 80.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 1595.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 55.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "54mhnkCKNyAzf1TvS25sUTytvwFkqYKkWsC2kNirafaH",
    "label": "Smart Wallet 54mh",
    "smartScore": 77.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2656.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "6LadVodRwFHmtuFV7vSdQSDWhKo651B3o3hsyLW8pze6",
    "label": "Smart Wallet 6Lad",
    "smartScore": 77.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2132.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "8wGoELqsopxr4v1VKuRUdTE9k4n97BP9Nxc3cwvo2FPE",
    "label": "Smart Wallet 8wGo",
    "smartScore": 77.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 3100.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "9WmjHX36ALYVigbT1StPRn8iAxUUWEAMpmo8DvqiGWLz",
    "label": "Smart Wallet 9Wmj",
    "smartScore": 77.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2704.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "EqY79m8W7HouAvrTmjJJdsF6f1CbNRhEJa5f3AdrpP2Z",
    "label": "Smart Wallet EqY7",
    "smartScore": 77.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2576.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "F3d8ZhqSfwDwfBC3P7CFBcn8QwoBBocDBZDoJjs8pcz3",
    "label": "Smart Wallet F3d8",
    "smartScore": 77.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 3099.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "GyWDFgRbYeefQr8k7EPn9mzcMNFvKWdQLkokVqujGQeW",
    "label": "Smart Wallet GyWD",
    "smartScore": 77.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 3515.5,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "J8m3e5G7c77rj13H1zSPXExUvtzMLSyqq1i94duvwLz2",
    "label": "Smart Wallet J8m3",
    "smartScore": 77.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 2772.0,
    "avgPostEntryReturn": 1823.3443504683355,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "WIF",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 35.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  },
  {
    "address": "9WN3qbWie94fnst9rmSe1N71XTy6dKeA7FcycRLtvAYa",
    "label": "Smart Wallet 9WN3",
    "smartScore": 74.25,
    "independenceScore": 100.0,
    "selectivityScore": 100.0,
    "precocityAvgSec": 758659.0,
    "avgPostEntryReturn": 608.0345802838895,
    "exitEfficiency": 30.0,
    "totalTokensBought": 2,
    "totalWinnersEntered": 2,
    "fundingSource": "ONCHAIN",
    "hitTokens": [
      "BONK",
      "POPCAT"
    ],
    "controlTokens": [],
    "scoreBreakdown": {
      "earlyBigWins": 80.0,
      "precocity": 15.0,
      "selectivity": 100.0,
      "postEntryReturn": 100.0,
      "exitManagement": 30.0,
      "independence": 100.0
    }
  }
];
export const CLUSTERS: ClusterInfo[] = [];
  {
    "clusterId": "CLUST_8921",
    "rootAddress": "3DNKTCDRqaWQ99P1ugE9v5ApedSPZR7XK8YtqYJ7wHpf",
    "members": [
      "3DNKTCDRqaWQ99P1ugE9v5ApedSPZR7XK8YtqYJ7wHpf",
      "3rifrbSvsd2YMydAD9sg4yuGsPPVrW8KZLVnFg64tQNr",
      "54mhnkCKNyAzf1TvS25sUTytvwFkqYKkWsC2kNirafaH",
      "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
    ],
    "relationType": "DIRECT_FUNDING (BINANCE)",
    "avgScore": 84.5,
    "confidence": 0.96,
    "totalVolumeSol": 15.4
  }
];
export const BACKTEST_SUMMARY = {status:"NOT_RUN", decision:"DATA_INCOMPLETE"};
