import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import pandas as pd
import pipeline


class CliRoutingTests(unittest.TestCase):
    def test_each_supported_suffix_selects_its_reader(self):
        source = pd.DataFrame([{"date":"2024-01-01", "product":"A", "quantity":1, "price":2.0}])
        for extension, reader in [("csv", "read_csv"), ("json", "read_json"), ("jsonl", "read_json_lines")]:
            with self.subTest(extension=extension), patch("sys.argv", ["pipeline.py", "input." + extension]):
                with patch.object(pipeline, reader, return_value=source) as read, patch("pipeline.load_to_postgres") as load:
                    pipeline.main()
                read.assert_called_once_with("input." + extension)
                self.assertEqual(load.call_args.args[1], "sales")

    def test_custom_table_name_reaches_loader(self):
        source = pd.DataFrame([{"date":"2024-01-01", "product":"A", "quantity":1, "price":2.0}])
        with patch("sys.argv", ["pipeline.py", "input.csv", "archive_sales"]):
            with patch("pipeline.read_csv", return_value=source), patch("pipeline.load_to_postgres") as load:
                pipeline.main()
        self.assertEqual(load.call_args.args[1], "archive_sales")
