-- Add quantity-size distributions by product
-- Separate single-unit, small-batch, and large-batch sales lines.
-- Read-only; see docs/analytics/product-line-size-buckets.md for assumptions.
SELECT product,
  CASE WHEN quantity = 0 THEN 'zero' WHEN quantity = 1 THEN 'single'
       WHEN quantity BETWEEN 2 AND 9 THEN 'small_batch' ELSE 'large_batch' END AS size_bucket,
  COUNT(*) AS sales_lines, SUM(quantity) AS units
FROM sales WHERE quantity >= 0 GROUP BY product, 2 ORDER BY product, 2;
