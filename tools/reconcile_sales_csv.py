"""Compare exact four-field CSV values including duplicate multiplicity."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path

FIELDS = ("date", "product", "quantity", "price")

def values(path):
    counts = Counter()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not set(FIELDS).issubset(reader.fieldnames):
            raise ValueError("both CSVs need date, product, quantity, and price headers")
        if len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError("duplicate CSV headers are ambiguous")
        for record in reader:
            if None in record or any(v is None for v in record.values()):
                raise ValueError("CSV record width does not match header")
            counts[tuple(record[field] for field in FIELDS)] += 1
    return counts

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", type=Path)
    parser.add_argument("actual", type=Path)
    args = parser.parse_args()
    expected, actual = values(args.expected), values(args.actual)
    missing = sum((expected - actual).values())
    unexpected = sum((actual - expected).values())
    print(json.dumps({"expected_rows": sum(expected.values()), "actual_rows": sum(actual.values()),
                      "missing_rows": missing, "unexpected_rows": unexpected,
                      "equal": expected == actual}, indent=2))
    raise SystemExit(1 if missing or unexpected else 0)

if __name__ == "__main__":
    main()
