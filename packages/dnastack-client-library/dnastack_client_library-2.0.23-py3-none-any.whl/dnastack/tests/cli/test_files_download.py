import unittest
from click.testing import CliRunner
import pathlib
from dnastack import __main__ as dnastack_cli

from .base import BaseCliTestCase
from .utils import set_cli_config
from .. import *


class TestCliFilesCommand(BaseCliTestCase):
    def test_drs_download(self):
        self.assertCommand(
            [
                "files",
                "download",
                TEST_DRS_WITH_ACCESS_URL,
                "-o",
                "out",
            ]
        )

        self.assertTrue(
            pathlib.Path(
                f"{os.getcwd()}/out/{TEST_DRS[TEST_DRS_WITH_ACCESS_URL]}"
            ).exists()
        )

        # clean up ./out directory
        if pathlib.Path(
            f"{os.getcwd()}/out/{TEST_DRS[TEST_DRS_WITH_ACCESS_URL]}"
        ).exists():
            pathlib.Path(
                f"{os.getcwd()}/out/{TEST_DRS[TEST_DRS_WITH_ACCESS_URL]}"
            ).unlink()
        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    @unittest.skip(
        "Disabling test since the current test file is too large to download in a reasonable amount of time."
    )
    def test_drs_download_access_id(self):
        self.assertCommand(
            [
                "files",
                "download",
                TEST_DRS_WITH_ACCESS_ID,
                "-o",
                "out",
            ]
        )

        self.assertTrue(
            pathlib.Path(
                f"{os.getcwd()}/out/{TEST_DRS[TEST_DRS_WITH_ACCESS_ID]}"
            ).exists()
        )
        # clean up ./out directory
        if pathlib.Path(
            f"{os.getcwd()}/out/{TEST_DRS[TEST_DRS_WITH_ACCESS_ID]}"
        ).exists():
            pathlib.Path(
                f"{os.getcwd()}/out/{TEST_DRS[TEST_DRS_WITH_ACCESS_ID]}"
            ).unlink()
        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_multiple_drs_download(self):
        self.assertCommand(
            ["files", "download"]
            + list(TEST_DRS.keys())
            + [
                "-o",
                "out",
            ],
        )

        for drs_file in TEST_DRS.values():
            self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/{drs_file}").exists())

        # clean up ./out directory
        for drs_file in TEST_DRS.values():
            if pathlib.Path(f"{os.getcwd()}/out/{drs_file}").exists():
                pathlib.Path(f"{os.getcwd()}/out/{drs_file}").unlink()

        pathlib.Path(f"{os.getcwd()}/out").rmdir()

    def test_input_file_flag_drs_download(self):
        with open("download_input_file.txt", "w") as input_file:
            # for some reason writelines doesn't add newlines so add them ourself
            input_file.writelines([f"{drs_url}\n" for drs_url in TEST_DRS.keys()])
            input_file.close()

        self.assertCommand(
            [
                "files",
                "download",
                "-i",
                pathlib.Path("./download_input_file.txt"),
                "-o",
                "out",
            ],
        )

        for drs_file in TEST_DRS.values():
            self.assertTrue(pathlib.Path(f"{os.getcwd()}/out/{drs_file}").exists())

        # clean up ./out directory
        if pathlib.Path(f"{os.getcwd()}/download_input_file.txt").exists():
            pathlib.Path(f"{os.getcwd()}/download_input_file.txt").unlink()
        for drs_file in TEST_DRS.values():
            if pathlib.Path(f"{os.getcwd()}/out/{drs_file}").exists():
                pathlib.Path(f"{os.getcwd()}/out/{drs_file}").unlink()
        pathlib.Path(f"{os.getcwd()}/out").rmdir()
