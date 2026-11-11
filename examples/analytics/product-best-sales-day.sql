-- Add best revenue day per product
-- Find every date tied for a product's highest recorded daily revenue.
-- Read-only; see docs/analytics/product-best-sales-day.md for assumptions.
WITH daily AS (
  SELECT product, date, SUM(quantity * price) AS revenue FROM sales GROUP BY product, date
), ranked AS (
  SELECT *, RANK() OVER (PARTITION BY product ORDER BY revenue DESC) AS revenue_rank FROM daily
)
SELECT product, date, revenue FROM ranked WHERE revenue_rank = 1 ORDER BY product, date;
