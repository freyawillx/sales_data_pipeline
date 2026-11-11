# multiset reconciliation for sales CSV exports

Compares the four stored columns as exact CSV strings, independent of row order and sensitive to duplicate multiplicity. Extra columns are ignored. Formatting differences such as `3.50` versus `3.5` count as mismatches; normalize both exports under an agreed contract first. The tool prints counts rather than raw sales values and exits 1 for a mismatch, 0 for equality. It does not infer which repeated values are legitimate transactions. Both multisets are held in memory.

Run from the repository root:

```bash
python tools/reconcile_sales_csv.py expected.csv actual.csv
python tools/reconcile_sales_csv.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
