import pandas as pd
import json
import sys
from utils.data_cleaner import clean_sales_data
from utils.db_loader import load_to_postgres

def read_csv(path):
    print(f"📥 Reading CSV: {path}")
    return pd.read_csv(path)

def read_json(path):
    print(f"📥 Reading JSON: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def main():
    if len(sys.argv) < 2:
        print("❗ Usage: python pipeline.py <data_file> [table_name]")
        sys.exit(1)

    file_path = sys.argv[1]
    table_name = sys.argv[2] if len(sys.argv) > 2 else "sales"

    if file_path.endswith(".csv"):
        df = read_csv(file_path)
    elif file_path.endswith(".json"):
        df = read_json(file_path)
    else:
        print("❗ Supported formats: .csv, .json")
        sys.exit(1)

    df_clean = clean_sales_data(df)
    if df_clean.empty:
        print('No valid sales rows to load.')
        return
    load_to_postgres(df_clean, table_name)

if __name__ == "__main__":
    main()
