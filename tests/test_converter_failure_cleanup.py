import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools/csv_to_json_lines.py"


class ConverterCleanupTests(unittest.TestCase):
    def test_late_malformed_record_leaves_no_partial_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory)/"input.csv", Path(directory)/"output.jsonl"
            source.write_text("date,product,quantity,price\n2024-01-01,A,1,2\n2024-01-02,B,1,2,EXTRA\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(TOOL), str(source), str(output)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())

    def test_preexisting_output_is_never_deleted_or_changed(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory)/"input.csv", Path(directory)/"output.jsonl"
            source.write_text("date,product,quantity,price\n2024-01-01,A,1,2\n", encoding="utf-8")
            output.write_text("preserve me", encoding="utf-8")
            result = subprocess.run([sys.executable, str(TOOL), str(source), str(output)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(encoding="utf-8"), "preserve me")
