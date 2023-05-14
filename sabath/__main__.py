#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii

import sys

if sys.version_info < (3,):
    raise RuntimeError("Only Python 3 supported")


import argparse


def cmdparse(argv):
    parser = argparse.ArgumentParser(prog=argv[0],
        description="SABATH: Surrogate AI Benchmarking Applications' Testing Harness",
        epilog="The project is currently under development and new commands are possible in the future.",
        prefix_chars="-",
        usage="%(prog)s <command> [sub-command] [options]")
    return  parser.parse_args(args=argv[1:])


def main(argv):
    cmdargs = cmdparse(argv)
    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))
