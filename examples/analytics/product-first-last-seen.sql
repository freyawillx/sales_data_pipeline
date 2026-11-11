-- Add product observation span reporting
-- Show each product's first and most recent recorded sale dates.
-- Read-only; see docs/analytics/product-first-last-seen.md for assumptions.
SELECT product, MIN(date) AS first_seen, MAX(date) AS last_seen,
       COUNT(DISTINCT date) AS observed_sale_days
FROM sales GROUP BY product ORDER BY first_seen, product;
