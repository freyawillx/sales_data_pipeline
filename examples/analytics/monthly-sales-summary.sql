-- Add a monthly sales summary query
-- Produce a chronological monthly volume and revenue report.
-- Read-only; see docs/analytics/monthly-sales-summary.md for assumptions.
SELECT CAST(date_trunc('month', date) AS DATE) AS month_start,
       COUNT(*) AS sales_lines, SUM(quantity) AS units,
       SUM(quantity * price) AS gross_revenue
FROM sales GROUP BY 1 ORDER BY 1;
