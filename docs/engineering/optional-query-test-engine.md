# Execute a query fixture without a PostgreSQL server

DuckDB can exercise the ordinary sales-query expressions on a small in-memory schema.

```python
from pathlib import Path
import duckdb
connection = duckdb.connect(":memory:")
try:
    connection.execute("CREATE TABLE sales(date DATE, product TEXT, quantity INTEGER, price DOUBLE)")
    connection.execute("INSERT INTO sales VALUES ('2024-01-01','A',2,3.5)")
    query = Path("examples/analytics/daily-sales-summary.sql").read_text(encoding="utf-8")
    assert connection.execute(query).fetchone()[3] == 7.0
finally:
    connection.close()
```

Install the optional duckdb package first. Successful execution in this engine is not a PostgreSQL integration test: privileges, driver adaptation, locking, catalog functions, and engine-specific behavior still need a disposable PostgreSQL environment.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
