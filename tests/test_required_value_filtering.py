import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_missing_values_are_filtered_in_each_required_column(self):
        for column in ("date", "product", "quantity", "price"):
            with self.subTest(column=column):
                values = [row(product="kept"), row(**{column: None})]
                result = clean_sales_data(pd.DataFrame(values))
                self.assertEqual(result["product"].tolist(), ["kept"])

    def test_all_incomplete_rows_produce_an_empty_result(self):
        values = [row(date=None), row(product=None), row(quantity=None), row(price=None)]
        result = clean_sales_data(pd.DataFrame(values))
        self.assertTrue(result.empty)
        self.assertEqual(result.columns.tolist(), ["date", "product", "quantity", "price"])
