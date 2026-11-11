-- Add a statistical daily revenue review queue
-- Flag recorded days more than two sample standard deviations from average daily revenue.
-- Read-only; see docs/analytics/daily-revenue-outlier-review.md for assumptions.
WITH daily AS (SELECT date, SUM(quantity * price) AS revenue FROM sales GROUP BY date),
stats AS (SELECT AVG(revenue) AS mean_revenue, STDDEV_SAMP(revenue) AS stddev FROM daily)
SELECT daily.*, stats.mean_revenue, stats.stddev
FROM daily CROSS JOIN stats
WHERE ABS(revenue - mean_revenue) > 2 * stddev ORDER BY date;
