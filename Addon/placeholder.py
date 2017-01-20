"""This module contains `tsaotun Vwgen` class"""

from tsaotun.lib.Docker.Addon.command import Command
from tsaotun.cli import Tsaotun

class Vwgen(Command):
    """This class implements `tsaotun Vwgen` command"""

    name = "tsaotun vwgen"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        args["console"] = args["v_console"]
        args["color"] = args["v_color"]
        args["verbosity"] = args["v_verbosity"]
        del args["v_console"]
        del args["v_color"]
        del args["v_verbosity"]

        t_cli = Tsaotun()
        t_cli.send('addon disable VWGen')
        from ..VWGen import cli as v_cli
        v_cli(args)
        self.settings[self.name] = ""
        t_cli.send('addon enable VWGen')

    def final(self):
        return self.settings[self.name]
