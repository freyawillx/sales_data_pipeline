-- Add product sales frequency over observed business dates
-- Compare how often each product appears across dates present anywhere in the dataset.
-- Read-only; see docs/analytics/product-sales-frequency.md for assumptions.
WITH total_days AS (SELECT COUNT(DISTINCT date) AS observed_dates FROM sales)
SELECT product, COUNT(DISTINCT date) AS product_dates, total_days.observed_dates,
       100.0 * COUNT(DISTINCT date) / NULLIF(total_days.observed_dates, 0) AS observed_day_percent
FROM sales CROSS JOIN total_days GROUP BY product, total_days.observed_dates
ORDER BY observed_day_percent DESC, product;
