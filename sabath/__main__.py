#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii


"""
Main entry point into SABATH (SABATH: Surrogate AI Benchmarking Applications'
Testing Harness).

@author Piotr Luszczek
"""


import sys


if sys.version_info < (3,):
    raise RuntimeError("Only Python 3+ supported")


import argparse
from .commands import dispatch


def cmdparse(argv):
    mainparser = argparse.ArgumentParser(
        prog=argv[0],
        description="SABATH: Surrogate AI Benchmarking Applications' Testing Harness",
        epilog="The project is currently under development and new commands are possible in the future.",
        prefix_chars="-",
        usage="%(prog)s <command> [<command>] [options]")

    # don't use pathlib to support Python 3.3 and earlier
    mainparser.add_argument("--root", type=str, help="Directory root for SABATH files")

    actparser = mainparser.add_subparsers(
        title="Actions",
        description="Choose one of possible commands and their arguments.",
        help="names for specific commands",
        dest="command")

    parsers = dict()
    for cmd, hlp in (
        ("fetch", "Download a model or one of its datasets"),
        ("list", "List models or datasets"),
        ("info", "Show information about models or datasets"),
        ("run", "Run a model with one of its datasets"),
    ):
        parsers[cmd] = actparser.add_parser(cmd, help=hlp)

    parsers["fetch"].add_argument("--model", type=str, help="Name of the model to fetch.")
    parsers["fetch"].add_argument("--dataset", type=str, help="Name of the dataset to fetch.")

    parsers["run"].add_argument("model", nargs=1, help="Name of the model to run.")
    parsers["run"].add_argument("dataset", nargs=1, help="Name of the dataset to run.")

    return mainparser.parse_args(args=argv[1:])


def main(argv):
    cmdargs = cmdparse(argv)
    if cmdargs.command is None:
        print("SABATH is Surrogate AI Benchmarking Applications' Testing Harness.\n"
              "Please specify one of the available commands or "
              "use '-h' flag for more informatin.")
        return 127

    dispatch(cmdargs)
    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))
