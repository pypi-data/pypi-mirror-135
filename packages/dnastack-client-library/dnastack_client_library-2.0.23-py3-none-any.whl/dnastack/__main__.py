import json
import click
import os
from typing import Any, Type, AnyStr, Optional
import yaml
from requests import Request
from .auth.authorizers import TokenStore, RefreshTokenAuth, OAuthTokenAuth
from .auth import DeviceCodeAuth, OAuthClientParams, PersonalAccessTokenAuth
from .client import (
    PublisherClient,
    DataConnectClientV2,
    CollectionsClient,
    WesClient,
    BaseServiceClient,
)
from .cli import *
from .cli.utils import (
    set_config_obj,
    save_config_to_file,
    get_config,
    get_service_config_key,
    set_config,
    save_service_client_to_config,
    create_publisher_client_from_config,
)
from .constants import (
    CLI_DIRECTORY,
    DEPRECATED_CONFIG_KEYS,
    __version__,
)


def fix_deprecated_keys(ctx: click.Context) -> None:
    """
    Change deprecated keys to their current values and save to file

    :param ctx: The context to fix the deprecated keys for
    :return:
    """
    new_keys = {}
    deprecated_keys = []

    # try to fix deprecated keys
    for key in ctx.obj.keys():
        if key in DEPRECATED_CONFIG_KEYS.keys():
            var_path = DEPRECATED_CONFIG_KEYS[key]
            # there is a new key that the value can be set to. set the analogous value to the existing one
            if var_path is not None:
                new_keys[var_path] = ctx.obj[key]
            deprecated_keys.append(key)

    # add the new keys
    for new_key, value in new_keys.items():
        var_path = new_key.split(".")
        set_config_obj(ctx.obj, var_path=var_path, value=value)

    # delete the deprecated keys
    for dep_key in deprecated_keys:
        del ctx.obj[dep_key]

    save_config_to_file(ctx)


def load_config_from_file(ctx: click.Context) -> None:
    """
    Load a config from the CLIs config file and load it into the :attr:`Context.obj` attribute of the Context

    It also fixes deprecated config keys once loaded

    :param ctx: The :class:`Context` to load config into
    """
    ctx.obj = {}

    # create the cli directory if necessary
    if not os.path.exists(CLI_DIRECTORY):
        os.mkdir(CLI_DIRECTORY)

    config_file_path = f"{CLI_DIRECTORY}/config.yaml"

    # create the config file if necessary
    if not os.path.exists(config_file_path):

        with open(config_file_path, "w+") as config_file:
            yaml.dump(ctx.obj, config_file)
            config_file.close()

    with open(config_file_path, "r+") as config_file:
        data = yaml.safe_load(config_file)
        if data:
            ctx.obj = data

    fix_deprecated_keys(ctx)


def save_publisher_client_to_config(ctx: click.Context) -> None:
    """Save the Context's configuration to a save file"""

    if "client" in ctx.obj:
        publisher_client = ctx.obj["client"]
    else:
        return

    save_service_client_to_config(ctx, publisher_client.dataconnect, "data_connect")
    save_service_client_to_config(ctx, publisher_client.collections, "collections")
    save_service_client_to_config(ctx, publisher_client.wes, "wes")


@click.group("dnastack")
@click.option("--debug", is_flag=True)
@click.version_option(__version__, message="%(version)s")
def dnastack(debug):
    ctx = click.get_current_context()
    load_config_from_file(ctx)

    if ctx.invoked_subcommand != "config":
        create_publisher_client_from_config(ctx)

    ctx.obj["debug"] = debug


@dnastack.result_callback()
def dnastack_callback(result: Any, debug: bool):
    if "client" in click.get_current_context().obj.keys():
        save_publisher_client_to_config(click.get_current_context())


@dnastack.command("version")
@click.option("--debug", is_flag=True)
def get_version():
    click.echo(__version__)


dnastack.add_command(dataconnect_commands.dataconnect)
dnastack.add_command(config_commands.config)
dnastack.add_command(file_commands.files)
dnastack.add_command(auth_commands.auth)
dnastack.add_command(collections_commands.collections)
dnastack.add_command(wes_commands.wes)

if __name__ == "__main__":
    dnastack.main(prog_name="dnastack")
