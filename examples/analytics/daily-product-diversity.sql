-- Add daily distinct-product and line-volume reporting
-- Compare each day's product breadth with its recorded line volume.
-- Read-only; see docs/analytics/daily-product-diversity.md for assumptions.
SELECT date, COUNT(DISTINCT product) AS distinct_products, COUNT(*) AS sales_lines,
       CAST(COUNT(*) AS DOUBLE PRECISION) / NULLIF(COUNT(DISTINCT product), 0)
         AS lines_per_product
FROM sales GROUP BY date ORDER BY date;
