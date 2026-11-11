# Observe pipeline runs

The CLI prints basic progress, but it has no structured run record or rejected
row report. Capture a small operational manifest around each invocation:

| Metric | Why record it |
| --- | --- |
| Source digest and size | Identify the exact immutable input |
| Parsed and retained row counts | Detect unexpected filtering |
| Minimum and maximum sale date | Detect stale or misplaced periods |
| Total units | Reconcile volume independently of price |
| Runtime, exit code, and error class | Diagnose execution failures |
| Destination database and trusted table | Establish where the run was intended |

Avoid storing product-level sensitive information unless necessary. Never
place credentials in the manifest. A count of retained rows is not proof
that they were committed; reconcile against the destination after a load.

```python
from pipeline import read_csv
from utils.data_cleaner import clean_sales_data
raw = read_csv("sample.csv")
clean = clean_sales_data(raw)
print({"parsed_rows": len(raw), "retained_rows": len(clean),
       "removed_rows": len(raw) - len(clean)})
```

Set alert thresholds with the source owner. An empty file may be legitimate
on a closure day but suspicious during normal trading. Compare periods with
matching coverage and distinguish no sales from missing ingestion. The schema
has no batch ID, so ambiguous partial outcomes still need careful reconciliation
rather than an automatic retry driven only by metrics.
