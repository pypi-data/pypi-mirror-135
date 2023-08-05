import os
import unittest
import pathlib
from ... import PublisherClient
from .. import *
import json
from ...auth import RefreshTokenAuth, OAuthClientParams


class TestCliWesCommand(unittest.TestCase):
    def setUp(self):
        self.auth = RefreshTokenAuth(
            refresh_token=TEST_WALLET_REFRESH_TOKEN["wes"],
            oauth_client=OAuthClientParams(
                base_url=TEST_AUTH_PARAMS["wes"]["url"],
                client_id=TEST_AUTH_PARAMS["wes"]["client"]["id"],
                client_secret=TEST_AUTH_PARAMS["wes"]["client"]["secret"],
                client_redirect_url=TEST_AUTH_PARAMS["wes"]["client"]["redirect_url"],
                scope=TEST_AUTH_SCOPES["wes"],
            ),
        )
        self.wes_url = TEST_WES_URI
        self.publisher_client = PublisherClient(wes_url=self.wes_url, auth=self.auth)

    def test_wes_info_with_auth(self):
        result = self.publisher_client.wes.info()

        self.assertIsNotNone(result)

        self.assertIn("workflow_type_versions", result.keys())
        self.assertIn("supported_wes_versions", result.keys())
        self.assertIn("supported_filesystem_protocols", result.keys())
        self.assertIn("workflow_engine_versions", result.keys())
        self.assertIn("system_state_counts", result.keys())
