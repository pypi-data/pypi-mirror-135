from typing import List
from dnastack.client import *
from ..utils import catch_errors, get_client
from ...exceptions import ServiceException, DRSDownloadException
import click
import os


@click.group()
def files():
    pass


@files.command("download")
@click.pass_context
@click.argument("urls", required=False, nargs=-1)
@click.option(
    "-o", "--output-dir", required=False, default=os.getcwd(), show_default=True
)
@click.option("-i", "--input-file", required=False, default=None)
@click.option("-q", "--quiet", is_flag=True, required=False, default=False)
@catch_errors((ServiceException, DRSDownloadException))
def download(
    ctx: click.Context,
    urls: List[str],
    output_dir: str = os.getcwd(),
    input_file: str = None,
    quiet: bool = False,
):
    download_urls = []

    if len(urls) > 0:
        download_urls = list(urls)
    elif input_file:
        with open(input_file, "r") as infile:
            download_urls = filter(
                None, infile.read().split("\n")
            )  # need to filter out invalid values
    else:
        if not quiet:
            click.echo("Enter one or more URLs. Press q to quit")

        while True:
            try:
                url = click.prompt("", prompt_suffix="", type=str)
                url = url.strip()
                if url[0] == "q" or len(url) == 0:
                    break
            except click.Abort:
                break

            download_urls.append(url)
    get_client(ctx).download(
        urls=download_urls, output_dir=output_dir, display_progress_bar=(not quiet)
    )
