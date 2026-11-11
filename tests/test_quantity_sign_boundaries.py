import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_negative_quantities_are_removed_without_losing_zero(self):
        result = clean_sales_data(pd.DataFrame([row(quantity=q) for q in [-3, -1, 0, 1, 12]]))
        self.assertEqual(result["quantity"].tolist(), [0, 1, 12])

    def test_numeric_quantity_strings_follow_the_same_rule(self):
        result = clean_sales_data(pd.DataFrame([row(quantity=q) for q in ["-2", "0", "15"]]))
        self.assertEqual(result["quantity"].tolist(), [0, 15])
