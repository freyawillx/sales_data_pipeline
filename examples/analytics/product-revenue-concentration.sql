-- Add a product revenue concentration index
-- Compute the sum of squared product revenue shares as a concentration indicator.
-- Read-only; see docs/analytics/product-revenue-concentration.md for assumptions.
WITH totals AS (SELECT product, SUM(quantity * price) AS revenue FROM sales GROUP BY product),
shares AS (SELECT revenue / NULLIF(SUM(revenue) OVER (), 0) AS share FROM totals)
SELECT COUNT(*) AS products, SUM(share * share) AS concentration_index FROM shares;
