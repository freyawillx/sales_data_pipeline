"""Fingerprint immutable source files without exposing their contents."""
import argparse
import hashlib
import json
from pathlib import Path

def fingerprint(path):
    before = path.stat()
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            size += len(block)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns) or size != after.st_size:
        raise RuntimeError("source changed while hashing; use an immutable input")
    return {"path": str(path), "bytes": size, "sha256": digest.hexdigest()}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [fingerprint(path) for path in args.inputs]
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump({"algorithm": "sha256", "files": rows}, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"files": len(rows)}))

if __name__ == "__main__":
    main()
