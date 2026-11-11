-- Add product-name spelling and whitespace collision checks
-- Find exact product names that collapse to the same lowercase trimmed spelling.
-- Read-only; see docs/analytics/product-name-normalization-audit.md for assumptions.
SELECT LOWER(TRIM(product)) AS normalized_name,
       COUNT(DISTINCT product) AS stored_spellings,
       COUNT(*) AS sales_lines, SUM(quantity * price) AS revenue
FROM sales GROUP BY LOWER(TRIM(product)) HAVING COUNT(DISTINCT product) > 1
ORDER BY normalized_name;
