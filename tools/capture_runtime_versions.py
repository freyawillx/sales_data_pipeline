"""Report interpreter and runtime package versions without dumping environment variables."""
import argparse
import importlib.metadata
import json
import platform
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="new JSON path; defaults to stdout")
    args = parser.parse_args()
    versions = {}
    for name in ("pandas", "numpy", "psycopg2-binary"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    report = {"python": platform.python_version(), "implementation": platform.python_implementation(),
              "system": platform.system(), "machine": platform.machine(), "packages": versions}
    content = json.dumps(report, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(content)
    else:
        print(content, end="")

if __name__ == "__main__":
    main()
