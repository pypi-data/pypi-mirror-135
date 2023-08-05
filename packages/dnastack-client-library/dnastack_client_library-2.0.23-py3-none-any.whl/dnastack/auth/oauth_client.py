from typing import AnyStr, Optional

from ..constants import DEFAULT_AUTH_SCOPES
from ..exceptions import InvalidOAuthClientParamsError


class OAuthClientParams:
    """
    The parameters required to authorize using an OAuth 2.0 Connect client

    :param base_url: The base url used to connect to the OAuth 2.0 client
    :param authorization_url: The authorization url used to connect to the OAuth 2.0 client
    :param device_code_url: The device code used to connect to the OAuth 2.0 client
    :param token_url: The token url used to connect to the OAuth 2.0 client
    :param client_id: The id of the OAuth 2.0 client
    :param client_secret: The secret of the OAuth 2.0 client
    :param client_redirect_url: The redirect url of the OAuth 2.0 client
    :param scope: AnyStr = The scope that the OAuth 2.0 client is allowed to authorize for
    """

    def __init__(
        self,
        client_id: AnyStr,
        client_secret: AnyStr,
        client_redirect_url: AnyStr,
        scope: AnyStr = DEFAULT_AUTH_SCOPES,
        base_url: AnyStr = None,
        authorization_url: AnyStr = None,
        device_code_url: Optional[AnyStr] = None,
        token_url: AnyStr = None,
    ):
        self.base_url = base_url
        if self.base_url:
            self.authorization_url = (
                authorization_url
                if authorization_url
                else self.base_url + "oauth/authorize"
            )
            self.device_code_url = (
                device_code_url
                if device_code_url
                else self.base_url + "oauth/device/code"
            )
            self.token_url = token_url if token_url else self.base_url + "oauth/token"
        else:
            if not token_url:
                raise InvalidOAuthClientParamsError(
                    "No token url is defined. "
                    "Either one of base_url or token_url must be defined"
                )
            else:
                self.token_url = token_url

            self.authorization_url = authorization_url if authorization_url else None
            self.device_code_url = device_code_url if device_code_url else None

        self.client_id = client_id
        self.client_secret = client_secret
        self.client_redirect_url = client_redirect_url
        self.scope = scope


DEFAULT_AUTH_CLIENT = OAuthClientParams(
    base_url="https://wallet.publisher.dnastack.com/",
    client_id="publisher-cli",
    client_secret="WpEmHtAiB73pCrhbEyci42sBFcfmWBdj",
    client_redirect_url="https://wallet.publisher.dnastack.com/",
    scope=DEFAULT_AUTH_SCOPES,
)
