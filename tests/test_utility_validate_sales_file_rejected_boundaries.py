"""Behavioral subprocess tests for tools/validate_sales_file.py: rejected-boundaries."""
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
TOOL = Path(__file__).resolve().parents[1] / "tools/validate_sales_file.py"


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

    def test_fractional_quantity_is_rejected_before_cleaner_truncation(self):
        source = self.file("input.csv", "date,product,quantity,price\n2024-01-01,A,1.5,2\n")
        report = json.loads(self.run_tool(source, expected=1).stdout)
        self.assertEqual(report["issues_by_field"], {"quantity":1})

    def test_nonfinite_and_oversized_values_are_rejected(self):
        source = self.file("input.csv", "date,product,quantity,price\n2024-01-01,A,2147483648,2\n2024-01-01,B,1,Infinity\n")
        report = json.loads(self.run_tool(source, expected=1).stdout)
        self.assertEqual(report["invalid_rows"], 2)
        self.assertEqual(report["issues_by_field"], {"quantity":1,"price":1})
