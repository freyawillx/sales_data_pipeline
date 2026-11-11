# a reproducible runtime version report

Captures the active interpreter and installed runtime versions to accompany bug reports or benchmark results. Missing packages are represented by null rather than silently omitted. Output files are created exclusively and never overwritten. No database connection, credential lookup, environment dump, hostname, or user directory is included. This is an observation of the current environment, not a dependency lockfile or a guarantee that a different platform can install the same distributions. Keep source revision and input digest alongside it for fuller reproducibility.

Run from the repository root:

```bash
python tools/capture_runtime_versions.py --output runtime-versions.json
python tools/capture_runtime_versions.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
