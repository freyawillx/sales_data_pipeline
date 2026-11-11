"""Behavioral subprocess tests for tools/validate_sales_file.py: accepted-boundaries."""
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

    def test_zero_quantity_and_zero_price_are_valid(self):
        source = self.file("input.csv", "date,product,quantity,price\n2024-01-01,A,0,0\n")
        report = json.loads(self.run_tool(source).stdout)
        self.assertEqual(report["invalid_rows"], 0)

    def test_maximum_nonnegative_postgresql_integer_is_valid(self):
        source = self.file("input.csv", "date,product,quantity,price\n2024-01-01,A,2147483647,1\n")
        self.assertEqual(json.loads(self.run_tool(source).stdout)["invalid_rows"], 0)
