# a non-mutating sales quality profile

Reports overlapping defect counts, including nonfinite and fractional quantities the current cleaner does not safely reject. It does not predict an exact retained-row count because multiple rules can apply to one row and its stricter checks differ from the cleaner. Only aggregate counts are printed. pandas loads the full CSV in memory; NumPy is already a pandas dependency. Date inference follows pandas defaults, so establish a source-specific date policy separately.

Run from the repository root:

```bash
python tools/profile_sales_quality.py sample.csv
python tools/profile_sales_quality.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
