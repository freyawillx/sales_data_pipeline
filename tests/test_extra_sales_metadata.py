import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_extra_columns_stay_aligned_after_row_filtering(self):
        source = pd.DataFrame([row(product="bad", date=None, source_id="a"), row(product="good", source_id="b")])
        result = clean_sales_data(source)
        self.assertEqual(result["source_id"].tolist(), ["b"])
        self.assertEqual(result["product"].tolist(), ["good"])

    def test_extra_column_values_are_not_coerced(self):
        source = pd.DataFrame([row(source_id="0007", source_file="jan.csv")])
        result = clean_sales_data(source)
        self.assertEqual(result.iloc[0]["source_id"], "0007")
        self.assertEqual(result.iloc[0]["source_file"], "jan.csv")
