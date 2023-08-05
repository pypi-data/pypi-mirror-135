from requests import Request
from ..utils import catch_errors, get_client
from ...exceptions import (
    LoginException,
    RefreshException,
    OAuthTokenException,
    ServiceTypeNotFoundError,
    AuthException,
)
import click


@click.group("auth")
def auth():
    pass


@auth.command("login")
@click.argument("service")
@click.option("--no-browser", "-b", is_flag=True, default=False)
@click.pass_context
@catch_errors(
    error_types=(
        AuthException,
        LoginException,
    ),
    success_msg="Login successful!",
)
def cli_login(ctx: click.Context, service: str, no_browser: bool):
    client = get_client(ctx)
    if service == "dataconnect":
        service_to_authorize = client.dataconnect
    elif service == "collections":
        service_to_authorize = client.collections
    elif service == "wes":
        service_to_authorize = client.wes
    else:
        raise ServiceTypeNotFoundError(service)

    if not service_to_authorize:
        raise LoginException(service_type=service, msg="There is no configured service")
    elif not service_to_authorize.auth:
        raise LoginException(
            url=service_to_authorize.url,
            msg="There is no auth configured.",
        )
    service_to_authorize.auth.authorize(
        Request(url=service_to_authorize.url), open_browser=(not no_browser)
    )
