-- Add quantity-weighted product prices
-- Calculate realized average unit price weighted by recorded quantities.
-- Read-only; see docs/analytics/weighted-product-price.md for assumptions.
SELECT product, SUM(quantity) AS units,
       SUM(quantity * price) / NULLIF(SUM(quantity), 0) AS weighted_unit_price,
       AVG(price) AS unweighted_line_price
FROM sales GROUP BY product ORDER BY product;
