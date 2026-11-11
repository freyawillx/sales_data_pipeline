-- Add cumulative revenue by product
-- Follow each product's cumulative revenue independently through time.
-- Read-only; see docs/analytics/running-product-revenue.md for assumptions.
WITH daily AS (
  SELECT product, date, SUM(quantity * price) AS revenue FROM sales GROUP BY product, date
)
SELECT product, date, revenue,
       SUM(revenue) OVER (PARTITION BY product ORDER BY date
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue
FROM daily ORDER BY product, date;
