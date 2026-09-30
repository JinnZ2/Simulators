#!/usr/bin/env python3
"""M1 numerator, M6, and the maturity confound.  KLOC is measured
separately (kloc.py) because it is the only step that needs blobs.
"""
import subprocess, collections, json, sys, os
import subsystems as S

REPO = ("/tmp/claude-0/-home-user/edb5a076-aa65-52b4-b9f8-d9089c041f39"
        "/scratchpad/ks/linux")
SEP1, SEP2 = "\x01", "\x02"


def git(args, tag=None):
    cmd = ["git", "-C", REPO]
    if tag:
        cmd += ["-c", "mailmap.blob=%s:.mailmap" % tag]
    return subprocess.run(cmd + args, capture_output=True, text=True,
                          check=True, errors="replace").stdout


def interval(prev, tag):
    """One log pass. -> [(sha, name, email, [files])]"""
    raw = git(["log", "--no-merges",
               "--pretty=format:%s%%H%s%%aN%s%%aE" % (SEP1, SEP2, SEP2),
               "--name-only", "%s..%s" % (prev, tag)], tag=tag)
    out = []
    for blk in raw.split(SEP1):
        if not blk.strip():
            continue
        head, _, rest = blk.partition("\n")
        parts = head.split(SEP2)
        if len(parts) != 3:
            continue
        files = [f for f in rest.split("\n") if f.strip()]
        out.append((parts[0], parts[1], parts[2], files))
    return out


def attribute(commits):
    """-> {path: {'commits': n, 'authors': Counter}}"""
    acc = {p: {"commits": 0, "authors": collections.Counter()}
           for p in S.PATHS}
    for _sha, name, email, files in commits:
        who = "%s <%s>" % (name, email)
        for p in S.PATHS:
            if any(f.startswith(p) for f in files):
                acc[p]["commits"] += 1
                acc[p]["authors"][who] += 1
    return acc


def concentration(counter):
    """M6: share of commits held by the top 1 and top 3 individuals."""
    tot = sum(counter.values())
    if tot == 0:
        return None, None, 0          # absent, never 0.0
    top = [c for _w, c in counter.most_common(3)]
    return top[0] / tot, sum(top) / tot, len(counter)


def first_commit_date(path):
    """Maturity confound: first commit anywhere in history touching path."""
    out = git(["log", "--reverse", "--format=%cs", "--max-count=1",
               "--diff-filter=A", "--", path]).strip()
    if not out:
        out = git(["log", "--format=%cs", "--", path]).strip().split("\n")[-1]
    return out or None


def selftest():
    n = 0
    def chk(c, name):
        nonlocal n
        n += 1
        assert c, name
    a, b, k = concentration(collections.Counter())
    chk(a is None and b is None and k == 0, "empty -> None, never 0.0")
    c1 = collections.Counter({"x": 10})
    chk(concentration(c1) == (1.0, 1.0, 1), "single author -> 1.0/1.0")
    c2 = collections.Counter({"a": 5, "b": 3, "c": 1, "d": 1})
    t1, t3, k = concentration(c2)
    chk(abs(t1 - 0.5) < 1e-12, "top1 = 5/10")
    chk(abs(t3 - 0.9) < 1e-12, "top3 = 9/10")
    chk(k == 4, "distinct authors")
    c3 = collections.Counter({"a": 1, "b": 1})
    chk(concentration(c3)[1] == 1.0, "top3 caps at total when <3 authors")
    # attribution: a commit touching two subsystems counts in both
    fake = [("s", "N", "e@x", ["mm/page_alloc.c", "block/bio.c"]),
            ("t", "N", "e@x", ["Documentation/x.rst"])]
    acc = attribute(fake)
    chk(acc["mm/"]["commits"] == 1, "attributed to mm")
    chk(acc["block/"]["commits"] == 1, "attributed to block")
    chk(acc["lib/"]["commits"] == 0, "untouched stays 0")
    chk(sum(v["commits"] for v in acc.values()) == 2, "no double count within a path")
    print("checks: %d  failed: 0" % n)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    res = {}
    tags = [t for t, _d in S.TAGS]
    for i in range(1, len(tags)):
        prev, tag = tags[i - 1], tags[i]
        acc = attribute(interval(prev, tag))
        cell = {}
        for p in S.PATHS:
            t1, t3, k = concentration(acc[p]["authors"])
            cell[p] = {"commits": acc[p]["commits"], "top1": t1,
                       "top3": t3, "authors": k}
        res["%s..%s" % (prev, tag)] = cell
        print("%s..%s  done" % (prev, tag), file=sys.stderr)
    age = {p: first_commit_date(p) for p in S.PATHS}
    json.dump({"intervals": res, "first_commit": age},
              open("measures.json", "w"), indent=1, sort_keys=True)
    print("wrote measures.json")
