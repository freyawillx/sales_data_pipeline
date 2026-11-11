-- Add a weekly sales summary query
-- Aggregate daily records into Monday-start calendar weeks.
-- Read-only; see docs/analytics/weekly-sales-summary.md for assumptions.
SELECT CAST(date_trunc('week', date) AS DATE) AS week_start,
       SUM(quantity) AS units, SUM(quantity * price) AS gross_revenue
FROM sales GROUP BY 1 ORDER BY 1;
