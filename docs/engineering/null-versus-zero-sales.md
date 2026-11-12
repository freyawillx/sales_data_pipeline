# Keep missing values distinct from legitimate zeros

The current cleaner retains zero quantities and zero prices but removes missing required values.

```python
import pandas as pd
from utils.data_cleaner import clean_sales_data
rows = pd.DataFrame({"date":["2024-01-01"]*2, "product":["Free","Missing"],
                     "quantity":[1,1], "price":[0.0,None]})
assert clean_sales_data(rows)["product"].tolist() == ["Free"]
```

Do not fill every missing price with zero merely to pass validation. A free promotion and an unknown price have different meanings. Track rejected records through your source manifest and obtain a correction when the value is genuinely unknown.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
