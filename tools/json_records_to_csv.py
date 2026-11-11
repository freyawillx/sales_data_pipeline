"""Convert flat JSON sales objects into a new UTF-8 CSV."""
import argparse
import csv
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = json.loads(args.input.read_text(encoding="utf-8"))
    required = ["date", "product", "quantity", "price"]
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        parser.error("input must be an array of objects")
    for record in rows:
        if not set(required).issubset(record):
            parser.error("each record must include all four required fields")
        if any(isinstance(value, (dict, list)) for value in record.values()):
            parser.error("nested values cannot be represented as flat CSV fields")
    extras = sorted({key for record in rows for key in record} - set(required))
    with args.output.open("x", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=required + extras)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"records": len(rows), "columns": required + extras}))

if __name__ == "__main__":
    main()
