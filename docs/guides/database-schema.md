# Stored sales schema

The loader creates the following columns if its destination table is absent:

```sql
CREATE TABLE sales (
    date DATE,
    product TEXT,
    quantity INTEGER,
    price FLOAT
);
```

The actual command uses `CREATE TABLE IF NOT EXISTS`. It does not migrate an
existing incompatible table, inspect its constraints, add missing columns,
or erase old rows. Use schema introspection before loading into a database
that was initialized by a different application:

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = current_schema() AND table_name = 'sales'
ORDER BY ordinal_position;
```

Every successful run appends rows. There is no primary key, source identifier,
unique constraint, currency, ingestion timestamp, or load-batch identifier.
The table also lacks NOT NULL and nonnegative CHECK constraints, so direct
writes can bypass rules imposed by the Python cleaner.

The loader inserts only `date`, `product`, `quantity`, and `price` even if an
input frame contains other columns. Timestamps are written into a DATE column,
so time-of-day is not retained. PostgreSQL INTEGER has a finite range: validate
large quantities before loading. Any schema extension should include an
explicit migration, compatible loader change, and recovery procedure.
