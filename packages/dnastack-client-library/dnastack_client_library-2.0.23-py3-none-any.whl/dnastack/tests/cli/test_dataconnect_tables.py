import unittest
from click.testing import CliRunner
import json
from dnastack import __main__ as dnastack_cli

from .base import BaseCliTestCase
from .utils import *
from .. import *


class TestCliDataConnectTablesCommand(BaseCliTestCase):
    def setUpCLI(self):
        self.data_connect_url = TEST_DATA_CONNECT_URI

        self.set_config("data_connect.url", self.data_connect_url)
        self.define_oauth_client("data_connect", TEST_OAUTH_CLIENTS["publisher"])
        self.define_refresh_token("data_connect", TEST_WALLET_REFRESH_TOKEN["publisher"])

    def test_tables_list(self):
        result = self.assertCommand(
            ["dataconnect", "tables", "list"],
            json_output=True,
            has_list_of_keys=["name", "data_model"],
        )
        for item in result:
            self.assertIn("$ref", item["data_model"].keys())

    def test_tables_get_table(self):
        table_info_object = self.assertCommand(
            ["dataconnect", "tables", "get", TEST_DATA_CONNECT_VARIANTS_TABLE],
            json_output=True,
            has_keys=["name", "description", "data_model"],
        )
        self.assertIn("$id", table_info_object["data_model"].keys())
        self.assertIn("$schema", table_info_object["data_model"].keys())
        self.assertIn("description", table_info_object["data_model"].keys())

        for property in table_info_object["data_model"]["properties"]:
            assert_has_property(
                self, table_info_object["data_model"]["properties"][property], "format"
            )
            assert_has_property(
                self, table_info_object["data_model"]["properties"][property], "type"
            )
            assert_has_property(
                self,
                table_info_object["data_model"]["properties"][property],
                "$comment",
            )

    def test_tables_get_table_does_not_exist(self):
        self.assertCommand(
            ["dataconnect", "tables", "get", "some table name"], exit_code=1
        )
