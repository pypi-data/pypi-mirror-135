import unittest
import warnings

from click.testing import CliRunner
import json
from dnastack import __main__ as dnastack_cli

from .base import BaseCliTestCase
from .. import *
from .utils import *


class TestCliWesCommand(BaseCliTestCase):
    def setUpCLI(self):
        self.wes_url = TEST_WES_URI

        self.set_config("wes.url", self.wes_url)
        self.define_oauth_client("wes", TEST_OAUTH_CLIENTS["wes"])
        self.define_refresh_token("wes", TEST_WALLET_REFRESH_TOKEN["wes"])

    def test_wes_info_with_auth(self):
        result_objects = self.assertCommand(["wes", "info"], json_output=True)

        assert_has_property(self, result_objects, "workflow_type_versions")
        assert_has_property(self, result_objects, "supported_wes_versions")
        assert_has_property(self, result_objects, "supported_filesystem_protocols")
        assert_has_property(self, result_objects, "workflow_engine_versions")
        assert_has_property(self, result_objects, "system_state_counts")
