# Normalize agreed numeric fields before CSV reconciliation

The reconciliation utility compares strings exactly, so 3.50 and 3.5 differ even when their decimal values match.

```python
from decimal import Decimal
left = {"quantity":"2", "price":"3.50"}
right = {"quantity":"2.0", "price":"3.5"}
key = lambda row: (Decimal(row["quantity"]), Decimal(row["price"]))
assert key(left) == key(right)
```

Normalize only fields whose numeric interpretation is agreed. Product identifiers must remain text, and dates need a separate canonical rule. Preserve duplicate multiplicity after normalization instead of comparing sets, which would hide repeated rows.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
