-- ==============================================================================
-- DUNE ANALYTICS REPRODUCIBLE QUERY SUITE (Section 12 of Concept Note)
-- Blockchain: Solana | Tables: solana.dex_trades, solana.transfers, solana.account_activity
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: First 100 Buyers on Solana DEXes for BONK, WIF, and POPCAT
-- ------------------------------------------------------------------------------
WITH first_swaps AS (
    SELECT
        token_bought_mint_address AS mint,
        trader_id AS wallet_address,
        block_time,
        token_bought_amount,
        amount_usd,
        tx_id,
        ROW_NUMBER() OVER (PARTITION BY token_bought_mint_address ORDER BY block_time ASC) as buyer_rank
    FROM solana.dex_trades
    WHERE token_bought_mint_address IN (
        'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263', -- BONK
        'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm', -- WIF
        '7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr'  -- POPCAT
    )
    AND block_time >= TIMESTAMP '2022-12-01'
)
SELECT *
FROM first_swaps
WHERE buyer_rank <= 100
ORDER BY mint, buyer_rank ASC;

-- ------------------------------------------------------------------------------
-- QUERY 2: Multi-Winner Recurrence & Overlap Matrix (BONK ∩ WIF ∩ POPCAT)
-- ------------------------------------------------------------------------------
WITH early_cohorts AS (
    SELECT DISTINCT
        trader_id AS wallet_address,
        CASE
            WHEN token_bought_mint_address = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' THEN 'BONK'
            WHEN token_bought_mint_address = 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm' THEN 'WIF'
            WHEN token_bought_mint_address = '7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr' THEN 'POPCAT'
        END AS winner_symbol
    FROM (
        SELECT
            token_bought_mint_address,
            trader_id,
            ROW_NUMBER() OVER (PARTITION BY token_bought_mint_address ORDER BY block_time ASC) as rank
        FROM solana.dex_trades
        WHERE token_bought_mint_address IN (
            'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263',
            'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm',
            '7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr'
        )
    )
    WHERE rank <= 250
),
total_activity AS (
    SELECT
        trader_id AS wallet_address,
        COUNT(DISTINCT token_bought_mint_address) as lifetime_distinct_tokens_bought,
        COUNT(1) as total_trades_count
    FROM solana.dex_trades
    GROUP BY trader_id
)
SELECT
    c.wallet_address,
    COUNT(DISTINCT c.winner_symbol) AS winners_hit_count,
    ARRAY_AGG(c.winner_symbol) AS winners_list,
    COALESCE(a.lifetime_distinct_tokens_bought, 1) AS total_tokens_bought,
    ROUND(CAST(COUNT(DISTINCT c.winner_symbol) AS DOUBLE) / COALESCE(a.lifetime_distinct_tokens_bought, 1) * 100.0, 2) AS selectivity_percentage
FROM early_cohorts c
LEFT JOIN total_activity a ON c.wallet_address = a.wallet_address
GROUP BY c.wallet_address, a.lifetime_distinct_tokens_bought
HAVING COUNT(DISTINCT c.winner_symbol) >= 2
ORDER BY selectivity_percentage DESC, winners_hit_count DESC;

-- ------------------------------------------------------------------------------
-- QUERY 3: First SOL Funding Transaction (Clustering & Parent Identification)
-- ------------------------------------------------------------------------------
SELECT
    t.tx_from AS funder_parent_address,
    t.tx_to AS target_wallet_address,
    t.amount AS sol_amount,
    t.block_time,
    t.tx_id
FROM solana.transfers t
WHERE t.tx_to IN (SELECT DISTINCT wallet_address FROM early_cohorts)
AND t.block_time = (
    SELECT MIN(block_time)
    FROM solana.transfers sub
    WHERE sub.tx_to = t.tx_to
);
