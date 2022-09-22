from typing import Callable
from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser, with_category


class AnotherFunction:
    def __init__(self, cmd: Cmd):
        self.cmd = cmd

    def __call__(self, statement: str) -> bool:
        """command to do other things"""
        self.cmd.poutput(f"ANother command {statement}")
