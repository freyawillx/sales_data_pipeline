# Recognize a UTF-8 byte-order mark in source files

A leading BOM can be mistaken for part of a header or rejected by a JSON decoder using the wrong text mode.

```python
import json
payload = b'\xef\xbb\xbf[{"product":"Widget"}]'
rows = json.loads(payload.decode("utf-8-sig"))
assert rows[0]["product"] == "Widget"
```

Choose UTF-8 explicitly for a portable adapter. utf-8-sig also accepts ordinary UTF-8 without a BOM. Do not remove arbitrary leading characters to make a parse succeed; encoding detection and business schema validation are separate concerns.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
