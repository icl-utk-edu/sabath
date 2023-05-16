#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii

import sys

if sys.version_info < (3,):
    raise RuntimeError("Only Python 3 supported")


import argparse


def cmdparse(argv):
    parser = argparse.ArgumentParser(
        prog=argv[0],
        description="SABATH: Surrogate AI Benchmarking Applications' Testing Harness",
        epilog="The project is currently under development and new commands are possible in the future.",
        prefix_chars="-",
        usage="%(prog)s <action> [<command>] [options]")

    actparser = parser.add_subparsers(
        title="Actions",
        description="Choose one of possible actions and their commands.",
        help="names for specific actions",
        dest="action")

    runparser = actparser.add_parser("run", help="Run a model with one of its datasets.")
    runparser.add_argument("model", help="Name of the model to use.")
    runparser.add_argument("dataset", help="Name of the dataset to use.")

    return  parser.parse_args(args=argv[1:])


def main(argv):
    cmdargs = cmdparse(argv)
    if cmdargs.action is None:
        print("Please specify an action. Use '-h' flag for more informatin.")
        return 127

    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))
