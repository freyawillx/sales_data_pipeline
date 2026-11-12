# Compare runtime reports when a source behaves differently

Unpinned runtime requirements can produce different inference or warnings after an upgrade.

```python
import importlib.metadata
import platform
report = {"python": platform.python_version(),
          "pandas": importlib.metadata.version("pandas"),
          "psycopg2-binary": importlib.metadata.version("psycopg2-binary")}
print(report)
```

Use tools/capture_runtime_versions.py for a portable JSON report. Attach the source digest, source revision, and a synthetic reproducer as well. A version snapshot describes one environment; it does not replace a reviewed lockfile or a cross-platform compatibility check.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
