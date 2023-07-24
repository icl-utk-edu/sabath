#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii


"""
Main entry point into SABATH (SABATH: Surrogate AI Benchmarking Applications'
Testing Harness).

@author Piotr Luszczek
"""


import argparse
from .commands import dispatch


def parse(argv):
    mainparser = argparse.ArgumentParser(
        prog=argv[0],
        description="SABATH: Surrogate AI Benchmarking Applications' Testing Harness",
        epilog="The project is currently under development and new commands are possible in the future.",
        prefix_chars="-",
        usage="%(prog)s <command> [<command>] [options]")

    # don't use pathlib to support Python 3.3 and earlier
    mainparser.add_argument("--root", type=str, help="Directory root for SABATH code files (by default, it is discovered from SABATH invocation)")
    mainparser.add_argument("--cache", type=str, help="Directory for SABATH cache files (models and datasets)")

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

    parsers["fetch"].add_argument("-m", "--model", type=str, help="Name of the model to fetch.")
    parsers["fetch"].add_argument("-d", "--dataset", type=str, help="Name of the dataset to fetch.")

    parsers["run"].add_argument("model", nargs=1, help="Name of the model to run.")
    parsers["run"].add_argument("dataset", nargs=1, help="Name of the dataset to run.")

    return mainparser.parse_args(args=argv[1:])


def main(argv):
    args = parse(argv)
    if args.command is None:
        print("SABATH is Surrogate AI Benchmarking Applications' Testing Harness.\n\n"
              "Please specify one of the available commands or "
              "use '-h' flag for more information.")
        return 127

    return dispatch(args)
