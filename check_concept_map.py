#!/usr/bin/env python3
"""Check concept_map.json and render CONCEPT_MAP.md from it.

    python3 check_concept_map.py            check: every path exists, MD matches JSON
    python3 check_concept_map.py --write    rewrite CONCEPT_MAP.md from the JSON
    python3 check_concept_map.py --strict   also fail when another repo's checkout is absent
    python3 check_concept_map.py --selftest plant defects, show each check fires

A location is {repo, ref, path, role, builder, note}. Simulators paths with ref null
are read from this working tree. Other repos are read with `git cat-file -e ref:path`
from a sibling checkout (../<repo>, ../jinnz2/<repo>, or $CONCEPT_MAP_REPOS/<repo>).
No checkout: NOT_CHECKED, never OK. A pinned `tip` that no longer matches the ref is STALE.
No code is moved by this file. Stdlib only.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
JSON, MD = os.path.join(HERE, "concept_map.json"), os.path.join(HERE, "CONCEPT_MAP.md")
ROLES = ("canonical", "candidate", "copy", "nearest")
PENDING = "pending cross-run"


def checkout(repo):
    roots = [os.path.join(HERE, ".."), os.path.join(HERE, "..", "jinnz2")]
    if os.environ.get("CONCEPT_MAP_REPOS"):
        roots.insert(0, os.environ["CONCEPT_MAP_REPOS"])
    for r in roots:
        d = os.path.join(r, repo)
        if os.path.isdir(os.path.join(d, ".git")):
            return d
    return None


def git(d, *a):
    p = subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def check_location(loc, here=HERE):
    """-> (state, detail); state in OK / MISSING / STALE / NOT_CHECKED."""
    repo, ref, path = loc["repo"], loc.get("ref"), loc["path"]
    if repo == "Simulators" and not ref:
        return ("OK", "") if os.path.exists(os.path.join(here, path)) else ("MISSING", "not in this tree")
    d = here if repo == "Simulators" else checkout(repo)
    if d is None:
        return "NOT_CHECKED", "no checkout of %s" % repo
    if not ref:
        return "MISSING", "a path in another repo needs a ref"
    rc, tip = git(d, "rev-parse", "--short=7", ref)
    if rc:
        return "NOT_CHECKED", "ref %s not fetched in %s" % (ref, d)
    if loc.get("tip") and not tip.startswith(loc["tip"][:7]):
        return "STALE", "%s is now %s, row pinned %s" % (ref, tip, loc["tip"])
    rc, _ = git(d, "cat-file", "-e", "%s:%s" % (ref, path.rstrip("/")))
    return ("OK", "") if rc == 0 else ("MISSING", "not at %s" % ref)


def row_problems(row):
    out, locs = [], row.get("locations", [])
    for k in ("concept", "home", "status", "decided_by", "locations"):
        if k not in row:
            out.append("field %s absent" % k)
    for l in locs:
        if l.get("role") not in ROLES:
            out.append("role %r not in %s" % (l.get("role"), ROLES))
        if not l.get("builder"):
            out.append("%s: builder absent (write 'not recorded')" % l.get("path"))
    n = {r: sum(1 for l in locs if l.get("role") == r) for r in ROLES}
    home = row.get("home")
    if home == "CANONICAL" and (n["canonical"] != 1 or row.get("decided_by") == PENDING):
        out.append("CANONICAL needs exactly one canonical location and a decision that is not pending")
    if home == "CANDIDATE" and (n["candidate"] < 2 or n["canonical"]):
        out.append("CANDIDATE needs two or more candidate locations and no canonical one")
    if home == "SINGLE" and (n["candidate"] + n["canonical"] != 1):
        out.append("SINGLE needs exactly one home location")
    if home == "NOT_LOCATED" and (n["candidate"] or n["canonical"] or not row.get("searched")):
        out.append("NOT_LOCATED needs no home location and a stated search")
    if home not in ("CANONICAL", "CANDIDATE", "SINGLE", "NOT_LOCATED"):
        out.append("home %r unknown" % home)
    return out


def where(l):
    return "%s%s:%s" % (l["repo"], "@" + l["ref"] if l.get("ref") else "", l["path"])


def render(data):
    o = ["# CONCEPT_MAP", "",
         "Generated from `concept_map.json` by `check_concept_map.py --write`. Edit the JSON, not this file.",
         "One block per concept. No code is moved. As of %s." % data["as_of"], "",
         "home: CANONICAL (decided), CANDIDATE (two or more homes, undecided), SINGLE (one copy), NOT_LOCATED.", ""]
    for r in data["rows"]:
        o += ["## %s" % r["concept"], "", "- home: %s" % r["home"], "- status: %s" % r["status"],
              "- decided by: %s" % r["decided_by"]]
        if r.get("searched"):
            o.append("- searched: %s" % r["searched"])
        if r.get("note"):
            o.append("- note: %s" % r["note"])
        if r["locations"]:
            o += ["", "| role | where | builder | note |", "|---|---|---|---|"]
            for l in r["locations"]:
                o.append("| %s | `%s` | %s | %s |" % (l["role"], where(l), l["builder"], l.get("note", "")))
        o.append("")
    return "\n".join(o)


def run(data, md_text, strict=False, here=HERE, quiet=False):
    fails, notchecked, ok = [], [], 0
    for r in data["rows"]:
        for p in row_problems(r):
            fails.append("%s: %s" % (r.get("concept"), p))
        for l in r.get("locations", []):
            st, why = check_location(l, here)
            if st == "OK":
                ok += 1
            elif st == "NOT_CHECKED":
                notchecked.append("%s: %s (%s)" % (r["concept"], where(l), why))
            else:
                fails.append("%s: %s %s (%s)" % (r["concept"], st, where(l), why))
    if md_text != render(data):
        fails.append("CONCEPT_MAP.md does not match concept_map.json (run --write)")
    if strict:
        fails += ["NOT_CHECKED under --strict: " + x for x in notchecked]
    if not quiet:
        for x in notchecked:
            print("NOT_CHECKED  " + x)
        for x in fails:
            print("FAIL  " + x)
        print("rows %d   paths OK %d   NOT_CHECKED %d   failed %d" % (len(data["rows"]), ok, len(notchecked), len(fails)))
    return fails, notchecked


def selftest(data):
    import copy
    base, n, bad = render(data), 0, 0

    def expect(name, d, text, word):
        nonlocal n, bad
        f, _ = run(d, text, quiet=True)
        hit = any(word in x for x in f)
        n += 1
        bad += 0 if hit else 1
        print("%s  %s" % ("fires " if hit else "SILENT", name))
    d = copy.deepcopy(data); d["rows"][0]["locations"][0]["path"] = "no/such/path.py"
    d["rows"][0]["locations"][0]["repo"], d["rows"][0]["locations"][0]["ref"] = "Simulators", None
    expect("missing path", d, render(d), "MISSING")
    expect("MD out of date", data, base + "x", "does not match")
    d = copy.deepcopy(data); d["rows"][0]["home"] = "CANONICAL"
    expect("canonical with no decision", d, render(d), "CANONICAL needs")
    d = copy.deepcopy(data); d["rows"][0]["locations"][0]["builder"] = ""
    expect("builder absent", d, render(d), "builder absent")
    d = copy.deepcopy(data)
    nl = [r for r in d["rows"] if r["home"] == "NOT_LOCATED"][0]; nl["searched"] = ""
    expect("NOT_LOCATED with no search", d, render(d), "NOT_LOCATED needs")
    d = copy.deepcopy(data)
    pinned = [l for r in d["rows"] for l in r["locations"] if l.get("tip")]
    if pinned and check_location(pinned[0])[0] == "OK":
        pinned[0]["tip"] = "0000000"
        expect("pinned tip moved", d, render(d), "STALE")
    else:
        print("NOT_RUN  pinned tip moved (no checkout holding a pinned ref)")
    print("planted %d   silent %d" % (n, bad))
    return bad


if __name__ == "__main__":
    data = json.load(open(JSON, encoding="utf-8"))
    if "--write" in sys.argv:
        open(MD, "w", encoding="utf-8").write(render(data))
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest(data) else 0)
    md = open(MD, encoding="utf-8").read() if os.path.exists(MD) else ""
    f, _ = run(data, md, strict="--strict" in sys.argv)
    sys.exit(1 if f else 0)
