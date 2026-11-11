# Worked example: daily sales summary query

This self-contained dataset demonstrates `daily-sales-summary.sql` using repeated sales
lines, zero quantities, unequal product prices, a year boundary, and a product
name with surrounding spaces. It is synthetic and contains no customer data.

The ten lines contain 13 units and gross revenue 53.0 across eight recorded
dates. An identical A-product line appears twice deliberately; no deduplication
is implied. Zero-quantity rows are observations, not missing dates. Each row is
a sales line rather than an order.

Use a disposable database with an existing four-column `sales` table, empty
before importing. Do not import these records into a real reporting table:

```bash
psql -X -v ON_ERROR_STOP=1 -c "\copy sales(date, product, quantity, price) FROM 'examples/worked/daily-sales-summary/input.csv' CSV HEADER"
psql -X -v ON_ERROR_STOP=1 --csv -f examples/analytics/daily-sales-summary.sql
```

`expected.csv` records the query output produced by DuckDB for comparison.
Its NULL values are empty cells, dates use ISO formatting, and floating-point
rendering may differ between engines. Compare numbers using an explicit
tolerance, not raw CSV text. PostgreSQL syntax was parsed separately; the
saved result is not a claim of a live PostgreSQL test.

Read `docs/analytics/daily-sales-summary.md` for this metric's interpretation and limitations.
For a custom table or schema, review and adapt both the import and SQL references.
The example does not run the append-only pipeline or change its default behavior.
