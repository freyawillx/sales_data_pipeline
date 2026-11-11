# Schedule the existing CLI

A scheduler should use an explicit interpreter, working directory, input
path, and destination. For example, a POSIX wrapper can invoke an installed
environment without relying on interactive activation:

```bash
/opt/sales/.venv/bin/python /opt/sales/pipeline.py /data/incoming/sales.csv sales
```

The paths are deployment examples; provision them deliberately. Inject
database settings through the scheduler's credential mechanism and record
stdout, stderr, exit status, source digest, and start/end timestamps. Never
log the whole environment to capture configuration.

Prevent overlapping runs operationally. The application has no lock, batch
ledger, idempotency key, or checkpoint. An automatic retry can duplicate rows
if the previous execution committed before the scheduler lost its result.
Route ambiguous failures for reconciliation rather than blindly rerunning.

Pin and review dependency versions in the deployment process, while preserving
a tested upgrade path. Validate a new input source with a disposable database
before scheduling it against a shared destination. Keep immutable source files
until your retention policy permits removal.

A zero exit status should be accompanied by row-count and coverage checks.
The cleaner can remove invalid records, so process success is not equivalent
to complete business-data acceptance. Escalate unexpectedly empty or heavily
filtered batches using thresholds agreed with the data owner.
