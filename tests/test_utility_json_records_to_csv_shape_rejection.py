"""Behavioral subprocess tests for tools/json_records_to_csv.py: shape-rejection."""
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
TOOL = Path(__file__).resolve().parents[1] / "tools/json_records_to_csv.py"


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

    def test_nested_values_are_rejected(self):
        source = self.file("input.json", json.dumps([dict(ROW, details={"nested":1})]))
        output = self.directory / "out.csv"
        self.run_tool(source, output, expected=2)
        self.assertFalse(output.exists())

    def test_object_root_is_rejected(self):
        source = self.file("input.json", json.dumps(ROW))
        output = self.directory / "out.csv"
        self.run_tool(source, output, expected=2)
        self.assertFalse(output.exists())
