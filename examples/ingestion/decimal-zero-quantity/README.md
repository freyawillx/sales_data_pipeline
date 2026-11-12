# Ingestion example: decimal zero quantity

A whole-valued decimal string can represent zero units; textual scale is not retained.

The source has 1 records. Cleaning retains 1.
`expected.csv` contains the actual cleaned values, with dates serialized as
calendar dates. This synthetic example performs no database writes.

Run from the repository root:

```python
from io import StringIO
from pathlib import Path
import pandas as pd
from pipeline import read_json_lines
from utils.data_cleaner import clean_sales_data

folder = Path("examples/ingestion/decimal-zero-quantity")
clean = clean_sales_data(read_json_lines(folder / "input.jsonl"))
actual = clean.to_csv(index=False, date_format="%Y-%m-%d", lineterminator="\n")
assert actual == (folder / "expected.csv").read_text(encoding="utf-8")
```

The fixture was exercised with the real reader and cleaner. Its expected product
labels were checked independently before saving the output. CSV formatting may
vary across pandas versions; investigate a textual difference before changing
the business expectation. This is a focused cleaning example, not a claim that
all source data is accepted or that a PostgreSQL transaction succeeds. Loading
again with the CLI would append rows again; run the example above for validation.
