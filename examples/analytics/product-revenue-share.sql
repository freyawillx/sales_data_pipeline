-- Add product revenue contribution shares
-- Express each product's revenue as a percentage of all recorded revenue.
-- Read-only; see docs/analytics/product-revenue-share.md for assumptions.
WITH totals AS (
  SELECT product, SUM(quantity * price) AS revenue FROM sales GROUP BY product
)
SELECT product, revenue,
       100.0 * revenue / NULLIF(SUM(revenue) OVER (), 0) AS revenue_percent
FROM totals ORDER BY revenue DESC, product;
