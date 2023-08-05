import unittest

from .base import BaseCliTestCase
from .. import *


class TestCliServiceRegistry(BaseCliTestCase):
    def setUpCLI(self):
        self.define_service_registry(TEST_SERVICE_REGISTRY)

    @unittest.skip("skip until correct client is configured in service reg")
    def test_service_registry(self):

        self.set_config(
            "data_connect.url",
            "https://collection-service.staging.dnastack.com/library/data-connect",
        )
        self.set_config(
            "data_connect.auth.refresh_token",
            TEST_WALLET_REFRESH_TOKEN["publisher"],
        )

        self.assertCommand(["dataconnect", "tables", "list"], json_output=True)

        service_config = self.get_config("data_connect", json_output=True)

        self.assertEqual(
            "https://collection-service.staging.dnastack.com/library/data-connect/",
            service_config["url"],
        )
        auth_config = service_config["auth"]

        self.assertIn("url", list(auth_config.keys()))
        self.assertIn("client", auth_config.keys())

        client_config = auth_config["client"]

        self.assertIn("id", client_config.keys())
        self.assertIn("secret", client_config.keys())
        self.assertIn("redirect_url", client_config.keys())

    def test_service_registry_existing_config(self):

        # we want to set to prod to make sure they aren't overridden by the service registry
        self.set_config("data_connect.auth.url", TEST_AUTH_PARAMS["prod"]["url"])
        self.set_config(
            "data_connect.auth.client.id", TEST_AUTH_PARAMS["prod"]["client"]["id"]
        )
        self.set_config(
            "data_connect.auth.client.redirect_url",
            TEST_AUTH_PARAMS["prod"]["client"]["redirect_url"],
        )
        self.set_config(
            "data_connect.auth.client.secret",
            TEST_AUTH_PARAMS["prod"]["client"]["secret"],
        )

        self.set_config(
            "data_connect.url",
            "https://collection-service.staging.dnastack.com/library/data-connect",
        )

        service_config = self.get_config("data_connect", json_output=True)

        self.assertEqual(
            "https://collection-service.staging.dnastack.com/library/data-connect/",
            service_config["url"],
        )
        auth_config = service_config["auth"]

        self.assertEqual(auth_config["url"], TEST_AUTH_PARAMS["prod"]["url"])
        self.assertEqual(
            auth_config["client"]["id"], TEST_AUTH_PARAMS["prod"]["client"]["id"]
        )

    def test_service_registry_no_registry_entry(self):

        self.set_config(
            "data_connect.url",
            "https://collection-service.staging.dnastack.com/doesnt-exist/data-connect",
        )

        service_config = self.get_config("data_connect", json_output=True)

        # make sure the url gets configured but none of the auth fields do
        self.assertIn("url", service_config.keys())
        self.assertNotIn("auth", service_config.keys())
