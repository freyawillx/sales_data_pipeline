import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_schema_only_input_remains_empty(self):
        source = pd.DataFrame(columns=["date", "product", "quantity", "price"])
        result = clean_sales_data(source)
        self.assertTrue(result.empty)
        self.assertEqual(result.columns.tolist(), source.columns.tolist())
        self.assertTrue(source.empty)

    def test_batch_with_only_invalid_dates_is_empty(self):
        source = pd.DataFrame([row(date="bad"), row(date="also bad")])
        result = clean_sales_data(source)
        self.assertTrue(result.empty)
        self.assertEqual(len(source), 2)
