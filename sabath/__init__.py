#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii


import os, logging


root = os.getenv("SABATH_ROOT")
if root is None:
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

cache = os.path.join(root, "var", "sabath", "cache")

logging.basicConfig(filename=os.path.join(cache, "sabath.log"), encoding="utf-8", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

__all__ = ["cache", "root"]
