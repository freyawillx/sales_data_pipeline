# Distinguish CSV records from physical source lines

Embedded newlines mean a logical sales record can consume multiple file lines.

```python
import csv
from io import StringIO
source = 'date,product,quantity,price\n2024-01-01,"Multi\nline",1,2\n'
reader = csv.DictReader(StringIO(source))
records = [(number, reader.line_num, row) for number, row in enumerate(reader, 1)]
assert len(records) == 1
assert records[0][1] == 3
```

A source-record number and parser line number answer different diagnostic questions. Record both when building a rejection workflow. Chunk using parsed records rather than operating-system line counts, so a quoted product is never cut in half.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
