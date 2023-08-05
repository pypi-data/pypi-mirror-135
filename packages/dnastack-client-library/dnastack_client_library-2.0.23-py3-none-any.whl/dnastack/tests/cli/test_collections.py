import csv
import unittest
from io import StringIO

import json

from .base import BaseCliTestCase
from .utils import assert_has_property, set_cli_config, clear_config
from .. import *


class TestCliCollectionsCommand(BaseCliTestCase):
    def setUpCLI(self):
        clear_config()
        self.collections_url = TEST_COLLECTIONS_URI
        self.set_config("collections.url", self.collections_url)

    def test_collections_list(self):
        result = self.assertCommand(["collections", "list"], json_output=True)
        for item in result:
            assert_has_property(self, item, "name")
            assert_has_property(self, item, "id")

    def test_collections_tables_list(self):
        result = self.assertCommand(
            ["collections", "tables", "list", TEST_COLLECTION_NAME], json_output=True
        )
        for item in result:
            assert_has_property(self, item, "name")
            assert_has_property(self, item, "data_model")
            assert_has_property(self, item["data_model"], "$ref")

    def test_collections_tables_list_bad_collection(self):
        result = self.assertCommand(
            ["collections", "tables", "list", "bad-collection"], json_output=True
        )
        self.assertEqual(len(result), 0)

    def test_collections_query(self):
        result = self.assertCommand(
            ["collections", "query", TEST_COLLECTION_NAME, TEST_COLLECTION_QUERY],
            json_output=True,
        )

        self.assertGreater(len(list(result)), 0)

        for item in result:
            assert_has_property(self, item, "start_position")
            assert_has_property(self, item, "sequence_accession")

    def test_collections_query_paginated(self):
        result = self.assertCommand(
            [
                "collections",
                "query",
                TEST_COLLECTION_NAME,
                TEST_COLLECTION_QUERY_PAGINATED,
            ],
            json_output=True,
        )
        self.assertEqual(
            len(result),
            50000,
            f"The paginated result did not return all entries (result: {result})",
        )

        for item in result:
            assert_has_property(self, item, "start_position")
            assert_has_property(self, item, "sequence_accession")

    def test_collections_query_csv(self):
        result = self.assertCommand(
            [
                "collections",
                "query",
                TEST_COLLECTION_NAME,
                TEST_COLLECTION_QUERY,
                "--format",
                "csv",
            ],
        )

        csv_string = StringIO(result)
        csv_results = csv.reader(csv_string)

        header_row = next(csv_results)

        self.assertGreater(len(header_row), 0)

        self.assertIn("start_position", header_row)
        self.assertIn("sequence_accession", header_row)

        for item in csv_results:
            self.assertEqual(len(item), len(header_row))

    def test_collections_query_bad_query(self):
        result = self.assertCommand(
            [
                "collections",
                "query",
                TEST_COLLECTION_NAME,
                "SELECT badfield FROM badtable",
            ],
            exit_code=1,
        )
        # make sure it gives the collection name and url
        self.assertIn(TEST_COLLECTIONS_URI, result)

    def test_collections_query_bad_collection(self):
        result = self.assertCommand(
            ["collections", "query", "badcollection", "SELECT * FROM table"],
            exit_code=1,
        )

        # make sure it gives the collection name and url
        self.assertIn(TEST_COLLECTIONS_URI, result)
