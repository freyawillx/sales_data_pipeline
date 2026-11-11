"""Inspect file structure without loading data into PostgreSQL."""
import argparse
import json
from pathlib import Path
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    suffix = args.input.suffix.lower()
    if suffix == ".csv":
        frame = pd.read_csv(args.input)
    elif suffix == ".json":
        records = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
            parser.error("JSON must be an array of objects")
        frame = pd.DataFrame(records)
    elif suffix == ".jsonl":
        frame = pd.read_json(args.input, lines=True)
    else:
        parser.error("input must be CSV, JSON, or JSONL")
    required = ["date", "product", "quantity", "price"]
    report = {"rows": len(frame), "columns": frame.columns.tolist(),
              "missing_columns": [c for c in required if c not in frame],
              "null_counts": {str(c): int(frame[c].isna().sum()) for c in frame},
              "dtypes": {str(c): str(frame[c].dtype) for c in frame}}
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
