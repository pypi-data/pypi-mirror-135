import uuid
from time import time
from typing import AnyStr, Union, Dict, Any, Optional
from requests import Request
from .utils import get_audience_from_url


class TokenStore:
    """
    A basic implementation of TokenStore. It is meant to enable a many to one relationship in between servers
    to authorize and
    """

    def __init__(self):

        # __tokens is a mapping of a token UUID to token dictionary
        # The keys of the token dictionary are as follows:
        #   issuer - the OAuth server issuing the token.
        #   expiry - a timestamp describing when the token expires
        #   access_token - the access token used to authorize
        #   refresh_token - a refresh_token used to
        #   scope - the scope of the token
        self.__tokens = {}

        # __server_token_map is a mapping of audiences to token UUIDs
        self.__server_token_map = {}

    @property
    def tokens(self):
        return list(self.__tokens.values())

    def get_token(self, req: Request = None) -> Union[AnyStr, None]:
        """
        Get a stored token that authorizes a specific request

        :param req: The request.Request to authorize
        :return: An OAuth access token if found, otherwise None
        """
        base_url = get_audience_from_url(req.url)
        token_id = self.__server_token_map.get(base_url)
        if token_id:
            return self.__tokens.get(token_id).get("access_token")
        return None

    def set_token(
        self, token: Dict[AnyStr, Any], req: Optional[Request] = None
    ) -> None:
        """
        Add a token to the token store along with the request it authorizes

        :param token: The OAuth token entry to store. It is a dictionary with the following keys:
          issuer - the OAuth server issuing the token.
          expiry - a timestamp describing when the token expires
          access_token - the access token used to authorize
          refresh_token - a refresh_token used to
          scope - the scope of the token
        :param req: The request.Request that the token authorizes
        """
        token_id = None
        # see if there is an existing token, and if so get the token id
        for stored_token_id, stored_token in self.__tokens.items():
            if int(stored_token.get("expiry")) > time():
                del self.__tokens[stored_token_id]
                continue
            elif token.get("access_token") == stored_token.get("access_token"):
                token_id = stored_token_id

        if not token_id:
            token_id = str(uuid.uuid4())
            self.__tokens[token_id] = token
        if req:
            self.__server_token_map[get_audience_from_url(req.url)] = token_id

    def clear(self) -> None:
        """Clear the tokens in storage"""
        self.__tokens = {}
        self.__server_token_map = {}
