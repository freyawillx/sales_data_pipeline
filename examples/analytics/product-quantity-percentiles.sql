-- Add per-product quantity distribution percentiles
-- Compare typical and high-volume line quantities for every product.
-- Read-only; see docs/analytics/product-quantity-percentiles.md for assumptions.
SELECT product, COUNT(*) AS sales_lines,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY quantity) AS median_quantity,
  percentile_cont(0.95) WITHIN GROUP (ORDER BY quantity) AS p95_quantity
FROM sales GROUP BY product ORDER BY product;
