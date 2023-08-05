import csv
import json
import sys
from json import JSONEncoder
from urllib.parse import urlunparse, urlparse
from typing import Any, Union, List, Callable, Tuple, Optional, Type, Mapping, AnyStr
import io
import click
import yaml
from click import UsageError, Option
from click.decorators import FC

from .. import DataConnectClientV2, WesClient, CollectionsClient, PublisherClient
from ..auth import (
    PersonalAccessTokenAuth,
    DeviceCodeAuth,
    RefreshTokenAuth,
    OAuthClientParams,
)
from ..client import BaseServiceClient
from ..client.dataconnect_client import DataConnectClientV2
from ..exceptions import NoConfigException, InvalidConfigTypeException, ConfigException
from ..constants import (
    ACCEPTED_CONFIG_KEYS,
    ACCEPTED_OAUTH_KEYS,
    DEPRECATED_CONFIG_KEYS,
    CLI_DIRECTORY,
    HIDDEN_CONFIG_KEYS,
)


def get_client(ctx: click.Context):
    """Return the created PublisherClient instance"""
    return ctx.obj["client"]


def get_service_config_key(service: Any) -> str:
    """Get the configuration base key for a :class:`ServiceType`"""
    if isinstance(service, DataConnectClientV2):
        return "data_connect"
    elif isinstance(service, CollectionsClient):
        return "collections"
    elif isinstance(service, WesClient):
        return "wes"
    else:
        raise ConfigException(service)


# GETTERS
def get_config(
    ctx: click.Context,
    var_path: Union[list, str],
    raise_error: bool = True,
    delimiter: str = ".",
    default: Any = None,
) -> Any:
    """
    Get a configured value from a path

    :param ctx: The click Context used to store the config
    :param var_path: The config key. Can either be a delimited string or a list representing a path to the value
    :param raise_error: Don't raise an error if the configuration key is invalid or the configuration doesn't exist.
        This is True by default
    :param delimiter: The character(s) used to delimit the key. '.' is used by default
    :param default: The value to use if no configuration is set.
    :return: The configured value
    :raises NoConfigException if no configuration is set. InvalidConfigTypeException if the value at the key
        is different than expected
    """

    # TODO: remove the raise_error functionality and replace by having calling functions use try-catch blocks

    if isinstance(var_path, str):
        var_path = var_path.split(delimiter)

    format_var_path(var_path)
    obj = ctx.obj
    for key in var_path:
        try:
            obj = obj[key]
        except KeyError:
            if raise_error:
                raise NoConfigException(key=key)
            else:
                return default

    if raise_error and type(obj) != get_type_of_config(var_path):
        raise InvalidConfigTypeException(
            key=".".join(var_path),
            expected=get_type_of_config(var_path),
            actual=type(obj).__name__,
        )

    # for the last object we don't error if it's not there, just return None
    return obj


# SETTERS
def set_config(
    ctx: click.Context,
    var_path: Union[list, str],
    delimiter: str = ".",
    value: Any = None,
) -> None:
    """
    Set the configured value for a path

    If the value is a url, it adds a trailing slash if it is not there

    :param ctx: The click Context used to store the config
    :param var_path: The config key. Can either be a delimited string or a list representing a path to the value
    :param delimiter: The character(s) used to delimit the key. '.' is used by default
    :param value: The value to set the config
    """
    if type(var_path) == str:
        var_path = var_path.split(delimiter)

    assert len(var_path) >= 1

    # standardize the url in the path and value to use a trailing slash
    format_var_path(var_path)
    if is_url(value):
        value = format_url_for_config(value)

    set_config_obj(ctx.obj, var_path, value)
    save_config_to_file(ctx)


def set_config_obj(obj: dict, var_path: list, value: Any) -> None:
    """Sets the value at the config objects path to the specified value"""
    var_name = var_path[0]
    if var_name not in obj.keys():
        obj[var_name] = None

    if len(var_path) == 1:
        obj[var_name] = value
    else:
        if obj[var_name] is not None:
            assert type(obj[var_name]) == dict
            set_config_obj(obj[var_name], var_path[1:], value)
        else:
            obj[var_name] = {}
            set_config_obj(obj[var_name], var_path[1:], value)


# HELPERS
def is_accepted_key(key: Union[List[str], str], delimiter: str = ".") -> bool:
    """Returns true if the config key is valid"""

    if type(key) == str:
        var_path = key.split(delimiter)
    else:
        var_path = key

    obj = ACCEPTED_CONFIG_KEYS

    # since wallet servers can really be anything, we only check if the key following "oauth"
    # is a proper url, and whether the third is a valid oauth key
    if var_path[0] == "oauth":

        if len(var_path) > 3:
            return False

        # if they define which token, check if it's a valid url
        if len(var_path) > 1:
            wallet_url_info = urlparse(var_path[1])
            if not (wallet_url_info.scheme == "https" and wallet_url_info.netloc):
                return False

        # if they look for a specific value within a token, make sure it's a valid value
        if len(var_path) > 2:
            oauth_key = var_path[2]
            if oauth_key not in ACCEPTED_OAUTH_KEYS.keys():
                return False

        return True

    try:
        for var in var_path:
            obj = obj[var]
    except KeyError:
        return False
    return True


def is_deprecated_key(key: str) -> bool:
    """Returns true if a specific config key has been marked as deprecated"""
    return key in DEPRECATED_CONFIG_KEYS.keys()


def get_type_of_config(var_path: list) -> type:
    """Get the expected type of the config value at a path"""

    obj = ACCEPTED_CONFIG_KEYS

    # since we don't know what the middle key is for "oauth"
    # we return a dictionary if it's asking for the middle key,
    # and rely on the accepted_oauth_keys for if it's asking for a value inside a oauth token
    if var_path[0] == "oauth":
        if len(var_path) == 2:
            return dict
        elif len(var_path) == 3:
            return ACCEPTED_OAUTH_KEYS.get(var_path[2])
        else:
            return type(None)

    for var in var_path:
        obj = obj.get(var)

        if obj is None:
            return type(None)

    # in the case where we don't reach an end value, we return dict
    if type(obj) == dict:
        return dict

    return obj


class remove_hidden_keys:
    def __init__(self, obj: dict):
        self.hidden_keys = {}
        self.obj = obj

    # we don't want to persist the client object so we delete it before saving
    def __enter__(self):
        for key in HIDDEN_CONFIG_KEYS:
            if key in self.obj.keys():
                self.hidden_keys[key] = self.obj[key]
                del self.obj[key]
        return self.obj

    def __exit__(self, type, value, traceback):
        for key, val in self.hidden_keys.items():
            self.obj[key] = val


def save_config_to_file(ctx: click.Context) -> None:
    """Save the current config object to a file"""
    with open(f"{CLI_DIRECTORY}/config.yaml", "w") as config_file, remove_hidden_keys(
        ctx.obj
    ) as config_output:
        yaml.dump(config_output, config_file)
        config_file.close()


def create_service_client_from_config(
    ctx: click.Context, key: AnyStr, cls: Type[BaseServiceClient]
) -> Optional[BaseServiceClient]:

    service_url = get_config(ctx, var_path=[key, "url"], raise_error=False)
    service_auth = None
    service_oauth_client = None

    service_auth_config = get_config(ctx, var_path=[key, "auth"], raise_error=False)

    if service_auth_config:
        service_auth_client = service_auth_config.get("client")
        if service_auth_client:
            service_oauth_client = OAuthClientParams(
                base_url=service_auth_config.get("url"),
                authorization_url=service_auth_config.get("authorization_url"),
                device_code_url=service_auth_config.get("device_code_url"),
                token_url=service_auth_config.get("token_url"),
                client_id=service_auth_client.get("id"),
                client_secret=service_auth_client.get("secret"),
                client_redirect_url=service_auth_client.get("redirect_url"),
                scope=service_auth_client.get("scope"),
            )

        refresh_token = service_auth_config.get("refresh_token")
        personal_access_token = service_auth_config.get("personal_access_token")
        email = service_auth_config.get("email")
        # Have a preference of Refresh Token > Device Code >>>> PAT for the CLI
        if refresh_token:
            service_auth = RefreshTokenAuth(
                refresh_token=refresh_token,
                oauth_client=service_oauth_client,
            )
        elif personal_access_token and email:
            service_auth = PersonalAccessTokenAuth(
                email=email,
                personal_access_token=personal_access_token,
                oauth_client=service_oauth_client,
            )
        else:
            service_auth = DeviceCodeAuth(
                oauth_client=service_oauth_client,
            )

    if service_url:
        return cls(
            url=service_url,
            auth=service_auth,
            registry_url=get_config(ctx, "service_registry.url", False),
        )
    else:
        return None


def save_service_client_to_config(
    ctx, client: Optional[BaseServiceClient], key: AnyStr
) -> None:

    if not client:
        return

    set_config(ctx, var_path=[key, "url"], value=client.url)
    if client.auth:
        auth_config = {}

        if client.auth.oauth_client:
            auth_config = {
                "url": client.auth.oauth_client.base_url,
                "authorization_url": client.auth.oauth_client.authorization_url,
                "device_code_url": client.auth.oauth_client.device_code_url,
                "token_url": client.auth.oauth_client.token_url,
                "client": {
                    "id": client.auth.oauth_client.client_id,
                    "secret": client.auth.oauth_client.client_secret,
                    "redirect_url": client.auth.oauth_client.client_redirect_url,
                    "scope": client.auth.oauth_client.scope,
                },
            }

        if isinstance(client.auth, RefreshTokenAuth):
            auth_config["refresh_token"] = client.auth.refresh_token
        elif isinstance(client.auth, PersonalAccessTokenAuth):
            auth_config["personal_access_token"] = client.auth.personal_access_token
            auth_config["email"] = client.auth.email

        set_config(ctx, var_path=[key, "auth"], value=auth_config)


def create_publisher_client_from_config(ctx: click.Context) -> None:
    """
    Create a :class:`PublisherClient` from a configured Context object

    :param ctx: The :class:`Context` to use to create the client
    """

    publisher_client = PublisherClient()

    publisher_client.dataconnect = create_service_client_from_config(
        ctx, "data_connect", DataConnectClientV2
    )
    publisher_client.collections = create_service_client_from_config(
        ctx, "collections", CollectionsClient
    )
    publisher_client.wes = create_service_client_from_config(ctx, "wes", WesClient)

    ctx.obj["client"] = publisher_client


# CLICK EXTENSIONS
class MutuallyExclusiveOption(Option):
    """
    A click Option wrapper for sets of options where one but not both must be specified
    """

    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        help = kwargs.get("help", "")
        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs["help"] = help + (
                " NOTE: This argument is mutually exclusive with "
                " arguments: [" + ex_str + "]."
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(
        self, ctx: click.Context, opts: Mapping[str, Any], args: List[str]
    ) -> Tuple[Any, List[str]]:
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(self.name, ", ".join(self.mutually_exclusive))
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)


def parse_key_value_param(parameter: str, param_name: str) -> str:
    """Parse a parameters specified in a K=V format and dumps to a JSON str"""
    param_key_value = parameter.split("=")

    if len(param_key_value) != 2:
        click.secho(
            f"Invalid format for {param_name}. Must be a single key-value pair in the format K=V",
            fg="red",
        )
        sys.exit(1)

    return json.dumps({param_key_value[0].strip(): param_key_value[1].strip()})


def catch_errors(
    error_types: Tuple[Type, ...] = (Exception,), success_msg: Optional[str] = None
) -> Callable[[FC], FC]:
    """
    A decorator factory that gracefully handles errors of the specified error_types

    :param error_types: The types of exceptions to be handled. Defaults to the base Exception class
    :param success_msg: A message to be displayed if the command is successful
    :return: A decorator that handles the specified error types and displays a message if successful
    """

    def decorator(command: Callable) -> Callable:
        def handled_command(*args, **kwargs):
            try:
                command(*args, **kwargs)
                if success_msg:
                    click.secho(success_msg, fg="green")
            except error_types as e:
                click.secho(e, fg="red")

                if click.get_current_context().obj["debug"]:
                    click.echo("Current config:")
                    with remove_hidden_keys(
                        click.get_current_context().obj
                    ) as config_obj:
                        click.echo(json.dumps(config_obj))
                    raise e
                else:
                    sys.exit(1)

        return handled_command

    return decorator


# FORMATTERS
def format_url_for_config(url: str) -> str:
    """
    Format a url as a config value by adding a trailing slash if necessary

    :param url: The url config value
    :return: The properly formatted config value
    """
    parsed_url = urlparse(url)
    new_path = "/"
    if not (parsed_url.path == "" or parsed_url == "/"):
        if parsed_url.path[-1] == "/":
            new_path = parsed_url.path
        else:
            new_path = parsed_url.path + "/"
    return str(urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, "", "", "")))


def format_var_path(var_path: list) -> None:
    """
    Format a config path by adding trailing slashes to url keys if necessary

    :param var_path: The path to the config value
    :return: The properly formatted path to the config value
    """
    for i in range(len(var_path)):
        if is_url(var_path[i]):
            var_path[i] = format_url_for_config(var_path[i])


def format_query_result_as_csv(query_results: List[dict], include_headers: bool = True) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    # if we have at least one result, add the headers
    if len(query_results) > 0 and include_headers:
        writer.writerow(query_results[0].keys())

    for res in query_results:
        data_row = list(map(lambda x: str(x).replace(",", "\,"), res.values()))
        writer.writerow(data_row)

    return output.getvalue()


# Misc Helpers:
def is_url(val: Any) -> bool:
    if type(val) is not str:
        return False
    parsed_url = urlparse(val)
    return parsed_url.scheme == "https" and parsed_url.netloc
