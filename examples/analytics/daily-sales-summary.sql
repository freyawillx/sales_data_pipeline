-- Add a daily sales summary query
-- Compare recorded units, sales lines, and gross revenue for each calendar date.
-- Read-only; see docs/analytics/daily-sales-summary.md for assumptions.
SELECT date AS sale_date, COUNT(*) AS sales_lines,
       SUM(quantity) AS units, SUM(quantity * price) AS gross_revenue
FROM sales GROUP BY date ORDER BY date;
