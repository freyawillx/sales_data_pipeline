# Preserve product labels that resemble missing-value tokens

CSV inference can interpret labels such as NA as missing instead of as product text.

```python
from io import StringIO
import pandas as pd
source = "date,product,quantity,price\n2024-01-01,NA,2,3.5\n"
adapted = pd.read_csv(StringIO(source), keep_default_na=False)
assert adapted.iloc[0]["product"] == "NA"
```

This is an explicit source-adapter policy, not a flag provided by the CLI. Empty numeric strings still need numeric validation. Decide which tokens mean missing in each field rather than applying a global replacement after data loss has occurred.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
