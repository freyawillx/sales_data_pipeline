"""Behavioral subprocess tests for tools/reconcile_sales_csv.py: difference-detection."""
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
TOOL = Path(__file__).resolve().parents[1] / "tools/reconcile_sales_csv.py"


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

    def test_one_extra_duplicate_is_reported(self):
        first = self.file("a.csv", GOOD)
        second = self.file("b.csv", GOOD + GOOD.splitlines()[1] + "\n")
        report = json.loads(self.run_tool(first, second, expected=1).stdout)
        self.assertEqual(report["unexpected_rows"], 1)
        self.assertEqual(report["missing_rows"], 0)

    def test_numeric_text_is_compared_exactly(self):
        first = self.file("a.csv", GOOD)
        second = self.file("b.csv", GOOD.replace("3.50", "3.5"))
        report = json.loads(self.run_tool(first, second, expected=1).stdout)
        self.assertEqual(report["missing_rows"], 1)
        self.assertEqual(report["unexpected_rows"], 1)
