# Prepare JSON sales records

The `.json` reader expects one complete JSON document whose root is an array
of objects. An object containing a `sales` array is not the same contract.

```json
[
  {"date":"2024-01-01","product":"Widget","quantity":2,"price":3.5},
  {"date":"2024-01-02","product":"Other","quantity":1,"price":0.0}
]
```

Generate portable JSON with Python rather than concatenating strings:

```python
import json
from pathlib import Path
rows = [{"date": "2024-01-01", "product": "Caf\u00e9", "quantity": 2, "price": 3.5}]
Path("sample.json").write_text(json.dumps(rows, ensure_ascii=True), encoding="ascii")
```

Escaped Unicode is useful because the current reader opens the file using
the platform's default text encoding. Literal non-ASCII files need a matching
default encoding or a deliberate reader change. The serialized product above
still becomes `Café` in memory.

Validate shape with `read_json("sample.json")`, then apply
`clean_sales_data`. Array members that are numbers, strings, arrays, or null
are rejected. An empty array is valid JSON but produces no required columns,
so it cannot pass straight into the current cleaner. Syntactically valid JSON
is not proof of valid business data: missing fields and invalid numeric values
are checked later. The CLI invocation is `python pipeline.py sample.json`.
