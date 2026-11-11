# Check CSV chunk manifests with logical record counts

Chunk counts should follow parsed records rather than physical file lines.

```python
records, rows_per_chunk = 25001, 10000
expected_chunks = (records + rows_per_chunk - 1) // rows_per_chunk
assert expected_chunks == 3
assert sum([10000, 10000, 5001]) == records
```

The splitter repeats a header in each nonempty chunk; a header-only input produces no chunks. Verify each source and chunk digest, expected logical counts, and completion status. Prepared chunks do not make database retries safe without a load ledger and reconciliation policy.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
