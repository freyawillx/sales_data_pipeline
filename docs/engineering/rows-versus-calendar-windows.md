# Distinguish observation windows from calendar windows

Seven recorded observations and seven calendar days differ when the source has date gaps.

```sql
WITH daily(date, revenue) AS (
  VALUES (DATE '2024-01-01', 10.0), (DATE '2024-02-01', 20.0)
)
SELECT date,
  AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS observation_mean,
  AVG(revenue) OVER (ORDER BY CAST(date AS TIMESTAMP)
    RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW) AS calendar_mean
FROM daily ORDER BY date;
```

Neither query fills missing dates with zero. A calendar-window mean still divides by recorded observations in that interval. State the denominator explicitly before comparing moving averages across products or periods with different data coverage.

This example is a focused adapter, check, or reporting workflow. It does not add
an undocumented CLI option or silently change ingestion defaults. Review it
against your source contract and use synthetic or disposable data first. Python
examples need the runtime requirements; the DuckDB example additionally needs
its optional package. SQL examples target PostgreSQL unless stated otherwise.
Keep exact source identity and expected outcomes alongside any production run.
