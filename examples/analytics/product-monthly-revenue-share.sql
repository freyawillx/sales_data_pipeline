-- Add product revenue shares within each month
-- Track how each month's revenue mix is distributed across products.
-- Read-only; see docs/analytics/product-monthly-revenue-share.md for assumptions.
WITH monthly AS (
  SELECT CAST(date_trunc('month', date) AS DATE) AS month_start,
         product, SUM(quantity * price) AS revenue FROM sales GROUP BY 1, 2
)
SELECT *, 100.0 * revenue / NULLIF(SUM(revenue) OVER (PARTITION BY month_start), 0)
  AS month_revenue_percent
FROM monthly ORDER BY month_start, revenue DESC, product;
