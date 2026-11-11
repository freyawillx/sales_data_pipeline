-- Add a quarterly sales summary query
-- Summarize sales using ordinary calendar quarters.
-- Read-only; see docs/analytics/quarterly-sales-summary.md for assumptions.
SELECT CAST(date_trunc('quarter', date) AS DATE) AS quarter_start,
       SUM(quantity) AS units, SUM(quantity * price) AS gross_revenue
FROM sales GROUP BY 1 ORDER BY 1;
