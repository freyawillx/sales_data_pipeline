import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import pandas as pd
import pipeline


class CliRejectionTests(unittest.TestCase):
    def test_missing_file_argument_exits_before_database_access(self):
        with patch("sys.argv", ["pipeline.py"]), patch("pipeline.load_to_postgres") as load:
            with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as error:
                pipeline.main()
        self.assertEqual(error.exception.code, 1)
        load.assert_not_called()

    def test_unsupported_extension_does_not_reach_database(self):
        with patch("sys.argv", ["pipeline.py", "sales.xlsx"]), patch("pipeline.load_to_postgres") as load:
            with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as error:
                pipeline.main()
        self.assertEqual(error.exception.code, 1)
        load.assert_not_called()
