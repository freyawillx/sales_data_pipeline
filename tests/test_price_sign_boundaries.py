import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_negative_prices_are_removed_and_free_sales_survive(self):
        result = clean_sales_data(pd.DataFrame([row(price=p) for p in [-3.0, -0.01, 0.0, 2.5]]))
        self.assertEqual(result["price"].tolist(), [0.0, 2.5])

    def test_price_strings_are_converted_before_sign_validation(self):
        result = clean_sales_data(pd.DataFrame([row(price=p) for p in ["-1.25", "0.00", "9.99"]]))
        self.assertEqual(result["price"].tolist(), [0.0, 9.99])
