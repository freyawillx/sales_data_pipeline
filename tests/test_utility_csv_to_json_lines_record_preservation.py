"""Behavioral subprocess tests for tools/csv_to_json_lines.py: record-preservation."""
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
TOOL = Path(__file__).resolve().parents[1] / "tools/csv_to_json_lines.py"


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

    def test_csv_quotes_and_numeric_text_survive_conversion(self):
        source = self.file("input.csv", 'date,product,quantity,price\n2024-01-01,"Widget, deluxe",0002,3.50\n')
        output = self.directory / "out.jsonl"
        self.run_tool(source, output)
        record = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(record["product"], "Widget, deluxe")
        self.assertEqual(record["quantity"], "0002")

    def test_utf8_product_is_valid_escaped_json(self):
        source = self.file("input.csv", 'date,product,quantity,price\n2024-01-01,Caf\u00e9,1,2\n')
        output = self.directory / "out.jsonl"
        self.run_tool(source, output)
        self.assertEqual(json.loads(output.read_text(encoding="ascii"))["product"], "Caf\u00e9")
