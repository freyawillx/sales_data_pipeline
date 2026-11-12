# Audit exact source headers before cleaning

Unexpected capitalization or duplicate names can make a source ambiguous before any numeric validation begins.

```python
import csv
from io import StringIO
header = next(csv.reader(StringIO("date,product,quantity,price\n")))
required = {"date", "product", "quantity", "price"}
assert len(header) == len(set(header)), "duplicate headers"
assert required.issubset(header), "missing required fields"
```

Check the original header before pandas can rename duplicate columns. Do not silently lowercase or merge fields unless the source contract explicitly defines that mapping. Preserve the original spelling in any rejection report.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
