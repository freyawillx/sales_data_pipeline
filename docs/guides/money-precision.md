# Prices and monetary precision

The cleaner converts price to Python/pandas floating point, and the loader
creates a PostgreSQL FLOAT column. Decimal values such as 0.1 do not generally
have an exact binary floating-point representation. This affects totals and
equality comparisons even when displayed output looks rounded.

```python
from decimal import Decimal
print(0.1 + 0.2)
print(Decimal("0.1") + Decimal("0.2"))
```

Use revenue calculations from this schema for exploratory analysis with
documented tolerances. Do not describe them as an exact financial ledger.
Rounding every line and rounding a final total can produce different results;
the required rule belongs to the business contract.

An exact-money redesign needs coordinated changes: parse from decimal strings
without an intermediate float, preserve decimal values during cleaning, use
a chosen PostgreSQL NUMERIC precision/scale, and define currency and rounding.
Altering only the database column does not recover precision already lost
earlier in ingestion.

Reconcile against a trusted source using the same currency, date cutoff,
unit convention, and rounding policy. Record both absolute and relative
differences rather than silently adjusting records to match a total. This
schema has no currency field, so combining files in different currencies
cannot yield a meaningful single monetary total without an upstream contract.
