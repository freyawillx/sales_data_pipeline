import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


def row(**changes):
    values = {"date": "2024-01-01", "product": "Widget", "quantity": 2, "price": 3.5}
    values.update(changes)
    return values


class SalesContractTests(unittest.TestCase):
    def test_cleaning_a_clean_frame_does_not_change_it(self):
        once = clean_sales_data(pd.DataFrame([row(), row(product="Other", quantity="3", price="1.25")]))
        twice = clean_sales_data(once)
        pd.testing.assert_frame_equal(once, twice)

    def test_repeated_runs_do_not_accumulate_mutations(self):
        source = pd.DataFrame([row(), row(product="bad", price=-2)])
        first = clean_sales_data(source)
        second = clean_sales_data(source)
        pd.testing.assert_frame_equal(first, second)
        self.assertEqual(len(source), 2)
