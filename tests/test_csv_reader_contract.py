import json
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from pipeline import read_csv, read_json, read_json_lines


class CsvReaderContractTests(unittest.TestCase):
    def test_quoted_product_with_comma_is_one_value(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sales.csv"
            path.write_text('date,product,quantity,price\n2024-01-01,"Widget, deluxe",2,3.50\n', encoding="utf-8")
            result = read_csv(path)
        self.assertEqual(result["product"].tolist(), ["Widget, deluxe"])
        self.assertEqual(result.iloc[0]["quantity"], 2)

    def test_header_only_csv_returns_expected_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.write_text("date,product,quantity,price\n", encoding="utf-8")
            result = read_csv(path)
        self.assertTrue(result.empty)
        self.assertEqual(result.columns.tolist(), ["date", "product", "quantity", "price"])
