-- Add an audit for malformed rows written outside the cleaner
-- Count stored rows that violate the cleaner's basic required-field and nonnegative rules.
-- Read-only; see docs/analytics/invalid-stored-sales-audit.md for assumptions.
SELECT COUNT(*) AS total_lines,
  COUNT(*) FILTER (WHERE date IS NULL OR product IS NULL OR quantity IS NULL OR price IS NULL)
    AS missing_required_values,
  COUNT(*) FILTER (WHERE TRIM(product) = '') AS blank_products,
  COUNT(*) FILTER (WHERE quantity < 0) AS negative_quantities,
  COUNT(*) FILTER (WHERE price < 0) AS negative_prices
FROM sales;
