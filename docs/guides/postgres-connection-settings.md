# Configure the PostgreSQL connection

`utils/db_loader.py` reads libpq-style environment variables at connection time:

| Variable | Code default |
| --- | --- |
| `PGDATABASE` | `salesdb` |
| `PGUSER` | No explicit value |
| `PGPASSWORD` | No explicit value |
| `PGHOST` | `localhost` |
| `PGPORT` | `5432` |

For example, in PowerShell, set nonsecret connection details before running:

```powershell
$env:PGDATABASE = 'salesdb'
$env:PGUSER = 'sales_loader'
$env:PGHOST = 'localhost'
$env:PGPORT = '5432'
python pipeline.py sample.csv sales
```

Supply authentication using your approved PostgreSQL credential mechanism.
Do not paste real passwords into committed examples, shell transcripts, or
issue reports. This project does not load a `.env` file automatically: creating
such a file alone does not populate `os.getenv`.

Test connectivity separately with `psql -X -c 'SELECT current_database(), current_user;'`
using the same process environment. A successful connection does not imply
the role can create or insert into the target table. Prefer a dedicated role
restricted to the destination schema and operations actually required.

For remote connections, arrange certificate validation and transport settings
through a reviewed libpq configuration. Never disable verification merely to
suppress an error. Avoid printing the full process environment when debugging.
