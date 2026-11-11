-- Add cumulative product revenue concentration
-- Show how quickly revenue accumulates when products are ordered from largest to smallest.
-- Read-only; see docs/analytics/pareto-product-revenue.md for assumptions.
WITH totals AS (SELECT product, SUM(quantity * price) AS revenue FROM sales GROUP BY product)
SELECT product, revenue,
  100.0 * SUM(revenue) OVER (ORDER BY revenue DESC, product
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    / NULLIF(SUM(revenue) OVER (), 0) AS cumulative_revenue_percent
FROM totals ORDER BY revenue DESC, product;
