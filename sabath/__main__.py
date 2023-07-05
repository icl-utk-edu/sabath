#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii

import sys

if sys.version_info < (3,):
    raise RuntimeError("Only Python 3+ supported")


import argparse


def cmdparse(argv):
    mainparser = argparse.ArgumentParser(
        prog=argv[0],
        description="SABATH: Surrogate AI Benchmarking Applications' Testing Harness",
        epilog="The project is currently under development and new commands are possible in the future.",
        prefix_chars="-",
        usage="%(prog)s <action> [<command>] [options]")

    actparser = mainparser.add_subparsers(
        title="Actions",
        description="Choose one of possible actions and their commands.",
        help="names for specific actions",
        dest="action")

    parsers = dict()
    for cmd, hlp in (
        ("download", "Download a model or one of its datasets"),
        ("run", "Run a model with one of its datasets"),
        ("list", "List models and/or datasets"),
    ):
        parsers[cmd] = actparser.add_parser(cmd, help=hlp)

    parsers["download"].add_argument("model", help="Name of the model to download.")
    parsers["download"].add_argument("dataset", nargs="?", help="Name of the model to download.")

    parsers["run"].add_argument("model", help="Name of the model to run.")
    parsers["run"].add_argument("dataset", help="Name of the dataset to run.")

    return mainparser.parse_args(args=argv[1:])


def main(argv):
    cmdargs = cmdparse(argv)
    if cmdargs.action is None:
        print("Please specify an action. Use '-h' flag for more informatin.")
        return 127

    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))
