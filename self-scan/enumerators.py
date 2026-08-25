#!/usr/bin/env python3
"""Handoff item 1 -- is self-enumeration one defect or two?

The hypothesis, relayed: `census.py` hung on itself AND wrote into the
tree it measured, and anything enumerating the tree it runs in has both
by construction, because the exclusion and the isolation are one
problem.

That is a structural claim about a population, so it is tested against
the population rather than argued. Two properties per module, both
measured by running it, neither inferred from source:

  ENUMERATES_SELF   the module's own file falls inside a directory it
                    actually walked, globbed or listed at run time
  WRITES_INTO_TREE  running it changes the working tree

Measurement, not static analysis. `os.walk` is traced by wrapping it in
a `sitecustomize` on the child's path, so what is recorded is the roots
the module really visited, not the ones a reader would guess from a
literal. A module whose root is a variable, or is joined at run time,
or is passed in, is measured the same way as one with a hard-coded
path.

Both arms run in a throwaway worktree, for the reason SS_009 records.
The write arm needs that isolation to be safe; the read arm needs it so
the two arms see the same tree.

CC0. stdlib only. Parses under Python 3.9.
"""

import ast
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import resolve  # noqa: E402

SKIP_DIRS = {".git", "__pycache__", "legacy", "node_modules"}
WALKERS = {"walk", "glob", "iglob", "listdir", "scandir"}

# `census.py` cannot run itself (SS_017) and neither can this module run
# itself under a tracer that would then trace the tracing. Both are in
# the inventory and neither is executed; the state says so.
NO_RUN = {
    os.path.join("self-scan", "census.py"):
        "SS_017 -- a census cannot run its own run",
    os.path.join("self-scan", "enumerators.py"):
        "this module enumerates enumerators, so it is one",
}

# `--selftest` is the entry point every module here exposes, and for
# several it does NOT reach the enumeration -- which is the whole
# behaviour under test. Where a module has a real enumerating
# invocation it is DECLARED here, never guessed, and a module whose
# selftest reaches nothing is retried with no arguments before it is
# recorded as not enumerating at run time.
INVOCATIONS = {
    # Found by running them, not by reading the usage line: `scan.py`
    # with no argument prints usage and exits 0 without walking, and
    # `mine_logs.py .` raises FileNotFoundError before its glob because
    # the guards path defaults relative to the cwd.
    os.path.join("uninstrumented", "scan.py"): ["."],
    os.path.join("reasoning-gate", "mine_logs.py"):
        ["reasoning-gate", "reasoning-gate/guards.json"],
    os.path.join("inverseminar", "inverseminar.py"): ["triage"],
    os.path.join("uninstrumented", "scan_audit.py"): [],
}

TRACER = '''
import atexit, json, os, glob
_LOG = os.environ.get("ENUM_TRACE")
_seen = []
_walk, _listdir, _glob, _iglob = os.walk, os.listdir, glob.glob, glob.iglob


def _rec(kind, p):
    try:
        _seen.append([kind, os.path.abspath(p)])
    except Exception:
        pass


def walk(top, *a, **k):
    _rec("walk", top)
    return _walk(top, *a, **k)


def listdir(path="."):
    _rec("listdir", path)
    return _listdir(path)


def _g(pat, *a, **k):
    _rec("glob", pat)
    return _glob(pat, *a, **k)


def _ig(pat, *a, **k):
    _rec("glob", pat)
    return _iglob(pat, *a, **k)


os.walk, os.listdir, glob.glob, glob.iglob = walk, listdir, _g, _ig


@atexit.register
def _dump():
    if _LOG:
        try:
            open(_LOG, "w").write(json.dumps(_seen))
        except Exception:
            pass
'''


def enumerators():
    """Modules that call a directory-enumeration primitive."""
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in sorted(fn):
            if not f.endswith(".py"):
                continue
            p = os.path.join(dp, f)
            try:
                tree = ast.parse(open(p, encoding="utf-8",
                                      errors="replace").read())
            except SyntaxError:
                continue
            calls = set()
            for n in ast.walk(tree):
                if isinstance(n, ast.Call):
                    name = (getattr(n.func, "attr", None)
                            or getattr(n.func, "id", None))
                    if name in WALKERS:
                        calls.add(name)
            if calls:
                out.append((os.path.relpath(p, ROOT), sorted(calls)))
    return sorted(out)


def executes(path):
    """Does this module RUN other code, or open a file for writing?

    The replacement predictor. `census.py` had both defects, and the
    reason was not that it enumerated -- it was that it EXECUTED what it
    enumerated, and the writes were the children's. Reading a tree
    cannot dirty it; running what is in the tree can.

    Static, on the AST, because the alternative is running each module
    twice with a different question and this one is decidable from the
    source: a subprocess call, an exec, or an open in a write mode.
    """
    try:
        tree = ast.parse(open(path, encoding="utf-8",
                              errors="replace").read())
    except SyntaxError:
        return None, []
    why = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            name = getattr(n.func, "attr", None) or getattr(n.func, "id",
                                                            None)
            if name in ("run", "Popen", "call", "check_output",
                        "check_call") and isinstance(n.func, ast.Attribute):
                base = getattr(n.func.value, "id", "")
                if base in ("subprocess", "sp"):
                    why.add("subprocess." + name)
            if name in ("system", "execv", "execl", "fork", "spawnv"):
                why.add("os." + name)
            if name in ("exec", "eval", "compile"):
                why.add(name)
            if name == "open":
                for a in list(n.args[1:]) + [k.value for k in n.keywords
                                             if k.arg == "mode"]:
                    if isinstance(a, ast.Constant) and \
                            isinstance(a.value, str) and \
                            any(m in a.value for m in ("w", "a", "x")):
                        why.add("open(mode=%r)" % a.value)
            if name in ("makedirs", "mkdir", "mkstemp", "mkdtemp"):
                why.add("os." + name)
    return bool(why), sorted(why)


def _inside(root, path):
    """Is `path` inside `root`, or is `root` the directory holding it?"""
    root = os.path.abspath(root)
    path = os.path.abspath(path)
    if os.path.isdir(root):
        return path.startswith(root.rstrip(os.sep) + os.sep)
    # a glob pattern: compare the directory part
    d = os.path.dirname(root)
    return os.path.dirname(path) == d or (
        d and path.startswith(d.rstrip(os.sep) + os.sep))


def measure(rel, base, args):
    """(enumerates_self, writes, roots, note) for one module."""
    trace_dir = tempfile.mkdtemp(prefix="enum_")
    open(os.path.join(trace_dir, "sitecustomize.py"), "w").write(TRACER)
    log = os.path.join(trace_dir, "trace.json")

    env_pp = trace_dir
    old = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = (env_pp + os.pathsep + old) if old else env_pp
    os.environ["ENUM_TRACE"] = log
    try:
        rc0, before = resolve._run(["git", "status", "--porcelain"], cwd=base)
        rc, out = resolve._run([sys.executable,
                                os.path.join(base, rel)] + args, cwd=base)
        rc1, after = resolve._run(["git", "status", "--porcelain"], cwd=base)
    finally:
        if old is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = old
        os.environ.pop("ENUM_TRACE", None)

    roots = []
    if os.path.exists(log):
        try:
            roots = json.load(open(log))
        except ValueError:
            roots = []

    own = os.path.join(base, rel)
    self_seen = any(_inside(r, own) for _k, r in roots)
    note = ""
    if rc is None:
        note = "did not complete: " + out[:70]
    elif not roots:
        note = "no enumeration reached at run time"
    return {
        "enumerates_self": self_seen,
        "writes": before != after,
        "roots": len(roots),
        "distinct_roots": len({r for _k, r in roots}),
        "wrote": sorted(set(after.split("\n")) - set(before.split("\n")))[:4],
        "rc": rc,
        "note": note,
    }


def run(limit=None):
    rows = []
    with resolve._isolated() as wt:
        base = wt or ROOT
        resolve.BASE = base
        try:
            for rel, calls in enumerators()[:limit]:
                ex, why = executes(os.path.join(ROOT, rel))
                r = {"path": rel, "calls": calls, "executes": ex,
                     "executes_why": why}
                if rel in NO_RUN:
                    r.update({"state": "NOT_RUN", "reason": NO_RUN[rel],
                              "enumerates_self": None, "writes": None,
                              "roots": None, "note": NO_RUN[rel]})
                else:
                    # --selftest first: it is the entry point every module
                    # here exposes, and it exercises the enumeration
                    # without asking the module to do its real job.
                    src = open(os.path.join(ROOT, rel), encoding="utf-8",
                               errors="replace").read()
                    if rel in INVOCATIONS:
                        args = INVOCATIONS[rel]
                    else:
                        args = ["--selftest"] if "--selftest" in src else []
                    m = measure(rel, base, args)
                    # A selftest that reached no enumeration has not
                    # exercised the property under test. Retry with the
                    # bare invocation before recording a zero.
                    if not m["roots"] and args:
                        m2 = measure(rel, base, [])
                        if m2["roots"]:
                            m, args = m2, []
                    r.update(m)
                    r["state"] = "RUN"
                    r["args"] = args
                rows.append(r)
        finally:
            resolve.BASE = None
    return rows


def table(rows, key="enumerates_self"):
    """A 2x2 of `key` against observed writing."""
    cells = {(True, True): 0, (True, False): 0,
             (False, True): 0, (False, False): 0}
    for r in rows:
        if r.get("state") != "RUN" or r.get("enumerates_self") is None:
            continue
        cells[(bool(r.get(key)), bool(r["writes"]))] += 1
    return cells


def association(c):
    """(n_yes, rate_yes, n_no, rate_no) -- None where a group is empty."""
    y = c[(True, True)] + c[(True, False)]
    n = c[(False, True)] + c[(False, False)]
    return (y, (c[(True, True)] / float(y)) if y else None,
            n, (c[(False, True)] / float(n)) if n else None)


def render(rows):
    out = []
    out.append("ENUMERATORS -- self-inclusion against tree-writing")
    out.append("")
    out.append("Hypothesis under test: a module that enumerates the tree")
    out.append("it runs in BOTH includes itself in what it enumerates AND")
    out.append("changes that tree by running -- the two being one thing.")
    out.append("That predicts a diagonal 2x2: both or neither.")
    out.append("")
    out.append("%-52s %-6s %-6s %-7s %s"
               % ("module", "self", "writes", "roots", "note"))
    out.append("-" * 104)
    for r in rows:
        if r.get("state") == "NOT_RUN":
            out.append("%-52s %-6s %-6s %-7s %s"
                       % (r.get("path", "?")[:52], "-", "-", "-",
                          "NOT RUN: " + r["reason"][:38]))
            continue
        out.append("%-52s %-6s %-6s %-7s %s"
                   % (r.get("path", "?")[:52],
                      "yes" if r["enumerates_self"] else "no",
                      "yes" if r["writes"] else "no",
                      r.get("distinct_roots", "-"),
                      (", ".join(r.get("wrote", []))[:34] if r["writes"]
                       else r.get("note", "")[:34])))
    out.append("")
    c = table(rows)
    n = sum(c.values())
    out.append("2x2 over %d modules that ran" % n)
    out.append("                       writes: yes   writes: no")
    out.append("  enumerates self yes  %11d   %10d"
               % (c[(True, True)], c[(True, False)]))
    out.append("  enumerates self no   %11d   %10d"
               % (c[(False, True)], c[(False, False)]))
    out.append("")
    if not n:
        out.append("  NOT ADDRESSABLE -- no module ran")
        return "\n".join(out)

    # Diagonal share is the wrong statistic when a margin is skewed: if
    # almost nothing writes, the diagonal is whatever the self column
    # happens to be, and reads high for a reason that has nothing to do
    # with the hypothesis. The hypothesis is about ASSOCIATION, so the
    # readout is the write rate WITHIN each self group.
    self_yes = c[(True, True)] + c[(True, False)]
    self_no = c[(False, True)] + c[(False, False)]
    w_yes = (c[(True, True)] / float(self_yes)) if self_yes else None
    w_no = (c[(False, True)] / float(self_no)) if self_no else None
    diag = c[(True, True)] + c[(False, False)]
    out.append("  diagonal share: %d of %d (%.0f%%) -- NOT the test."
               % (diag, n, 100.0 * diag / n))
    out.append("")
    out.append("  ASSOCIATION, which is the test:")
    out.append("    of %d that enumerate themselves, %d write  (%s)"
               % (self_yes, c[(True, True)],
                  "%.0f%%" % (100 * w_yes) if w_yes is not None else "--"))
    out.append("    of %d that do not,             %d write  (%s)"
               % (self_no, c[(False, True)],
                  "%.0f%%" % (100 * w_no) if w_no is not None else "--"))
    if w_yes is None or w_no is None:
        out.append("    NOT ADDRESSABLE -- one group is empty.")
    else:
        out.append("    difference: %+.0f points" % (100 * (w_yes - w_no)))
    total_w = c[(True, True)] + c[(False, True)]
    out.append("")
    out.append("  %d of %d modules write at all. A margin this thin bounds"
               % (total_w, n))
    out.append("  what any association here can show, and the bound is")
    out.append("  stated rather than left for the reader to notice.")

    # The replacement predictor.
    c2 = table(rows, "executes")
    ey, ry, en, rn = association(c2)
    out.append("")
    out.append("ALTERNATIVE PREDICTOR -- does the module RUN what it finds")
    out.append("")
    out.append("  census.py did both, and enumeration was not why.")
    out.append("  Reading a tree cannot change it; running what is in the")
    out.append("  tree can, and its writes were its children's. So the")
    out.append("  same 2x2 against `executes`:")
    out.append("")
    out.append("                       writes: yes   writes: no")
    out.append("  executes yes         %11d   %10d"
               % (c2[(True, True)], c2[(True, False)]))
    out.append("  executes no          %11d   %10d"
               % (c2[(False, True)], c2[(False, False)]))
    out.append("")
    out.append("    of %d that execute or write by design, %d write  (%s)"
               % (ey, c2[(True, True)],
                  "%.0f%%" % (100 * ry) if ry is not None else "--"))
    out.append("    of %d that do not,                     %d write  (%s)"
               % (en, c2[(False, True)],
                  "%.0f%%" % (100 * rn) if rn is not None else "--"))
    if ry is None or rn is None:
        out.append("    NOT ADDRESSABLE -- one group is empty.")
    else:
        out.append("    difference: %+.0f points" % (100 * (ry - rn)))
    out.append("")
    out.append("  This is a WEAKER test than the first: `executes` is read")
    out.append("  from the source and `writes` is observed, so a module")
    out.append("  that opens a file for writing is close to predicting")
    out.append("  itself. It is reported for the contrast with the")
    out.append("  enumeration column, not as an independent finding.")
    return "\n".join(out)


def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- inventory
    es = enumerators()
    paths = [p for p, _c in es]
    chk("inventory finds a known repo-wide walker",
        "uninstrumented/scan.py" in paths)
    chk("inventory finds a known globber",
        "reasoning-gate/mine_logs.py" in paths)
    chk("inventory finds the triage module",
        "inverseminar/inverseminar.py" in paths)
    chk("inventory records which primitive was seen",
        any("walk" in c for _p, c in es))
    chk("inventory skips legacy/",
        not any(p.startswith("legacy/") for p in paths))

    # -- _inside
    chk("_inside is true for a file under a walked dir",
        _inside(ROOT, os.path.join(ROOT, "self-scan", "enumerators.py")))
    chk("_inside is false for a sibling dir",
        not _inside(os.path.join(ROOT, "notes"),
                    os.path.join(ROOT, "self-scan", "x.py")))
    chk("_inside handles a glob pattern by its directory",
        _inside(os.path.join(ROOT, "self-scan", "*.py"),
                os.path.join(ROOT, "self-scan", "enumerators.py")))
    chk("_inside is false for a glob in another dir",
        not _inside(os.path.join(ROOT, "notes", "*.py"),
                    os.path.join(ROOT, "self-scan", "enumerators.py")))

    # -- the tracer records what a child really enumerated
    tmp = tempfile.mkdtemp()
    open(os.path.join(tmp, "sitecustomize.py"), "w").write(TRACER)
    probe = os.path.join(tmp, "probe.py")
    open(probe, "w").write("import os\n"
                           "for _ in os.walk(os.path.dirname(__file__)):\n"
                           "    pass\n")
    log = os.path.join(tmp, "t.json")
    old = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = tmp
    os.environ["ENUM_TRACE"] = log
    try:
        resolve._run([sys.executable, probe], cwd=tmp)
    finally:
        if old is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = old
        os.environ.pop("ENUM_TRACE", None)
    chk("the tracer writes a log", os.path.exists(log))
    if os.path.exists(log):
        rec = json.load(open(log))
        chk("the tracer records the walked root",
            any(k == "walk" for k, _r in rec))
        chk("the recorded root is the one the child used",
            any(os.path.abspath(r) == os.path.abspath(tmp)
                for _k, r in rec))

    # -- a module that enumerates nothing is measured as such
    quiet = os.path.join(tmp, "quiet.py")
    open(quiet, "w").write("print('nothing')\n")
    chk("a module with no enumeration is not in the inventory",
        "quiet.py" not in paths)

    # -- the 2x2 counts only rows that ran
    c = table([{"state": "RUN", "enumerates_self": True, "writes": True},
               {"state": "RUN", "enumerates_self": False, "writes": False},
               {"state": "NOT_RUN", "enumerates_self": None,
                "writes": None}])
    chk("2x2 counts only rows that ran", sum(c.values()) == 2)
    chk("2x2 places both diagonal cells",
        c[(True, True)] == 1 and c[(False, False)] == 1)

    # -- render reports association, not diagonal share, and says so
    txt = render([])
    chk("render survives an empty run", "NOT ADDRESSABLE" in txt)
    chk("render prints both margins", "writes: no" in txt)
    rows = [{"state": "RUN", "enumerates_self": True, "writes": True},
            {"state": "RUN", "enumerates_self": True, "writes": False},
            {"state": "RUN", "enumerates_self": False, "writes": False},
            {"state": "RUN", "enumerates_self": False, "writes": False}]
    t = render(rows)
    chk("render names the diagonal share as not the test",
        "NOT the test" in t)
    chk("render reports a within-group write rate", "50%" in t and "0%" in t)
    chk("render prints the difference", "difference: +50 points" in t)
    one = render([{"state": "RUN", "enumerates_self": True,
                   "writes": True}])
    chk("an empty group makes the association NOT ADDRESSABLE",
        "NOT ADDRESSABLE -- one group is empty" in one)

    # -- the alternative predictor is read from source and separable
    ex, why = executes(os.path.abspath(__file__))
    chk("this module is detected as executing", ex is True)
    chk("the reason is named", any("subprocess" in w or "open" in w
                                   or "mkdtemp" in w for w in why))
    tmp2 = tempfile.mkdtemp()
    ro = os.path.join(tmp2, "ro.py")
    open(ro, "w").write("import os\nfor _ in os.walk('.'):\n    pass\n"
                        "open('x').read()\n")
    chk("a read-only module is not detected as executing",
        executes(ro)[0] is False)
    chk("table can be keyed on either column",
        table([{"state": "RUN", "enumerates_self": False,
                "executes": True, "writes": True}],
              "executes")[(True, True)] == 1)
    chk("association returns None for an empty group",
        association({(True, True): 0, (True, False): 0,
                     (False, True): 1, (False, False): 0})[1] is None)

    # -- declared invocations, not guessed
    chk("the named enumerators have declared invocations",
        os.path.join("uninstrumented", "scan.py") in INVOCATIONS
        and os.path.join("reasoning-gate", "mine_logs.py") in INVOCATIONS
        and os.path.join("inverseminar", "inverseminar.py") in INVOCATIONS)

    # -- this module and census are in the inventory and not run
    chk("this module is in the inventory",
        "self-scan/enumerators.py" in paths)
    chk("this module is on the do-not-run list",
        os.path.join("self-scan", "enumerators.py") in NO_RUN)
    chk("census is on the do-not-run list",
        os.path.join("self-scan", "census.py") in NO_RUN)

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    limit = None
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])
    print(render(run(limit)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
