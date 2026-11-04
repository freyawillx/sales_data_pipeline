"""Behavioral subprocess tests for tools/clean_sales_to_csv.py: export-contract."""
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
TOOL = Path(__file__).resolve().parents[1] / "tools/clean_sales_to_csv.py"


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

    def test_numeric_strings_are_cleaned_and_bad_date_removed(self):
        source = self.file("input.csv", GOOD + "bad,Rejected,1,2\n")
        output = self.directory / "clean.csv"
        report = json.loads(self.run_tool(source, output).stdout)
        self.assertEqual(report, {"input_rows":3, "output_rows":2, "removed_rows":1})
        self.assertIn("bad,Rejected", source.read_text(encoding="utf-8"))

    def test_extra_source_column_is_retained(self):
        source = self.file("input.csv", "date,product,quantity,price,batch\n2024-01-01,A,1,2,b7\n")
        output = self.directory / "clean.csv"
        self.run_tool(source, output)
        with output.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(rows[0]["batch"], "b7")
