"""Convert CSV records to JSONL while preserving CSV field text."""
import argparse
import csv
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    count = 0
    with args.input.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        required = {"date", "product", "quantity", "price"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            parser.error("CSV must contain date, product, quantity, and price headers")
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            parser.error("CSV contains duplicate headers")
        with args.output.open("x", encoding="utf-8", newline="") as target:
            for record in reader:
                if None in record or any(v is None for v in record.values()):
                    parser.error("CSV record width does not match the header")
                target.write(json.dumps(record, ensure_ascii=True) + "\n")
                count += 1
    print(json.dumps({"records": count}))

if __name__ == "__main__":
    main()
