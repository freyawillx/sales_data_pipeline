-- Add duplicate-value revenue exposure estimates
-- Estimate revenue associated with repeated copies of identical four-field line values.
-- Read-only; see docs/analytics/duplicate-import-exposure.md for assumptions.
WITH repeated AS (
  SELECT date, product, quantity, price, COUNT(*) AS copies FROM sales
  GROUP BY date, product, quantity, price HAVING COUNT(*) > 1
)
SELECT COUNT(*) AS repeated_value_groups, COALESCE(SUM(copies - 1), 0) AS extra_copies,
       COALESCE(SUM((copies - 1) * quantity * price), 0) AS candidate_extra_revenue
FROM repeated;
