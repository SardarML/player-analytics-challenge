-- Net deposits per brand and month, EUR, real accounts, approved only (Snowflake SQL)
WITH tx AS (
    SELECT player_id, created_at, currency, amount AS signed_amount, 'D' AS kind
    FROM deposits WHERE status = 'approved'
    UNION ALL
    SELECT player_id, created_at, currency, -amount, 'W'
    FROM withdrawals WHERE status = 'approved'
)
SELECT p.brand,
       DATE_TRUNC('month', tx.created_at) AS month,
       ROUND(SUM(CASE WHEN kind = 'D' THEN signed_amount * fx.rate_to_eur ELSE 0 END), 2) AS deposits_eur,
       ROUND(SUM(CASE WHEN kind = 'W' THEN -signed_amount * fx.rate_to_eur ELSE 0 END), 2) AS withdrawals_eur,
       ROUND(SUM(signed_amount * fx.rate_to_eur), 2) AS net_deposits_eur
FROM tx
JOIN players p ON p.player_id = tx.player_id AND p.account_type = 'real'
JOIN fx_rates fx ON fx.currency = tx.currency AND fx.date = CAST(tx.created_at AS DATE)
GROUP BY 1, 2
ORDER BY 1, 2;
