-- Add exact duplicate sales-line detection
-- Identify repeated combinations of all four stored sales fields.
-- Read-only; see docs/analytics/duplicate-sales-lines.md for assumptions.
SELECT date, product, quantity, price, COUNT(*) AS occurrences
FROM sales GROUP BY date, product, quantity, price HAVING COUNT(*) > 1
ORDER BY occurrences DESC, date, product;
