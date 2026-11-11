# Back up and verify a sales destination

Treat a dump as sensitive data and store it under your normal retention and
access policy. Use PostgreSQL's tools with the same reviewed connection
environment, keeping credentials out of command text:

```bash
pg_dump --format=custom --table=public.sales --file=sales.dump salesdb
pg_restore --list sales.dump
```

Substitute the actual schema and table. Listing a dump verifies that an
archive can be read; it does not establish that a complete restore works.
Restore into a newly provisioned disposable database, never over the live
destination as a casual test:

```bash
pg_restore --dbname=sales_restore_check --no-owner --no-privileges sales.dump
```

This assumes `sales_restore_check` already exists and is empty. Review tool
output and errors. Compare counts, date endpoints, total units, and product
coverage with a source snapshot recorded at backup time. Approximate revenue
totals alone are insufficient because prices are floating point and offsetting
row errors can cancel in an aggregate.

Document PostgreSQL/tool compatibility, role provisioning, restoration time,
and how the application will reconnect after a real recovery. A table-only
dump is not a backup of every role, setting, extension, or related dataset.
Keep an immutable source manifest if reloading original files is part of the
recovery plan, and account for duplicate risk during replay.
