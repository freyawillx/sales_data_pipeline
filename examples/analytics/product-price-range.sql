-- Add product price variation summaries
-- Identify products recorded with multiple distinct unit prices.
-- Read-only; see docs/analytics/product-price-range.md for assumptions.
SELECT product, MIN(price) AS lowest_price, MAX(price) AS highest_price,
       MAX(price) - MIN(price) AS price_spread, COUNT(DISTINCT price) AS price_points
FROM sales GROUP BY product HAVING COUNT(DISTINCT price) > 1
ORDER BY price_spread DESC, product;
