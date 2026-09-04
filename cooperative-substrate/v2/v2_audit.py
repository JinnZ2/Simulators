#!/usr/bin/env python3
"""Reads WORK_ORDER_V2.md against the folder and the two v2 instruments
built for it. The delivered v2/p4_goal.py is read and never edited; the
seed scope_test.py and the v1 parts are imported, not rewritten. Every
number in the CSP_021.. rows of ../CLAIM_TABLE.md is computed here.
Refuses --selftest (checks live in selftest_v2.py).
"""

import ast
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(PARENT, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, PARENT)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
import p5_lag as P5  # noqa: E402
import scope_check as SC  # noqa: E402
import no_severity  # noqa: E402

# The v2 manifest, and where each item lands in the folder. A DELIVERED
# item is on disk as delivered; RENAMES_V1 names the v1 file that already
# implements it (rebuilding would be MF_019 copy drift); NEW is built
# here; SEEDED extends an existing file; DECLINED is first-party thesis
# authorship the audit posture does not produce.
MANIFEST = {
    "p4_goal.py": ("DELIVERED_TRUNCATED", "v2/p4_goal.py"),
    "p3_comprehension.py": ("RENAMES_V1", "p3_comprehension.py"),
    "p2_substrate.py": ("RENAMES_V1", "p2_substrate_audit.py"),
    "p1_records.py": ("RENAMES_V1", "p1_deps_extract.py"),
    "p5_lag.py": ("NEW", "v2/p5_lag.py"),
    "scope_check.py": ("SEEDED", "v2/scope_check.py"),
    "run_all.py": ("RENAMES_V1", "run_all.py"),
    "EVIDENCE.md": ("RENAMES_V1", "EVIDENCE_PACK.md"),
    "CLAIMS.md": ("DECLINED", "CLAIM_TABLE.md (CSP_ ids; a first-party CS_ thesis file is not authored)"),
    "README.md": ("PRESENT", "README.md + v2/README.md"),
}


def truncation():
    """Detect, do not assert. p4_goal.py is delivered. It happens to end
    on a syntactically complete line, so it parses; the truncation is
    STRUCTURAL and is read that way -- run() has no return, the module
    has no __main__ guard, only one of the three stances the docstring
    names appears in the body, and the last assignment binds an
    undefined name. The file cannot run; it is left as delivered."""
    path = os.path.join(HERE, "p4_goal.py")
    src = open(path, encoding="utf-8").read()
    try:
        tree = ast.parse(src)
        parses = True
    except SyntaxError:
        return {"parses": False, "bytes": len(src), "complete": False, "reason": "does not parse"}
    run = next((n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "run"), None)
    run_returns = run is not None and any(isinstance(n, ast.Return) for n in ast.walk(run))
    has_guard = any(isinstance(n, ast.If) and getattr(getattr(n.test, "left", None), "id", None) == "__name__"
                    for n in ast.walk(tree))
    stances_named = [s for s in ("accept", "correct", "contest") if ('"%s"' % s) in src or ("'%s'" % s) in src]
    bound = set()
    if run is not None:
        for n in ast.walk(run):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                bound.add(n.id)
            if isinstance(n, ast.arg):
                bound.add(n.arg)
    last = src.rstrip().splitlines()[-1]
    # the last line reads `stance, used, value = "accept", pr`; `pr` is
    # bound nowhere in run() (the binding is `prior`), so the file would
    # raise NameError -- a truncation tell that survives the file parsing.
    rhs_names = [n for n in re.findall(r"[A-Za-z_]\w*", last.split("=", 1)[-1]) if not (len(n) >= 2 and n[0] in "\"'")]
    binds_undefined = any(n not in bound and n not in ("accept", "correct", "contest") for n in rhs_names)
    return {"parses": parses, "bytes": len(src), "run_has_return": run_returns, "has_main_guard": has_guard,
            "stances_in_body": stances_named, "stances_expected": 3, "last_line": last,
            "binds_undefined_last": binds_undefined,
            "complete": bool(run_returns and has_guard and len(stances_named) == 3)}


def manifest_map():
    out = {}
    for name, (kind, where) in MANIFEST.items():
        target = where.split(" ")[0].split("(")[0]
        exists = os.path.exists(os.path.join(ROOT, "cooperative-substrate", target)) if "/" not in target \
            else os.path.exists(os.path.join(PARENT, target))
        out[name] = {"kind": kind, "where": where, "target_exists": exists}
    counts = {}
    for v in out.values():
        counts[v["kind"]] = counts.get(v["kind"], 0) + 1
    return {"map": out, "counts": counts}


def v1_has_correct_mode():
    """The v2 P4 cut is error-correction (consumes prior output,
    terminates) against contestation (refuses it, does not). v1's
    p4_goal_coherence models a random walk with one contest probability
    and no error-correct mode, so it cannot represent the v2 falsifier's
    antecedent (a terminating chain with a contesting step is impossible
    in v1; a terminating chain with an error-correcting step is not
    expressible at all)."""
    src = open(os.path.join(PARENT, "p4_goal_coherence.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    return {"v1_functions": funcs, "mentions_correct_mode": "correct" in src.lower().split("contest")[0][-200:] if "contest" in src.lower() else False,
            "has_three_stances": all(w in src for w in ("accept", "correct", "contest")),
            "v2_delivered_names_the_cut": "stance" in open(os.path.join(HERE, "p4_goal.py"), encoding="utf-8").read()}


def p5_anchors():
    out = {}
    for a in P5.ANCHORS:
        e = P5.evaluate(a)
        out[a["name"]] = {"ratio": e["gate"]["ratio"], "verdict": e["gate"]["verdict"],
                          "precondition": e["precondition"]["state"], "cell": e["compliance"]["cell"]}
    return out


def scope_null():
    conds, cases = SC.seed_cases()
    ns = SC.null_search(cases)
    return {"cases": len(cases), "harsh_cases": [c["name"] for c in cases if c["harsh"]],
            "all_present": [c["name"] for c in cases if SC.all_present(c)],
            "null": ns}


def scan_flags(text):
    """§6 targets a SECTION or a byline, not a mention. A lexical scan
    for the words 'author' / 'working-style' / 'cooperation outperforms'
    fires on any faithful text that NAMES the non-goal to disclaim it
    (the v2 README must quote 'not valid for ... cooperation outperforms
    competition' from the order's own envelope) -- `T1-1` / `DF_010`.
    So a flag is a markdown heading whose title is an author / about /
    working-style section, or a python author byline, not a prose
    mention."""
    flags = []
    for line in text.splitlines():
        s = line.strip().lower()
        heading = s.startswith("#") and any(w in s for w in ("author", "working style", "working-style", "about the"))
        byline = s.startswith("author:") or "__author__" in s or s.startswith("# author") or s.startswith("written by")
        if heading or byline:
            flags.append(line.strip())
    return flags


def non_goal_scan():
    """§6 over the DELIVERABLE files. The scanner excludes its own source
    (it names the target words, the `scan.py` / UNI_009 self-reference)
    and looks for author / working-style SECTIONS, not prose mentions of
    the non-goal. The values-advocacy half of §6 is not lexically
    separable from its disclaimer and is met by the audit posture (no
    first-party `CS_` thesis file authored: CSP_022, CSP_026), not by a
    word list."""
    targets = ["p5_lag.py", "scope_check.py", "p4_goal.py", "README.md"]
    hits = {}
    for f in targets:
        p = os.path.join(HERE, f)
        if not os.path.exists(p):
            continue
        h = scan_flags(open(p, encoding="utf-8").read())
        if h:
            hits[f] = h
    return {"scanned": targets, "excluded": ["v2_audit.py (names the target words; scanning it is the scan.py self-reference)"],
            "hits": hits, "clean": not hits, "values_half": "not lexically separable from its disclaimer; met by the audit posture (no CS_ thesis file)"}


def render():
    L = ["cooperative-substrate v2 audit"]
    t = truncation()
    L.append("v2/p4_goal.py (delivered): parses %s, %d bytes; %s" % (
        t["parses"], t["bytes"], ("stops at line %d, ends mid-statement %s, last line %r" % (t["stops_at_line"], t["ends_mid_statement"], t["last_line"])) if not t["parses"] else "last line %r" % t["last_line"]))
    mm = manifest_map()
    L.append("manifest map (%s):" % mm["counts"])
    for name, v in mm["map"].items():
        L.append("  %-22s %-18s %-55s exists %s" % (name, v["kind"], v["where"], v["target_exists"]))
    v1 = v1_has_correct_mode()
    L.append("v1 P4 vs v2 cut: v1 functions %s; v1 has three stances %s; v2 delivered names the cut (stance column) %s" % (
        v1["v1_functions"], v1["has_three_stances"], v1["v2_delivered_names_the_cut"]))
    L.append("P5 anchors:")
    for n, r in p5_anchors().items():
        L.append("  %-46s ratio %-10s %-16s pre %-16s cell %s" % (
            n[:46], ("%.1f" % r["ratio"]) if r["ratio"] is not None else "undefined", r["verdict"], r["precondition"], r["cell"]))
    sn = scope_null()
    L.append("scope_check null: %d cases, harsh %s, all-C1-C4 %s -> %s" % (
        sn["cases"], sn["harsh_cases"], sn["all_present"], sn["null"]["verdict"]))
    L.append("  %s" % sn["null"]["reason"])
    ng = non_goal_scan()
    L.append("§6 non-goal scan: clean %s hits %s" % (ng["clean"], ng["hits"]))
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("v2_audit has no selftest; run selftest_v2.py", file=sys.stderr)
        sys.exit(2)
    print(render())
