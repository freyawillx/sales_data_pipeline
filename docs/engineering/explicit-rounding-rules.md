# Make reporting rounding rules explicit

Rounding every line and rounding an aggregate can produce different displayed totals.

```python
from decimal import Decimal, ROUND_HALF_UP
values = [Decimal("0.005"), Decimal("0.005")]
cent = Decimal("0.01")
per_line = sum(v.quantize(cent, rounding=ROUND_HALF_UP) for v in values)
final = sum(values).quantize(cent, rounding=ROUND_HALF_UP)
assert per_line != final
```

This is a demonstration of a chosen arithmetic rule, not a recommendation for a particular accounting policy. The stored pipeline prices are floats. An exact-money redesign must preserve decimal values before insertion, not just round a binary approximation for display.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
