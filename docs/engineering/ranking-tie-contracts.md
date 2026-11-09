# Define whether ranked reports retain ties

DENSE_RANK can return more than three rows when several products share a top-three revenue rank.

```sql
WITH totals(product, revenue) AS (VALUES ('A', 10.0), ('B', 10.0), ('C', 5.0))
SELECT product, revenue,
       DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM totals ORDER BY revenue DESC, product;
```

Do not replace a rank predicate with LIMIT merely to force a fixed number of products. If exactly N rows is the business requirement, define a deterministic tie-breaker and explain the changed meaning. Keep product ordering stable for reproducible saved outputs.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
