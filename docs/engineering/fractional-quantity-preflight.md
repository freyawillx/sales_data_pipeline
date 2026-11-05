# Reject fractional quantities before integer conversion

The cleaner converts quantities to integers, which can truncate a fractional input rather than rejecting it.

```python
from decimal import Decimal
quantity = Decimal("2.5")
accepted = (quantity.is_finite() and quantity >= 0
            and quantity == quantity.to_integral_value()
            and quantity <= 2147483647)
assert not accepted
```

Use tools/validate_sales_file.py for strict CSV preflight. Decide separately whether a business needs fractional units; supporting them would require a schema and cleaner change. Never repair a fractional value by rounding without a source-owner rule.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
