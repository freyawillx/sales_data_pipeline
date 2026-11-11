-- Add sales-line revenue distribution percentiles
-- Summarize typical and high-value line revenue with ordered-set aggregates.
-- Read-only; see docs/analytics/sales-line-revenue-percentiles.md for assumptions.
SELECT COUNT(*) AS sales_lines,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY quantity * price) AS median_line_revenue,
  percentile_cont(0.9) WITHIN GROUP (ORDER BY quantity * price) AS p90_line_revenue,
  percentile_cont(0.99) WITHIN GROUP (ORDER BY quantity * price) AS p99_line_revenue
FROM sales;
