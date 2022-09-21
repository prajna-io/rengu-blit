""" Root cli context for blit
"""

from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins

from blit.cli.common import blit_storage_option, blit_metadata_option


@with_plugins(iter_entry_points("blit_cli"))
@click.group()
@click.help_option("-h", "--help")
@click.pass_context
@click.option(
    "--verbose",
    "-v",
    default=0,
    count=True,
    help="Verbosity level [0=no messages, 3=all messages]",
    envvar="VERBOSE",
)
@blit_storage_option
@blit_metadata_option
def cli(ctx, verbose: int, blit_store: str, blit_metadata):
    """Tool for managing binary objects in conjunction with rengu"""

    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["blit_store"] = blit_store
    ctx.obj["blit_metadata"] = blit_metadata
