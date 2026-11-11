-- Add first-observed product counts by month
-- Count products by the month of their earliest stored sales record.
-- Read-only; see docs/analytics/new-products-per-month.md for assumptions.
WITH first_sale AS (SELECT product, MIN(date) AS first_date FROM sales GROUP BY product)
SELECT CAST(date_trunc('month', first_date) AS DATE) AS first_month,
       COUNT(*) AS first_observed_products
FROM first_sale GROUP BY 1 ORDER BY 1;
