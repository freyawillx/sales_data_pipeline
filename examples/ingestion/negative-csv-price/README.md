# Ingestion example: negative csv price

Negative prices are excluded independently of otherwise valid fields.

The source has 2 records. Cleaning retains 1.
`expected.csv` contains the actual cleaned values, with dates serialized as
calendar dates. This synthetic example performs no database writes.

Run from the repository root:

```python
from io import StringIO
from pathlib import Path
import pandas as pd
from pipeline import read_csv
from utils.data_cleaner import clean_sales_data

folder = Path("examples/ingestion/negative-csv-price")
clean = clean_sales_data(read_csv(folder / "input.csv"))
actual = clean.to_csv(index=False, date_format="%Y-%m-%d", lineterminator="\n")
assert actual == (folder / "expected.csv").read_text(encoding="utf-8")
```

The fixture was exercised with the real reader and cleaner. Its expected product
labels were checked independently before saving the output. CSV formatting may
vary across pandas versions; investigate a textual difference before changing
the business expectation. This is a focused cleaning example, not a claim that
all source data is accepted or that a PostgreSQL transaction succeeds. Loading
again with the CLI would append rows again; run the example above for validation.
