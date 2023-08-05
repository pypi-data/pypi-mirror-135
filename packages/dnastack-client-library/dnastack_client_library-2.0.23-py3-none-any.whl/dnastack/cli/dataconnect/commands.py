import click
import json
import os
from datetime import datetime
from requests import HTTPError

from .tables import commands as tables_commands
from ..utils import catch_errors, get_client, format_query_result_as_csv
from ...client.base_exceptions import ApiError, ServerApiError
from ...exceptions import ServiceException


@click.group("dataconnect")
def dataconnect():
    pass


@dataconnect.command("query")
@click.pass_context
@click.argument("query")
@click.option("-d", "--download", is_flag=True)
@click.option("-r", "--raw", is_flag=True)
@click.option("--debug", is_flag=True)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["json", "csv"]),
    show_choices=True,
    default="json",
    show_default=True,
)
@catch_errors((ApiError, ServerApiError,))
def query(
    ctx: click.Context,
    query: str,
    download: bool = False,
    raw: bool = False,
    debug: bool = False,
    format: str = "json",
):
    results = get_client(ctx).dataconnect.query(query)

    try:
        if format == "json":
            output = json.dumps(list(results), indent=4)
        else:
            output = format_query_result_as_csv(list(results), not raw)
    except HTTPError as h:
        error_json = json.loads(h.response.text)
        error_msg = "Unable to get the paginated response"
        if "errors" in error_json:
            error_msg += f": {error_json['errors'][0]['title']}"
        raise ServiceException(
            service_type="dataconnect",
            url=get_client(ctx).dataconnect.url,
            msg=error_msg,
        )

    if download:
        # TODO: be able to specify output file
        download_file = (
            f"{os.getcwd()}"
            f"/query{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            f"{'.csv' if format == 'csv' else '.json'}"
        )
        with open(download_file, "w") as fs:
            fs.write(output)
    else:
        click.echo(output, nl=(format != "csv"))


dataconnect.add_command(tables_commands.tables)
