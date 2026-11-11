# Verify a first load

Use a disposable database or dedicated test table. The current loader appends,
so repeat a smoke test only after checking whether the previous attempt
inserted its data. Prepare a one-row CSV with known values:

```csv
date,product,quantity,price
2024-01-01,Smoke Widget,2,3.50
```

After configuring the PostgreSQL environment, run:

```bash
python pipeline.py sample.csv smoke_sales
psql -X -v ON_ERROR_STOP=1 -c "SELECT date, product, quantity, price FROM smoke_sales;"
```

Confirm the date, full product label, quantity 2, and price 3.5. Then check:

```sql
SELECT COUNT(*) AS lines, SUM(quantity) AS units,
       SUM(quantity * price) AS revenue
FROM smoke_sales;
```

In a previously empty destination, expect one line, two units, and revenue
approximately 7.0. A larger count may indicate existing data or a rerun.
Do not compare floating-point totals using display formatting alone.

A failure before insertion can still leave a created table because table
creation and insertion currently have separate commits. Inspect both schema
and rows after an exception. If the helper raises `NameError: execute_values`,
fix its missing import rather than repeatedly retrying the same load.
Remove the disposable database through your normal local cleanup workflow.
