from ....exceptions import ServiceException
from ...utils import MutuallyExclusiveOption, catch_errors, get_client
import json
import click


@click.group("run")
def run():
    pass


@run.command("get")
@click.pass_context
@click.argument("run_id")
@click.option("--status", required=False, is_flag=True)
@catch_errors((ServiceException,))
def get_run(ctx: click.Context, run_id: str, status: bool = False):
    click.echo(
        json.dumps(
            get_client(ctx).wes.get(
                run_id,
                status,
            ),
            indent=4,
        )
    )


@run.command("cancel")
@click.pass_context
@click.argument("run_id")
@catch_errors((ServiceException,))
def cancel_run(ctx: click.Context, run_id: str):
    click.echo(
        json.dumps(
            get_client(ctx).wes.cancel(run_id),
            indent=4,
        )
    )


@run.command("logs")
@click.pass_context
@click.argument("run_id")
@click.option(
    "--stdout",
    is_flag=True,
    default=False,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["stderr", "url"],
)
@click.option(
    "--stderr",
    is_flag=True,
    default=False,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["stdout", "url"],
)
@click.option(
    "--url",
    default=None,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["stdout", "stderr"],
)
@click.option("-t", "--task", required=False, default=None)
@click.option("-i", "--index", required=False, default=0, type=int)
@catch_errors((ServiceException,))
def get_run_logs(
    ctx: click.Context,
    run_id: str,
    stdout: bool = False,
    stderr: bool = False,
    url: str = None,
    task: str = None,
    index: int = 0,
):
    click.echo(
        get_client(ctx).wes.run_logs(
            run_id,
            stdout,
            stderr,
            url,
            task,
            index,
        )
    )
