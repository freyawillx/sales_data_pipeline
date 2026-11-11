# Handle a lost connection near commit without a blind retry

A client can lose its response after a server has committed, leaving the outcome uncertain.

```python
run = {"source_sha256":"recorded-outside-this-example",
       "parsed_rows":100, "retained_rows":98,
       "destination":"sales", "outcome":"unknown"}
assert run["outcome"] == "unknown"
# Reconcile destination evidence before changing this to success or retrying.
```

The current table has no batch ID or source-event key, so a count alone may not resolve concurrent writes. Preserve immutable source evidence and escalate ambiguous outcomes to the data owner. A rollback request after a broken connection is not proof that a previous commit did not occur.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
