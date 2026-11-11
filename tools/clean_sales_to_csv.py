"""Run the existing cleaner and save its result to a new CSV file."""
import argparse
import json
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.data_cleaner import clean_sales_data

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CSV source")
    parser.add_argument("output", type=Path, help="new CSV path; existing files are refused")
    args = parser.parse_args()
    raw = pd.read_csv(args.input)
    clean = clean_sales_data(raw)
    with args.output.open("x", encoding="utf-8", newline="") as stream:
        clean.to_csv(stream, index=False, date_format="%Y-%m-%d")
    print(json.dumps({"input_rows": len(raw), "output_rows": len(clean),
                      "removed_rows": len(raw) - len(clean)}))

if __name__ == "__main__":
    main()
