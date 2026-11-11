-- Add weekend and weekday sales comparison
-- Separate weekend revenue from Monday-through-Friday revenue.
-- Read-only; see docs/analytics/weekend-sales-comparison.md for assumptions.
SELECT CASE WHEN EXTRACT(ISODOW FROM date) IN (6, 7)
            THEN 'weekend' ELSE 'weekday' END AS day_group,
       COUNT(DISTINCT date) AS observed_days, SUM(quantity * price) AS revenue,
       SUM(quantity * price) / NULLIF(COUNT(DISTINCT date), 0) AS revenue_per_observed_day
FROM sales GROUP BY 1 ORDER BY 1;
