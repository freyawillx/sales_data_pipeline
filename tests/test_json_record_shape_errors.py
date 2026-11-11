import json
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from pipeline import read_csv, read_json, read_json_lines


class JsonMemberShapeTests(unittest.TestCase):
    def test_nonobject_members_are_rejected_with_a_clear_message(self):
        for data in [[1], [None], [["nested"]], [{"date": "2024-01-01"}, "bad"]]:
            with self.subTest(data=data), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "bad.json"
                path.write_text(json.dumps(data), encoding="ascii")
                with self.assertRaisesRegex(ValueError, "array of sales objects"):
                    read_json(path)

    def test_invalid_json_syntax_surfaces_as_a_decode_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("[{", encoding="ascii")
            with self.assertRaises(json.JSONDecodeError):
                read_json(path)
