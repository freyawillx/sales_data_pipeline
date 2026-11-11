-- Add same-month prior-year revenue comparisons
-- Match each month to the same calendar month one year earlier.
-- Read-only; see docs/analytics/year-over-year-monthly-revenue.md for assumptions.
WITH monthly AS (
  SELECT CAST(date_trunc('month', date) AS DATE) AS month_start,
         SUM(quantity * price) AS revenue FROM sales GROUP BY 1
)
SELECT current.month_start, current.revenue, prior.revenue AS prior_year_revenue,
  100.0 * (current.revenue - prior.revenue) / NULLIF(prior.revenue, 0) AS percent_change
FROM monthly current LEFT JOIN monthly prior
  ON prior.month_start = current.month_start - INTERVAL '1 year'
ORDER BY current.month_start;
