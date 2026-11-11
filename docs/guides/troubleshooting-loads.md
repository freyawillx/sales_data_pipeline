# Diagnose a failed sales load

Preserve the input and exact exception before retrying. The loader is not
idempotent, and a failure report does not by itself establish what the
database committed.

| Symptom | First check |
| --- | --- |
| Usage text | Supply an input path to `pipeline.py` |
| Unsupported format | Use a lowercase `.csv`, `.json`, or `.jsonl` suffix |
| File not found | Check the current working directory and resolved path |
| Missing-column KeyError | Inspect exact header names and JSON fields |
| JSON array-of-objects error | Use an array root with object members |
| Integer conversion exception | Check fractional, infinite, and oversized quantities |
| PostgreSQL authentication failure | Verify role, database, environment, and credential mechanism |
| `NameError: execute_values` | Check the batching helper import in the loader |

Separate parsing and cleaning from database access:

```python
from pipeline import read_csv
from utils.data_cleaner import clean_sales_data
raw = read_csv("sample.csv")
print(raw.columns.tolist(), len(raw))
clean = clean_sales_data(raw)
print("retained", len(clean))
```

Avoid dumping entire sensitive datasets or environment variables into issue
reports. Reduce the case to synthetic rows that reproduce the failure.
Before a retry, inspect destination row counts and the relevant date range.
If the insert outcome is uncertain, reconcile it instead of assuming zero
rows were written. Record the Python and dependency versions with the error.
