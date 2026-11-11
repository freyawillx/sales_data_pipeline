-- Add monthly unit and average-price comparisons
-- Place volume changes next to changes in realized average unit price.
-- Read-only; see docs/analytics/monthly-unit-revenue-bridge.md for assumptions.
WITH monthly AS (
  SELECT CAST(date_trunc('month', date) AS DATE) AS month_start,
         SUM(quantity) AS units, SUM(quantity * price) AS revenue FROM sales GROUP BY 1
)
SELECT *, revenue / NULLIF(units, 0) AS realized_unit_price,
  units - LAG(units) OVER (ORDER BY month_start) AS unit_change,
  revenue - LAG(revenue) OVER (ORDER BY month_start) AS revenue_change
FROM monthly ORDER BY month_start;
