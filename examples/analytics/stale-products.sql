-- Add stale product activity detection
-- List products whose last recorded date is over thirty days before the dataset's latest date.
-- Read-only; see docs/analytics/stale-products.md for assumptions.
WITH latest AS (SELECT MAX(date) AS as_of_date FROM sales)
SELECT product, MAX(date) AS last_seen, latest.as_of_date
FROM sales CROSS JOIN latest GROUP BY product, latest.as_of_date
HAVING MAX(date) < latest.as_of_date - INTERVAL '30 days'
ORDER BY last_seen, product;
