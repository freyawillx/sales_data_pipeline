# Add a monthly sales summary query

Produce a chronological monthly volume and revenue report.

Run from the repository root against a database already populated by the pipeline:

```bash
psql -X -v ON_ERROR_STOP=1 -f examples/analytics/monthly-sales-summary.sql
```

The query reads the default `sales` table (`date`, `product`, `quantity`, `price`).
For a custom destination, change the table reference before running it. It performs
no writes. Review the full query before applying it to production data.

Grouping by a full month-start date keeps different years separate. A partly loaded current month is not directly comparable to a complete previous month.

Each stored row is a sales line, not necessarily an order or a customer. Revenue
here means `quantity * price`, without currency conversion, discounts, tax, or
refund adjustments. The loader uses floating-point prices, so comparisons and
totals can have rounding differences. Treat these results as analysis, not a
financial ledger. An empty source produces no grouped results, or a NULL total
for an ungrouped SUM, according to normal SQL aggregation rules.
