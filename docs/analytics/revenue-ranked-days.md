# Add ranked daily revenue and cumulative revenue shares

Identify whether a small number of unusually large days dominate recorded revenue.

Run from the repository root against a database already populated by the pipeline:

```bash
psql -X -v ON_ERROR_STOP=1 -f examples/analytics/revenue-ranked-days.sql
```

The query reads the default `sales` table (`date`, `product`, `quantity`, `price`).
For a custom destination, change the table reference before running it. It performs
no writes. Review the full query before applying it to production data.

The rank preserves revenue ties while the cumulative total uses date to order tied days consistently. Review import duplication before interpreting exceptional dates.

Each stored row is a sales line, not necessarily an order or a customer. Revenue
here means `quantity * price`, without currency conversion, discounts, tax, or
refund adjustments. The loader uses floating-point prices, so comparisons and
totals can have rounding differences. Treat these results as analysis, not a
financial ledger. An empty source produces no grouped results, or a NULL total
for an ungrouped SUM, according to normal SQL aggregation rules.
