"""Behavioral subprocess tests for tools/source_file_manifest.py: byte-fingerprints."""
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
TOOL = Path(__file__).resolve().parents[1] / "tools/source_file_manifest.py"


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

    def test_hash_matches_source_bytes_including_line_endings(self):
        source = self.directory / "input.csv"
        source.write_bytes(b"a,b\r\n1,2\r\n")
        output = self.directory / "manifest.json"
        self.run_tool(source, "--output", output)
        entry = json.loads(output.read_text())["files"][0]
        self.assertEqual(entry["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
        self.assertEqual(entry["bytes"], len(source.read_bytes()))

    def test_multiple_sources_include_empty_file(self):
        first, second = self.file("a.csv", GOOD), self.file("empty.csv", "")
        output = self.directory / "manifest.json"
        self.run_tool(first, second, "--output", output)
        entries = json.loads(output.read_text())["files"]
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[1]["sha256"], hashlib.sha256(b"").hexdigest())
