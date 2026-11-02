"""Behavioral subprocess tests for tools/clean_sales_to_csv.py: output-safety."""
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

    def test_existing_export_is_unchanged(self):
        source = self.file("input.csv", GOOD)
        output = self.file("output.csv", "keep me")
        self.run_tool(source, output, expected=1)
        self.assertEqual(output.read_text(encoding="utf-8"), "keep me")

    def test_missing_required_schema_does_not_create_output(self):
        source = self.file("input.csv", "product\nA\n")
        output = self.directory / "output.csv"
        self.run_tool(source, output, expected=1)
        self.assertFalse(output.exists())
