# Normalize source-specific price notation explicitly

Thousands separators and decimal commas must be interpreted under a declared locale convention.

```python
from decimal import Decimal
source_price = "1.234,50"
# This source contract declares dot thousands and comma decimal marks.
normalized = source_price.replace(".", "").replace(",", ".")
value = Decimal(normalized)
assert value == Decimal("1234.50")
```

This transformation is valid only for the stated source convention. It is not a universal sanitizer. Reject mixed conventions and unexpected currency symbols. Converting through float afterward follows the current pipeline's approximate-price model, not an exact ledger.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
