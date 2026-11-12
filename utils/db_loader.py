import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values


def load_to_postgres(df: pd.DataFrame, table_name="sales"):
    """Append a batch atomically, quoting the destination as one SQL identifier."""
    if not isinstance(table_name, str) or not table_name.strip():
        raise ValueError("table_name must be a nonblank table identifier")
    rows = list(df[["date", "product", "quantity", "price"]].itertuples(index=False, name=None))
    identifier = sql.Identifier(table_name)
    connection = psycopg2.connect(
        dbname=os.getenv("PGDATABASE", "salesdb"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
    )
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                date DATE, product TEXT, quantity INTEGER, price FLOAT
            );
        """).format(identifier))
        if rows:
            execute_values(cursor,
                sql.SQL("INSERT INTO {} (date, product, quantity, price) VALUES %s;").format(identifier),
                rows, page_size=1000)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            connection.close()
    print(f"Loaded {len(rows)} rows into table {table_name!r}.")
