import threading
import unittest
import jwt
from selenium.webdriver.common.by import By

from .base import BaseCliTestCase
from .utils import *
from .. import *
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep, time


class TestCliAuthCommand(BaseCliTestCase):
    def setUpCLI(self):
        self.data_connect_url = TEST_DATA_CONNECT_URI
        self.collections_url = TEST_COLLECTIONS_URI

        self.set_config("data_connect.url", self.data_connect_url)
        self.set_config("collections.url", self.collections_url)
        self.define_oauth_client("data_connect", TEST_OAUTH_CLIENTS["publisher"])
        self.define_oauth_client("collections", TEST_OAUTH_CLIENTS["publisher"])

    @staticmethod
    def do_login_steps(proc, auth_test, allow=True):
        # wait for device code url
        retries = 5
        while True:
            device_code_url = proc.stdout.readline().decode("utf-8")
            if device_code_url:
                break
            elif retries == 0:
                raise Exception()
            sleep(1)
            retries -= 1

        auth_test.assertIsNotNone(device_code_url)

        # make sure the browser is opened in headless mode
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(device_code_url)

        driver.execute_script(
            (
                f"document.querySelector('form[name=\"token\"] input[name=\"token\"]').value = '{TEST_WALLET_PERSONAL_ACCESS_TOKEN_DNASTACK}';"
                f"document.querySelector('form[name=\"token\"] input[name=\"email\"]').value = '{TEST_WALLET_EMAIL}';"
            )
        )
        token_form = driver.find_element(By.CSS_SELECTOR, "form[name='token']")
        token_form.submit()

        sleep(2)

        driver.find_element(By.ID, "continue-btn").click()

        if allow:
            driver.find_element(By.ID, "allow-btn").click()
        else:
            driver.find_element(By.ID, "deny-btn").click()

        driver.quit()

    @unittest.skip("skipping temporarily due to 'slow down' messages")
    def test_login(self):
        proc = subprocess.Popen(
            [
                "python3",
                "-m",
                "dnastack",
                "auth",
                "login",
                "dataconnect",
                "--no-browser",
            ],
            stdout=subprocess.PIPE,
        )

        login_thread = threading.Thread(
            target=self.do_login_steps,
            args=(
                proc,
                self,
            ),
        )
        login_thread.start()

        login_thread.join()
        proc.wait(timeout=20)
        output, error = proc.communicate()
        exit_code = proc.returncode

        self.assertEqual(
            exit_code,
            0,
            msg=f"Login failed with output: {output.decode('utf-8')} (exit code {exit_code})",
        )
        self.assertIn("login successful", output.decode("utf-8").lower())

        self.assertIsNotNone(get_cli_config(self.runner, f"tokens"))
        token = json.loads(get_cli_config(self.runner, f"tokens"))

        assert_has_property(self, token, "access_token")
        self.access_token = token["access_token"]

        assert_has_property(self, token, "refresh_token")
        self.refresh_token = token["refresh_token"]

        access_jwt = jwt.decode(self.access_token, options={"verify_signature": False})
        self.assertEqual(access_jwt["tokenKind"], "bearer")
        jwt_scopes = access_jwt["scope"].split(" ")
        for scope in TEST_AUTH_SCOPES["publisher"].split():
            self.assertIn(scope, jwt_scopes)
        self.assertEqual(
            access_jwt["azp"], TEST_AUTH_PARAMS["publisher"]["client"]["id"]
        )
        self.assertEqual(f"{access_jwt['iss']}/", TEST_AUTH_PARAMS["publisher"]["url"])
        self.assertGreater(access_jwt["exp"], time())

    def test_login_no_config(self):
        clear_config()
        result = self.assertCommand(["auth", "login", "dataconnect"], exit_code=1)
        self.assertIn(
            "there is no configured service",
            result.lower(),
        )

    @unittest.skip("skipping temporarily due to 'slow down' messages")
    def test_login_deny(self):
        proc = subprocess.Popen(
            [
                "python3",
                "-m",
                "dnastack",
                "auth",
                "login",
                "dataconnect",
                "--no-browser",
            ],
            stdout=subprocess.PIPE,
        )

        login_thread = threading.Thread(
            target=self.do_login_steps,
            args=(proc, self, False),
            name="login",
        )
        login_thread.start()

        login_thread.join()
        proc.wait(timeout=5)
        output, err = proc.communicate()

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("login failed", output.decode("utf-8").lower())
        self.assertIn("access denied", output.decode("utf-8").lower())

    # def test_refresh(self):
    #     old_token = json.loads(
    #         get_cli_config(self.runner, f"oauth|{self.wallet_url}", delimiter="|")
    #     )
    #
    #     result = self.runner.invoke(
    #         dnastack_cli.dnastack,
    #         ["auth", "refresh", "dataconnect"],
    #     )
    #
    #     self.assertEqual(result.exit_code, 0)
    #
    #     # make sure the access_token has changed
    #     new_token = json.loads(
    #         get_cli_config(self.runner, f"oauth|{self.wallet_url}", delimiter="|")
    #     )
    #     self.assertNotEqual(old_token["access_token"], new_token["access_token"])
    #
    # def test_refresh_token_missing_token(self):
    #     wallet_url = get_cli_config(self.runner, "data_connect.auth.url")
    #     set_cli_config(
    #         self.runner, f"oauth|{wallet_url}|access_token", "", delimiter="|"
    #     )
    #     set_cli_config(
    #         self.runner, f"oauth|{wallet_url}|refresh_token", "", delimiter="|"
    #     )
    #
    #     result = self.runner.invoke(
    #         dnastack_cli.dnastack,
    #         ["auth", "refresh", "dataconnect"],
    #     )
    #
    #     self.assertNotEqual(
    #         result.exit_code,
    #         0,
    #         msg=(
    #             f"'auth refresh' with no token did not fail as expected."
    #             f" output: {result.output}"
    #             f" exit code: {result.exit_code}"
    #         ),
    #     )
    #     self.assertIn("There is no refresh token configured", result.output)
    #
    # def test_refresh_token_bad_token(self):
    #     wallet_url = get_cli_config(self.runner, "data_connect.auth.url")
    #     set_cli_config(
    #         self.runner, f"oauth|{wallet_url}|access_token", "", delimiter="|"
    #     )
    #     set_cli_config(
    #         self.runner, f"oauth|{wallet_url}|refresh_token", "badtoken", delimiter="|"
    #     )
    #     result = self.runner.invoke(
    #         dnastack_cli.dnastack,
    #         ["auth", "refresh", "dataconnect"],
    #     )
    #
    #     self.assertNotEqual(result.exit_code, 0)
    #     self.assertIn("Unable to refresh token", result.output)
