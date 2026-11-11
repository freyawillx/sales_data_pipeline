import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_impossible_and_unparseable_dates_are_removed(self):
        values = [row(date=value, product=str(i)) for i, value in enumerate(
            ["2024-02-29", "2023-02-29", "2024-02-30", "not-a-date"])]
        result = clean_sales_data(pd.DataFrame(values))
        self.assertEqual(result["product"].tolist(), ["0"])
        self.assertEqual(result.iloc[0]["date"], pd.Timestamp("2024-02-29"))

    def test_year_boundary_dates_remain_distinct(self):
        result = clean_sales_data(pd.DataFrame([row(date="2023-12-31"), row(date="2024-01-01")]))
        self.assertEqual(result["date"].tolist(), [pd.Timestamp("2023-12-31"), pd.Timestamp("2024-01-01")])
