import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_common_whitespace_only_names_are_removed(self):
        source = pd.DataFrame([row(product=p) for p in ["", " ", "\t", "\n", "Widget"]])
        result = clean_sales_data(source)
        self.assertEqual(result["product"].tolist(), ["Widget"])

    def test_nonblank_surrounding_spaces_are_currently_preserved(self):
        result = clean_sales_data(pd.DataFrame([row(product=" Widget ")]))
        self.assertEqual(result.iloc[0]["product"], " Widget ")
