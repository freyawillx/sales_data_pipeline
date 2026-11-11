-- Add monthly active-product counts
-- Measure the number of distinct products appearing in each recorded month.
-- Read-only; see docs/analytics/product-monthly-activity.md for assumptions.
SELECT CAST(date_trunc('month', date) AS DATE) AS month_start,
       COUNT(DISTINCT product) AS active_products,
       COUNT(*) AS sales_lines
FROM sales GROUP BY 1 ORDER BY 1;
