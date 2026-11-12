# Understand why equivalent text files can have different hashes

A source digest identifies bytes, not the logical records those bytes encode.

```python
import hashlib
unix = b"a,b\n1,2\n"
windows = b"a,b\r\n1,2\r\n"
assert hashlib.sha256(unix).hexdigest() != hashlib.sha256(windows).hexdigest()
assert unix.splitlines() == windows.splitlines()
```

Record the original digest before normalization. If a workflow needs a semantic fingerprint, define canonical encoding, field order, types, row order, and duplicate treatment separately. Do not use newline-normalized hashes as a substitute for preserving the immutable source.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
