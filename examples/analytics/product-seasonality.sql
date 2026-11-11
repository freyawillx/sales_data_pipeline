-- Add product revenue seasonality by calendar month
-- Compare a product's observed revenue across month-of-year buckets.
-- Read-only; see docs/analytics/product-seasonality.md for assumptions.
SELECT product, EXTRACT(MONTH FROM date) AS calendar_month,
       COUNT(DISTINCT EXTRACT(YEAR FROM date)) AS observed_years,
       SUM(quantity * price) AS revenue,
       SUM(quantity * price) / NULLIF(COUNT(DISTINCT EXTRACT(YEAR FROM date)), 0)
         AS revenue_per_observed_year
FROM sales GROUP BY product, 2 ORDER BY product, 2;
