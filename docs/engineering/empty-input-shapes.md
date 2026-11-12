# Distinguish an empty record array from an empty typed batch

A JSON empty array produces a frame without columns, while a header-only CSV has a known schema.

```python
import pandas as pd
required = ["date", "product", "quantity", "price"]
no_schema = pd.DataFrame([])
typed_empty = pd.DataFrame([], columns=required)
assert no_schema.empty and typed_empty.empty
assert list(no_schema.columns) != list(typed_empty.columns)
```

Decide whether an empty source is valid before synthesizing its schema. Do not create columns merely to hide a missing-header defect. Record parsed and retained counts independently and decide with the source owner whether a zero-row batch should be loaded.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
