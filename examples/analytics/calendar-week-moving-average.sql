-- Add a calendar-based trailing revenue average
-- Average recorded daily revenue within the trailing seven-calendar-day interval.
-- Read-only; see docs/analytics/calendar-week-moving-average.md for assumptions.
WITH daily AS (
  SELECT date, SUM(quantity * price) AS revenue FROM sales GROUP BY date
)
SELECT date, revenue, AVG(revenue) OVER (
  ORDER BY CAST(date AS TIMESTAMP)
  RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW) AS trailing_recorded_average
FROM daily ORDER BY date;
