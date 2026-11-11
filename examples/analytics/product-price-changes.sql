-- Add changes in observed daily product prices
-- Detect changes between consecutive recorded daily weighted product prices.
-- Read-only; see docs/analytics/product-price-changes.md for assumptions.
WITH daily AS (
  SELECT product, date, SUM(quantity * price) / NULLIF(SUM(quantity), 0) AS unit_price
  FROM sales GROUP BY product, date
), compared AS (
  SELECT *, LAG(unit_price) OVER (PARTITION BY product ORDER BY date) AS previous_price
  FROM daily
)
SELECT *, unit_price - previous_price AS price_change
FROM compared WHERE ABS(unit_price - previous_price) > 0.000001
ORDER BY product, date;
