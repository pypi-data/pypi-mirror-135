import os
from typing import Union, List, Any, AnyStr

from requests.auth import AuthBase

from . import *
from .base_client import BaseServiceClient
from ..auth import OAuthTokenAuth
from ..constants import DEFAULT_SERVICE_REGISTRY


class PublisherClient:
    """
    A Client for DNAStack suite of products (Data Connect, WES, Collections, etc.)


    :param dataconnect_url: The url for the Data Connect instance
    :param collections_url: The url for the Collections instance
    :param wes_url: The url for the Workflow Execution Service (WES) instance
    """

    def __init__(
        self,
        dataconnect_url: str = None,
        collections_url: str = None,
        wes_url: str = None,
        auth: AuthBase = None,
        registry_url: AnyStr = DEFAULT_SERVICE_REGISTRY,
    ):
        self.auth = auth
        self.__services = []

        if dataconnect_url:
            if isinstance(self.auth, OAuthTokenAuth):
                self.__dataconnect = DataConnectClientV2(url=dataconnect_url, auth=self.auth, registry_url=registry_url)
            else:
                self.__dataconnect = DataConnectClientV2(url=dataconnect_url, auth=None, registry_url=registry_url)

        if collections_url:
            self.__collections = CollectionsClient(
                url=collections_url, auth=self.auth, registry_url=registry_url
            )

        if wes_url:
            self.__wes = WesClient(url=wes_url, auth=auth, registry_url=registry_url)

        if isinstance(self.auth, OAuthTokenAuth):
            self.__files = FilesClient(self.auth)
        else:
            self.__files = FilesClient(None)

    @property
    def dataconnect(self) -> DataConnectClientV2:
        return self.__dataconnect

    @dataconnect.setter
    def dataconnect(self, client: DataConnectClientV2):
        assert client is None or isinstance(client, DataConnectClientV2)
        self.__dataconnect = client

    @property
    def collections(self) -> CollectionsClient:
        return self.__collections

    @collections.setter
    def collections(self, client: CollectionsClient):
        assert client is None or isinstance(client, CollectionsClient)
        self.__collections = client

    @property
    def wes(self) -> WesClient:
        return self.__wes

    @wes.setter
    def wes(self, client: WesClient):
        assert client is None or isinstance(client, WesClient)
        self.__wes = client

    @property
    def files(self) -> FilesClient:
        return self.__files

    @files.setter
    def files(self, client: FilesClient):
        assert client is None or isinstance(client, WesClient)
        self.__wes = client

    def get_services(self) -> List[BaseServiceClient]:
        """
        Return all configured services.

        :return: List of all configured clients (dataconnect, collections, wes)
        """
        return [self.dataconnect, self.collections, self.wes]

    def load(self, urls: Union[str, List[str]]) -> Any:
        """
        Return the raw output of one or more DRS resources

        :param urls: One or a list of DRS urls (drs://...)
        :return: The raw output of the specified DRS resource
        """
        if isinstance(urls, str):
            urls = [urls]

        download_content = []

        self.files.download_files(
            urls=urls,
            display_progress_bar=False,
            out=download_content,
        )
        return download_content

    def download(
        self,
        urls: Union[str, List[str]],
        output_dir: str = os.getcwd(),
        display_progress_bar: bool = False,
    ) -> None:
        """
        Download one or more DRS resources from the specified urls

        :param urls: One or a list of DRS urls (drs://...)
        :param output_dir: The directory to output the downloaded files to.
        :param display_progress_bar: Display the progress of the downloads. This is False by default
        :return:
        """
        if isinstance(urls, str):
            urls = [urls]

        self.files.download_files(
            urls=urls,
            output_dir=output_dir,
            display_progress_bar=display_progress_bar,
        )
