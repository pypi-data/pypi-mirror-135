import csv
from io import StringIO

from .base import BaseCliTestCase
from .utils import *
from .. import *


class TestCliDataConnectQueryCommand(BaseCliTestCase):
    def setUpCLI(self):
        self.data_connect_url = TEST_DATA_CONNECT_URI

        self.set_config("data_connect.url", self.data_connect_url)
        self.define_oauth_client("data_connect", TEST_OAUTH_CLIENTS["publisher"])
        self.define_refresh_token("data_connect", TEST_WALLET_REFRESH_TOKEN["publisher"])

    def test_variant_query(self):
        result = self.assertCommand(
            [
                "dataconnect",
                "query",
                f"SELECT * from {TEST_DATA_CONNECT_VARIANTS_TABLE} LIMIT 5",
            ],
            json_output=True,
        )

        for item in result:
            assert_has_property(self, item, "start_position")
            assert_has_property(self, item, "end_position")
            assert_has_property(self, item, "reference_bases")
            assert_has_property(self, item, "alternate_bases")
            assert_has_property(self, item, "sequence_accession")

    def test_csv_query(self):
        result = self.assertCommand(
            [
                "dataconnect",
                "query",
                f"SELECT * FROM {TEST_DATA_CONNECT_VARIANTS_TABLE} LIMIT 5",
                "-f",
                "csv",
            ],
        )
        csv_string = StringIO(result)
        csv_results = csv.reader(csv_string)

        header_row = next(csv_results)

        # tests that headers are present
        self.assertIn("start_position", header_row)
        self.assertIn("end_position", header_row)
        self.assertIn("reference_bases", header_row)
        self.assertIn("alternate_bases", header_row)
        self.assertIn("sequence_accession", header_row)

        for item in csv_results:
            self.assertEqual(len(item), len(header_row))

    def test_drs_url_query(self):
        result = self.assertCommand(
            [
                "dataconnect",
                "query",
                f"SELECT drs_url FROM {TEST_DATA_CONNECT_FILES_TABLE} LIMIT 5",
            ],
            json_output=True,
        )

        for item in result:
            assert_has_property(self, item, "drs_url")

    def test_incorrect_column_query(self):
        result = self.assertCommand(
            [
                "dataconnect",
                "query",
                f"SELECT imaginary_field FROM {TEST_DATA_CONNECT_VARIANTS_TABLE} LIMIT 5",
            ],
            exit_code=1,
        )
        self.assertIn("Column 'imaginary_field' cannot be resolved", result)

    def test_broken_query(self):
        self.assertCommand(["dataconnect", "query", "broken_query"], exit_code=1)
