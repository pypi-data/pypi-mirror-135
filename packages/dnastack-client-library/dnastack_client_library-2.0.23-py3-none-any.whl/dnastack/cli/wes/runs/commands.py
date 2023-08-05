from typing import List, Any
from ....exceptions import ServiceException, WorkflowFailedException
from ...utils import catch_errors, get_client, parse_key_value_param
import json
import click


@click.group("runs")
def runs():
    pass


@runs.command("execute")
@click.pass_context
@click.option("-u", "--workflow-url", required=True)
@click.option("-a", "--attachment", required=False, multiple=True, default=[])
@click.option("--inputs-file", required=False, default=None)
@click.option("-e", "--engine-parameter", required=False, default=None)
@click.option("--engine-parameters-file", required=False, default=None)
@click.option("-t", "--tag", required=False, default=None)
@click.option("--tags-file", required=False, default=None)
@catch_errors((ServiceException,))
def runs_execute(
    ctx: click.Context,
    workflow_url: str,
    attachment: List[Any],
    inputs_file: str = None,
    engine_parameter: str = None,
    engine_parameters_file: str = None,
    tag: str = None,
    tags_file: str = None,
):
    engine_param = None
    tag_param = None

    if engine_parameter:
        engine_param = parse_key_value_param(engine_parameter, "engine-parameter")

    if tag:
        tag_param = parse_key_value_param(tag, "tag")

    result = get_client(ctx).wes.execute(
        workflow_url,
        attachment,
        inputs_file,
        engine_param,
        engine_parameters_file,
        tag_param,
        tags_file,
    )

    if "error_code" in result.keys():
        raise WorkflowFailedException(
            f"Workflow failed with exception: {result['msg'].strip()}"
        )

    click.echo(json.dumps(result, indent=4))


@runs.command("list")
@click.pass_context
@click.option("-s", "--page-size", required=False, default=20, type=int)
@click.option("-t", "--page-token", required=False, default=None)
@click.option("--all", is_flag=True, required=False)
@catch_errors((ServiceException,))
def runs_list(
    ctx: click.Context, page_size: int = 20, page_token: str = None, all: bool = False
):
    if all:
        response = get_client(ctx).wes.list()
    else:
        response = get_client(ctx).wes.list(
            page_size=page_size, next_page_token=page_token
        )

    click.echo(
        json.dumps(
            response,
            indent=4,
        )
    )

    if response.get("next_page_token", None) is not None:
        click.echo("wes runs list --page-token " + response["next_page_token"])
