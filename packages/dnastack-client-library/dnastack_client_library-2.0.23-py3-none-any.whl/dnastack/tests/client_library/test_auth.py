import unittest
from ... import PublisherClient
from requests import Request

from .. import *
from ...auth import (
    PersonalAccessTokenAuth,
    RefreshTokenAuth,
    OAuthClientParams,
    OAuthTokenAuth,
)
from ...auth.oauth_client import DEFAULT_AUTH_CLIENT
from ...auth.token_store import TokenStore


class TestClientLibraryAuthCommand(unittest.TestCase):
    def setUp(self):
        self.dataconnect_url = TEST_DATA_CONNECT_URI
        self.collections_url = TEST_COLLECTIONS_URI

        self.oauth_client = DEFAULT_AUTH_CLIENT

        self.auth = PersonalAccessTokenAuth(
            email=TEST_WALLET_EMAIL,
            personal_access_token=TEST_WALLET_PERSONAL_ACCESS_TOKEN_PUBLISHER,
            oauth_client=self.oauth_client,
        )
        self.publisher_client = PublisherClient(
            dataconnect_url=self.dataconnect_url,
            collections_url=self.collections_url,
            auth=self.auth,
        )

    def test_login_nested_client(self):
        self.publisher_client.dataconnect.authorize()
        self.assertIsNotNone(
            self.publisher_client.auth.token_store.get_token(
                Request(url=self.dataconnect_url)
            )
        )

    def test_login_bad_credentials(self):
        self.publisher_client.personal_access_token = "badtoken"
        with self.assertRaises(Exception) as ctx:
            self.publisher_client.dataconnect.authorize()
            self.assertIsNotNone(ctx.exception.message)
            self.assertIn(
                "The personal access token and/or email provided is invalid",
                ctx.exception.message,
            )

    def test_login_bad_drs_server(self):
        with self.assertRaises(Exception) as ctx:
            self.publisher_client.files.authorize(drs_server="badserver")
            self.assertIsNotNone(ctx.exception.message)
            self.assertIn("The authorization failed", ctx.exception.message)

    def test_refresh_token(self):
        # first we must clear the existing token and replace with just a refresh_token

        refresh_auth = RefreshTokenAuth(
            refresh_token=TEST_WALLET_REFRESH_TOKEN["publisher"],
            oauth_client=self.publisher_client.auth.oauth_client,
        )
        self.publisher_client.dataconnect.auth = refresh_auth

        self.publisher_client.auth.token_store.clear()

        self.publisher_client.dataconnect.authorize()

        self.assertIsNotNone(
            self.publisher_client.dataconnect.auth.token_store.get_token(
                Request(url=self.dataconnect_url)
            )
        )

    def test_refresh_token_missing_token(self):
        with self.assertRaises(Exception) as ctx:
            self.publisher_client.auth.oauth[
                self.publisher_client.dataconnect.get_auth_url()
            ] = {}
            self.publisher_client.auth.refresh_token_for_service(
                service_type="dataconnect"
            )

            self.assertIsNotNone(ctx.exception.message)
            self.assertIn(
                "There is no refresh token configured.", ctx.exception.message
            )

    def test_refresh_token_bad_token(self):
        with self.assertRaises(Exception) as ctx:
            self.publisher_client.auth.oauth[
                self.publisher_client.dataconnect.get_wallet_url()
            ] = {}
            self.publisher_client.auth.set_refresh_token_for_service(
                service_type="dataconnect", token="badrefresh"
            )

            self.publisher_client.auth.refresh_token_for_service(
                service_type="dataconnect"
            )

            self.assertIsNotNone(ctx.exception.message)
            self.assertIn(
                "There is no refresh token configured.", ctx.exception.message
            )
