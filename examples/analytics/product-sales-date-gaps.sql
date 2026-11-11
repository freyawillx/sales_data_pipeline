-- Add gaps between product sales dates
-- Locate intervals longer than seven days between recorded sales of a product.
-- Read-only; see docs/analytics/product-sales-date-gaps.md for assumptions.
WITH days AS (SELECT DISTINCT product, date FROM sales), gaps AS (
  SELECT product, date, LAG(date) OVER (PARTITION BY product ORDER BY date) AS previous_date
  FROM days
)
SELECT * FROM gaps WHERE date > previous_date + INTERVAL '7 days'
ORDER BY product, date;
