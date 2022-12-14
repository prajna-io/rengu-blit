"""blit command line tool
"""

# region imports

from copy import deepcopy
from typing import List, Tuple, Optional

from pprint import pprint

from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser, with_category, constants


# endregion


# region argument handlers
common_arguments = Cmd2ArgumentParser()
common_arguments.add_argument("-v", "--verbose", action="count", help="Rengu base")
common_arguments.add_argument("-B", "--base", action="store", help="Rengu base")
# endregion




@with_category("Configuration")
@with_argparser(deepcopy(common_arguments))
def do_foo(*args) -> bool:
    """Do foo!"""
    pprint(args)


class BlitApp(Cmd):
    """BlitApp
    Cmd for blit application"""

    prompt = "[blit] "

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.processes = []
        self.hidden_commands.append("-relative-run-script")

    #region underscores to dashes
    def get_all_commands(self) -> List[str]:
        """Return a list of all commands"""
        return [
            name[len(constants.COMMAND_FUNC_PREFIX) :].replace("_", "-")
            for name in self.get_names()
            if name.startswith(constants.COMMAND_FUNC_PREFIX) and callable(getattr(self, name))
        ]

    def _cmd_func_name(self, command: str) -> str:
        """Get the method name associated with a given command.
        :param command: command to look up method name which implements it
        :return: method name which implements the given command
        """
        target = constants.COMMAND_FUNC_PREFIX + command
        target = target.replace("-", "_")
        return target if callable(getattr(self, target, None)) else ''
    
    #endregion

    @with_category("Testing Features")
    @with_argparser(deepcopy(common_arguments))
    def do_test_feature_one(self, args:Cmd2ArgumentParser) -> bool:
        """Bubba!"""
        print("test_feature_one")
        print(args)
    
    def help_test_feature_one(self):
        print("HELP")
    
    @with_category("Configuration")
    @with_argparser(deepcopy(common_arguments))
    def do_info(self, args: Cmd2ArgumentParser) -> bool:
        """Provide basic information on the blit environment"""
        pprint(self.__dict__)
        self.poutput(args)

    @with_category("Configuration")
    def do_load_foo(self, statement: str) -> bool:
        """load the foo module"""
        setattr(self, "do_foo", types.MethodType(do_foo, self))

    @with_category("Configuration")
    def do_load_bar(self, statment: str) -> bool:
        """load the bar module"""
        import blit.cmd.more

        self.register_command_set(blit.cmd.more.MoreCommands())

    job_arguments = deepcopy(common_arguments)
    job_arguments.add_argument(
        "-q",
        "--queue",
        action="store_const",
        help="job queue to manage",
        default=0,
        const=int,
    )

    job_bg_arguments = deepcopy(job_arguments)
    job_bg_arguments.add_argument("args", nargs="+", help="job arguments")

    @with_category("Process Management")
    @with_argparser(job_bg_arguments)
    def do_bg(self, arguments: Cmd2ArgumentParser) -> bool:
        """Start an OS job in the background"""

        import subprocess

        print(f"using queue {arguments.queue}")

        process = subprocess.Popen(
            arguments.args,
            shell=True,
            start_new_session=True,
            text=True,
            stdout=subprocess.PIPE,
            close_fds=True,
        )
        self.processes.append(process)

    @with_category("Process Management")
    @with_argparser(job_arguments)
    def do_jobs(self, args: Cmd2ArgumentParser) -> bool:
        """show running jobs and their output"""
        print(args)

        import subprocess

        for process in self.processes:
            print(f"{process.pid}> {process.args}")

            try:
                buf_out, buf_err = process.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                pass

            print(buf_out, buf_err)
            exit_code = process.poll()
            if exit_code is not None:
                print(f"--- exited with {exit_code}")
                self.processes.remove(process)

    # endregion

    @staticmethod
    def main():
        """Main entry to BlitApp"""
        import sys

        app = BlitApp()

        if len(sys.argv) > 1:
            sys.exit(app.onecmd(" ".join(sys.argv[1:])))
        else:
            sys.exit(app.cmdloop())
