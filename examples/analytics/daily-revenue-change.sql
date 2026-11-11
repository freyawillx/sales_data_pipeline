-- Add day-to-day recorded revenue changes
-- Compare each observed day's revenue with the previous observed day.
-- Read-only; see docs/analytics/daily-revenue-change.md for assumptions.
WITH daily AS (
  SELECT date, SUM(quantity * price) AS revenue FROM sales GROUP BY date
), previous AS (
  SELECT *, LAG(date) OVER (ORDER BY date) AS previous_date,
            LAG(revenue) OVER (ORDER BY date) AS previous_revenue FROM daily
)
SELECT *, revenue - previous_revenue AS absolute_change,
  100.0 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0) AS percent_change
FROM previous ORDER BY date;
