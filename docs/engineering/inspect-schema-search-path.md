# Inspect schema resolution before loading a table name

A simple sales identifier resolves through the connection's search path.

```sql
SHOW search_path;
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name = 'sales'
ORDER BY table_schema;
```

Confirm the intended schema and role rather than assuming every database has the same public.sales table. The current CLI exposes one table-name string, not a separate schema argument. Keep destination selection trusted even after SQL identifier quoting is introduced.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
