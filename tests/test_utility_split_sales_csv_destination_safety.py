"""Behavioral subprocess tests for tools/split_sales_csv.py: destination-safety."""
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

    def test_nonpositive_chunk_size_is_rejected(self):
        source = self.file("input.csv", GOOD)
        target = self.directory / "parts"
        self.run_tool(source, target, "--rows", "0", expected=2)
        self.assertFalse(target.exists())

    def test_existing_directory_contents_are_untouched(self):
        source = self.file("input.csv", GOOD)
        target = self.directory / "parts"
        target.mkdir()
        marker = target / "keep.txt"
        marker.write_text("keep")
        self.run_tool(source, target, expected=1)
        self.assertEqual(marker.read_text(), "keep")
        self.assertEqual(list(target.glob("*.csv")), [])
