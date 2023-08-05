import unittest
from ... import PublisherClient
from .. import *
from ...auth import RefreshTokenAuth, OAuthClientParams
from ...client.base_exceptions import ApiError


def assert_has_property(self, obj, attribute):
    self.assertTrue(
        attribute in obj,
        msg="obj lacking an attribute. obj: %s, intendedAttribute: %s"
        % (obj, attribute),
    )


class TestClientLibraryDataConnectQueryCommand(unittest.TestCase):
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
        self.publisher_client = PublisherClient(dataconnect_url=TEST_DATA_CONNECT_URI, auth=self.auth)

    def test_variant_query(self):
        result = self.publisher_client.dataconnect.query(
            f"SELECT * FROM {TEST_DATA_CONNECT_VARIANTS_TABLE} LIMIT 10"
        )
        self.assertIsNotNone(result)

        for item in result:
            assert_has_property(self, item, "start_position")
            assert_has_property(self, item, "end_position")
            assert_has_property(self, item, "reference_bases")
            assert_has_property(self, item, "alternate_bases")
            assert_has_property(self, item, "sequence_accession")

    def test_drs_url_query(self):
        result = self.publisher_client.dataconnect.query(
            f"SELECT drs_url FROM {TEST_DATA_CONNECT_FILES_TABLE} LIMIT 10"
        )
        self.assertIsNotNone(result)

        for item in result:
            assert_has_property(self, item, "drs_url")

    def test_incorrect_column_query(self):
        with self.assertRaises(ApiError):
            results = self.publisher_client.dataconnect.query(
                f"SELECT invalid_column FROM {TEST_DATA_CONNECT_VARIANTS_TABLE} LIMIT 10"
            )
            # some errors are only apparent after the paginated response is returned, so we try to get a list
            # to raise the error
            list(results)

    def test_broken_query(self):
        with self.assertRaises(ApiError):
            results = self.publisher_client.dataconnect.query("broken_query")

            # some errors are only apparent after the paginated response is returned, so we try to get a list
            # to raise the error
            list(results)
