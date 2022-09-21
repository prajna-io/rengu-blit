""" Info plugin for blit cli
"""
from pkg_resources import iter_entry_points

import click
from click.core import Context


@click.command()
@click.help_option("-h", "--help")
@click.pass_context
def info(ctx: Context):
    """Show basic information about the blit environment"""

    print("Environment")
    print("-" * 70)
    if ctx.obj["verbose"]:
        print(f"VERBOSE={ctx.obj['verbose']}")
    print(f"BLIT_STORE={ctx.obj['blit_store']}")
    print(f"BLIT_METADATA={ctx.obj['blit_metadata']}")
    print()

    for module in ["cli", "store", "metadata"]:
        print(f"{module} modules")
        print("-" * 70)
        for entry_point in iter_entry_points(f"blit_{module}"):
            print(entry_point)
        print()
