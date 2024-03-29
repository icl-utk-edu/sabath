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


from .argvparse import main


if "__main__" == __name__:
    sys.exit(main(sys.argv))
