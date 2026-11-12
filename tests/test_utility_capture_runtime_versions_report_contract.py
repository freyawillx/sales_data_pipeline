"""Behavioral subprocess tests for tools/capture_runtime_versions.py: report-contract."""
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
TOOL = Path(__file__).resolve().parents[1] / "tools/capture_runtime_versions.py"


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

    def test_stdout_contains_versions_without_environment_dump(self):
        report = json.loads(self.run_tool().stdout)
        self.assertIn("python", report)
        self.assertIn("pandas", report["packages"])
        self.assertNotIn("environment", report)
        self.assertNotIn("hostname", report)

    def test_file_output_has_same_report_structure(self):
        output = self.directory / "runtime.json"
        self.run_tool("--output", output)
        report = json.loads(output.read_text())
        self.assertEqual(set(report), {"python", "implementation", "system", "machine", "packages"})
