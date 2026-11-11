import unittest
import pandas as pd
from utils.data_cleaner import clean_sales_data


class RequiredSchemaTests(unittest.TestCase):
    def test_missing_columns_are_reported_in_contract_order(self):
        source = pd.DataFrame({"product": ["A"]})
        before = source.copy(deep=True)
        with self.assertRaisesRegex(ValueError, "Missing required sales columns: date, quantity, price"):
            clean_sales_data(source)
        pd.testing.assert_frame_equal(source, before)

    def test_empty_no_schema_frame_has_actionable_error(self):
        with self.assertRaisesRegex(ValueError, "date, product, quantity, price"):
            clean_sales_data(pd.DataFrame())

    def test_schema_only_frame_is_still_a_valid_empty_batch(self):
        result = clean_sales_data(pd.DataFrame(columns=["date", "product", "quantity", "price"]))
        self.assertTrue(result.empty)
