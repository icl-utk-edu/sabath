#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii


import os


root = os.getenv("SABATH_ROOT")
if root is None:
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

cache = os.path.join(root, "var", "sabath", "cache")

__all__ = ["cache", "root"]
