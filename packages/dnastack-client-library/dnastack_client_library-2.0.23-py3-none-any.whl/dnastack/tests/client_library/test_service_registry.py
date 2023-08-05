import os
import unittest
import pathlib
import warnings

from ... import PublisherClient
from .. import *
from ...auth import DeviceCodeAuth


class TestClientLibraryServiceRegistry(unittest.TestCase):
    def test_service_registry(self):

        self.publisher_client = PublisherClient(
            dataconnect_url="https://collection-service.staging.dnastack.com/library/data-connect/",
            registry_url=TEST_SERVICE_REGISTRY,
        )

        self.assertEqual(
            "https://collection-service.staging.dnastack.com/library/data-connect/",
            self.publisher_client.dataconnect.url,
        )

        # make sure it uses the staging auth params
        self.assertEqual(
            self.publisher_client.dataconnect.auth.oauth_client.authorization_url,
            TEST_AUTH_PARAMS["staging"]["url"] + "oauth/authorize",
        )

        self.publisher_client = PublisherClient(
            dataconnect_url="https://collection-service.staging.dnastack.com/library/data-connect/",
            registry_url=TEST_SERVICE_REGISTRY,
            auth=DeviceCodeAuth(),
        )

        self.assertIsNotNone(self.publisher_client.dataconnect.auth)
        self.assertIsInstance(self.publisher_client.dataconnect.auth, DeviceCodeAuth)

        self.assertEqual(
            self.publisher_client.dataconnect.auth.oauth_client.authorization_url,
            TEST_AUTH_PARAMS["staging"]["url"] + "oauth/authorize",
        )

    def test_service_registry_no_registry_entry(self):

        self.publisher_client = PublisherClient(
            dataconnect_url="https://collection-service.staging.dnastack.com/doesnt-exist/data-connect/",
            registry_url=TEST_SERVICE_REGISTRY,
        )

        # make sure the service's url is still configured
        self.assertEqual(
            "https://collection-service.staging.dnastack.com/doesnt-exist/data-connect/",
            self.publisher_client.dataconnect.url,
        )

        # make sure it uses no auth
        self.assertIsNone(self.publisher_client.dataconnect.auth)

        self.publisher_client = PublisherClient(
            dataconnect_url="https://collection-service.staging.dnastack.com/doesnt-exist/data-connect/",
            registry_url=TEST_SERVICE_REGISTRY,
            auth=DeviceCodeAuth(),
        )

        self.assertIsNotNone(self.publisher_client.dataconnect.auth)
        self.assertIsInstance(self.publisher_client.dataconnect.auth, DeviceCodeAuth)

        self.assertIsNone(self.publisher_client.dataconnect.auth.oauth_client)
