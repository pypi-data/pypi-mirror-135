from dnastack.client import *
from ...utils import catch_errors, get_client
from ....client.base_exceptions import ApiError
from ....exceptions import ServiceException
import json
import click


@click.group("tables")
def tables():
    pass


@tables.command("list")
@click.pass_context
@click.argument("collection_name")
@catch_errors((ApiError, ServiceException,))
def list_tables(ctx: click.Context, collection_name: str):
    click.echo(json.dumps(get_client(ctx).collections.list_tables(collection_name), indent=4))
