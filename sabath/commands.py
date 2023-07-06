#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii


"""
SABATH commands

@author Piotr Luszczek
"""


import json, os, subprocess, sys
import sabath


def git(cmd, *args):
    return subprocess.Popen(("git", cmd) + args, executable="git").wait()


def tar(*args):
    return subprocess.Popen(("tar",) + args, executable="tar").wait()


def wget(url, *args):
    return subprocess.Popen(("wget", url) + args, executable="wget").wait()


def repo_path(m_or_d, name):
    return os.path.join(sabath.root, "var", "sabath", "repos", "builtin", m_or_d, name[0], name + ".json")


def cache_path(name, kind):
    return os.path.join(sabath.cache, name[0], name, kind)


def fetch(args):
    if args.model:
        model = json.load(open(repo_path("models", args.model)))
        if "git" in model:
            cchpth = cache_path(args.model, "git")
            if not os.path.exists(cchpth):
                os.makedirs(cchpth, exist_ok=True)

            if git("clone", model["git"], cchpth):
                raise RuntimeError

    elif args.dataset:
        dataset = json.load(open(repo_path("datasets", args.dataset)))
        if "url" in dataset:
            cchpth = cache_path(args.dataset, "url")
            if not os.path.exists(cchpth):
                os.makedirs(cchpth, exist_ok=True)

            base, fname = os.path.split(dataset["url"])
            lfname = os.path.join(cchpth, fname)

            if not os.path.exists(lfname):
                wget(dataset["url"], "-q", "-P", cchpth)

            # if it's TAR file and output doesnt exist
            if os.path.splitext(fname)[-1] == ".tar" and not os.path.exists(lfname[:-4]):
                tar("-C", cchpth, "-xf", lfname)


def run(args):
    model = json.load(open(repo_path("models", args.model[0])))
    dataset = json.load(open(repo_path("datasets", args.dataset[0])))
    model["run"]


def dispatch(args):
    if args.root:
        sabath.root = args.root

    if not os.path.exists(sabath.root):
        print("Root path {} doesn't exist".format(sabath.root), file=sys.stderr)
        raise FileNotFoundError

    if "fetch" == args.command:
        fetch(args)

    elif "run" == args.command:
        run(args)
