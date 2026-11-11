# Detect duplicate CSV headers before type inference

Duplicate required fields have no unambiguous mapping to one stored database column.

```python
import csv
from collections import Counter
from io import StringIO
header = next(csv.reader(StringIO("date,product,quantity,price,price\n")))
duplicates = [name for name, count in Counter(header).items() if count > 1]
assert duplicates == ["price"]
```

Reject or explicitly map a duplicate header at the source boundary. A renamed price.1 column is not evidence that the correct price was selected. Retain only synthetic header examples when discussing malformed inputs in public issues.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
