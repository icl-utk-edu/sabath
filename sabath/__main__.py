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


import argparse, os


root = os.getenv("SABATH_ROOT")
if root is None:
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def cmdparse(argv):
    mainparser = argparse.ArgumentParser(
        prog=argv[0],
        description="SABATH: Surrogate AI Benchmarking Applications' Testing Harness",
        epilog="The project is currently under development and new commands are possible in the future.",
        prefix_chars="-",
        usage="%(prog)s <action> [<command>] [options]")

    # don't use pathlib to support Python 3.3 and earlier
    mainparser.add_argument("--root", type=str, help="Directory root for SABATH files")

    actparser = mainparser.add_subparsers(
        title="Actions",
        description="Choose one of possible actions and their commands.",
        help="names for specific actions",
        dest="action")

    parsers = dict()
    for cmd, hlp in (
        ("fetch", "Download a model or one of its datasets"),
        ("list", "List models or datasets"),
        ("info", "Show information about models or datasets"),
        ("run", "Run a model with one of its datasets"),
    ):
        parsers[cmd] = actparser.add_parser(cmd, help=hlp)

    parsers["fetch"].add_argument("model", help="Name of the model to fetch.")
    parsers["fetch"].add_argument("dataset", nargs="?", help="Name of the model to fetch.")

    parsers["run"].add_argument("model", help="Name of the model to run.")
    parsers["run"].add_argument("dataset", help="Name of the dataset to run.")

    return mainparser.parse_args(args=argv[1:])


def cmddispatch(args):
    global root

    if args.root:
        root = args.root

    if not os.path.exists(root):
        print("Root path {} doesn't exist".format(root), file=sys.stderr)
        raise FileNotFoundError


def main(argv):
    cmdargs = cmdparse(argv)
    if cmdargs.action is None:
        print("Please specify an action. Use '-h' flag for more informatin.")
        return 127

    cmddispatch(cmdargs)
    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))
