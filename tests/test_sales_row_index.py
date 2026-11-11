import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_nonsequential_index_is_preserved_for_surviving_rows(self):
        source = pd.DataFrame([row(product="A"), row(date=None), row(product="C")], index=[10, 20, 30])
        result = clean_sales_data(source)
        self.assertEqual(result.index.tolist(), [10, 30])
        self.assertEqual(result["product"].tolist(), ["A", "C"])

    def test_cleaning_does_not_sort_sales_by_date(self):
        source = pd.DataFrame([row(date="2024-02-01"), row(date="2024-01-01")])
        result = clean_sales_data(source)
        self.assertEqual(result["date"].tolist(), [pd.Timestamp("2024-02-01"), pd.Timestamp("2024-01-01")])
