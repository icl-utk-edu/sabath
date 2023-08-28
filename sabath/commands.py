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


def fetch_fragment(fragment, link=None, path=None):
    cchpth = cache_path(fragment["url"], "url")
    os.makedirs(cchpth, exist_ok=True)

    base, fname = os.path.split(fragment["url"])
    lfname = os.path.join(cchpth, fname)

    if link:
        # create soft link (hard links don't work across devices and/or mount points)
        try:
            os.symlink(link, os.path.join(cchpth, lfname))  
        except FileExistsError:
            print("File or link already exists:", lfname)

    elif path:
        shutil.copy(path, cchpth, follow_symlinks=False)

    else:  # must attemp downloading
        if not os.path.exists(lfname):
            wget(fragment["url"], "-q", "-P", cchpth)
        f_type = fragment.get('type')
        # TODO: Add checks if downloads and extracts are complete 
        if f_type == "file_list":
            # Assuming that linking and copying point to downloaded and extracted 
            # dataset so doing that only here
            # We don't know how the file list will be retrieved in the future
            # so using local rather than external file
            wget('-i', lfname, "-q", "-P", cchpth)
        elif f_type == "archive":
            # FIXME: if the archive do not have top level directory all 
            #        files will be extracted loose, so the directory check 
            #        will not work
            # if not os.path.exists(lfname[:-4]):
            
            # It can guess the archive type
            shutil.unpack_archive(lfname, cchpth)

def hashable(dct):
    "Create hashable string by  normalizing a JSON-serializable dictionary"
    # return the same dictionary with sorted keys
    return json.dumps({k: dct[k] for k in sorted(dct.keys())})


def fetch(args):
    if args.model:
        model = json.load(open(repo_path("models", args.model)))
        if "git" in model:
            cchpth = cache_path(hashable(model["git"]), "git")
            if not os.path.exists(cchpth):
                os.makedirs(cchpth, exist_ok=True)

            repo = os.path.split(os.path.splitext(urllib.parse.urlparse(model["git"]["origin"]).path)[0])[-1]
            repopath = os.path.join(cchpth, repo)
            if os.path.exists(os.path.join(repopath, ".git")):
                print("Repo directory for {} already exists in {}".format(args.model, os.path.join(repopath, ".git")))

            else:
                if git("clone", model["git"]["origin"], "--tags", os.path.join(cchpth, repo)):
                    logging.error("Failed cloning repo for model " + args.model)
                    return 127

                else:  # cloning was successful
                    for dtl, prf in (("branch", ""), ("tag", "tags/"), ("commit", "")):
                        if dtl in model["git"]:  # extra detail present
                            curdir = os.getcwd()
                            os.chdir(repopath)
                            retcod = git("checkout", prf + model["git"][dtl])
                            os.chdir(curdir)
                            if retcod:
                                print("Checking out {} {} for model {} failed.".format(dtl, model["git"][dtl], args.model))
                                return 127
                            else:
                                print("Checked out", dtl, model["git"][dtl])

    elif args.dataset:
        if args.link and args.path:
            print("Both links and paths specified. Ignoring paths and using links only.")

        dataset = json.load(open(repo_path("datasets", args.dataset)))

        fragments = dataset["fragments"]
        for attr in "link", "path":
            lorp = getattr(args, attr)
            if lorp:
                if len(lorp) != len(fragments):
                    print("Mismatch in number of links/paths:", len(lorp), "and data set fragments:", len(fragments))
                    return 127
                break
        else:
            attr = ""  # no links or paths options found in arguments

        d = dict()
        missing_url = False
        for i, fragment in enumerate(fragments):
            if 'url' in fragment:
                if attr:
                    d[attr] = getattr(args, attr)[i]
                fetch_fragment(fragment, **d)

            else:
                print("Missing URL for data set", "'" + args.dataset + "'", "fragment", i,
                    "" if "id" not in fragment else "'" + fragment["id"] + "'")
                missing_url = True

        if missing_url:
            return 127

        return 0

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
