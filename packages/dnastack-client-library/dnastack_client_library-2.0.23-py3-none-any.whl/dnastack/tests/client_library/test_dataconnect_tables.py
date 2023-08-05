import unittest
from ... import PublisherClient
from .. import *
from ...auth import RefreshTokenAuth, OAuthClientParams


def assert_has_property(self, obj, attribute):
    if isinstance(obj, dict):
        self.assertTrue(
            attribute in obj,
            msg="obj lacking an attribute. obj: %s, intendedAttribute: %s"
                % (obj, attribute),
            )
    else:
        self.assertTrue(
            hasattr(obj, attribute),
            msg="obj lacking an attribute. obj: %s, intendedAttribute: %s"
            % (obj, attribute),
        )


class TestClientLibraryDataConnectTablesCommand(unittest.TestCase):
    def setUp(self):

        self.auth = RefreshTokenAuth(
            refresh_token=TEST_WALLET_REFRESH_TOKEN["publisher"],
            oauth_client=OAuthClientParams(
                base_url=TEST_AUTH_PARAMS["publisher"]["url"],
                client_id=TEST_AUTH_PARAMS["publisher"]["client"]["id"],
                client_secret=TEST_AUTH_PARAMS["publisher"]["client"]["secret"],
                client_redirect_url=TEST_AUTH_PARAMS["publisher"]["client"][
                    "redirect_url"
                ],
            ),
        )
        self.publisher_client = PublisherClient(
            dataconnect_url=TEST_DATA_CONNECT_URI, auth=self.auth
        )

    def test_tables_list(self):
        result = self.publisher_client.dataconnect.list_tables()

        self.assertIsNotNone(result)

        rows = list(result)
        self.assertGreater(len(rows), 0)
        item = rows[0]
        assert_has_property(self, item, "name")
        assert_has_property(self, item, "data_model")
        assert_has_property(self, item.data_model, "$ref")

    def test_tables_get_table(self):
        get_table_result = self.publisher_client.dataconnect.get_table(TEST_DATA_CONNECT_VARIANTS_TABLE)

        self.assertIsNotNone(get_table_result)

        assert_has_property(self, get_table_result, "name")
        assert_has_property(self, get_table_result, "description")
        assert_has_property(self, get_table_result, "data_model")
        assert_has_property(self, get_table_result.data_model, "$id")
        assert_has_property(self, get_table_result.data_model, "$schema")
        assert_has_property(self, get_table_result.data_model, "description")

        for property in get_table_result.data_model["properties"]:
            assert_has_property(self, get_table_result.data_model["properties"][property], "format")
            assert_has_property(self, get_table_result.data_model["properties"][property], "type")
            assert_has_property(self, get_table_result.data_model["properties"][property], "$comment")

    def test_tables_get_table_does_not_exist(self):
        with self.assertRaises(Exception) as cm:
            self.publisher_client.dataconnect.get_table("some table name")
