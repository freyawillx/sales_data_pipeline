# Analyze sales without modifying the destination

Use a separate PostgreSQL role with SELECT access when exploring loaded data.
Avoid reusing a loader role that can create and insert tables merely because
its credentials are already convenient. For an interactive review session:

```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout = '30s';
SELECT date, SUM(quantity) AS units, SUM(quantity * price) AS revenue
FROM sales GROUP BY date ORDER BY date;
ROLLBACK;
```

The timeout is an example, not a recommended universal limit. Pick an agreed
budget appropriate to the data volume and operational workload. Read-only
transactions still consume resources and can conflict with maintenance.

For a reviewed query file, use
`psql -X -v ON_ERROR_STOP=1 -f path/to/query.sql`. Keep table names explicit
and inspect the file before execution. If consistent snapshots across several
reports are necessary, choose an isolation strategy with the database owner;
separate commands can otherwise see different committed datasets.

Remember the schema's limits: sales rows do not identify customers or orders,
prices use floating point, and a missing date may indicate no sales or no
import. Export only the fields needed for the task and apply your normal
access controls to report files as well as the source database.
