-- Add cumulative daily revenue analysis
-- Track the accumulated recorded revenue over the observed date range.
-- Read-only; see docs/analytics/cumulative-daily-revenue.md for assumptions.
WITH daily AS (
  SELECT date, SUM(quantity * price) AS revenue FROM sales GROUP BY date
)
SELECT date, revenue,
       SUM(revenue) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
         AS cumulative_revenue
FROM daily ORDER BY date;
