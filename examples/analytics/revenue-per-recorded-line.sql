-- Add revenue-per-sales-line comparisons by month
-- Calculate average line revenue without implying that a line is a complete order.
-- Read-only; see docs/analytics/revenue-per-recorded-line.md for assumptions.
SELECT CAST(date_trunc('month', date) AS DATE) AS month_start,
       COUNT(*) AS sales_lines, SUM(quantity * price) AS revenue,
       AVG(quantity * price) AS average_line_revenue,
       AVG(CAST(quantity AS DOUBLE PRECISION)) AS average_line_quantity
FROM sales GROUP BY 1 ORDER BY 1;
