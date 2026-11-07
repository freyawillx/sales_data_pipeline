# Compare saved query output using typed cells

Text CSV equality is too strict when SQL engines render equivalent dates or floats differently.

```python
import math
from datetime import date
left_date, right_date = "2024-01-01", "2024-01-01"
assert date.fromisoformat(left_date) == date.fromisoformat(right_date)
assert math.isclose(float("3.5000000001"), float("3.5"), rel_tol=1e-8, abs_tol=1e-8)
```

Choose tolerances based on the report's scale and contract. Keep NULL distinct from zero and empty text, and preserve row multiplicity. Only ignore row order when the result contract permits it; ranking and running-total queries explicitly depend on ordering.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
