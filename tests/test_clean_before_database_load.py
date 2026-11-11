import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import pandas as pd
import pipeline


class CleanBeforeLoadTests(unittest.TestCase):
    def test_invalid_neighbor_is_removed_before_loader_call(self):
        source = pd.DataFrame([
            {"date":"2024-01-01", "product":"good", "quantity":"2", "price":"3.50"},
            {"date":"2024-01-01", "product":"bad", "quantity":"oops", "price":"3.50"}])
        with patch("sys.argv", ["pipeline.py", "input.csv"]):
            with patch("pipeline.read_csv", return_value=source), patch("pipeline.load_to_postgres") as load:
                pipeline.main()
        loaded = load.call_args.args[0]
        self.assertEqual(loaded["product"].tolist(), ["good"])
        self.assertEqual(loaded.iloc[0]["quantity"], 2)
        self.assertEqual(loaded.iloc[0]["date"], pd.Timestamp("2024-01-01"))
        self.assertEqual(len(source), 2)

    def test_all_rejected_rows_are_passed_as_an_empty_frame(self):
        source = pd.DataFrame([{"date":None, "product":"bad", "quantity":1, "price":2.0}])
        with patch("sys.argv", ["pipeline.py", "input.csv"]):
            with patch("pipeline.read_csv", return_value=source), patch("pipeline.load_to_postgres") as load:
                pipeline.main()
        self.assertTrue(load.call_args.args[0].empty)
