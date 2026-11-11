# Rerun and retry precautions

Loading the same input twice appends the same values twice. The current table
has no source-event key and the loader has no upsert, batch marker, or automatic
deduplication. Cleaning a frame repeatedly does not change that behavior.

Before retrying a production job:

1. Record the source path, content digest, expected rows, and intended table.
2. Check whether a previous attempt reached the insertion commit.
3. Compare destination counts and values for the relevant date range.
4. Ask the data owner to resolve an ambiguous result before rerunning.

An investigation query can expose repeated values:

```sql
SELECT date, product, quantity, price, COUNT(*) AS copies
FROM sales GROUP BY date, product, quantity, price
HAVING COUNT(*) > 1;
```

Identical values are not proof of duplicates. Two legitimate transactions can
have the same date, product, quantity, and price. Never automatically remove
all repeated groups based on those four columns.

A durable idempotency design needs a stable source identifier or a separately
tracked batch identity and transaction policy. Document late-arriving records,
corrected files, rollback behavior, and concurrency before implementing one.
Until then, serialize runs operationally and retain a load manifest outside
the table. A content hash can identify a file, but it cannot distinguish
legitimate identical transactions inside it.
