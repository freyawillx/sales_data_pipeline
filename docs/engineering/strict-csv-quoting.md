# Check CSV quoting with the standard library parser

A permissive parser can accept trailing junk after a closing quote.

```python
import csv
from io import StringIO
malformed = 'date,product,quantity,price\n2024-01-01,"Widget"junk,1,2\n'
try:
    list(csv.reader(StringIO(malformed), strict=True))
except csv.Error:
    print("rejected malformed quoting")
else:
    raise AssertionError("malformed input was accepted")
```

Strict syntax validation is separate from business validation. Correct quoting does not make a negative quantity valid. Quoted commas, escaped quotes, and embedded newlines are valid CSV features and should not be removed by hand-written line splitting.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
