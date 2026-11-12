# Run related read-only reports on one database snapshot

Separate statements can otherwise observe different committed states while new sales are appended.

```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT COUNT(*) AS lines FROM sales;
SELECT SUM(quantity) AS units, SUM(quantity * price) AS revenue FROM sales;
ROLLBACK;
```

Use an agreed timeout and close the transaction promptly; read-only work still consumes resources. This is a reporting workflow, not a change to loader isolation. Check permissions and operational policy before running reports on a shared destination.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
