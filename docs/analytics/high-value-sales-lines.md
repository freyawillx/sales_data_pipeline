# Add a high-value sales-line review query

List lines at or above the global 95th percentile of recorded line revenue.

Run from the repository root against a database already populated by the pipeline:

```bash
psql -X -v ON_ERROR_STOP=1 -f examples/analytics/high-value-sales-lines.sql
```

The query reads the default `sales` table (`date`, `product`, `quantity`, `price`).
For a custom destination, change the table reference before running it. It performs
no writes. Review the full query before applying it to production data.

This is a review queue, not a fraud decision. Ties at the threshold can include more than five percent of lines, especially in small datasets.

Each stored row is a sales line, not necessarily an order or a customer. Revenue
here means `quantity * price`, without currency conversion, discounts, tax, or
refund adjustments. The loader uses floating-point prices, so comparisons and
totals can have rounding differences. Treat these results as analysis, not a
financial ledger. An empty source produces no grouped results, or a NULL total
for an ungrouped SUM, according to normal SQL aggregation rules.
