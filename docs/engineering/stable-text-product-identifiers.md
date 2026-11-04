# Keep leading zeros in text product identifiers

A numeric-looking product code is an identifier, not a quantity.

```python
from io import StringIO
import pandas as pd
source = "date,product,quantity,price\n2024-01-01,0007,2,3.5\n"
adapted = pd.read_csv(StringIO(source), dtype={"product": "string"})
assert adapted.iloc[0]["product"] == "0007"
```

The existing CSV reader does not set this dtype explicitly. Passing a normalized CSV back through inference can lose the zeros again, so use a reviewed adapter or a JSON string contract. Do not infer product identity from numeric equality.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
