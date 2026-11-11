-- Add an overall sales data coverage report
-- Summarize the stored date range, line volume, and product coverage in one row.
-- Read-only; see docs/analytics/observed-data-coverage.md for assumptions.
SELECT COUNT(*) AS sales_lines, COUNT(DISTINCT date) AS observed_dates,
       COUNT(DISTINCT product) AS products, MIN(date) AS first_date, MAX(date) AS last_date,
       COUNT(*) FILTER (WHERE date IS NULL) AS null_date_lines
FROM sales;
