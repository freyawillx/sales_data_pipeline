import json
import tempfile
import unittest
from pathlib import Path
from pipeline import read_json


class JsonEncodingTests(unittest.TestCase):
    def test_utf8_bom_does_not_break_valid_sales_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sales.json"
            path.write_text(json.dumps([{"product":"Widget"}]), encoding="utf-8-sig")
            self.assertEqual(read_json(path)["product"].tolist(), ["Widget"])

    def test_literal_utf8_product_round_trips_without_platform_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sales.json"
            path.write_text(json.dumps([{"product":"Caf\u00e9"}], ensure_ascii=False), encoding="utf-8")
            self.assertEqual(read_json(path)["product"].tolist(), ["Caf\u00e9"])
