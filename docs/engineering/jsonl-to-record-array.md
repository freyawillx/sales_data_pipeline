# Convert JSON Lines into an explicit record array

A JSONL source cannot be made into a JSON array by blindly adding brackets around raw lines.

```python
import json
source_lines = ['{"product":"A","quantity":1}', '{"product":"B","quantity":2}']
records = [json.loads(line) for line in source_lines]
assert all(isinstance(record, dict) for record in records)
serialized = json.dumps(records, ensure_ascii=True)
assert len(json.loads(serialized)) == 2
```

This conversion materializes all records, so it is not a streaming-memory guarantee. Require all four sales fields before loading. Empty lines and malformed objects need an explicit source policy, and a valid array root does not establish valid dates or numeric values.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
