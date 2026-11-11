# Run the sales pipeline locally

The executable is `pipeline.py`. It requires a sales input path and writes to
PostgreSQL; it is not a CSV-export command. From a fresh checkout:

```bash
git clone https://github.com/freyawillx/sales_data_pipeline.git
cd sales_data_pipeline
python -m venv .venv
```

Activate `.venv` using `.venv/bin/activate` on a POSIX shell or
`.venv\Scripts\Activate.ps1` in PowerShell, then install with the selected Python:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Create a disposable PostgreSQL database named `salesdb`, set `PGUSER` and the
connection settings appropriate to it, and prepare `sample.csv`:

```csv
date,product,quantity,price
2024-01-01,Widget,2,3.50
```

```bash
python pipeline.py sample.csv sales
```

The destination is created if absent. Existing rows are retained and another
run appends again. Verify the inserted row before retrying a failed load.
Use a trusted simple table name; the current SQL builder interpolates it.
If a nonempty load raises `NameError: execute_values`, the batching helper
import is missing from `utils/db_loader.py`; install the fix before proceeding.
Keep credentials outside version control and use a local disposable database
while learning the workflow.
