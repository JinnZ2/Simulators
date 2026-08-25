#!/usr/bin/env python3
"""What can actually be run here, and what does running it need.

Written to answer two things at once.

THE QUESTION: are there tests that can be run? This walks the whole
tree, finds every module exposing `--selftest` and every `tests/`
directory, runs them, and reports what passed.

THE CLAIM UNDER TEST, relayed from another instance: that the numbers in
`CLAUDE.md` are unbacked because "the claim and the check live on
different machines" -- the sim ran on hardware that could run it, the
number was written down elsewhere, and the maintenance operation needs a
resource the author does not have.

That is measurable rather than arguable, and the measurement is the
import graph. A module whose imports are all in `sys.stdlib_module_names`
is checkable by anyone with a Python; one that needs numpy is not, on a
phone. So this reports, per module, the SMALLEST environment that can
run it, derived from its actual imports rather than from a declaration.

`sys.stdlib_module_names` exists from Python 3.10. Under 3.9 the tier is
reported UNKNOWN rather than guessed.

Everything runs in a throwaway git worktree, for the reason self-scan
SS_009 records: running a repository's own suites writes files, and a
census that dirties the tree is measuring something it changed.

CC0. stdlib only. Parses under Python 3.9.
"""

import ast
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import resolve  # noqa: E402  -- for parse_count and the worktree helper

TIMEOUT = 180

STDLIB = getattr(sys, "stdlib_module_names", None)

# Tiers, smallest first. A module's tier is the smallest one holding
# every third-party module it imports.
TIERS = (
    ("stdlib", frozenset()),
    ("stdlib+pytest", frozenset({"pytest"})),
    ("numeric", frozenset({"pytest", "numpy", "scipy", "jsonschema",
                           "psutil"})),
    ("numeric+plot", frozenset({"pytest", "numpy", "scipy", "jsonschema",
                                "psutil", "matplotlib", "sklearn",
                                "pandas", "seaborn", "IPython",
                                "ipywidgets", "sympy", "streamlit",
                                "requests", "openai", "sqlalchemy",
                                "fastapi", "pydantic", "rapidfuzz",
                                "geopandas", "pypdf", "psycopg2",
                                "uvicorn", "geoalchemy2", "torch"})),
)

SKIP_DIRS = {".git", "__pycache__", "legacy", "node_modules"}

# This module advertises `--selftest`, so it discovers itself, and the
# first version then RAN itself -- which runs itself. The census cannot
# census its own run. It stays in the inventory and in the tier count,
# where it is a real row, and is not executed; the state says so rather
# than the row disappearing.
#
# UNI_010's self-reference loop in a third form: not a scanner reading
# its own output, but a runner running itself. Found by it hanging.
SELF = os.path.join("self-scan", "census.py")
SELF_STATE = "EXCLUDED_SELF_REFERENCE"


def top_imports(path):
    """Top-level module names this file imports, from the AST.

    Static, so a conditional or guarded import counts. That is the right
    direction here: a module that imports numpy inside a try still needs
    numpy to exercise the branch, and the question is what an operator
    must install to check the claim, not what it takes to avoid a
    traceback.
    """
    try:
        tree = ast.parse(open(path, encoding="utf-8", errors="replace").read())
    except SyntaxError as exc:
        return None, "SyntaxError: %s" % exc
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level:            # relative import, inside the repo
                continue
            if node.module:
                names.add(node.module.split(".")[0])
    return names, None


def local_modules():
    """Every importable name that lives in this repository."""
    out = set()
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f.endswith(".py"):
                out.add(f[:-3])
        for d in dn:
            if os.path.exists(os.path.join(dp, d, "__init__.py")):
                out.add(d)
    return out


def tier_of(path, local):
    """(tier name, the third-party names that set it)."""
    names, err = top_imports(path)
    if names is None:
        return "UNPARSED", set(), err
    if STDLIB is None:
        return "UNKNOWN", set(), "sys.stdlib_module_names needs Python 3.10"
    third = {n for n in names
             if n not in STDLIB and n not in local and not n.startswith("_")}
    for name, allowed in TIERS:
        if third <= allowed:
            return name, third, None
    return "beyond", third, None


def selftest_modules():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in sorted(fn):
            if not f.endswith(".py"):
                continue
            p = os.path.join(dp, f)
            try:
                src = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            if "--selftest" not in src:
                continue
            rel = os.path.relpath(p, ROOT)
            # A file under tests/ belongs to the pytest arm. One of them
            # merely MENTIONS the flag in a docstring, and running it
            # with --selftest gets an argparse error that reads as a
            # failing selftest. Counting it in both arms would also
            # double-count its checks.
            if os.sep + "tests" + os.sep in os.sep + rel or \
               rel.startswith("tests" + os.sep):
                continue
            out.append(rel)
    return sorted(out)


def test_dirs():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for d in sorted(dn):
            if d == "tests":
                out.append(os.path.relpath(os.path.join(dp, d), ROOT))
    return sorted(out)


def run_selftest(rel, base):
    rc, out = resolve._run([sys.executable, os.path.join(base, rel),
                            "--selftest"])
    n, f = resolve.parse_count(out, None)
    if rc is None:
        return {"state": "TIMEOUT_OR_ERROR", "checks": None, "failed": None,
                "detail": out[:120]}
    if n is None:
        # No count this parser can extract. That is not the same as a
        # module that did not pass: several here print only
        # `SELFTEST PASS (0 checks failed)` and no per-check lines, so
        # the count is genuinely not in the output. Reporting those as
        # RAN_NO_COUNT beside a module that errored would put a green
        # module and a broken one in one bin, which is the mistake this
        # whole folder is about.
        clean = re.search(r"SELFTEST\s+PASS\b", out) or \
            re.search(r"\b0\s+failed\b", out)
        dirty = re.search(r"SELFTEST\s+FAIL\b", out) or \
            re.search(r"\b[1-9]\d*\s+failed\b", out)
        if rc == 0 and clean and not dirty:
            state = "GREEN_UNCOUNTED"
        elif dirty:
            state = "SOME_FAILED_UNCOUNTED"
        elif rc == 0:
            state = "RAN_NO_VERDICT"
        else:
            state = "NONZERO_EXIT_NO_VERDICT"
        return {"state": state, "checks": None, "failed": None,
                "detail": out.strip().split("\n")[-1][:120] if out else ""}
    return {"state": "GREEN" if not f else "SOME_FAILED",
            "checks": n, "failed": f, "detail": ""}


_SUM = re.compile(r"(?:(\d+) failed[, ]+)?(\d+) passed(?:[, ]+(\d+) skipped)?")


def run_pytest_dir(rel, base):
    rc, out = resolve._run([sys.executable, "-m", "pytest", "-q",
                            os.path.join(base, rel)])
    m = None
    for m in _SUM.finditer(out):
        pass
    if not m:
        last = [l for l in out.strip().split("\n") if l.strip()]
        return {"state": "NO_SUMMARY", "passed": None, "failed": None,
                "skipped": None, "detail": (last[-1] if last else "")[:120]}
    failed = int(m.group(1) or 0)
    passed = int(m.group(2))
    skipped = int(m.group(3) or 0)
    return {"state": "GREEN" if not failed else "SOME_FAILED",
            "passed": passed, "failed": failed, "skipped": skipped,
            "detail": ""}


def census(run=True):
    local = local_modules()
    mods = selftest_modules()
    dirs = test_dirs()
    rows = {"selftest": [], "pytest": []}
    with resolve._isolated() as wt:
        base = wt or ROOT
        # resolve._run resolves its cwd through resolve.base(), so the
        # worktree has to be published there as well as used for paths.
        # The first version passed the path and left the cwd at ROOT,
        # and one module wrote a denial record into the tree being
        # measured -- SS_009 recurring one module over, in the module
        # written to record SS_009.
        resolve.BASE = base
        for rel in mods:
            t, third, err = tier_of(os.path.join(ROOT, rel), local)
            r = {"path": rel, "tier": t, "needs": sorted(third),
                 "tier_error": err}
            if run:
                if rel == SELF:
                    r.update({"state": SELF_STATE, "checks": None,
                              "failed": None,
                              "detail": "a census cannot run its own run"})
                else:
                    r.update(run_selftest(rel, base))
            rows["selftest"].append(r)
        for rel in dirs:
            r = {"path": rel}
            if run:
                r.update(run_pytest_dir(rel, base))
            rows["pytest"].append(r)
        resolve.BASE = None
    return rows


def render(rows):
    out = []
    out.append("TEST CENSUS")
    out.append("what is here, whether it runs, and the smallest")
    out.append("environment that can run it")
    out.append("")

    st = rows["selftest"]
    out.append("MODULES EXPOSING --selftest: %d" % len(st))
    tiers = {}
    for r in st:
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
    for name, _ in TIERS:
        if name in tiers:
            out.append("  %-14s %3d" % (name, tiers[name]))
    for k in sorted(tiers):
        if k not in dict(TIERS):
            out.append("  %-14s %3d" % (k, tiers[k]))
    out.append("")

    states = {}
    checks = 0
    for r in st:
        states[r.get("state")] = states.get(r.get("state"), 0) + 1
        checks += r.get("checks") or 0
    out.append("  state:")
    for k in sorted(states, key=lambda x: (x is None, str(x))):
        out.append("    %-22s %3d" % (k, states[k]))
    out.append("  checks counted across all modules: %d" % checks)
    out.append("")

    # The measurement the relayed claim turns on.
    runnable = [r for r in st if r["tier"] == "stdlib"]
    green = [r for r in runnable
             if r.get("state") in ("GREEN", "GREEN_UNCOUNTED")]
    out.append("  STDLIB-ONLY REACH")
    out.append("    %d of %d modules import nothing outside the standard"
               % (len(runnable), len(st)))
    out.append("    library, and %d of those %d run green here."
               % (len(green), len(runnable)))
    out.append("    checks inside that boundary: %d, over the %d that"
               % (sum(r.get("checks") or 0 for r in green),
                  sum(1 for r in green if r.get("checks"))))
    out.append("    print a count. %d pass without printing one, so that"
               % sum(1 for r in green if not r.get("checks")))
    out.append("    total is a FLOOR and not the number of checks here.")
    out.append("")

    pt = rows["pytest"]
    out.append("TEST DIRECTORIES: %d" % len(pt))
    tp = tf = ts = 0
    for r in pt:
        out.append("  %-42s %-12s %s"
                   % (r["path"][:42], r.get("state"),
                      ("%s passed, %s failed, %s skipped"
                       % (r.get("passed"), r.get("failed"), r.get("skipped")))
                      if r.get("passed") is not None else r.get("detail", "")))
        tp += r.get("passed") or 0
        tf += r.get("failed") or 0
        ts += r.get("skipped") or 0
    out.append("  total: %d passed, %d failed, %d skipped" % (tp, tf, ts))
    out.append("")

    notgreen = [r for r in st if r.get("state")
                not in ("GREEN", "GREEN_UNCOUNTED")]
    out.append("NOT GREEN (%d modules)" % len(notgreen))
    for r in notgreen:
        if True:
            out.append("  %-52s %-22s %s"
                       % (r["path"][:52], r.get("state"),
                          (",".join(r["needs"]) or r.get("detail", ""))[:40]))
    return "\n".join(out)


# The one exemption, declared and measured rather than taken.
#
# The pytest arm relays the tool's OWN last line into the detail column
# when it prints no summary -- "5 errors in 0.66s". That word is
# pytest's, and rewording it would misquote the tool. Nothing else in
# the emitted report is exempt, and the selftest below runs the
# three-arm harness sheet-structure-scan SSS_049 kept for a real case:
# clean with the relay masked, the relay is the only thing that fires
# without the mask, and a planted violation is still caught.
RELAYED_PREFIX = "  "
RELAYED_MARK = "NO_SUMMARY"


def _mask_relayed(text):
    """Blank the detail column on rows carrying a tool's own output."""
    out = []
    for line in text.split("\n"):
        if RELAYED_MARK in line:
            out.append(line.split(RELAYED_MARK)[0] + RELAYED_MARK)
        else:
            out.append(line)
    return "\n".join(out)


def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    import tempfile
    tmp = tempfile.mkdtemp()

    p = os.path.join(tmp, "a.py")
    open(p, "w").write("import os, numpy\nfrom . import x\n"
                       "from collections import OrderedDict\n")
    names, err = top_imports(p)
    chk("top_imports finds absolute imports", names == {"os", "numpy",
                                                        "collections"})
    chk("top_imports skips relative imports", "x" not in names)
    chk("top_imports reports no error on valid source", err is None)

    p2 = os.path.join(tmp, "b.py")
    open(p2, "w").write("def f(:\n")
    n2, e2 = top_imports(p2)
    chk("unparseable source returns None and a reason",
        n2 is None and "SyntaxError" in e2)

    local = {"resolve", "extract"}
    if STDLIB:
        p3 = os.path.join(tmp, "c.py")
        open(p3, "w").write("import os, json\nimport resolve\n")
        t, third, _ = tier_of(p3, local)
        chk("a stdlib-plus-local module is tier stdlib",
            t == "stdlib" and not third)
        p4 = os.path.join(tmp, "d.py")
        open(p4, "w").write("import numpy\n")
        t4, third4, _ = tier_of(p4, local)
        chk("numpy lands above stdlib+pytest", t4 == "numeric")
        chk("the setting import is named", third4 == {"numpy"})
        p5 = os.path.join(tmp, "e.py")
        open(p5, "w").write("import zzq_unknown_pkg\n")
        t5, _t, _ = tier_of(p5, local)
        chk("an unrecognised third-party import is `beyond`", t5 == "beyond")
        p6 = os.path.join(tmp, "f.py")
        open(p6, "w").write("try:\n    import numpy\nexcept ImportError:\n"
                            "    numpy = None\n")
        t6, _t6, _ = tier_of(p6, local)
        chk("a guarded import still sets the tier", t6 == "numeric")
    else:
        chk("tier is UNKNOWN without stdlib_module_names",
            tier_of(p, local)[0] == "UNKNOWN")

    # -- discovery finds this file's own siblings
    mods = selftest_modules()
    chk("discovery finds this module", "self-scan/census.py" in mods)
    chk("discovery finds a module in another folder",
        any(m.startswith("uninstrumented/") for m in mods))
    chk("discovery skips legacy/", not any(m.startswith("legacy/")
                                           for m in mods))
    dirs = test_dirs()
    chk("test dirs include the repo suite", "tests" in dirs)
    chk("test dirs include a folder suite", "reasoning-gate/tests" in dirs)

    # -- self-reference: discovered, counted, never executed
    chk("this module discovers itself", SELF in mods)
    rows = census(run=False)
    chk("a tier-only census does not execute anything",
        all("state" not in r for r in rows["selftest"]))
    chk("BASE is released after a census", resolve.BASE is None)
    rc0, before = resolve._run(["git", "status", "--porcelain"])
    census(run=False)
    rc1, after = resolve._run(["git", "status", "--porcelain"])
    chk("a census leaves the working tree unchanged", before == after)
    r = run_selftest("self-scan/extract.py", ROOT)
    chk("a sibling module's selftest runs and is counted",
        r["state"] == "GREEN" and r["checks"] > 10)
    chk("a module printing only a PASS line is GREEN_UNCOUNTED",
        run_selftest("shape-spec-audit/shadow_read.py", ROOT)["state"]
        == "GREEN_UNCOUNTED")
    chk("files under tests/ are not in the selftest arm",
        not any(m.startswith("tests" + os.sep) for m in mods))
    chk("a folder's tests/ is not in the selftest arm either",
        not any(os.sep + "tests" + os.sep in m for m in mods))

    # -- the no-severity constraint, three arms
    sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
    import no_severity
    sample = os.path.join(HERE, "samples", "census.sample.txt")
    if os.path.exists(sample):
        raw = open(sample, encoding="utf-8").read()
        chk("the report is clean once relayed tool output is masked",
            not no_severity.hits(_mask_relayed(raw)))
        unmasked = no_severity.hits(raw)
        chk("the relayed tool line is the only thing that fires",
            all(RELAYED_MARK in h[2] for h in unmasked))
        planted = _mask_relayed(raw) + "\nthis module is broken\n"
        chk("a planted violation is still caught",
            bool(no_severity.hits(planted)))

    # -- render never divides
    txt = render({"selftest": [], "pytest": []})
    chk("render survives an empty census", "TEST CENSUS" in txt)
    chk("render states the stdlib reach even at zero",
        "STDLIB-ONLY REACH" in txt)

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    print(render(census(run="--tiers-only" not in argv)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
