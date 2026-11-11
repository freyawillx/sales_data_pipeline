# Prepare CSV sales safely

Use a comma-delimited file with exactly spelled required headers. Quote fields
containing commas using normal CSV quoting, rather than manually splitting
strings on commas:

```csv
date,product,quantity,price
2024-01-01,"Widget, deluxe",2,3.50
2024-01-02,"A ""quoted"" product",1,5.00
```

Inspect and clean without opening a database connection:

```python
from pipeline import read_csv
from utils.data_cleaner import clean_sales_data
source = read_csv("sample.csv")
cleaned = clean_sales_data(source)
print({"input_rows": len(source), "retained_rows": len(cleaned)})
print(cleaned.to_string(index=False))
```

Numeric formatting is not locale-aware. Values such as `1,234.50` or `3,50`
should be normalized deliberately before this reader; do not assume that
quoting a localized number makes it a supported numeric value. pandas also
recognizes some default missing-value tokens during CSV parsing, which can
affect a product label that resembles such a token.

The CLI recognizes lowercase `.csv`. It has no delimiter or encoding flag.
A header-only CSV supplies the schema but no rows; a completely empty file
is a parser error. Confirm the header and retained count before running
`python pipeline.py sample.csv`. Repeating that command appends rows again.
