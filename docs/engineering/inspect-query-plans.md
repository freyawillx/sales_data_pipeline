# Inspect aggregation plans before adding indexes

An index does not automatically make an all-history sales aggregation faster.

```sql
EXPLAIN
SELECT date, SUM(quantity * price) AS revenue
FROM sales GROUP BY date ORDER BY date;
```

Plain EXPLAIN inspects a plan without executing the query. EXPLAIN ANALYZE executes it and should be used deliberately under an agreed workload budget. Measure representative data and remember that additional indexes also increase insertion work.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
