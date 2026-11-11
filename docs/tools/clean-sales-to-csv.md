# an explicit clean-to-CSV utility without a database load

Applies the repository's actual cleaner, keeps extra columns, and writes a new UTF-8 CSV. It refuses to overwrite an existing output and reports removed-row counts. Source row indexes are not exported as an extra column. Dates are serialized as calendar dates, matching the destination DATE column; time-of-day is not preserved. Existing cleaner limitations, including fractional quantity truncation and nonfinite-value handling, still apply. All input is held in memory.

Run from the repository root:

```bash
python tools/clean_sales_to_csv.py sample.csv cleaned.csv
python tools/clean_sales_to_csv.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
