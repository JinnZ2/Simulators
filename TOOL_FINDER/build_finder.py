#!/usr/bin/env python3
"""build_finder.py -- builds TOOL_FINDER.md and finder.json from entries.py.

CC0. Stdlib only, parses under 3.8. Co-authored (JinnZ2 + Claude), 2026-11-09.

  python3 TOOL_FINDER/build_finder.py            verify quotes, write both files
  python3 TOOL_FINDER/build_finder.py --run      also run each entry's own check
                                                 and record status.json
  python3 TOOL_FINDER/build_finder.py --selftest

Every `measures` and `breaks_when` quote must be a literal substring
(whitespace-normalised) of the file it cites, in a checkout of that repo.
A quote that is not found stops the build: a "verbatim" field that is not
verbatim is the defect this index exists to avoid. A repo with no local
checkout reads QUOTE_NOT_CHECKED for its entries, never a pass.

Sibling checkouts are looked for at ../<dir> beside this repo; override with
FINDER_<REPO>_PATH (e.g. FINDER_METHOD_LAYER_PATH).

status: RUN      the entry's own check command exited 0, in this session
        UNKNOWN  it was run and exited non-zero, or timed out
        NOT_RUN  no check command is stated, or the repo is not checked out
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import entries as EN  # noqa: E402

DIRS = {"Simulators": None, "method-layer": "method-layer", "JinnZ2": "jinnz2",
        "Shadow-Hunting": "shadow-hunting", "Cross-Domain-Toolkit": "cross-domain-toolkit"}
STATUS = os.path.join(HERE, "status.json")
STATES = ("RUN", "NOT_RUN", "UNKNOWN")


def repo_dir(repo):
    if repo == "Simulators":
        return ROOT
    env = os.environ.get("FINDER_%s_PATH" % repo.upper().replace("-", "_"))
    cand = env or os.path.join(os.path.dirname(ROOT), DIRS[repo])
    return cand if os.path.isdir(cand) else None


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def locate(repo, rel, quote):
    """(state, line) -- FOUND with first line number, MISSING, or NOT_CHECKED."""
    if quote == EN.NB:
        return "NO_QUOTE", None
    d = repo_dir(repo)
    if d is None:
        return "QUOTE_NOT_CHECKED", None
    p = os.path.join(d, rel)
    if not os.path.isfile(p):
        return "MISSING_FILE", None
    text = open(p, encoding="utf-8", errors="replace").read()
    flat = norm(text)
    q = norm(quote)
    k = flat.find(q)
    if k < 0:
        return "MISSING", None
    # map the normalised offset back to a line: accumulate normalised lines
    pos = 0
    for i, line in enumerate(text.split("\n"), 1):
        n = norm(line)
        if not n:
            continue
        end = pos + len(n)
        if k < end:
            return "FOUND", i
        pos = end + 1   # the single space norm() puts between lines
    return "FOUND", None


def git_head(d):
    try:
        return subprocess.check_output(["git", "-C", d, "rev-parse", "--short", "HEAD"],
                                       text=True).strip()
    except Exception:
        return None


def _worktree(d):
    """A detached throwaway worktree at HEAD, so a check that writes files
    (a ledger, a denial record, a regenerated queue) cannot edit the tree
    being indexed. Uncommitted changes are invisible to it: commit first."""
    import tempfile
    w = tempfile.mkdtemp(prefix="finder_wt_")
    os.rmdir(w)
    subprocess.check_call(["git", "-C", d, "worktree", "add", "-q", "--detach", w, "HEAD"])
    return w


def run_checks():
    out, wts = {}, {}
    try:
        for e in EN.E:
            key = "%s:%s" % (e["repo"], e["path"])
            d = repo_dir(e["repo"])
            if not e["check"]:
                out[key] = {"status": "NOT_RUN", "why": "no check command stated"}
                continue
            if d is None:
                out[key] = {"status": "NOT_RUN", "why": "repo not checked out"}
                continue
            if d not in wts:
                wts[d] = _worktree(d)
            cwd = wts[d]
            try:
                p = subprocess.run(e["check"], shell=True, cwd=cwd, capture_output=True, text=True,
                                   timeout=300, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
                lines = [l for l in (p.stdout + p.stderr).split("\n") if l.strip()]
                out[key] = {"status": "RUN" if p.returncode == 0 else "UNKNOWN",
                            "exit": p.returncode, "last_line": lines[-1][:160] if lines else "",
                            "commit": git_head(cwd), "cmd": e["check"], "where": "worktree at HEAD"}
            except subprocess.TimeoutExpired:
                out[key] = {"status": "UNKNOWN", "why": "timeout 300 s", "cmd": e["check"]}
    finally:
        for d, w in wts.items():
            subprocess.call(["git", "-C", d, "worktree", "remove", "--force", w])
    return out


def build(status):
    rows, problems = [], []
    for e in EN.E:
        key = "%s:%s" % (e["repo"], e["path"])
        m_state, m_line = locate(e["repo"], e["measures_file"], e["measures"])
        b_state, b_line = (("NO_QUOTE", None) if e["breaks_file"] is None
                           else locate(e["repo"], e["breaks_file"], e["breaks_when"]))
        for st, f in ((m_state, e["measures_file"]), (b_state, e["breaks_file"])):
            if st in ("MISSING", "MISSING_FILE"):
                problems.append("%s: quote %s in %s" % (key, st, f))
        s = status.get(key, {"status": "NOT_RUN", "why": "build run without --run"})
        rows.append(dict(e, measures_src="%s:%s" % (e["measures_file"], m_line or "?"),
                         measures_quote_state=m_state,
                         breaks_src=("%s:%s" % (e["breaks_file"], b_line or "?")) if e["breaks_file"] else None,
                         breaks_quote_state=b_state, status=s["status"], status_detail=s))
    return rows, problems


def md(rows):
    L = ["# TOOL_FINDER", "",
         "Find a tool by what you need it to do. CC0. Co-authored (JinnZ2 + Claude), 2026-11-09.",
         "Generated by `build_finder.py` from `entries.py`; `finder.json` holds the same content.", "",
         "## HOW TO USE", "",
         "- Search this page by NEED (section headings) or by ALIAS (plain phrases in each entry).",
         "- Tool names here are intentionally not common terms. A common term carries baggage or a wrong",
         "  assumption, so names follow function-fit. Searching by name alone will miss tools.",
         "- Read **breaks when** before use. A tool used past its stated limit returns a readout about",
         "  nothing.",
         "- **measures** and **breaks when** are verbatim quotes from the tool's own text, located by",
         "  file:line and checked as literal substrings at build time. Aliases are ALIAS_PROPOSED: written",
         "  from the tool's stated scope, not from its code, and not tested against real searches.",
         "- **status**: RUN = the tool's own check exited 0 in the build session; UNKNOWN = it ran and",
         "  exited non-zero; NOT_RUN = no check stated or repo not checked out. Status is about the check,",
         "  never about whether the tool is right.",
         "- An entry may serve more than one need; it is listed under its first need and named under the others.",
         "- **precision / assumes / chain** (Amendment A1) are A1_READING: a model reading of each tool's stated",
         "  scope, not verbatim. chain names which hops of sensor -> encoding -> transmission -> decoding ->",
         "  inference the tool reads or ignores. A hop a tool ignores is a hop it cannot vouch for: an AI",
         "  reading its output reads through that hop UNVERIFIED (see Simulators `tools/channel_chain.py`).",
         ""]
    for key, title in EN.NEEDS:
        L.append("## %s" % title)
        L.append("")
        prim = [r for r in rows if r["need"] == key]
        sec = [r for r in rows if key in r["also"]]
        for r in prim:
            L.append("### %s  (%s / `%s`)" % (r["name"], r["repo"], r["path"]))
            L.append("- need: %s" % title)
            L.append("- aliases: " + "; ".join(r["aliases"]))
            L.append("- measures (%s): \"%s\"" % (r["measures_src"], r["measures"]))
            if r["breaks_when"] == EN.NB:
                L.append("- breaks when: NO_STATED_LIMITS")
            else:
                L.append("- breaks when (%s): \"%s\"" % (r["breaks_src"], r["breaks_when"]))
            L.append("- precision: %s" % r["precision"])
            L.append("- assumes: %s" % r["assumes"])
            L.append("- chain: %s" % r["chain"])
            sd = r["status_detail"]
            det = sd.get("last_line") or sd.get("why") or ""
            L.append("- status: %s%s" % (r["status"], (" -- `%s` -> %s" % (sd.get("cmd"), det)) if sd.get("cmd") else (" -- " + det if det else "")))
            L.append("")
        if sec:
            L.append("Also serves this need: " + ", ".join("%s (%s)" % (r["name"], r["repo"]) for r in sec))
            L.append("")
    L += ["## NAME_COLLISION", "", "| name | one | other | note |", "|---|---|---|---|"]
    for c in EN.NAME_COLLISIONS:
        L.append("| %s |" % " | ".join(x.replace("|", "\\|") for x in c))
    L += ["", "## GAPS", "", "Needs with no tool located in the repos read for this index.", "",
          "| need section | need | why it is a gap |", "|---|---|---|"]
    for g in EN.GAPS:
        L.append("| %s |" % " | ".join(g))
    L += ["", "## Scope of this index", "",
          "Repos read: Simulators, method-layer, JinnZ2/JinnZ2, Shadow-Hunting, Cross-Domain-Toolkit (A2).",
          "Other CC0 JinnZ2 repos were",
          "not read for this index; a need marked as a GAP may have a tool there. `tools/tool_inventory.json`",
          "(Simulators) lists 3469 modules across 81 repos and is the wider, unverified search surface.", ""]
    return "\n".join(L)


def selftest():
    ok = tot = 0
    def check(c, lab):
        nonlocal ok, tot
        tot += 1
        ok += bool(c)
        if not c:
            print("FAIL:", lab)
    check(locate("Simulators", "tail-check/README.md", "Was an inference about a person SAID") [0] == "FOUND", "known quote found")
    check(locate("Simulators", "tail-check/README.md", "this sentence is not in the file")[0] == "MISSING", "missing quote refused")
    check(locate("Simulators", "tail-check/README.md", EN.NB)[0] == "NO_QUOTE", "NO_STATED_LIMITS not checked as a quote")
    st, ln = locate("Simulators", "tail-check/README.md", "Was an inference about a person SAID")
    check(open(os.path.join(ROOT, "tail-check/README.md")).read().split("\n")[ln - 1].startswith("Was an inference"), "line number points at the quote")
    st, ln = locate("Simulators", "tail-check/README.md", "case-sensitive substring after")
    check("case-sensitive" in open(os.path.join(ROOT, "tail-check/README.md")).read().split("\n")[ln - 1], "line number for a mid-line quote")
    rows, probs = build({})
    check(probs == [], "every quote verbatim: %s" % probs)
    check(all(r["status"] in STATES for r in rows), "status vocabulary")
    check(all(3 <= len(r["aliases"]) <= 8 for r in rows), "3-8 aliases per entry")
    keys = {k for k, _ in EN.NEEDS}
    check(all(r["need"] in keys and set(r["also"]) <= keys for r in rows), "every need is a declared section")
    check(all(any(r["need"] == k for r in rows) for k in keys), "every section has a primary entry")
    j = json.loads(json.dumps({"entries": rows}))
    check(len(j["entries"]) == len(EN.E), "json round trip")
    check(len(set("%s:%s" % (e["repo"], e["path"]) for e in EN.E)) == len(EN.E), "no duplicate entry")
    check(all(e.get("precision") and e.get("assumes") and e.get("chain") for e in EN.E), "A1 fields on every entry")
    check(set(EN.A1) == {e["name"] for e in EN.E}, "A1 table matches entries exactly")
    print("checks: %d   failed: %d" % (tot, tot - ok))
    return 0 if ok == tot else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    status = {}
    if "--run" in argv:
        status = run_checks()
        json.dump(status, open(STATUS, "w"), indent=1, sort_keys=True)
    elif os.path.isfile(STATUS):
        status = json.load(open(STATUS))
    rows, probs = build(status)
    if probs:
        print("REFUSED: quotes not verbatim:\n  " + "\n  ".join(probs))
        return 1
    open(os.path.join(HERE, "TOOL_FINDER.md"), "w").write(md(rows))
    json.dump({"generated_by": "TOOL_FINDER/build_finder.py", "date": "2026-11-09",
               "needs": EN.NEEDS, "entries": rows,
               "name_collisions": [dict(zip(("name", "one", "other", "note"), c)) for c in EN.NAME_COLLISIONS],
               "gaps": [dict(zip(("need", "gap", "why"), g)) for g in EN.GAPS]},
              open(os.path.join(HERE, "finder.json"), "w"), indent=1)
    print("wrote TOOL_FINDER.md and finder.json: %d entries, %d collisions, %d gaps"
          % (len(rows), len(EN.NAME_COLLISIONS), len(EN.GAPS)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
