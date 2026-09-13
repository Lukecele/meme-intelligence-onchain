export type PositionStatus = "HOLDING" | "ACCUMULATING" | "PARTIAL_EXIT" | "FULL_EXIT";

export interface WalletInteraction {
  address: string;
  label: string;
  score: number;
  independenceScore: number;
  entryDelaySec: number;
  amountSol: number;
  clusterId?: string | null;
  txHash?: string;
  isWatchlistMatch?: boolean;
  positionStatus?: PositionStatus;
  currentHoldingTokens?: number;
  tokensBought?: number;
  tokensSold?: number;
  lastActionTime?: number;
  exitTxHash?: string;
}

export interface WalletProfile { hitTokens?: string[]; controlTokens?: string[]; hits?: number;
  address: string;
  label: string;
  smartScore: number;
  independenceScore: number;
  selectivityScore: number;
  precocityAvgSec: number;
  avgPostEntryReturn: number;
  exitEfficiency: number;
  totalTokensBought: number;
  totalWinnersEntered: number;
  totalControlEntered?: number;
  fundingSource: string;
  isExchangeFunded?: boolean;
  isBotSniper?: boolean;
  isCreatorInsider?: boolean;
  notes?: string;
  clusterId?: string | null;
  clusterRole?: string | null;
  scoreBreakdown?: {
    earlyBigWins?: number;
    precocity?: number;
    selectivity?: number;
    postEntryReturn?: number;
    exitManagement?: number;
    independence?: number;
    exitEfficiency?: number;
    holdingDiscipline?: number;
  };
  recentTrades?: {
    tokenSymbol: string;
    tokenMint: string;
    side: string;
    timestamp: number;
    amountUsd: number;
    returnMultiple: number;
  }[];
}

export interface ClusterInfo {
  clusterId: string;
  rootAddress: string;
  members: string[];
  relationType: string;
  avgScore: number;
  confidence: number;
  totalVolumeSol?: number;
  notes?: string;
}

export interface TokenMeta {
  symbol: string;
  name: string;
  mint: string;
  isWinner: boolean;
  isControl: boolean;
  launchTime: string;
  initialLiquidityUsd: number;
  peakMcapUsd: number;
  maxReturnX: number;
  hasAirdrop: boolean;
}

export interface ConvergenceAlert {
  id: string;
  tokenMint: string;
  symbol: string;
  name: string;
  dexId?: string;
  iconUrl?: string | null;
  timestamp: number;
  tokenAgeMinutes: number;
  marketCapUsd: number;
  liquidityUsd: number;
  priceUsd?: number;
  entryPriceUsd?: number;
  currentMarketCapUsd?: number;
  priceChangePct?: number;
  isLiveNow?: boolean;
  solPriceUsd?: number;
  score: number;
  confidence: number;
  signalLevel: "ALTO" | "MEDIO" | "BASSO";
  walletsCount: number;
  independentWalletsCount: number;
  timeSpanMinutes: number;
  creatorConcentrationPct: number;
  walletsInvolved: WalletInteraction[];
  smartWalletsExited?: boolean;
  activeHoldersCount?: number;
  exitedHoldersCount?: number;
  riskFlags: string[];
  safetyScore: number;
  mintAuthority: string | null;
  freezeAuthority: string | null;
}

export interface CopyTradeLogEvent {
  timestamp: number;
  actionType: "ENTRY_COPY" | "PARTIAL_EXIT_COPY" | "FULL_EXIT_COPY" | "ACCUMULATE_TAG";
  walletAddress: string;
  description: string;
  cashAmountUsd: number;
  tokensAmount: number;
  priceUsd: number;
}

export interface SimulatedTrade {
  id: string;
  tokenMint: string;
  symbol: string;
  name: string;
  entryTimestamp: number;
  entryPriceUsd: number;
  entryMcapUsd: number;
  amountInvestedUsd: number; // Demo amount, not real capital
  amountInvestedSol?: number;
  tokenAgeMinutes?: number;
  isLiveNow?: boolean;
  exactSoldPct?: number;
  leadWallet?: WalletInteraction;
  initialTokensAcquired: number;
  currentTokensHeld: number;
  currentPriceUsd: number;
  currentMcapUsd: number;
  currentPositionValueUsd: number; // currentTokensHeld * currentPriceUsd
  totalCashExtractedUsd: number; // Sum of partial exits + full exit cash
  totalNetPnlUsd: number; // totalCashExtractedUsd + currentPositionValueUsd - amountInvestedUsd
  totalNetPnlPct: number; // totalNetPnlUsd / amountInvestedUsd * 100
  status: "OPEN_FULL" | "OPEN_PARTIAL_EXITED" | "CLOSED_FULL_EXIT" | "CLOSED_MANUAL";
  partialSellsCount: number;
  exitTimestamp?: number;
  exitPriceUsd?: number;
  finalRealizedPnlUsd?: number;
  finalRealizedPnlPct?: number;
  exitReason?: string;
  copyTradeLogs: CopyTradeLogEvent[];
}
