import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_required_fields_are_selected_by_name(self):
        source = pd.DataFrame([row(quantity="4", price="2.25")])[["price", "product", "date", "quantity"]]
        result = clean_sales_data(source)
        self.assertEqual(result.columns.tolist(), source.columns.tolist())
        self.assertEqual(result.iloc[0]["quantity"], 4)
        self.assertEqual(result.iloc[0]["price"], 2.25)

    def test_metadata_can_precede_required_columns(self):
        source = pd.DataFrame([row(batch="b7")])[["batch", "price", "quantity", "product", "date"]]
        result = clean_sales_data(source)
        self.assertEqual(result.iloc[0]["batch"], "b7")
        self.assertEqual(result.columns.tolist(), source.columns.tolist())
