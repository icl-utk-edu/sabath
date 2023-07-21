#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii


"""
SABATH commands

@author Piotr Luszczek
"""


import json, logging, os, subprocess, sys, urllib.parse
import sabath


def git(cmd, *args):
    return subprocess.Popen(("git", cmd) + args, executable="git").wait()


def tar(*args):
    return subprocess.Popen(("tar",) + args, executable="tar").wait()


def wget(url, *args):
    return subprocess.Popen(("wget", url) + args, executable="wget").wait()


def repo_path(m_or_d, name):
    return os.path.join(sabath.root, "var", "sabath", "assets", "sabath", m_or_d, name[0], name + ".json")


def cache_path(name, kind):
    return os.path.join(sabath.cache, name[0], name, kind)


def fetch(args):
    if args.model:
        model = json.load(open(repo_path("models", args.model)))
        if "git" in model:
            cchpth = cache_path(args.model, "git")
            if not os.path.exists(cchpth):
                os.makedirs(cchpth, exist_ok=True)

            repo = os.path.split(os.path.splitext(urllib.parse.urlparse(model["git"]).path)[0])[-1]
            if os.path.exists(os.path.join(cchpth, repo, ".git")):
                print("Repo directory for {} already exists in {}".format(args.model, os.path.join(cchpth, repo, ".git")))

            else:
                if git("clone", model["git"], os.path.join(cchpth, repo)):
                    logging.error("Failed cloning repo for model " + args.model)
                    return 127

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

    return 0


def run(args):
    model = json.load(open(repo_path("models", args.model[0])))
    dataset = json.load(open(repo_path("datasets", args.dataset[0])))
    model["run"]


def set_cache(pth):
    if pth:
        for tst, msg in (
            (os.path.exists(pth), "doesn't exist"),
            (os.path.isdir(pth), "is not directory"),
            (os.access(pth, os.R_OK), "is not readable"),
            (os.access(pth, os.W_OK), "is not writeable"),
            (os.access(pth, os.X_OK), "is not executable"),
        ):
            if not tst:
                print("Cache path {}, ignoring {}".format(msg, pth),
                    file=sys.stderr)
                break

        else:
            logging.info("Cache directory set to " + pth)
            sabath.cache = pth


def dispatch(args):
    if args.root:
        sabath.root = args.root

    if args.cache:
        set_cache(args.cache)

    if not os.path.exists(sabath.root):
        print("Root path {} doesn't exist".format(sabath.root), file=sys.stderr)
        raise FileNotFoundError

    if "fetch" == args.command:
        fetch(args)

    elif "run" == args.command:
        run(args)
