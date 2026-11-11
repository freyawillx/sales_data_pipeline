import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_timestamp_inputs_remain_valid(self):
        source = pd.DataFrame([row(date=pd.Timestamp("2024-03-04")), row(date=pd.Timestamp("2024-03-05"))])
        result = clean_sales_data(source)
        self.assertEqual(result["date"].tolist(), source["date"].tolist())

    def test_missing_timestamp_is_removed(self):
        source = pd.DataFrame([row(date=pd.NaT, product="bad"), row(date=pd.Timestamp("2024-03-04"), product="good")])
        result = clean_sales_data(source)
        self.assertEqual(result["product"].tolist(), ["good"])
