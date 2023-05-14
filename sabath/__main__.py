#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii

import sys

if sys.version_info < (3,):
    raise RuntimeError("Only Python 3 supported")


def main(argv):
    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))
