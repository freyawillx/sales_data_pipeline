import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os

def load_to_postgres(df: pd.DataFrame, table_name="sales"):
    conn = psycopg2.connect(
        dbname=os.getenv('PGDATABASE', 'salesdb'),
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        host=os.getenv('PGHOST', 'localhost'),
        port=os.getenv('PGPORT', '5432')
    )
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date DATE,
            product TEXT,
            quantity INTEGER,
            price FLOAT
        );
    """)
    conn.commit()

    rows = list(df[['date', 'product', 'quantity', 'price']].itertuples(index=False, name=None))
    if rows:
        execute_values(
            cursor,
            f"INSERT INTO {table_name} (date, product, quantity, price) VALUES %s;",
            rows,
            page_size=1000,
        )
    conn.commit()
    conn.close()
    print(f"✅ Loaded {len(df)} rows into table '{table_name}'.")
