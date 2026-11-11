import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from utils.db_loader import load_to_postgres


class BatchInsertRegressionTests(unittest.TestCase):
    def test_nonempty_sales_call_imported_batch_insert(self):
        frame = pd.DataFrame({"date": [pd.Timestamp("2024-01-01")], "product": ["Widget"], "quantity": [2], "price": [3.5]})
        connection = MagicMock()
        with patch("utils.db_loader.psycopg2.connect", return_value=connection):
            with patch("utils.db_loader.execute_values") as batch_insert:
                load_to_postgres(frame)
        batch_insert.assert_called_once()
        args, kwargs = batch_insert.call_args
        self.assertIs(args[0], connection.cursor.return_value)
        self.assertEqual(args[2], [(pd.Timestamp("2024-01-01"), "Widget", 2, 3.5)])
        self.assertEqual(kwargs["page_size"], 1000)
        connection.close.assert_called_once()

    def test_empty_frame_does_not_call_batch_insert(self):
        frame = pd.DataFrame(columns=["date", "product", "quantity", "price"])
        connection = MagicMock()
        with patch("utils.db_loader.psycopg2.connect", return_value=connection):
            with patch("utils.db_loader.execute_values") as batch_insert:
                load_to_postgres(frame)
        batch_insert.assert_not_called()
        connection.close.assert_called_once()
