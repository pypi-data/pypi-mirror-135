from ..utils import *
from ...exceptions import (
    ConfigException,
    DeprecatedConfigException,
    InvalidConfigException,
)


@click.group("config")
def config():
    pass


@config.command("list")
@click.pass_context
def config_list(ctx: click.Context):
    with remove_hidden_keys(ctx.obj) as config_output:
        click.echo(json.dumps(config_output, indent=4))
    return


@config.command("get")
@click.pass_context
@click.argument("key")
@click.option("--delimiter", "-d", default=".")
@catch_errors(error_types=(ConfigException,))
def get(ctx: click.Context, key: str, delimiter: str):
    var_path = key.split(delimiter)

    if not is_accepted_key(var_path):
        raise InvalidConfigException(key)

    val = get_config(ctx, var_path, delimiter=delimiter)

    output = json.dumps(val, indent=4)

    # we don't want surrounding quotes in our single string outputs so remove them
    if isinstance(val, str):
        output = output.replace('"', "")

    click.echo(output)
    return


@config.command("set")
@click.pass_context
@click.argument("key")
@click.argument("value", required=False, default=None, nargs=1)
@click.option("--delimiter", "-d", default=".")
@catch_errors(error_types=(ConfigException,))
def config_set(ctx: click.Context, key: str, value: str, delimiter: str):
    if is_deprecated_key(key):
        raise DeprecatedConfigException(key)
    elif not is_accepted_key(key, delimiter):
        raise InvalidConfigException(key)

    set_config(ctx=ctx, var_path=key, delimiter=delimiter, value=value)

    with remove_hidden_keys(ctx.obj) as config_output:
        click.echo(json.dumps(config_output, indent=4))
