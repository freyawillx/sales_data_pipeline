import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from utils.db_loader import load_to_postgres


def frame():
    return pd.DataFrame({"date": [pd.Timestamp("2024-01-01")], "product": ["A"], "quantity": [1], "price": [2.0]})


class LoaderSafetyTests(unittest.TestCase):
    def test_success_commits_once_and_closes_both_resources(self):
        connection = MagicMock()
        with patch("utils.db_loader.psycopg2.connect", return_value=connection), patch("utils.db_loader.execute_values"):
            load_to_postgres(frame())
        connection.commit.assert_called_once()
        connection.rollback.assert_not_called()
        connection.cursor.return_value.close.assert_called_once()
        connection.close.assert_called_once()

    def test_insert_failure_rolls_back_without_committing_table_creation(self):
        connection = MagicMock()
        with patch("utils.db_loader.psycopg2.connect", return_value=connection):
            with patch("utils.db_loader.execute_values", side_effect=RuntimeError("insert failed")):
                with self.assertRaisesRegex(RuntimeError, "insert failed"):
                    load_to_postgres(frame())
        connection.commit.assert_not_called()
        connection.rollback.assert_called_once()
        connection.cursor.return_value.close.assert_called_once()
        connection.close.assert_called_once()

    def test_destination_is_composed_as_an_identifier_not_executable_sql(self):
        connection = MagicMock()
        destination = 'report"; DROP TABLE sales; --'
        with patch("utils.db_loader.psycopg2.connect", return_value=connection):
            with patch("utils.db_loader.execute_values") as insert:
                load_to_postgres(frame(), destination)
        # The driver owns identifier escaping. Render using a deterministic
        # quote_ident substitute because no live PostgreSQL connection is used.
        def quote(value, context):
            return '"' + value.replace('"', '""') + '"'
        with patch("psycopg2.extensions.quote_ident", side_effect=quote):
            create_sql = connection.cursor.return_value.execute.call_args.args[0].as_string(connection)
            insert_sql = insert.call_args.args[1].as_string(connection)
        quoted = '"report""; DROP TABLE sales; --"'
        self.assertIn(quoted, create_sql)
        self.assertIn(quoted, insert_sql)
        self.assertTrue(insert_sql.startswith("INSERT INTO " + quoted))

    def test_invalid_identifier_fails_before_connecting(self):
        for name in ["", "   ", None]:
            with self.subTest(name=name), patch("utils.db_loader.psycopg2.connect") as connect:
                with self.assertRaisesRegex(ValueError, "table_name"):
                    load_to_postgres(frame(), name)
                connect.assert_not_called()
