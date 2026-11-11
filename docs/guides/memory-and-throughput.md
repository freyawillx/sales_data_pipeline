# Memory and throughput limits

The readers materialize an entire DataFrame. Cleaning first copies it, and
`load_to_postgres` builds a Python list of the four selected fields before
calling `execute_values` with `page_size=1000`. That page size batches SQL
insertion; it does not limit the memory used to read or clean a file.

Inspect the source frame's memory footprint without touching PostgreSQL:

```python
from pipeline import read_csv
frame = read_csv("sample.csv")
print("rows", len(frame))
print("dataframe_bytes", int(frame.memory_usage(index=True, deep=True).sum()))
```

This estimate excludes interpreter overhead, temporary copies, and the later
row list. Measure process peak memory on representative input as well as wall
time. Compare the same input, dependency versions, database configuration,
and destination state when evaluating a change.

Splitting a source into files changes retry and commit boundaries. A future
chunked reader must define how partial success, rejected records, duplicates,
and source ordering are tracked. Do not assume that reducing a batch size
alone makes an entire run streaming or atomic.

Benchmark in a disposable environment first. Avoid printing every row while
measuring throughput; console I/O can dominate small runs. For PostgreSQL,
inspect workload and query plans before adding indexes, since each index
also adds work to insertion.
