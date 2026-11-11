# a shape-validated JSON array to CSV converter

Requires an array of flat records with all required keys, writes required fields first, then the union of extra fields in sorted order. Absent extra values become blank cells, and nulls serialize as blank CSV values. Nested objects or arrays are rejected before output creation. An empty array produces a header-only CSV. This conversion does not clean or coerce business values. It holds the JSON document in memory and refuses existing output files.

Run from the repository root:

```bash
python tools/json_records_to_csv.py sample.json converted.csv
python tools/json_records_to_csv.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
