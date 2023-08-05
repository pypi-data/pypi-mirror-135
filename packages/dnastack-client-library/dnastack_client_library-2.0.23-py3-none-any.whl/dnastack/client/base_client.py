from typing import AnyStr

import requests
from requests import Session, Request, Response
from requests.auth import AuthBase

from .service_registry import ServiceRegistry
from ..auth import OAuthTokenAuth, DeviceCodeAuth
from ..constants import DEFAULT_SERVICE_REGISTRY
from ..exceptions import ServiceException


class BaseServiceClient:
    """
    The base class for all DNAStack Clients

    :param parent: The parent :class:`PublisherClient` instance of the client. If a parent is not defined, the
    service client will create its own :class:`AuthClient` for authorization
    :param url: The url of the service to be configured
    :param **kwargs: Additional keyword arguments to be passed to the :class:`AuthClient` if necessary
    """

    def __init__(self, auth: AuthBase = None, url: AnyStr = None, registry_url: str = DEFAULT_SERVICE_REGISTRY,
                 **kwargs):
        self.__url = url
        self.__client = requests.Session()
        self.__registry = ServiceRegistry(registry_url)
        self.__authorized = False

        reg_config = self.__registry.get(self.url)

        if auth:
            self.auth = auth
        elif reg_config.oauth_client:
            self.auth = DeviceCodeAuth(reg_config.oauth_client)
        else:
            self.auth = None

    def __del__(self):
        self.__client.close()

    @property
    def url(self):
        return self.__url

    @property
    def auth(self) -> AuthBase:
        return self.__auth

    @auth.setter
    def auth(self, auth: AuthBase) -> None:
        self.__auth = auth
        self.__client.auth = auth
        self.__authorized = False

        # Try to additionally add OAuthClientParams if we don't have them
        # FIXME Explore the better way to do this as part of OAuthTokenAuth.
        if isinstance(self.auth, OAuthTokenAuth) and self.__auth.oauth_client is None:
            reg_config = self.__registry.get(self.url)
            if reg_config.oauth_client:
                self.__auth.oauth_client = reg_config.oauth_client
                self.__client.auth.oauth_client = reg_config.oauth_client

    @property
    def client(self) -> Session:
        return self.__client

    def authorize(self):
        if self.__authorized:
            return

        if isinstance(self.__auth, OAuthTokenAuth):
            self.__auth.authorize(Request(url=self.url))
            self.__authorized = True
        else:
            raise AttributeError(
                "The service auth must be a OAuthTokenAuth in order to authorize"
            )

    def _raise_error(self, res: Response, primary_reason: str):
        error_msg = primary_reason

        if res.status_code == 401:
            error_msg += ": The request was not authenticated"
        elif res.status_code == 403:
            error_msg += ": Access Denied"
        else:
            error_json = res.json()
            if "errors" in error_json:
                error_msg += f' ({error_json["errors"][0]["title"]})'

        raise ServiceException(msg=error_msg, url=self.url)
