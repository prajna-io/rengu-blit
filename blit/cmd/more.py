from pprint import pprint
from cmd2 import CommandSet, with_default_category, with_argparser

from . import common_arguments


@with_default_category("more commands")
class MoreCommands(CommandSet):
    """more commands for blit"""

    @with_argparser(common_arguments)
    def do_bar(self, *args) -> bool:
        """Do bar!"""
        pprint(args)
