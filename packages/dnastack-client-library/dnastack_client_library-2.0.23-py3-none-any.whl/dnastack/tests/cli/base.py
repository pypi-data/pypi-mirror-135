import json
import unittest
from json import JSONDecodeError
from typing import AnyStr, List, Union, Pattern, Dict, Any

from click.testing import CliRunner

from .utils import clear_config
from ...__main__ import dnastack as cli
from ...auth import OAuthClientParams


class BaseCliTestCase(unittest.TestCase):
    runner = CliRunner(mix_stderr=False)

    def __init__(self, *args, **kwargs):
        self.files = []
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        # FIXME [#180837771] Back up user's configuration and restore it when necessary.
        clear_config()
        self.setUpCLI()

    def setUpCLI(self):
        pass

    def assertCommand(
        self,
        command: List[AnyStr],
        exit_code: int = 0,
        json_output: bool = False,
        has_keys: List[AnyStr] = None,
        has_list_of_keys: List[AnyStr] = None,
        output_pattern: Union[Pattern[AnyStr], AnyStr] = None,
    ) -> Union[Dict[AnyStr, Any], AnyStr, None]:
        result = self.runner.invoke(cli, ["--debug"] + command)

        # print(f"PANDA: EXEC IN: dnastack {' '.join([str(c) for c in command])}")
        # print(f"PANDA: EXEC OUT({result.exit_code}): {result.output}")

        self.assertEqual(
            result.exit_code,
            exit_code,
            f"[dnastack {' '.join([str(c) for c in command])}] "
            f"{'succeeded' if exit_code else 'failed'} "
            f"unexpectedly, expected exit code [{exit_code}],"
            f" got [{result.exit_code}], output: {result.output}",
        )

        if output_pattern:
            self.assertRegex(result.output, output_pattern)

        if json_output:
            try:
                out = json.loads(result.output)

                if has_keys:
                    for key in has_keys:
                        self.assertIn(
                            key,
                            out.keys(),
                            f"Cannot find key [{key}] in the JSON output of "
                            f"{' '.join([str(c) for c in command])}. \n"
                            f"(output: {json.dumps(out)})",
                        )
                elif has_list_of_keys:
                    for item in out:
                        for key in has_list_of_keys:
                            self.assertIn(
                                key,
                                item.keys(),
                                f"Cannot find key [{key}] in an item of the JSON output of "
                                f"{' '.join([str(c) for c in command])}. \n"
                                f"(output: {json.dumps(out, indent=4)}) \n"
                                f"(item: {json.dumps(item, indent=4)})",
                            )

            except JSONDecodeError as j:
                self.fail(
                    f"Unable to parse output as JSON for command [{' '.join(command)}] (output: {result.output})"
                )
        else:
            out = result.output

        return out

    def get_config(self, key: AnyStr, **kwargs):
        result = self.assertCommand(["config", "get", key], **kwargs)
        return result

    def set_config(self, key: AnyStr, value: Any):
        self.assertCommand(["config", "set", key, value])

    def define_oauth_client(self, service: AnyStr, oauth_client: OAuthClientParams):
        self.set_config(f"{service}.auth.url", oauth_client.base_url)
        self.set_config(f"{service}.auth.token_url", oauth_client.token_url)
        self.set_config(
            f"{service}.auth.authorization_url", oauth_client.authorization_url
        )
        self.set_config(f"{service}.auth.device_code_url", oauth_client.device_code_url)
        self.set_config(f"{service}.auth.client.id", oauth_client.client_id)
        self.set_config(f"{service}.auth.client.secret", oauth_client.client_secret)
        self.set_config(
            f"{service}.auth.client.redirect_url", oauth_client.client_redirect_url
        )
        self.set_config(f"{service}.auth.client.scope", oauth_client.scope)

    def define_refresh_token(self, service: AnyStr, refresh_token: AnyStr):
        self.set_config(f"{service}.auth.refresh_token", refresh_token)

    def define_personal_access_token(self, service: AnyStr, email: AnyStr, personal_access_token: AnyStr):
        self.set_config(f"{service}.auth.email", email)
        self.set_config(f"{service}.auth.personal_access_token", personal_access_token)

    def define_service_registry(self, service_registry: AnyStr):
        self.set_config("service_registry.url", service_registry)
