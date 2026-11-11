-- Add month-to-month revenue comparisons
-- Compare revenue with the previous recorded month using a window function.
-- Read-only; see docs/analytics/monthly-revenue-change.md for assumptions.
WITH monthly AS (
  SELECT CAST(date_trunc('month', date) AS DATE) AS month_start,
         SUM(quantity * price) AS revenue FROM sales GROUP BY 1
), previous AS (
  SELECT *, LAG(month_start) OVER (ORDER BY month_start) AS previous_month,
            LAG(revenue) OVER (ORDER BY month_start) AS previous_revenue FROM monthly
)
SELECT *, 100.0 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0)
            AS percent_change
FROM previous ORDER BY month_start;
