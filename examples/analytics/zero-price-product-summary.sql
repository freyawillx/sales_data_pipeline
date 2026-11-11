-- Add a zero-price sales summary
-- Measure the recorded units associated with free or missing-value-as-zero pricing.
-- Read-only; see docs/analytics/zero-price-product-summary.md for assumptions.
SELECT product, COUNT(*) AS zero_price_lines, SUM(quantity) AS zero_price_units,
       MIN(date) AS first_seen, MAX(date) AS last_seen
FROM sales WHERE price = 0 GROUP BY product
ORDER BY zero_price_units DESC, product;
