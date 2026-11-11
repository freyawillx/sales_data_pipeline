-- Add weekday revenue and volume comparisons
-- Compare recorded sales across ISO weekdays, from Monday to Sunday.
-- Read-only; see docs/analytics/weekday-sales-pattern.md for assumptions.
SELECT EXTRACT(ISODOW FROM date) AS iso_weekday,
       COUNT(DISTINCT date) AS observed_days,
       SUM(quantity) AS units, SUM(quantity * price) AS revenue,
       SUM(quantity * price) / NULLIF(COUNT(DISTINCT date), 0) AS revenue_per_observed_day
FROM sales GROUP BY 1 ORDER BY 1;
