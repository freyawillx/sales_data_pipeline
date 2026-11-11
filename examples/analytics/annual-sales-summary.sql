-- Add an annual sales summary query
-- Compare full calendar-year totals without mixing product detail into the result.
-- Read-only; see docs/analytics/annual-sales-summary.md for assumptions.
SELECT EXTRACT(YEAR FROM date) AS sale_year,
       COUNT(DISTINCT product) AS distinct_products,
       SUM(quantity) AS units, SUM(quantity * price) AS gross_revenue
FROM sales GROUP BY 1 ORDER BY 1;
