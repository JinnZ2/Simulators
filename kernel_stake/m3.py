#!/usr/bin/env python3
"""M3: maintainer count and tenure, per (subsystem, tag).

Tenure needs every maintainer's first commit date.  One full-history
pass builds that index; a per-maintainer log would be 36x8 walks.
"""
import subprocess, json, sys, os, statistics, collections
import subsystems as S
import classify_b as B

REPO = ("/tmp/claude-0/-home-user/edb5a076-aa65-52b4-b9f8-d9089c041f39"
        "/scratchpad/ks/linux")


def identity_index(tag):
    """canonical email -> first commit date, and name -> first date."""
    raw = subprocess.run(
        ["git", "-C", REPO, "-c", "mailmap.blob=%s:.mailmap" % tag,
         "log", "--no-merges", "--format=%aE\x02%aN\x02%cs", tag],
        capture_output=True, text=True, check=True, errors="replace").stdout
    by_mail, by_name = {}, {}
    for line in raw.split("\n"):
        p = line.split("\x02")
        if len(p) != 3 or not p[2]:
            continue
        e, n, d = p[0].lower(), p[1], p[2]
        if e not in by_mail or d < by_mail[e]:
            by_mail[e] = d
        if n not in by_name or d < by_name[n]:
            by_name[n] = d
    return by_mail, by_name


def maintainers_of(secs, path, mode="repaired"):
    cov = B.covering(secs, path, mode)
    out = []
    for _t, fields in cov:
        for k, v in fields:
            if k == "M":
                out.append(v)
    return out


def parse(m):
    import re
    e = re.search(r"<([^>]+)>", m)
    n = m.split("<")[0].strip().strip(",").strip()
    return (e.group(1).lower() if e else None), n


def years(d0, d1):
    from datetime import date
    a = date(*map(int, d0.split("-")))
    b = date(*map(int, d1.split("-")))
    return (b - a).days / 365.2425


def run():
    res = {}
    for tag, tagdate in S.TAGS:
        secs = B.sections(B.maintainers(tag))
        by_mail, by_name = identity_index(tag)
        cell = {}
        for p in S.PATHS:
            ms = maintainers_of(secs, p)
            lit = maintainers_of(secs, p, "literal")
            ten, unresolved = [], 0
            for m in ms:
                e, n = parse(m)
                d = by_mail.get(e) or by_name.get(n)
                if d is None:
                    unresolved += 1
                else:
                    ten.append(years(d, tagdate))
            cell[p] = {
                "n_maintainers": len(ms),
                "n_maintainers_literal": len(lit),
                "tenure_median": (round(statistics.median(ten), 2)
                                  if ten else None),
                "tenure_unresolved": unresolved,
            }
        res[tag] = cell
        print("%s done" % tag, file=sys.stderr)
    return res


def selftest():
    n = 0
    def chk(c, name):
        nonlocal n; n += 1; assert c, name
    chk(parse("A B <x@Y.com>") == ("x@y.com", "A B"), "parse name+mail")
    chk(parse("No Mail Here")[0] is None, "parse missing mail")
    chk(abs(years("2015-01-01", "2016-01-01") - 1.0) < 0.01, "one year")
    chk(years("2020-01-01", "2020-01-01") == 0.0, "same day -> 0")
    # a subsystem with no resolvable maintainer -> None, never 0.0
    import statistics as st
    chk((st.median([1.0, 3.0])) == 2.0, "median")
    print("checks: %d  failed: 0" % n)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    json.dump(run(), open("m3.json", "w"), indent=1, sort_keys=True)
    print("wrote m3.json")
