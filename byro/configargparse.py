#!/usr/bin/env python3
"""
Extension of ConfigArgParse for better handling of subcommands
It is inherited and has only one change in api:
 - first param of constructor is list of subcommands
"""

__author__ = "Ondřej Profant"
__version__ = 0.1
__all__ = ["ByroParse"]

import sys
import configargparse


class ByroParse(configargparse.ArgParser):
    """
    Extension of ConfigArgParse for better handling of subcommands
    It is inherited and has only one change in api:
     - first param of constructor is list of subcommands
    """

    def __init__(self, commands, *args, **kwargs):
        self.commands = commands
        super(ByroParse, self).__init__(*args, **kwargs)
        self.usage = "%(prog)s [command] [option]"

    def parse_args(self, argv):
        if len(argv) < 2:
            self.print_help()
            sys.exit()

        cmd = argv[0]

        if cmd not in self.commands + ["-h", "-v", "--version", '--help']:
            print(cmd)
            self.print_help()
            sys.exit()

        parsed = super(ByroParse, self).parse_args(argv[1:])

        parsed.command = cmd

        return parsed

if __name__ == "__main__":
    parser = ByroParse(
        ["foo", "bar"],
        default_config_files=["config.ini"],
        args_for_setting_config_path=["-c", "--config"]
    )

    # version is specific, it can be use without subcommands
    parser.add_argument("-v", "--version", action='version', version="%(prog)s 2.0")
    parser.add_argument("-f", "--force-level")
    parser.add_argument("-d", "--debug-level")
    # ...

    print(parser.parse_args())