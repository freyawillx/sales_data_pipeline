# a database-free sales input inspection utility

Reports columns, inferred pandas types, row counts, and missing values as JSON, without printing individual sales values. It materializes the file in memory. Inspection is not acceptance validation: a present field can still contain invalid business data. JSON is explicitly read as UTF-8 here, unlike the current pipeline reader's platform-default encoding. Case-insensitive suffix handling belongs to this utility only.

Run from the repository root:

```bash
python tools/inspect_sales_input.py sample.csv
python tools/inspect_sales_input.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
