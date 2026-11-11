import json
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from pipeline import read_csv, read_json, read_json_lines


class JsonRecordTests(unittest.TestCase):
    def test_array_preserves_record_fields_and_escaped_unicode(self):
        records = [{"date": "2024-01-01", "product": "Caf\u00e9", "quantity": 2, "price": 3.5}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sales.json"
            path.write_text(json.dumps(records, ensure_ascii=True), encoding="ascii")
            result = read_json(path)
        self.assertEqual(result["product"].tolist(), ["Caf\u00e9"])
        self.assertEqual(result.iloc[0]["price"], 3.5)

    def test_empty_json_array_returns_empty_frame(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.json"
            path.write_text("[]", encoding="ascii")
            result = read_json(path)
        self.assertTrue(result.empty)
        self.assertEqual(len(result.columns), 0)
