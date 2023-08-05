import click
import json

from dnastack.client.base_exceptions import ApiError, ServerApiError
from ...utils import catch_errors, get_client


@click.group("tables")
def tables():
    pass


@tables.command("list")
@click.pass_context
@catch_errors((ApiError, ServerApiError,))
def list_tables(ctx: click.Context):
    click.echo(
        json.dumps(
            [
                t.dict()
                for t in get_client(ctx).dataconnect.list_tables()
            ],
            indent=4
        )
    )


@tables.command("get")
@click.pass_context
@click.argument("table_name")
@catch_errors((ApiError, ServerApiError,))
def get(ctx: click.Context, table_name):
    click.echo(
        json.dumps(
            get_client(ctx).dataconnect.get_table(table_name).dict(),
            indent=4,
        )
    )
