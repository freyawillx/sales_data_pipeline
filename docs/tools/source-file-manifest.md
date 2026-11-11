# streaming SHA-256 source file manifests

Hashes source bytes in fixed-size blocks and records size and supplied path. An existing manifest is never overwritten. A size/mtime check catches ordinary concurrent changes but is not a locking protocol; use immutable files for reliable provenance. Identical byte digests identify identical file contents, not distinct transactions or successful database loads. The manifest itself can disclose filenames, so store it under the appropriate access policy. It contains no sales values or credentials.

Run from the repository root:

```bash
python tools/source_file_manifest.py sample.csv --output source-manifest.json
python tools/source_file_manifest.py --help
```

This is an optional local utility. It does not connect to PostgreSQL or alter
the pipeline's default execution path. File arguments are local paths; keep
source and output files under appropriate data access controls. Use a small
synthetic input to verify the workflow before processing business data.
