import time
import unittest
import warnings

from click.testing import CliRunner
import json
from dnastack import __main__ as dnastack_cli

from .base import BaseCliTestCase
from .utils import *
from .. import *

unittest.TestLoader.sortTestMethodsUsing = None


def assert_has_property(self, obj, attribute):
    self.assertTrue(
        attribute in obj,
        msg="obj lacking an attribute. obj: %s, intendedAttribute: %s"
        % (obj, attribute),
    )


class TestCliWesRunsCommand(BaseCliTestCase):
    def setUpCLI(self):
        self.wes_url = TEST_WES_URI

        self.set_config("wes.url", self.wes_url)
        self.define_oauth_client("wes", TEST_OAUTH_CLIENTS["wes"])
        self.define_refresh_token("wes", TEST_WALLET_REFRESH_TOKEN["wes"])

    def test_wes_runs_execute(self):
        self.__execute_workflow()

    def test_wes_runs_execute_multiple_attachments(self):
        with open(TEST_WDL_MULTI_GREETING, "r") as main_wdl:
            wdl_main_file_path = self.__create_file("main.wdl", main_wdl.read())

        with open(TEST_WDL_MULTI_GREETING, "r") as greeting_wdl:
            wdl_greeting_attachment_file = self.__create_file(
                "greeting.wdl", greeting_wdl.read()
            )

        with open(TEST_WDL_MULTI_FAREWELL, "r") as farewell_wdl:
            wdl_farewell_attachment_file = self.__create_file(
                "farewell.wdl", farewell_wdl.read()
            )

        wdl_input_param_file_path = self.__create_file(
            "input.json", TEST_WDL_INPUT_PARAM_CONTENTS
        )
        wdl_engine_param_file_path = self.__create_file(
            "engine.json", TEST_WDL_ENGINE_PARAM_CONTENTS
        )
        wdl_tag_file_path = self.__create_file("tag.json", TEST_WDL_TAG_CONTENTS)
        result = self.assertCommand(
            [
                "wes",
                "runs",
                "execute",
                "--workflow-url",
                "main.wdl",
                "--attachment",
                wdl_main_file_path,
                "--attachment",
                wdl_greeting_attachment_file,
                "--attachment",
                wdl_farewell_attachment_file,
                "--inputs-file",
                wdl_input_param_file_path,
                "--engine-parameters-file",
                wdl_engine_param_file_path,
                "--tags-file",
                wdl_tag_file_path,
            ],
            json_output=True,
        )

        assert_has_property(self, result, "run_id")

        os.remove(wdl_main_file_path)
        os.remove(wdl_greeting_attachment_file)
        os.remove(wdl_farewell_attachment_file)
        os.remove(wdl_input_param_file_path)
        os.remove(wdl_engine_param_file_path)
        os.remove(wdl_tag_file_path)

        return result

    def test_wes_runs_list(self):
        self.__execute_workflow()
        self.__execute_workflow()
        result = self.assertCommand(["wes", "runs", "list", "--page-size", 1])
        output = result.split("wes runs list")
        result_objects = json.loads(output[0])
        assert_has_property(self, result_objects, "runs")
        assert_has_property(self, result_objects, "next_page_token")
        self.assertEqual(len(result_objects["runs"]), 1)
        self.assertEqual(
            f" --page-token {result_objects['next_page_token']}\n", output[1]
        )

        result = self.assertCommand(
            ["wes", "runs", "list", "--page-token", result_objects["next_page_token"]]
        )
        output = result.split("wes runs list")

        result_objects = json.loads(output[0])
        assert_has_property(self, result_objects, "runs")
        self.assertEqual(len(result_objects["runs"]), 1)

        result = self.assertCommand(["wes", "runs", "list", "--all"], json_output=True)
        assert_has_property(self, result, "runs")
        self.assertTrue(len(result["runs"]) > 0)
        self.assertTrue("next_page_token" not in result)

    def test_run_get(self):
        self.__execute_workflow()
        result = self.assertCommand(["wes", "runs", "list", "--page-size", 1])
        output = result.split("wes runs list")
        result_objects = json.loads(output[0])
        run_id = result_objects["runs"][0]["run_id"]

        result = self.assertCommand(["wes", "run", "get", run_id], json_output=True)

        assert_has_property(self, result, "run_id")
        assert_has_property(self, result, "request")
        assert_has_property(self, result, "state")
        assert_has_property(self, result, "run_log")
        assert_has_property(self, result, "task_logs")
        assert_has_property(self, result, "outputs")

        result = self.assertCommand(
            ["wes", "run", "get", run_id, "--status"], json_output=True
        )

        assert_has_property(self, result, "run_id")
        assert_has_property(self, result, "state")
        self.assertNotIn("request", result)
        self.assertNotIn("run_log", result)
        self.assertNotIn("task_logs", result)
        self.assertNotIn("outputs", result)

    def test_wes_run_cancel(self):
        result = self.__execute_workflow()
        run_id = result["run_id"]
        time.sleep(10)
        result = self.assertCommand(["wes", "run", "cancel", run_id], json_output=True)

        assert_has_property(self, result, "run_id")

    @unittest.skip(
        "Disabling temporarily since WES service is inconsistent and fails this test due to timeout"
    )
    def test_wes_run_logs(self):
        result = self.__execute_workflow()
        run_id = result["run_id"]
        time.sleep(5)
        time_remaining = 240

        run_status = self.assertCommand(
            ["wes", "run", "get", run_id, "--status"], json_output=True
        )

        while run_status.get("state") in ("INITIALIZING", "RUNNING"):
            if time_remaining <= 0:
                self.assertCommand(["wes", "run", "cancel", run_id])
                self.fail("The workflow timed out")
            time_remaining -= 10
            time.sleep(10)
            run_status = self.assertCommand(
                ["wes", "run", "get", run_id, "--status"], json_output=True
            )

        result = self.assertCommand(
            [
                "wes",
                "run",
                "logs",
                run_id,
                "--stdout",
                "--task",
                "hello_world.first_greeting",
            ]
        )

        self.assertEqual(result, "Hello World, my name is Patrick!\n\n")

        result = self.assertCommand(
            [
                "wes",
                "run",
                "logs",
                run_id,
                "--stdout",
                "--task",
                "hello_world.say_greeting",
                "--index",
                1,
            ]
        )

        self.assertEqual(result, "Hello World, my name is Patrick!\n\n")

        result = self.assertCommand(
            [
                "wes",
                "run",
                "logs",
                run_id,
                "--url",
                TEST_WES_URI
                + "ga4gh/wes/v1/runs/"
                + run_id
                + "/logs/task/hello_world.say_greeting/0/stdout",
            ]
        )

        self.assertEqual(result, "Hello World, my name is Patrick!\n\n")

    @staticmethod
    def __create_file(file_name, contents):
        with open(file_name, "w") as file:
            file.write(contents)
            return os.path.realpath(file.name)

    def __execute_workflow(self):
        wdl_file_path = self.__create_file("workflow.wdl", TEST_WDL_FILE_CONTENTS)
        wdl_input_param_file_path = self.__create_file(
            "input.json", TEST_WDL_INPUT_PARAM_CONTENTS
        )
        wdl_engine_param_file_path = self.__create_file(
            "engine.json", TEST_WDL_ENGINE_PARAM_CONTENTS
        )
        wdl_tag_file_path = self.__create_file("tag.json", TEST_WDL_TAG_CONTENTS)
        result_objects = self.assertCommand(
            [
                "wes",
                "runs",
                "execute",
                "--workflow-url",
                "workflow.wdl",
                "--attachment",
                wdl_file_path,
                "--inputs-file",
                wdl_input_param_file_path,
                "--engine-parameters-file",
                wdl_engine_param_file_path,
                "--tags-file",
                wdl_tag_file_path,
            ],
            json_output=True,
        )

        assert_has_property(self, result_objects, "run_id")

        os.remove(wdl_file_path)
        os.remove(wdl_input_param_file_path)
        os.remove(wdl_engine_param_file_path)
        os.remove(wdl_tag_file_path)

        return result_objects
