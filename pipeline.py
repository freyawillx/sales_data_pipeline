import pandas as pd
import json
import argparse
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
    parser = argparse.ArgumentParser(description='Clean sales data')
    parser.add_argument('data_file')
    parser.add_argument('table_name', nargs='?', default='sales')
    parser.add_argument('--output-csv', help='write cleaned rows to CSV instead of PostgreSQL')
    args = parser.parse_args()
    file_path = args.data_file
    table_name = args.table_name

    if file_path.endswith(".csv"):
        df = read_csv(file_path)
    elif file_path.endswith(".json"):
        df = read_json(file_path)
    else:
        parser.error('Supported formats: .csv, .json')

    df_clean = clean_sales_data(df)
    if args.output_csv:
        df_clean.to_csv(args.output_csv, index=False)
        print(f"Wrote {len(df_clean)} cleaned rows to {args.output_csv}")
    else:
        load_to_postgres(df_clean, table_name)

if __name__ == "__main__":
    main()
