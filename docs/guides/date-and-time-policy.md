# Date interpretation policy

Prefer ISO-style `YYYY-MM-DD` calendar dates in source files. The cleaner uses
`pandas.to_datetime(..., errors="coerce")` without an explicit source format,
so ambiguous inputs such as `01/02/2024` should be resolved before ingestion.
A value becoming parseable does not prove it represents the intended day.

```python
import pandas as pd
source_dates = pd.Series(["2024-02-01", "2024-02-30"])
parsed = pd.to_datetime(source_dates, format="%Y-%m-%d", errors="coerce")
print(parsed.isna().tolist())
```

When adapting a source, agree on its calendar and timezone before discarding
any information. The destination column is PostgreSQL DATE, so it cannot
retain time-of-day or timezone. If incoming events use timestamps, define
which business timezone determines their sale date. Merely removing a UTC
timezone can assign an event to the wrong local calendar day.

The current pipeline has no timezone or date-format CLI options. Mixed
timestamp formats and mixed timezone values need dedicated normalization and
regression fixtures, including daylight-saving transitions where relevant.
Keep year-boundary and leap-day examples in source acceptance checks.

Reports should state whether their periods use calendar dates or a separate
fiscal calendar. A week starting Monday and a business week with a different
cutoff are different aggregations, even if both are called weekly sales.
