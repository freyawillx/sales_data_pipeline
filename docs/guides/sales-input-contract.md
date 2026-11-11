# Sales input contract

Every record needs these case-sensitive column names:

| Field | Intended value | Cleaner behavior |
| --- | --- | --- |
| `date` | Unambiguous calendar date such as `2024-01-31` | Parsed by pandas; unparseable dates are removed |
| `product` | Nonblank product label | Missing and whitespace-only values are removed |
| `quantity` | Nonnegative whole units | Numeric coercion, integer conversion, then negative filtering |
| `price` | Nonnegative price per unit | Numeric coercion, floating-point conversion, then negative filtering |

```json
[{"date":"2024-01-31","product":"Widget","quantity":2,"price":3.5}]
```

Supply whole-number quantities. The current cleaner converts to integers
before sign filtering and can truncate fractions rather than rejecting them.
Validate finiteness upstream as infinity is not a supported business value.
Missing required columns cause an error; they are not filled automatically.

Extra source columns survive cleaning but are not written by the database
loader. There is no order ID, currency, customer, tax, discount, refund, or
source-event identifier in the stored schema. Do not infer those facts from
row position or product names. Negative quantities and prices are removed,
so this contract cannot represent returns without an explicit design change.

Keep a small accepted/rejected input fixture with each source integration.
Compare retained row counts after cleaning before permitting a production load.
