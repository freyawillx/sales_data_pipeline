import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools/validate_sales_file.py"


class StrictCsvQuotingTests(unittest.TestCase):
    def run_file(self, content):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sales.csv"
            source.write_text(content, encoding="utf-8")
            return subprocess.run([sys.executable, str(TOOL), str(source)], capture_output=True)

    def test_junk_after_closing_quote_is_rejected(self):
        result = self.run_file('date,product,quantity,price\n2024-01-01,"Widget"junk,1,2\n')
        self.assertNotEqual(result.returncode, 0)

    def test_correctly_escaped_quotes_are_accepted(self):
        result = self.run_file('date,product,quantity,price\n2024-01-01,"A ""quoted"" product",1,2\n')
        self.assertEqual(result.returncode, 0, result.stderr)
