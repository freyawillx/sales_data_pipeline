-- Add a zero-quantity sales review query
-- Find stored lines that contribute no units because their quantity is zero.
-- Read-only; see docs/analytics/zero-quantity-sales-lines.md for assumptions.
SELECT date, product, quantity, price FROM sales WHERE quantity = 0
ORDER BY date, product, price;
