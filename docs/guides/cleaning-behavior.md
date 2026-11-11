# Understand what cleaning does

`clean_sales_data` copies the input frame, removes rows missing required
values, rejects blank product labels, parses dates, coerces quantities and
prices, and filters negative converted values. It preserves surviving row
indexes and does not sort, deduplicate, or normalize product spelling.

```python
import pandas as pd
from utils.data_cleaner import clean_sales_data
raw = pd.DataFrame([
    {"date":"2024-01-01","product":"Widget","quantity":"2","price":"3.50"},
    {"date":"not-a-date","product":"Other","quantity":"1","price":"4.00"},
])
clean = clean_sales_data(raw)
assert len(raw) == 2
assert len(clean) == 1
```

Review counts before and after cleaning. Removed records are not written to
a rejection sink, and the function does not explain each rejection. Preserve
the original input securely if diagnosis or reconciliation is required.

Current limitations matter: integer conversion can truncate fractional
quantities; infinity is not handled as a clear validation error; and
missing columns raise rather than being synthesized. A nonblank product
such as ` Widget ` keeps its spaces. Extra fields survive cleaning but the
loader selects only the four database columns.

Repeated cleaning of supported valid data should be stable. Repeated loading
is a separate operation and appends records again. Do not confuse the two
kinds of repeatability when building a scheduler.
