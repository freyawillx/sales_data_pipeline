"""Strictly validate a CSV before using the permissive sales cleaner."""
import argparse
from collections import Counter
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
import json
import math
from pathlib import Path

def decimal_value(value):
    try:
        parsed = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return None
    return parsed if parsed.is_finite() else None

def problems(record):
    issues = []
    try:
        value = record["date"]
        if len(value) != 10 or date.fromisoformat(value).isoformat() != value:
            issues.append("date")
    except (TypeError, ValueError):
        issues.append("date")
    if not record["product"].strip():
        issues.append("product")
    quantity = decimal_value(record["quantity"])
    if quantity is None or quantity < 0 or quantity > 2147483647 or quantity != quantity.to_integral_value():
        issues.append("quantity")
    price = decimal_value(record["price"])
    if price is None or price < 0 or not math.isfinite(float(price)):
        issues.append("price")
    return issues

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    rows = 0
    invalid = 0
    counts = Counter()
    with args.input.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        required = {"date", "product", "quantity", "price"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            parser.error("CSV is missing required sales headers")
        if len(set(reader.fieldnames)) != len(reader.fieldnames):
            parser.error("CSV has duplicate headers")
        for record in reader:
            rows += 1
            if None in record or any(v is None for v in record.values()):
                found = ["record_width"]
            else:
                found = problems(record)
            if found:
                invalid += 1
                counts.update(found)
    print(json.dumps({"rows": rows, "invalid_rows": invalid, "issues_by_field": dict(counts)}, indent=2))
    raise SystemExit(1 if invalid else 0)

if __name__ == "__main__":
    main()
