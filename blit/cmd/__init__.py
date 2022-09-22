"""blit command line tool
"""

# region imports

from copy import deepcopy
from pprint import pprint

from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser, with_category


# endregion


# region argument handlers
common_arguments = Cmd2ArgumentParser()
common_arguments.add_argument("-v", "--verbose", action="count", help="Rengu base")
common_arguments.add_argument("-B", "--base", action="store", help="Rengu base")
# endregion


from functools import wraps


def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally

    return decorator


class DynamicCmd:
    """DynamicCmd add-on"""

    def __new__(cls, *args, **kwargs):
        print("Creating Instance")
        instance = super().__new__(cls, *args, **kwargs)

        instance.__dict__["do_foo"] = do_foo

        pprint(instance.__dict__)
        return instance


class BlitApp(Cmd):
    """BlitApp
    Cmd for blit application"""

    prompt = "[blit] "

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.processes = []

    @with_category("Configuration")
    @with_argparser(common_arguments)
    def do_info(self, args: Cmd2ArgumentParser) -> bool:
        """Provide basic information on the blit environment"""
        pprint(self.__dict__)
        self.poutput(args)

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


@add_method(BlitApp)
@with_category("Configuration")
def do_foo(*args) -> bool:
    """Do foo!"""
    pprint(args)
