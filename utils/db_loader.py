import pandas as pd
import psycopg2
from psycopg2 import sql

def load_to_postgres(df: pd.DataFrame, table_name="sales"):
    conn = psycopg2.connect(
        dbname="salesdb",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {} (
            date DATE,
            product TEXT,
            quantity INTEGER,
            price FLOAT
        );
    """).format(sql.Identifier(table_name)))
    conn.commit()

    for _, row in df.iterrows():
        cursor.execute(
            sql.SQL("INSERT INTO {} (date, product, quantity, price) VALUES (%s, %s, %s, %s);").format(sql.Identifier(table_name)),
            (row["date"], row["product"], row["quantity"], row["price"])
        )
    conn.commit()
    conn.close()
    print(f"✅ Loaded {len(df)} rows into table '{table_name}'.")
