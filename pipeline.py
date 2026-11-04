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
    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError('JSON input must be an array of sales objects')
    return pd.DataFrame(data)

def read_json_lines(path):
    print(f"Reading JSON Lines: {path}")
    return pd.read_json(path, lines=True)


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
    elif file_path.endswith(".jsonl"):
        df = read_json_lines(file_path)
    else:
        print("❗ Supported formats: .csv, .json, .jsonl")
        sys.exit(1)

    df_clean = clean_sales_data(df)
    load_to_postgres(df_clean, table_name)

if __name__ == "__main__":
    main()
