#! /usr/bin/env python3
# -*- coding: ascii -*-
# vim: set fileencoding=ascii


"""
SABATH commands

@author Piotr Luszczek
"""


import hashlib, json, logging, os, subprocess, shutil, sys, urllib.parse
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
    dgst = hashlib.sha256(name.encode()).hexdigest()
    return os.path.join(sabath.cache, dgst[:2], dgst[2:], kind)


def _fetch_cached(args, dataset):
    cchpth = cache_path(dataset["url"], "url")
    os.makedirs(cchpth, exist_ok=True)

    base, fname = os.path.split(dataset["url"])
    lfname = os.path.join(cchpth, fname)

    if args.link:
        # create soft link (hard links don't work across devices and/or mount points)
        os.symlink(args.link, os.path.join(cchpth, lfname))

    elif args.path:
        shutil.copy(args.path, cchpth, follow_symlinks=False)

    else:  # must attemp downloading
        if not os.path.exists(lfname):
            wget(dataset["url"], "-q", "-P", cchpth)

    # if it's TAR file and output doesnt exist
    if os.path.splitext(fname)[-1] == ".tar" and not os.path.exists(lfname[:-4]):
        shutil.unpack_archive(lfname, cchpth, format="tar")
        # tar("-C", cchpth, "-xf", lfname)


def fetch(args):
    if args.model:
        model = json.load(open(repo_path("models", args.model)))
        if "git" in model:
            cchpth = cache_path(model["git"], "git")
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
        missing_url = False
        if isinstance(dataset, dict):
            if "url" in dataset:  # single dict with url
                _fetch_cached(args, dataset)
            else:
                print("Missing URL for data set", args.dataset)
                missing_url = True
        else:  # must be a list-like then
            # TODO: support links and copying for multiple files
            if args.link or args.path:
                print("Using links or copying for multiple file datasets is not implemented yet")
                return 127
            ###
            for i, d in enumerate(dataset):
                if 'url' in d:
                    _fetch_cached(args, d)
                else:
                    print("Missing URL for data set", args.dataset,  "file", i)
                    missing_url = True
        if missing_url:
            return 127

    else:
        print("Please secify what to fetch: model or data set.")
        return 127

    return 0


def run(args):
    model = json.load(open(repo_path("models", args.model[0])))
    dataset = json.load(open(repo_path("datasets", args.dataset[0])))
    model["run"]
    return 127


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
        return 127

    if "fetch" == args.command:
        return fetch(args)

    elif "run" == args.command:
        return run(args)

    return 0
