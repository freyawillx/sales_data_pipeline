# a streaming CSV to JSON Lines converter

Streams one CSV record at a time, handles standard quoting, and preserves all field text, including leading zeros. Quantity and price remain JSON strings for later numeric conversion by the cleaner. The converter is not a business-data validator. Existing outputs are refused. If a malformed record appears midway, a partial output can remain; inspect and remove or quarantine it before retrying under a new path. A header-only CSV produces an empty JSONL file, which is not a populated pipeline input.

Run from the repository root:

```bash
python tools/csv_to_json_lines.py sample.csv converted.jsonl
python tools/csv_to_json_lines.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
