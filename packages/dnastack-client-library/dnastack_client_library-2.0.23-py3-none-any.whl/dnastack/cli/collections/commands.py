import json
from json import JSONEncoder

import click
from .tables import commands as tables_commands
from ..utils import catch_errors, get_client, format_query_result_as_csv
from ...exceptions import ServiceException


@click.group("collections")
def collections():
    pass


@collections.command(name="list")
@click.pass_context
@catch_errors((ServiceException,))
def list_collections(ctx: click.Context):
    click.echo(
        json.dumps(
            get_client(ctx).collections.list_collections(),
            indent=4,
        )
    )


@collections.command("query")
@click.pass_context
@click.argument("collection_name")
@click.argument("query")
@click.option(
    "-f",
    "--format",
    type=click.Choice(["json", "csv"]),
    show_choices=True,
    default="json",
    show_default=True,
)
@catch_errors((ServiceException,))
def query_collection(
    ctx: click.Context, collection_name: str, query: str, format: str = "json"
):
    results = get_client(ctx).collections.query(
        collection_name=collection_name,
        q=query,
    )
    if format == "json":
        click.echo(json.dumps(list(results), indent=4))
    else:
        click.echo(format_query_result_as_csv(list(results)), nl=False)


collections.add_command(tables_commands.tables)
