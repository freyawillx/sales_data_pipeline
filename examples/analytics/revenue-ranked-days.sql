-- Add ranked daily revenue and cumulative revenue shares
-- Identify whether a small number of unusually large days dominate recorded revenue.
-- Read-only; see docs/analytics/revenue-ranked-days.md for assumptions.
WITH daily AS (SELECT date, SUM(quantity * price) AS revenue FROM sales GROUP BY date)
SELECT date, revenue, DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_rank,
  100.0 * SUM(revenue) OVER (ORDER BY revenue DESC, date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    / NULLIF(SUM(revenue) OVER (), 0) AS cumulative_revenue_percent
FROM daily ORDER BY revenue DESC, date;
