import json
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from pipeline import read_csv, read_json, read_json_lines


class JsonLinesTests(unittest.TestCase):
    def test_separate_objects_become_separate_rows(self):
        records = [{"date": "2024-01-01", "product": "A", "quantity": 2, "price": 3.5},
                   {"date": "2024-01-02", "product": "B", "quantity": 0, "price": 0.0}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sales.jsonl"
            path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="ascii")
            result = read_json_lines(path)
        self.assertEqual(result["product"].tolist(), ["A", "B"])
        self.assertEqual(result["quantity"].tolist(), [2, 0])

    def test_malformed_line_raises_instead_of_silently_skipping(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            path.write_text('{"product":"A"}\nnot-json\n', encoding="ascii")
            with self.assertRaises(ValueError):
                read_json_lines(path)
