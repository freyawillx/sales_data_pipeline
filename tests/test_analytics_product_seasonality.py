"""Regressions for product-seasonality.

Optional engine: python -m pip install duckdb
Run: python -m unittest discover -s tests -p test_analytics_product_seasonality.py -v
DuckDB fixture execution does not replace live PostgreSQL integration testing.
"""
import unittest
from datetime import date, timedelta
from pathlib import Path
try:
    import duckdb
except ImportError:
    duckdb = None

ROWS = [('2023-01-01', 'A', 2, 3.0), ('2023-01-01', 'A', 2, 3.0), ('2023-01-02', 'B', 1, 4.0), ('2023-02-01', 'A', 0, 0.0), ('2024-01-01', 'A', 1, 5.0), ('2024-01-02', 'B', 3, 2.0), ('2024-01-03', 'B', 0, 0.0), ('2024-02-01', 'B', 1, 4.0), ('2024-02-01', ' B ', 1, 2.0), ('2024-04-01', 'C', 2, 10.0)]
QUERY = Path(__file__).resolve().parents[1] / "examples/analytics/product-seasonality.sql"


@unittest.skipIf(duckdb is None, "Install optional duckdb to run analytics fixtures")
class AnalyticsQueryTests(unittest.TestCase):
    def setUp(self):
        self.connection = duckdb.connect(":memory:")
        self.connection.execute("CREATE TABLE sales (date DATE, product TEXT, quantity INTEGER, price DOUBLE)")

    def tearDown(self):
        self.connection.close()

    def query(self, rows):
        if rows:
            self.connection.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", rows)
        return self.connection.execute(QUERY.read_text(encoding="utf-8")).fetchall()

    def test_representative_sales_have_expected_business_results(self):
        result = self.query(ROWS)
        a = next(r for r in result if r[0] == 'A' and r[1] == 1); self.assertEqual(a, ('A', 1, 2, 17.0, 8.5))

    def test_empty_source_has_explicit_result_contract(self):
        self.assertEqual(self.query([]), [])
