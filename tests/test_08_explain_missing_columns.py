import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


class MissingColumnsTests(unittest.TestCase):
    def test_error_names_missing_columns(self):
        with self.assertRaisesRegex(ValueError, "price, quantity"):
            clean_sales_data(pd.DataFrame({"date": ["2024-01-01"], "product": ["A"]}))
