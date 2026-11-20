#!/usr/bin/env python3
"""DRAFT. Build MULTI_HOME_REGISTER.json: the concept map's denominator.

Scope (from the root CLAUDE.md index line for CONCEPT_MAP.md): "one block per concept
that has more than one home across repos (Simulators, study-aperture, TAF)".

    CONCEPT_MAP_REPOS=<dir holding study-aperture/ and thermodynamic-accountability-framework/> \
        python3 build_multi_home_register.py            write the JSON
    ... python3 build_multi_home_register.py --check    rebuild and compare, write nothing

Sources, each named per row:
  S1 TOOL_FINDER/entries.py NAME_COLLISIONS, scope filter applied (both sides in the 3 repos,
     and the same concept on both sides; the filter decision is a reading, recorded per row)
  S2 playground-crossrun/adapters/concept_map.py ROWS with a location on both sides (18)
  S3 grep: top-level names and .py basenames shared across the 3 repos, each pair read by hand;
     same-name-different-concept pairs are listed under considered_not_included
  S4 concept_map.json rows whose locations span 2+ of the 3 repos

A home is repo:path@commit (12 hex: the last commit touching the path, as of HEAD for
Simulators and origin/main for the others) plus the blob id when the path is a file. Every home is
resolved with git at that commit; one that does not resolve makes the build refuse.
in_map_by_path is mechanical (a concept_map.json location has the same repo and path).
in_map, from 2026-11-20, is the strict mechanical rule: YES = one map row names the concept (in
its "concept" or its "covers" list) AND lists every registered home (repo + path); PARTIAL = a
row names it or lists a home, but no single row does both in full; NO = neither. Until
2026-11-20 in_map was a reading at grain by this session (L0); that reading is kept per row as
in_map_L0_2026-11-20. The "covers" lists in concept_map.json are the judgment now: who = this
session, written after REVIEW-2 (GPT-6, L2, studies/review/REVIEW2_in_map_GPT6_2026-11-20.md).
No code is moved. Stdlib only.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "MULTI_HOME_REGISTER.json")
REPOS = ("Simulators", "study-aperture", "thermodynamic-accountability-framework")
SA_PKG = "experimental/playground/"
RP_PKG = "relational-playground/playground/"
JUDGE = {"who": "Claude Code session (same session that built the register)", "level": "L0",
         "note": "in_map is mechanical (strict rule) from 2026-11-20; the judgment sits in the map's covers "
                 "lists, written by this session after REVIEW-2 at L2 (GPT-6, 2026-11-20); "
                 "was until 2026-11-20: self-reading; not independent; a REVIEW-2 at L2+ is the next stage"}


def repo_dir(r):
    if r == "Simulators":
        return HERE
    for root in [os.environ.get("CONCEPT_MAP_REPOS"), os.path.join(HERE, ".."), os.path.join(HERE, "..", "jinnz2")]:
        if root and os.path.isdir(os.path.join(root, r, ".git")):
            return os.path.join(root, r)
    return None


def git(d, *a):
    p = subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


SHAS = {}


def is_shallow(d):
    """True / False from git; None when git gives neither (read as not known, and refused)."""
    rc, out = git(d, "rev-parse", "--is-shallow-repository")
    return {"true": True, "false": False}.get(out) if rc == 0 else None


def refuse_shallow(r, d):
    # A home is pinned at the last commit touching its path. In a shallow checkout that commit
    # is the shallow boundary for every path older than the boundary, so the pin is wrong and
    # nothing in the output shows it (found 2026-11-20: study-aperture homes all read c26fbd2).
    sh = is_shallow(d)
    if sh is not False:
        sys.exit("REFUSED: %s checkout at %s is %s; homes cannot be pinned (git fetch --unshallow)"
                 % (r, d, "shallow" if sh else "of unknown depth"))


def sha(r):
    if r not in SHAS:
        d = repo_dir(r)
        if d is None:
            sys.exit("REFUSED: no checkout of %s (set CONCEPT_MAP_REPOS)" % r)
        refuse_shallow(r, d)
        rc, s = git(d, "rev-parse", "HEAD" if r == "Simulators" else "origin/main")
        SHAS[r] = s
    return SHAS[r]


def home(r, path, token=None):
    d = repo_dir(r)
    # last commit that touched the path: stable across unrelated commits
    c = git(d, "log", "-1", "--format=%H", sha(r), "--", path.rstrip("/"))[1] or sha(r)
    rc, kind = git(d, "cat-file", "-t", "%s:%s" % (c, path.rstrip("/")))
    if rc:
        raise SystemExit("REFUSED: %s:%s does not resolve at %s" % (r, path, c[:12]))
    h = {"repo": r, "path": path, "commit": c[:12], "kind": kind}
    if kind == "blob":
        h["blob"] = git(d, "rev-parse", "%s:%s" % (c, path))[1][:12]
        if token:
            text = git(d, "show", "%s:%s" % (c, path))[1]
            h["token"] = token
            h["token_found"] = token in text
    h["ref"] = "%s:%s@%s" % (r, path, c[:12])
    return h


def map_paths():
    d = json.load(open(os.path.join(HERE, "concept_map.json"), encoding="utf-8"))
    out = {}
    for row in d["rows"]:
        for l in row["locations"]:
            out.setdefault((l["repo"], l["path"].rstrip("/")), []).append(row["concept"])
    return d, out


def by_path(homes, mp):
    hits = sorted({c for h in homes for c in mp.get((h["repo"], h["path"].rstrip("/")), [])})
    return ("YES" if hits else "NO"), hits


def strict_in_map(concept, homes, data):
    """YES = one map row names the concept (concept or covers) and lists every home."""
    want = {(h["repo"], h["path"].rstrip("/")) for h in homes}
    named, part = [], []
    for mr in data["rows"]:
        names = mr["concept"] == concept or concept in mr.get("covers", [])
        have = {(l["repo"], l["path"].rstrip("/")) for l in mr["locations"]}
        if names and want <= have:
            return "YES", "%s (named in %s; %d of %d homes listed)" % (
                mr["concept"], "concept" if mr["concept"] == concept else "covers", len(want), len(want))
        if names:
            named.append("%s names it, lists %d of %d homes" % (mr["concept"], len(want & have), len(want)))
        elif want & have:
            part.append("%s lists %d of %d homes, does not name it" % (mr["concept"], len(want & have), len(want)))
    if named or part:
        return "PARTIAL", "; ".join(named + part)
    return "NO", "no map row names it or lists a home"


def split_loc(s):
    """'file.py :: token (note)' -> (file, token). VOID handled by the caller."""
    f, _, tok = s.partition("::")
    tok = tok.strip()
    for cut in (" (", " --"):
        if cut in tok:
            tok = tok.split(cut)[0]
    return f.strip(), tok.strip() or None


# ---- in_map readings (L0) for S2 rows; key = crossrun concept
# From 2026-11-20 these no longer set in_map (strict rule, see strict_in_map); they are emitted
# unchanged as in_map_L0_2026-11-20 so the earlier reading stays on the record.
S2_IN_MAP = {
    "boundary closure gate before any physics": ("YES", "L0 gate (budget closure)"),
    "noise band on a misclosure": ("PARTIAL", "same files as the L0 gate row; the tolerance itself is not named in the map"),
    "known-answer validation": ("YES", "known-answer / null harness"),
    "planted defects on the lab itself": ("PARTIAL", "the map row names the harness, not the planted-defect set"),
    "null harness": ("YES", "known-answer / null harness"),
    "zero cases is not a pass": ("PARTIAL", "a rule inside the known-answer files; not a map row"),
    "non-detection as bounded null": ("YES", "scoped absence (ABSENT_AT_SENSITIVITY)"),
    "UNKNOWN carries what would end it": ("YES", "UNKNOWN expiry"),
    "frozen anchor": ("YES", "anchor / return"),
    "return test (asserted return + tolerance)": ("YES", "anchor / return"),
    "system continuity vs configuration continuity": ("YES", "system continuity vs configuration continuity"),  # was ("NO", "") until 2026-11-20: map row of the same name added
    "observer declared before comparison": ("YES", "observer declared before comparison"),  # was ("NO", "") until 2026-11-20: map row of the same name added
    "observer regime partition (names differ: PASSIVE vs REACTIVITY; not merged)": ("YES", "observer regime partition (names differ: PASSIVE vs REACTIVITY; not merged)"),  # was ("NO", "") until 2026-11-20: map row of the same name added
    "no universal ranking": ("YES", "no universal ranking"),  # was ("NO", "") until 2026-11-20: map row of the same name added
    "applicability / domain of validity": ("YES", "applicability / domain of validity"),  # was ("NO", "") until 2026-11-20: map row of the same name added
    "percolation family": ("YES", "percolation"),
    "branching family": ("YES", "branching"),
    "value / condition basis vocabulary": ("YES", "value / condition basis vocabulary"),  # was ("NO", "") until 2026-11-20: map row of the same name added
}


def build():
    data, mp = map_paths()
    rows = []
    # S1
    rows.append({"concept": "stated_purpose / scope_valid (law purpose and scope against first principle intent)",
                 "homes": [home("Simulators", "law-audit-card/card.py"),
                           home("thermodynamic-accountability-framework", "core/regulatory_scope_audit.py")],
                 "source": "S1 TOOL_FINDER/entries.py NAME_COLLISIONS (\"same concept, two names\")",
                 "grain_note": "one concept, two names; law-audit-card imports the TAF module rather than reimplementing (entries.py note, 2026-11-10)"})
    # S2
    sys.path.insert(0, os.path.join(HERE, "playground-crossrun", "adapters"))
    import concept_map as CR  # noqa: E402
    for concept, sa, rp in CR.ROWS:
        if sa.startswith("VOID") or rp.startswith("VOID"):
            continue
        (fa, ta), (fr, tr) = split_loc(sa), split_loc(rp)
        rows.append({"concept": concept,
                     "homes": [home("study-aperture", SA_PKG + fa, ta), home("Simulators", RP_PKG + fr, tr)],
                     "source": "S2 playground-crossrun/adapters/concept_map.py ROWS (location on both sides)",
                     "grain_note": "crossrun grain is finer than map rows: one map row can cover several of these; "
                                   "combined-playground/cplay/ may carry a third Simulators copy, not checked per row"})
    # S3
    rows.append({"concept": "READING_PROTOCOL (how a folder is to be read)",
                 "homes": [home("Simulators", "READING_PROTOCOL.md"), home("study-aperture", "READING_PROTOCOL.md"),
                           home("thermodynamic-accountability-framework", "READING_PROTOCOL.md")],
                 "source": "S3 grep: top-level name shared by all three repos",
                 "grain_note": "study-aperture and TAF copies have the same blob; the Simulators copy differs"})
    rows.append({"concept": "driver-hours evidence register",
                 "homes": [home("Simulators", "automation-gap/driver_hours_evidence_register.py"),
                           home("thermodynamic-accountability-framework", "labor_thermodynamics/driver_hours_evidence_register.py")],
                 "source": "S3 grep: .py basename shared Simulators/TAF; same header, different blobs",
                 "grain_note": "one file in two places, drifted (diff 88 lines at these commits)"})
    for b in ("conditional_claims.py", "false_agree.py", "provenance_graph.py"):
        rows.append({"concept": "%s (vendored tool)" % b[:-3],
                     "homes": [home("Simulators", "tools/" + b), home("study-aperture", "vendored/" + b)],
                     "source": "S3 grep: .py basename shared Simulators/study-aperture; same blob",
                     "grain_note": "a vendored copy: same bytes today, can drift; whether a vendored copy is a home is a reading"})
    rows.append({"concept": "measurand declaration (measurand vs indication / declared identity)",
                 "homes": [home("Simulators", "instrument-epistemology/src/instrum/measurand.py"),
                           home("study-aperture", SA_PKG + "equations/measurand.py")],
                 "source": "S3 grep: .py basename shared Simulators/study-aperture; headers read",
                 "grain_note": "CANDIDATE match only: decomposition (instrument-epistemology) vs declared identity "
                               "on linked runs (playground); same word, possibly two concepts. "
                               "2026-11-20: possible two concepts (REVIEW-2); not split"})
    rows.append({"concept": "thermodynamic audit inside an economic sim",
                 "homes": [home("Simulators", "earth_economics/earth_economic_sim.py"),
                           home("thermodynamic-accountability-framework", "calibration/unified_audit.py")],
                 "source": "S3 grep: earth_economic_sim.py names TAF ('In reality, this would import modules from TAF')",
                 "grain_note": "CANDIDATE: a stand-in in Simulators for TAF's auditor; the TAF path is the nearest "
                               "auditor module read, not a declared counterpart"})
    # S4: map rows spanning 2+ repos, not already present by path
    seen = {(h["repo"], h["path"].rstrip("/")) for r in rows for h in r["homes"]}
    for mr in data["rows"]:
        reps = {l["repo"] for l in mr["locations"]} & set(REPOS)
        if len(reps) < 2:
            continue
        if any((l["repo"], l["path"].rstrip("/")) in seen for l in mr["locations"]):
            continue
        hs = []
        for l in mr["locations"]:
            if l["repo"] in REPOS and l.get("ref") in (None, "origin/main"):
                hs.append(home(l["repo"], l["path"]))
        rows.append({"concept": mr["concept"], "homes": hs,
                     "source": "S4 concept_map.json row spanning %d repos" % len(reps),
                     "grain_note": "taken from the map itself"})
    for r in rows:
        r["in_map_by_path"], r["map_rows_by_path"] = by_path(r["homes"], mp)
        if r["source"].startswith("S4"):
            l0 = ("YES", r["concept"])
        elif r["concept"] in S2_IN_MAP:
            l0 = S2_IN_MAP[r["concept"]]
        else:
            l0 = (("YES" if r["in_map_by_path"] == "YES" else "NO"), "by path; no other map row read as covering it")
        r["in_map"], r["in_map_basis"] = strict_in_map(r["concept"], r["homes"], data)
        r["in_map_rule"] = "strict: a row names the concept in concept or covers AND lists every home"
        r["in_map_L0_2026-11-20"] = {"in_map": l0[0], "basis": l0[1], "note": "builder reading before the strict rule"}
        r["grain_judgment"] = JUDGE
    considered = [
        {"name": "institutional_audit.py", "homes": ["Simulators:fragility-cascade/", "TAF:metrology/"],
         "why_not": "same name, different concepts (refutation verdicts vs premise-set audit), headers read"},
        {"name": "ablation.py", "homes": ["Simulators:forest-model-ledger/ledger/toolkit/", "Simulators:relational-playground/playground/analysis/", "TAF:judgment_registry/"],
         "why_not": "TAF copy is label ablation, a different concept; the two Simulators copies are one repo"},
        {"name": "sensitivity.py", "homes": ["Simulators:relational-playground/playground/experiments/", "study-aperture:experimental/playground/detection/"],
         "why_not": "parameter sensitivity vs instrument detection limit; different concepts"},
        {"name": "expiry_register.py, unified_audit.py (blind-reader-void12 packet sources)", "homes": ["Simulators:blind-reader-void12/.../sources/", "TAF:calibration/"],
         "why_not": "frozen specimen copies inside a study packet, not homes"},
        {"name": "TOOL_FINDER NAME_COLLISIONS, other 10", "homes": ["see TOOL_FINDER/entries.py"],
         "why_not": "one repo only, outside the 3 repos, or different concepts under one name (filter applied per row, L0)"},
        {"name": "coincidence card (map row)", "homes": ["Simulators only"],
         "why_not": "three homes, all in Simulators: multi-home, not across repos"},
    ]
    counts = {"rows": len(rows), "in_map YES": sum(r["in_map"] == "YES" for r in rows),
              "in_map PARTIAL": sum(r["in_map"] == "PARTIAL" for r in rows),
              "in_map NO": sum(r["in_map"] == "NO" for r in rows),
              "in_map_by_path YES": sum(r["in_map_by_path"] == "YES" for r in rows),
              "tokens not found": sum(1 for r in rows for h in r["homes"] if h.get("token_found") is False)}
    return {"status": "DRAFT", "as_of": "2026-11-20", "built_by": "build_multi_home_register.py",
            "scope": "concepts with more than one home across Simulators / study-aperture / thermodynamic-accountability-framework",
            "read_at": {r: ("HEAD" if r == "Simulators" else "origin/main@" + sha(r)[:12]) for r in REPOS},
            "denominator_note": "rows is a lower bound from four named sources, not an enumeration; "
                                "grep covered top-level names and .py basenames only",
            "counts": counts, "rows": rows, "considered_not_included": considered}


def selftest():
    """Builds a two-commit repo and a depth-1 clone of it in a temp dir; the builder must refuse
    the clone and accept the full repo. Touches no sibling."""
    import shutil
    import tempfile
    t = tempfile.mkdtemp()
    fails = 0
    try:
        full = os.path.join(t, "full")
        os.mkdir(full)
        ident = ["-c", "user.name=selftest", "-c", "user.email=selftest@example.invalid"]
        subprocess.run(["git", "-C", full, "init", "-q"], check=True)
        for n in ("1", "2"):
            open(os.path.join(full, "f"), "w").write(n)
            subprocess.run(["git", "-C", full, "add", "f"], check=True)
            subprocess.run(["git", "-C", full] + ident + ["commit", "-q", "-m", n], check=True)
        clone = os.path.join(t, "clone")
        subprocess.run(["git", "clone", "-q", "--depth", "1", "file://" + full, clone], check=True)

        def refused(d):
            try:
                refuse_shallow("x", d)
            except SystemExit as e:
                return str(e)
            return None
        checks = [
            ("full repo reads not shallow", is_shallow(full) is False),
            ("depth-1 clone reads shallow", is_shallow(clone) is True),
            ("not a repo reads unknown", is_shallow(t) is None),
            ("full repo is accepted", refused(full) is None),
            ("depth-1 clone is refused", (refused(clone) or "").startswith("REFUSED") and "shallow" in refused(clone)),
            ("unknown depth is refused", (refused(t) or "").startswith("REFUSED")),
        ]
        for name, ok in checks:
            print("%s  %s" % ("ok  " if ok else "FAIL", name))
            fails += 0 if ok else 1
    finally:
        shutil.rmtree(t, ignore_errors=True)
    print("checks: %d   failed: %d" % (len(checks), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    reg = build()
    text = json.dumps(reg, indent=1, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        same = os.path.exists(OUT) and open(OUT, encoding="utf-8").read() == text
        print("MULTI_HOME_REGISTER.json", "identical" if same else "DIFFERS")
        sys.exit(0 if same else 1)
    open(OUT, "w", encoding="utf-8").write(text)
    print("wrote MULTI_HOME_REGISTER.json:", json.dumps(reg["counts"]))
