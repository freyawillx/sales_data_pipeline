# Destination identifiers and transaction safety

The loader composes its destination using `psycopg2.sql.Identifier`. Table names
are quoted as identifiers rather than interpolated as executable SQL. Data values
continue to be passed through the driver's batch-insert helper.

The argument represents one table identifier. A string such as `public.sales`
is quoted as a single name containing a dot; it is not a schema/table pair.
Use `sales` under the intended connection search path. Schema-qualified support
would need an explicit interface and separate identifier components.

Creating the table and inserting the batch share one transaction. Successful
loads commit once; exceptions trigger rollback. Cursor and connection resources
are closed after success or failure. Existing data still remains in place, and
another successful run still appends duplicate values.

Keep a dedicated database role and trusted destination configuration. Correct
quoting does not grant privileges or decide which table a caller should access.
The regression suite mocks the connection boundary and verifies composition,
single-commit behavior, rollback, and cleanup. It does not substitute for a
disposable-database integration test of PostgreSQL permissions and transactions.
