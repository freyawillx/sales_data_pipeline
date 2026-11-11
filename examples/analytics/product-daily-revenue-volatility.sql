-- Add variability of recorded daily product revenue
-- Compare the spread of daily revenue values among products with multiple observed dates.
-- Read-only; see docs/analytics/product-daily-revenue-volatility.md for assumptions.
WITH daily AS (
  SELECT product, date, SUM(quantity * price) AS revenue FROM sales GROUP BY product, date
)
SELECT product, COUNT(*) AS observed_days, AVG(revenue) AS average_daily_revenue,
       STDDEV_SAMP(revenue) AS revenue_stddev,
       STDDEV_SAMP(revenue) / NULLIF(AVG(revenue), 0) AS coefficient_of_variation
FROM daily GROUP BY product HAVING COUNT(*) >= 2 ORDER BY product;
