-- Add a seven-observation revenue moving average
-- Smooth daily revenue using the current and previous six recorded dates.
-- Read-only; see docs/analytics/active-day-moving-average.md for assumptions.
WITH daily AS (
  SELECT date, SUM(quantity * price) AS revenue FROM sales GROUP BY date
)
SELECT date, revenue, AVG(revenue) OVER (
  ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS active_day_average
FROM daily ORDER BY date;
