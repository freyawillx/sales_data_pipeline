# Package a synthetic fixture with its query and runtime evidence

A saved result is easier to review when its source data, calculation, and environment are identifiable.

```python
import hashlib
source = b"date,product,quantity,price\n2024-01-01,A,2,3.5\n"
manifest = {"source_sha256":hashlib.sha256(source).hexdigest(),
            "expected_units":2, "expected_revenue":7.0,
            "query":"examples/analytics/daily-sales-summary.sql"}
assert manifest["expected_units"] == 2
```

Use synthetic names and values rather than copying customer data into a public regression. Record NULL representation and numeric tolerances for saved CSV output. An engine-specific fixture run validates that engine and dataset, not a live PostgreSQL deployment or every future input.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
