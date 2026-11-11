# Use JSON Lines input

JSON Lines places one complete JSON object on each line, with no surrounding
array and no comma between records:

```jsonl
{"date":"2024-01-01","product":"Widget","quantity":2,"price":3.5}
{"date":"2024-01-02","product":"Other","quantity":1,"price":4.0}
```

Save it as `sample.jsonl` and run `python pipeline.py sample.jsonl` after
preparing a disposable PostgreSQL destination. To inspect without writing:

```python
from pipeline import read_json_lines
from utils.data_cleaner import clean_sales_data
source = read_json_lines("sample.jsonl")
cleaned = clean_sales_data(source)
print(len(source), len(cleaned))
```

This path delegates to `pandas.read_json(..., lines=True)`. It does not use
the array-shape validation in `read_json`. Normalize records so they expose
all four required fields, and test the result before loading it. Malformed
JSON lines can abort the read; there is no dead-letter file or per-line retry.

JSONL is an input format here, not a streaming execution guarantee. The reader
still creates a full DataFrame, cleaning copies it, and the loader builds a
list of rows. A file too large for available memory needs an explicitly
designed chunked workflow, including failure and duplicate handling.
