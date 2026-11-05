# Check that grouped reports conserve source totals

A daily or product aggregation should not silently lose or multiply ordinary source lines.

```python
rows = [{"date":"2024-01-01", "quantity":2, "price":3.5},
        {"date":"2024-01-02", "quantity":1, "price":4.0}]
daily = {}
for row in rows:
    daily[row["date"]] = daily.get(row["date"], 0) + row["quantity"] * row["price"]
assert sum(daily.values()) == 11.0
```

Compare SQL grouped revenue and units with independent source calculations under the same filters. This invariant does not establish that duplicates are absent: the same duplicate can be included consistently in both sides. Include empty and zero-total cases separately.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
