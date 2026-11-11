-- Add missing calendar-date detection
-- Find dates with no stored sales between the earliest and latest recorded date.
-- Read-only; see docs/analytics/missing-calendar-dates.md for assumptions.
WITH bounds AS (SELECT MIN(date) AS first_date, MAX(date) AS last_date FROM sales),
calendar AS (
  SELECT CAST(day AS DATE) AS day FROM bounds,
       LATERAL generate_series(first_date, last_date, INTERVAL '1 day') AS series(day)
)
SELECT calendar.day FROM calendar LEFT JOIN sales ON sales.date = calendar.day
WHERE sales.date IS NULL ORDER BY calendar.day;
