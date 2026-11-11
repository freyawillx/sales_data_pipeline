-- Add monthly top-product rankings
-- Find the three highest-revenue product ranks within each recorded month.
-- Read-only; see docs/analytics/top-products-per-month.md for assumptions.
WITH totals AS (
  SELECT CAST(date_trunc('month', date) AS DATE) AS month_start,
         product, SUM(quantity * price) AS revenue
  FROM sales GROUP BY 1, 2
), ranked AS (
  SELECT *, DENSE_RANK() OVER (
    PARTITION BY month_start ORDER BY revenue DESC) AS revenue_rank
  FROM totals
)
SELECT * FROM ranked WHERE revenue_rank <= 3
ORDER BY month_start, revenue_rank, product;
