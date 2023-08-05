import webbrowser
from json import JSONDecodeError
from time import time, sleep
from typing import List, AnyStr, Dict, Any
from urllib.parse import urlparse, parse_qs, urlunparse

import click
import requests

from .oauth_client import OAuthClientParams, DEFAULT_AUTH_CLIENT
from ..constants import DEFAULT_AUTH_SCOPES
from ..exceptions import LoginException, RefreshException


def get_audience_from_url(url: str) -> str:
    """
    Return the formatted audience from

    :param url: The url to generate an audience from
    :raises LoginException if an audience cannot be generated
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme in ("https", "drs"):
        return str(urlunparse(("https", parsed_url.netloc, "/", "", "", "")))
    else:
        raise LoginException(
            url=url,
            msg=f"Cannot get audience from url (scheme must be either 'https' or 'drs')",
        )


def login_personal_access_token(
    audience: List[str],
    email: str,
    personal_access_token: str,
    oauth_client: OAuthClientParams,
) -> Dict[AnyStr, Any]:
    """
    Generate an access token for a service using a Personal Access Token (PAT)

    :param audience: The service url(s) to authorize
    :param email: The email to authenticate with the authorization server
    :param personal_access_token: The personal access token (PAT) to authenticate with the authorization server
    :param oauth_client: The authorization parameters of the service to be authorized.
    :return: A dict containing the OAuth access token as well as an expiry and a refresh token
    """
    session = requests.Session()
    # login at /login/token
    login_res = session.get(
        oauth_client.base_url + "login/token",
        params={"token": personal_access_token, "email": email},
        allow_redirects=False,
    )

    if not login_res.ok:
        session.close()
        raise LoginException(
            url=oauth_client.base_url,
            msg="The personal access token and/or email provided is invalid",
        )

    auth_code_res = session.get(
        oauth_client.base_url + "oauth/authorize",
        params={
            "response_type": "code",
            "scope": DEFAULT_AUTH_SCOPES,
            "client_id": oauth_client.client_id,
            "redirect_uri": oauth_client.client_redirect_url,
            "resource": ",".join(audience),
        },
        allow_redirects=False,
    )

    if "Location" in auth_code_res.headers:
        auth_code_redirect_url = urlparse(auth_code_res.headers["Location"])
    else:
        session.close()
        raise LoginException(url=oauth_client.base_url, msg="The authorization failed")

    if "code" in parse_qs(auth_code_redirect_url.query):
        auth_code = parse_qs(auth_code_redirect_url.query)["code"][0]
    else:
        session.close()
        raise LoginException(url=oauth_client.base_url, msg="The authorization failed")

    auth_token_res = session.post(
        oauth_client.base_url + "oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "scope": DEFAULT_AUTH_SCOPES,
            "resource": ",".join(audience),
            "client_id": oauth_client.client_id,
            "client_secret": oauth_client.client_secret,
        },
    )

    session.close()

    if auth_token_res.ok:
        return auth_token_res.json()

    raise LoginException(
        url=oauth_client.base_url,
        msg="Failed to get a token from the token endpoint",
    )


def login_device_code(
    audience: List[str] = None,
    oauth_client: OAuthClientParams = DEFAULT_AUTH_CLIENT,
    open_browser: bool = True,
) -> Dict[AnyStr, Any]:
    """
    Generate an access token for a service using the Device Code flow

    :param audience: The service url(s) to authorize
    :param oauth_client: The authorization parameters of the service to be authorized.
    :param open_browser: Open a browser window automatically to the auth server. If this is False, the user must
        follow a returned url to authorize
    :return: A dict containing the OAuth access token as well as an expiry and a refresh token
    """
    session = requests.Session()

    if not oauth_client.device_code_url:
        raise LoginException(
            url=" ".join(audience), msg="There is no device code url specified"
        )

    device_code_res = session.post(
        oauth_client.device_code_url,
        params={
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "client_id": oauth_client.client_id,
            "resource": ",".join(audience),
        },
        allow_redirects=False,
    )

    if device_code_res.ok:
        device_code_json = device_code_res.json()

        device_code = device_code_json["device_code"]
        device_verify_uri = device_code_json["verification_uri_complete"]
        poll_interval = int(device_code_json["interval"])
        expiry = time() + int(device_code_json["expires_in"])
        click.echo(f"{device_verify_uri}")

        if open_browser:
            webbrowser.open(device_verify_uri, new=2)
    else:
        if "error" in device_code_res.json():
            error_message = f'The device code request failed with message "{device_code_res.json()["error"]}"'
        else:
            error_message = "The device code request failed"

        raise LoginException(url=oauth_client.base_url, msg=error_message)

    while time() < expiry:
        auth_token_res = session.post(
            oauth_client.token_url,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
                "client_id": oauth_client.client_id,
            },
        )

        if auth_token_res.ok:
            session.close()
            return auth_token_res.json()
        elif "error" in auth_token_res.json():
            if auth_token_res.json().get("error") == "authorization_pending":
                continue
            error_msg = "Failed to retrieve a token"
            if "error_description" in auth_token_res.json():
                error_msg += f": {auth_token_res.json()['error_description']}"
            raise LoginException(url=oauth_client.base_url, msg=error_msg)

        sleep(poll_interval)
    raise LoginException(url=oauth_client.base_url, msg="The authorize step timed out.")


def login_refresh_token(
    token: AnyStr = None, oauth_client: OAuthClientParams = DEFAULT_AUTH_CLIENT
) -> Dict[AnyStr, Any]:
    """
    Generate an OAuth access token using an OAuth refresh token

    :param token: a dict containing the refresh token in the "refresh_token" field and optionally "scope"
    :param oauth_client: the parameters used to connect to
    :returns: A new token dict containing an access token
    :raises: RefreshException
    """
    if not token:
        raise RefreshException("The refresh token is missing")

    refresh_token_res = requests.post(
        oauth_client.token_url,
        data={
            "grant_type": "refresh_token",
            "refresh_token": token,
            "scope": oauth_client.scope,
        },
        auth=(oauth_client.client_id, oauth_client.client_secret),
    )

    if refresh_token_res.ok:
        fresh_token = refresh_token_res.json()
        return fresh_token
    else:
        error_msg = f"Unable to refresh token"
        try:
            error_json = refresh_token_res.json()
            error_msg += f": {error_json['error_description']}"
        except JSONDecodeError:
            pass

        raise RefreshException(url=oauth_client.base_url, msg=error_msg)
