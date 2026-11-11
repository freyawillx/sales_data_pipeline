# strict preflight validation for sale dates and numeric bounds

Streams CSV records and enforces canonical YYYY-MM-DD dates, nonblank products, finite nonnegative prices, and whole quantities within PostgreSQL's signed 32-bit nonnegative range. It rejects fractions before the current cleaner could truncate them. Exit 1 means invalid rows, while malformed headers produce argparse's error exit. Counts can overlap by field, and no record values are printed. Extra columns are permitted. This optional preflight does not alter the cleaner, normalize data, or guarantee database connectivity, privileges, or transaction success.

Run from the repository root:

```bash
python tools/validate_sales_file.py sample.csv
python tools/validate_sales_file.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
