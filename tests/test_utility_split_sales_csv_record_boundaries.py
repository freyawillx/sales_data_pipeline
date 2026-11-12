"""Behavioral subprocess tests for tools/split_sales_csv.py: record-boundaries."""
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROW = {"date":"2024-01-01", "product":"Widget", "quantity":2, "price":3.5}
GOOD = "date,product,quantity,price\n2024-01-01,Widget,2,3.50\n2024-01-02,Other,1,4.00\n"
TOOL = Path(__file__).resolve().parents[1] / "tools/split_sales_csv.py"


class UtilityBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def file(self, name, content):
        path = self.directory / name
        path.write_text(content, encoding="utf-8", newline="")
        return path

    def run_tool(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(TOOL), *map(str, args)],
            capture_output=True, text=True, encoding="utf-8",
            env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_each_chunk_repeats_header_and_preserves_total_rows(self):
        source = self.file("input.csv", GOOD)
        target = self.directory / "parts"
        report = json.loads(self.run_tool(source, target, "--rows", "1").stdout)
        self.assertEqual(report, {"rows":2, "chunks":2})
        for part in target.glob("*.csv"):
            self.assertEqual(part.read_text().splitlines()[0], "date,product,quantity,price")

    def test_embedded_newline_does_not_split_a_csv_record(self):
        source = self.file("input.csv", 'date,product,quantity,price\n2024-01-01,"Multi\nline",1,2\n')
        target = self.directory / "parts"
        self.run_tool(source, target, "--rows", "1")
        with next(target.glob("*.csv")).open(encoding="utf-8", newline="") as stream:
            records = list(csv.DictReader(stream))
        self.assertEqual(records[0]["product"], "Multi\nline")
