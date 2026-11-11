"""Split a UTF-8 CSV into new files with repeated headers."""
import argparse
import csv
import json
from pathlib import Path

def positive(value):
    count = int(value)
    if count <= 0:
        raise argparse.ArgumentTypeError("rows per file must be positive")
    return count

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output_directory", type=Path, help="must not already exist")
    parser.add_argument("--rows", type=positive, default=10000)
    args = parser.parse_args()
    count = 0
    chunks = 0
    target = None
    with args.input.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        header = next(reader, None)
        if not header or not {"date", "product", "quantity", "price"}.issubset(header):
            parser.error("input needs all four sales headers")
        if len(header) != len(set(header)):
            parser.error("duplicate headers are ambiguous")
        args.output_directory.mkdir(parents=True, exist_ok=False)
        try:
            for record in reader:
                if len(record) != len(header):
                    parser.error("CSV row width does not match header")
                if count % args.rows == 0:
                    if target is not None:
                        target.close()
                    chunks += 1
                    target = (args.output_directory / f"part-{chunks:05d}.csv").open("x", encoding="utf-8", newline="")
                    writer = csv.writer(target)
                    writer.writerow(header)
                writer.writerow(record)
                count += 1
        finally:
            if target is not None:
                target.close()
    print(json.dumps({"rows": count, "chunks": chunks}))

if __name__ == "__main__":
    main()
