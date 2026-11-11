-- Add a high-value sales-line review query
-- List lines at or above the global 95th percentile of recorded line revenue.
-- Read-only; see docs/analytics/high-value-sales-lines.md for assumptions.
WITH cutoff AS (
  SELECT percentile_cont(0.95) WITHIN GROUP (ORDER BY quantity * price) AS value FROM sales
)
SELECT date, product, quantity, price, quantity * price AS line_revenue
FROM sales CROSS JOIN cutoff WHERE quantity * price >= cutoff.value
ORDER BY line_revenue DESC, date, product;
