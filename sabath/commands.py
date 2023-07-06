#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii


"""
SABATH commands

@author Piotr Luszczek
"""


import json, os, subprocess
import sabath


def git(cmd, *args):
    return subprocess.Popen(("git", cmd) + args, executable="git").wait()

def fetch(args):
    if args.model:
        model = json.load(open(os.path.join(sabath.root, "var", "sabath", "repos", "builtin", "models", args.model[0],  args.model + ".json")))
        if "git" in model:
            cchpth = os.path.join(sabath.cache, args.model[0], args.model)
            if not os.path.exists(cchpth):
                os.makedirs(cchpth, exist_ok=True)

            if git("clone", model["git"], cchpth):
                raise RuntimeError


def dispatch(args):
    if args.root:
        sabath.root = args.root

    if not os.path.exists(sabath.root):
        print("Root path {} doesn't exist".format(sabath.root), file=sys.stderr)
        raise FileNotFoundError

    if "fetch" == args.command:
        fetch(args)
