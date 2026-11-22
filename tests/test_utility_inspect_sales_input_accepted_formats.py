"""Behavioral subprocess tests for tools/inspect_sales_input.py: accepted-formats."""
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
TOOL = Path(__file__).resolve().parents[1] / "tools/inspect_sales_input.py"


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

    def test_csv_structure_is_reported_without_row_values(self):
        source = self.file("input.csv", GOOD)
        result = self.run_tool(source)
        report = json.loads(result.stdout)
        self.assertEqual(report["rows"], 2)
        self.assertEqual(report["missing_columns"], [])
        self.assertNotIn("Widget", result.stdout)

    def test_json_object_array_reports_extra_columns(self):
        source = self.file("input.json", json.dumps([dict(ROW, source="batch-a")]))
        report = json.loads(self.run_tool(source).stdout)
        self.assertEqual(report["rows"], 1)
        self.assertIn("source", report["columns"])
