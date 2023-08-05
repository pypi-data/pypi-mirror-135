from typing import List, Iterator, AnyStr

from requests.auth import AuthBase

from .base_client import BaseServiceClient
from ..constants import DEFAULT_SERVICE_REGISTRY
from ..exceptions import ServiceException
from .utils import PaginatedResponse


class CollectionsClient(BaseServiceClient):
    """
    A Client for a DNAStack Collections instance

    :param url: The url of the Collections service
    :param auth:
    """

    def __init__(
        self,
        url: str,
        auth: AuthBase = None,
        registry_url: AnyStr = DEFAULT_SERVICE_REGISTRY,
    ):
        super().__init__(url=url, auth=auth, registry_url=registry_url)

    def list_collections(self) -> List[dict]:
        """
        Return a list of collections available at the Collections url

        :return: A list of collection metadata
        """
        res = self.client.get(self.url)

        if not res.ok:
            self._raise_error(res, "Unable to list collections")

        return res.json()

    def list_tables(self, collection_name: str) -> List[dict]:
        """
        Returns a list of table within the specified collection

        :param collection_name: The name of the collection
        :return: A dict of table metadata of the tables in the collection
        """
        collection_tables_url = self.url + f"{collection_name}/data-connect/tables"
        res = self.client.get(collection_tables_url)

        if not res.ok:
            self._raise_error(res, "Unable to list tables for collection")

        return res.json()

    def query(self, collection_name: AnyStr, q: AnyStr) -> Iterator:
        """
        Execute a SQL query against a Collection

        :param collection_name: The name of the collection
        :param q: The query to be executed
        :return: A dict object of query results
        """
        collection_query_url = self.url + f"{collection_name}/data-connect/search"
        res = self.client.post(collection_query_url, json={"query": q})

        if not res.ok:
            self._raise_error(res, "Unable to query collection")

        return PaginatedResponse(res)
