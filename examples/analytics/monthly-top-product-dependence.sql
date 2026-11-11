-- Add monthly dependence on the largest product
-- Track the fraction of each month's revenue contributed by its largest product total.
-- Read-only; see docs/analytics/monthly-top-product-dependence.md for assumptions.
WITH monthly AS (
  SELECT CAST(date_trunc('month', date) AS DATE) AS month_start,
         product, SUM(quantity * price) AS revenue FROM sales GROUP BY 1, 2
)
SELECT month_start, COUNT(*) AS products, SUM(revenue) AS total_revenue,
       MAX(revenue) AS largest_product_revenue,
       100.0 * MAX(revenue) / NULLIF(SUM(revenue), 0) AS largest_product_percent
FROM monthly GROUP BY month_start ORDER BY month_start;
