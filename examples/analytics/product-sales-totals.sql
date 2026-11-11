-- Add a product revenue and volume report
-- Identify products contributing the most recorded revenue.
-- Read-only; see docs/analytics/product-sales-totals.md for assumptions.
SELECT product, COUNT(*) AS sales_lines, SUM(quantity) AS units,
       SUM(quantity * price) AS gross_revenue
FROM sales GROUP BY product
ORDER BY gross_revenue DESC, product;
