# header-preserving CSV chunk preparation

Splits on parsed CSV records, so quoted commas and embedded newlines do not break row boundaries. Every output chunk repeats the original header; a header-only input creates no chunk files. Existing destination directories are refused. A failure can leave partial chunks: quarantine that directory rather than assuming completion. Splitting preparation is not an idempotent loading or checkpoint system. Track each chunk and reconcile database outcomes before retrying. Memory usage is bounded by individual parsed records.

Run from the repository root:

```bash
python tools/split_sales_csv.py sample.csv prepared-parts --rows 10000
python tools/split_sales_csv.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
