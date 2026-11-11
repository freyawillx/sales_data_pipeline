import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_whitespace_and_decimal_price_strings_are_accepted(self):
        result = clean_sales_data(pd.DataFrame([row(quantity=" 12 ", price=" 3.25 ")]))
        self.assertEqual(result.iloc[0]["quantity"], 12)
        self.assertEqual(result.iloc[0]["price"], 3.25)

    def test_invalid_price_does_not_drop_a_valid_neighbor(self):
        result = clean_sales_data(pd.DataFrame([row(product="bad", price="unknown"), row(product="good", price="2.50")]))
        self.assertEqual(result["product"].tolist(), ["good"])
        self.assertEqual(result.iloc[0]["price"], 2.5)
