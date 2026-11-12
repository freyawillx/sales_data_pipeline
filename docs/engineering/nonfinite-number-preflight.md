# Distinguish nonfinite numbers from ordinary missing values

Infinity can survive numeric coercion and later break conversion or contaminate totals.

```python
import math
values = [3.5, float("nan"), float("inf"), -float("inf")]
finite = [value for value in values if math.isfinite(value)]
assert finite == [3.5]
```

A value being numeric is not enough to make it a valid price or quantity. Strict validation should check finiteness, sign, integer requirements, and storage bounds independently. Profile aggregate counts without printing sensitive records.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
