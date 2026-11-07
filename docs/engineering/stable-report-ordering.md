# Use stable sorting when preparing review exports

A deterministic review order helps compare exports without changing the meaning of duplicate records.

```python
import pandas as pd
frame = pd.DataFrame({"date":["2024-01-02","2024-01-01","2024-01-01"],
                      "product":["B","A","A"], "source_record":[1,2,3]})
ordered = frame.sort_values(["date","product"], kind="stable")
assert ordered["source_record"].tolist() == [2,3,1]
```

Sorting does not deduplicate, reconcile, or establish an event sequence. Keep a source-record identifier as a deterministic tie-breaker when exact order matters. Database results need their own ORDER BY; physical insertion order is not a report contract.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
