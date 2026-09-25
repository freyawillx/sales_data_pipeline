import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


class FractionalQuantityTests(unittest.TestCase):
    def test_fractional_quantity_is_not_silently_truncated(self):
        rows = pd.DataFrame({"date": ["2024-01-01"] * 2, "product": ["whole", "fraction"], "quantity": [2, 2.5], "price": [3, 4]})
        self.assertEqual(clean_sales_data(rows)["product"].tolist(), ["whole"])
