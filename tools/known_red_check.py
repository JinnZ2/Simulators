#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""known_red_check -- KNOWN_RED.md's stated counts against an actual run.

WHY IT EXISTS
    KNOWN_RED.md section 16 said "33 cases in 6 metrics". That was true at
    85ce0d9, the commit that wrote it. Merge 5af0d47 brought c95a1e5 in
    beside it, crediting_rate_v2.py::position started running, and the true
    figure became 28 in 5. Nothing noticed. The record drifted because it was
    prose, and nothing reads prose.

    This file makes the figures something a run reads. KNOWN_RED.md carries a
    block of PIN lines, each figure with the commit it was measured at. This
    tool reruns the instruments the figures came from and fails on any
    mismatch.

PIN GRAMMAR (inside the block delimited by the two marker comments)
    PIN <kind> <subject> <value> @<commit>

    kind                  subject              value        source of truth
    ka.skipped.cases      -                    int          tools/known_answer.py
    ka.skipped.metrics    -                    int          tools/known_answer.py
    ka.skipped.metric     <metric id>          int          tools/known_answer.py
    rm.redirect_missing   <path>               -            tools/run_manifest.py
    rm.violation          <path>               -            tools/run_manifest.py
    rm.archived_target_missing
                          <path>               -            tools/run_manifest.py
                                                            (target_state tag)
    cg.duplicate          <path>::<name>       -            tests/test_compile_gate.py
                                                            sweep(), run in-process
    suite.failing         <test method name>   INTENDED |   python3 -m unittest
                                               UNINTENDED   discover -s tests
                                                            (only with --suite)

    The set kinds (ka.skipped.metric, rm.*, suite.failing) are compared as SETS.
    A pinned subject the run does not produce is a mismatch, and so is a
    subject the run produces that nobody pinned. Either direction of drift
    is caught.

    A PIN with no @<commit> is refused. An unpinned figure is the defect this
    tool exists for, so it is not accepted in the block that fixes it.

STATES, per pin
    MATCH        the run agrees.
    MISMATCH     it does not. Exit 1.
    NOT_CHECKED  suite.failing without --suite. A state, not a pass: the
                 suite pins are only checked when the suite is run.
    The commit on each pin is reported REACHABLE / UNREACHABLE and never fails
    the check. A shallow clone cannot see old commits. That is a property of
    the clone, not of the figure.

WHAT IT DOES NOT DO
    It does not check that a figure was TRUE at its pinned commit. It checks
    that the figure holds now. The pin says when it was last verified, not
    that it has been correct ever since. Rerunning at the pinned commit is
    `git worktree add`, done by hand. Section 19 of KNOWN_RED.md records
    the one rerun that has been done.

    --suite runs the suite in a throwaway worktree at HEAD (KNOWN_RED section
    8 and SS_009: the suite writes into the tree it runs in). That costs
    something: uncommitted changes are invisible to the suite pins.

USAGE
    python3 tools/known_red_check.py            ka + rm pins
    python3 tools/known_red_check.py --suite    also the suite.failing pins
    python3 tools/known_red_check.py --selftest
"""
from __future__ import annotations

import io
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWN_RED = os.path.join(ROOT, "KNOWN_RED.md")

BEGIN = "<!-- known-red-pins: begin -->"
END = "<!-- known-red-pins: end -->"

SCALAR_KINDS = ("ka.skipped.cases", "ka.skipped.metrics")
SET_KINDS = ("ka.skipped.metric", "rm.redirect_missing", "rm.violation",
             "rm.archived_target_missing", "cg.duplicate", "suite.failing")
KINDS = SCALAR_KINDS + SET_KINDS
SUITE_VALUES = ("INTENDED", "UNINTENDED")

_PIN = re.compile(r"^\s*PIN\s+(\S+)\s+(\S+)\s+(\S+)(?:\s+@(\S+))?\s*$")
_SHA = re.compile(r"^[0-9a-f]{7,40}$")


class PinError(ValueError):
    pass


# ----------------------------------------------------------------------------
# parsing
# ----------------------------------------------------------------------------

def parse(text):
    """Return the list of pins in the block. Raises PinError on any bad line."""
    if BEGIN not in text or END not in text:
        raise PinError("no pin block: both %r and %r are required" % (BEGIN, END))
    block = text.split(BEGIN, 1)[1].split(END, 1)[0]
    pins = []
    for n, line in enumerate(block.splitlines(), 1):
        s = line.strip()
        if not s.startswith("PIN"):
            continue
        m = _PIN.match(line)
        if not m:
            raise PinError("block line %d is malformed: %r" % (n, s))
        kind, subject, value, commit = m.groups()
        if commit is None:
            raise PinError("block line %d carries no @<commit>: an unpinned "
                           "figure is the defect this block exists to "
                           "remove: %r" % (n, s))
        if not _SHA.match(commit):
            raise PinError("block line %d: %r is not a commit hash" % (n, commit))
        if kind not in KINDS:
            raise PinError("block line %d: unknown kind %r" % (n, kind))
        if kind in SCALAR_KINDS or kind == "ka.skipped.metric":
            if not value.isdigit():
                raise PinError("block line %d: %s takes an integer, got %r"
                               % (n, kind, value))
            value = int(value)
        elif kind == "suite.failing":
            if value not in SUITE_VALUES:
                raise PinError("block line %d: suite.failing takes one of %s, "
                               "got %r" % (n, SUITE_VALUES, value))
        if kind in SCALAR_KINDS and subject != "-":
            raise PinError("block line %d: %s takes subject '-'" % (n, kind))
        pins.append({"kind": kind, "subject": subject, "value": value,
                     "commit": commit})
    keys = [(p["kind"], p["subject"]) for p in pins]
    dup = sorted(set(k for k in keys if keys.count(k) > 1))
    if dup:
        raise PinError("pinned twice: %s" % dup)
    return pins


# ----------------------------------------------------------------------------
# actual runs
# ----------------------------------------------------------------------------

_KA_HEAD = re.compile(r"^SKIPPED \(NOT_RUN\): (\d+) cases in (\d+) metrics")
_KA_ROW = re.compile(r"^\s+SKIPPED\s+(\d+)\s+(\S+)\s*$")


def parse_known_answer(out):
    """Read the SKIPPED block out of tools/known_answer.py output.

    No SKIPPED header can mean zero skips or a run that never got that far.
    Those are kept apart. Zero requires the run's own summary line to be
    present, otherwise the result is None.
    """
    cases = metrics = None
    per = {}
    for line in out.splitlines():
        m = _KA_HEAD.match(line)
        if m:
            cases, metrics = int(m.group(1)), int(m.group(2))
            continue
        m = _KA_ROW.match(line)
        if m:
            per[m.group(2)] = int(m.group(1))
    if cases is None:
        if "metrics registered:" in out:
            return {"cases": 0, "metrics": 0, "per": {}}
        return None
    return {"cases": cases, "metrics": metrics, "per": per}


def run_known_answer():
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools",
                                                     "known_answer.py")],
                       cwd=ROOT, capture_output=True, text=True)
    return parse_known_answer(p.stdout + p.stderr)


def run_manifest_state():
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    try:
        import run_manifest as rm
    finally:
        sys.path.pop(0)
    records, _ = rm.build()
    missing = sorted(r["path"] for r in records
                     if r["class"] == "REDIRECT" and r["target_resolves"] is False)
    viol = sorted(r["path"] for r in rm.violations(records))
    archived = sorted(r["path"] for r in records
                      if r.get("target_state") == "ARCHIVED_TARGET_MISSING")
    return {"redirect_missing": missing, "violation": viol,
            "archived_target_missing": archived}


def run_compile_dupes():
    """path::name for every top-level name bound twice, from the compile gate.

    Imported from tests/test_compile_gate.py by path rather than copied, so
    the pin and the red test read one function. None if it cannot load.
    """
    import importlib.util
    path = os.path.join(ROOT, "tests", "test_compile_gate.py")
    try:
        spec = importlib.util.spec_from_file_location("_cg_for_pins", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _n, _red, _skipped, dupes = mod.sweep()
    except Exception:
        return None
    return sorted("%s::%s" % (rel, name) for rel, name, _lines in dupes)


_FAILLINE = re.compile(r"^(FAIL|ERROR): (\S+)")


def parse_suite(out):
    """Failing test METHOD names from unittest output, or None if no summary.

    Method names, not full ids. KNOWN_RED section 15 and every earlier pass
    name tests by method, and the names in this suite are unique.
    """
    if not re.search(r"^Ran \d+ tests? in", out, re.M):
        return None
    return sorted(set(m.group(2) for m in
                      (_FAILLINE.match(l) for l in out.splitlines()) if m))


def run_suite():
    wt = tempfile.mkdtemp(prefix="known_red_suite_")
    os.rmdir(wt)
    subprocess.run(["git", "worktree", "add", "-f", "--detach", wt, "HEAD"],
                   cwd=ROOT, capture_output=True, text=True, check=True)
    try:
        p = subprocess.run([sys.executable, "-m", "unittest", "discover",
                            "-s", "tests"], cwd=wt, capture_output=True,
                           text=True,
                           env=dict(os.environ, KNOWN_RED_CHECK_NESTED="1"))
        return parse_suite(p.stdout + p.stderr)
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", wt],
                       cwd=ROOT, capture_output=True, text=True)


def reachable(commit):
    p = subprocess.run(["git", "cat-file", "-e", commit + "^{commit}"],
                       cwd=ROOT, capture_output=True, text=True)
    return p.returncode == 0


# ----------------------------------------------------------------------------
# comparison
# ----------------------------------------------------------------------------

def compare(pins, ka, rm_state, suite, cg=None):
    """One row per pin, plus one row per produced-but-unpinned subject.

    ka / rm_state / suite may be None. A source that did not run turns its
    pins into MISMATCH (for ka, rm) or NOT_CHECKED (for suite). The suite
    is optional by design. The other two are not.
    """
    rows = []

    def row(kind, subject, stated, actual, state, commit):
        rows.append({"kind": kind, "subject": subject, "stated": stated,
                     "actual": actual, "state": state, "commit": commit})

    by_kind = {}
    for p in pins:
        by_kind.setdefault(p["kind"], []).append(p)

    # scalars
    for kind, key in (("ka.skipped.cases", "cases"),
                      ("ka.skipped.metrics", "metrics")):
        for p in by_kind.get(kind, []):
            actual = None if ka is None else ka[key]
            row(kind, "-", p["value"], actual,
                "MATCH" if actual == p["value"] else "MISMATCH", p["commit"])

    # sets
    def set_rows(kind, produced, value_of):
        if produced is None:
            for p in by_kind.get(kind, []):
                row(kind, p["subject"], p["value"], None,
                    "NOT_CHECKED" if kind == "suite.failing" else "MISMATCH",
                    p["commit"])
            return
        pinned = {p["subject"]: p for p in by_kind.get(kind, [])}
        for subj in sorted(set(pinned) | set(produced)):
            p = pinned.get(subj)
            if p is None:
                row(kind, subj, None, value_of(subj), "MISMATCH", None)
                continue
            if subj not in produced:
                row(kind, subj, p["value"], None, "MISMATCH", p["commit"])
                continue
            want = p["value"]
            got = value_of(subj)
            ok = (got == want) if kind == "ka.skipped.metric" else True
            row(kind, subj, want, got, "MATCH" if ok else "MISMATCH",
                p["commit"])

    set_rows("ka.skipped.metric", None if ka is None else set(ka["per"]),
             lambda s: ka["per"].get(s))
    set_rows("rm.redirect_missing",
             None if rm_state is None else set(rm_state["redirect_missing"]),
             lambda s: "-")
    set_rows("rm.violation",
             None if rm_state is None else set(rm_state["violation"]),
             lambda s: "-")
    set_rows("rm.archived_target_missing",
             None if rm_state is None
             else set(rm_state.get("archived_target_missing", [])),
             lambda s: "-")
    if cg is not None or "cg.duplicate" in by_kind:
        set_rows("cg.duplicate", None if cg is None else set(cg),
                 lambda s: "-")
    set_rows("suite.failing", None if suite is None else set(suite),
             lambda s: "FAILING")
    return rows


def render(rows, reach):
    out = []
    w = max([len(r["subject"]) for r in rows] + [10])
    out.append("%-20s %-*s %-10s %-10s %-11s %s"
               % ("kind", w, "subject", "stated", "actual", "state", "@commit"))
    for r in rows:
        c = r["commit"] or "UNPINNED"
        if r["commit"]:
            c += " (%s)" % ("REACHABLE" if reach.get(r["commit"])
                            else "UNREACHABLE")
        out.append("%-20s %-*s %-10s %-10s %-11s %s"
                   % (r["kind"], w, r["subject"], r["stated"], r["actual"],
                      r["state"], c))
    n = {s: sum(1 for r in rows if r["state"] == s)
         for s in ("MATCH", "MISMATCH", "NOT_CHECKED")}
    out.append("")
    out.append("pins: %d   MATCH %d   MISMATCH %d   NOT_CHECKED %d"
               % (len(rows), n["MATCH"], n["MISMATCH"], n["NOT_CHECKED"]))
    if n["NOT_CHECKED"]:
        out.append("NOT_CHECKED is not a pass: run with --suite to check the "
                   "suite.failing pins.")
    out.append("VERDICT: %s" % ("FAIL -- KNOWN_RED.md does not match the run; "
                                "update the block AND its @commit, or the "
                                "tree moved and that is the finding"
                                if n["MISMATCH"] else "PASS"))
    return "\n".join(out), (1 if n["MISMATCH"] else 0)


def check(text, with_suite=False):
    pins = parse(text)
    ka = run_known_answer()
    rm_state = run_manifest_state()
    suite = run_suite() if with_suite else None
    cg = run_compile_dupes()
    rows = compare(pins, ka, rm_state, suite, cg)
    reach = {p["commit"]: reachable(p["commit"]) for p in pins}
    return rows, reach


# ----------------------------------------------------------------------------
# selftest
# ----------------------------------------------------------------------------

def selftest():
    fails = []
    n = [0]

    def ok(cond, what):
        n[0] += 1
        if not cond:
            fails.append(what)
            print("  FAIL", what)

    good = "\n".join([
        "x", BEGIN,
        "    PIN ka.skipped.cases - 3 @abcdef1",
        "    PIN ka.skipped.metrics - 2 @abcdef1",
        "    PIN ka.skipped.metric a.py::f 2 @abcdef1",
        "    PIN ka.skipped.metric b.py::g 1 @abcdef1",
        "    PIN rm.redirect_missing p/q.py - @abcdef1",
        "    PIN rm.violation p/q.py - @abcdef1",
        "    PIN suite.failing test_x INTENDED @abcdef1",
        END, "y"])
    pins = parse(good)
    ok(len(pins) == 7, "seven pins parse")
    ka = {"cases": 3, "metrics": 2, "per": {"a.py::f": 2, "b.py::g": 1}}
    rmst = {"redirect_missing": ["p/q.py"], "violation": ["p/q.py"]}
    rows = compare(pins, ka, rmst, ["test_x"])
    ok(all(r["state"] == "MATCH" for r in rows), "an agreeing run is all MATCH")
    ok(render(rows, {})[1] == 0, "all MATCH exits 0")

    # the 33/6 vs 28/5 drift, both scalars
    rows = compare(pins, dict(ka, cases=28, metrics=5), rmst, ["test_x"])
    ok(sum(r["state"] == "MISMATCH" for r in rows) == 2,
       "scalar drift is caught on both scalars")
    ok(render(rows, {})[1] == 1, "a mismatch exits 1")

    # a metric that cleared (pinned, no longer produced)
    rows = compare(pins, {"cases": 2, "metrics": 1, "per": {"a.py::f": 2}},
                   rmst, ["test_x"])
    ok(any(r["subject"] == "b.py::g" and r["state"] == "MISMATCH"
           for r in rows), "a pinned subject the run no longer produces")
    # a new one nobody pinned
    rows = compare(pins, dict(ka, per={"a.py::f": 2, "b.py::g": 1,
                                       "c.py::h": 4}), rmst, ["test_x"])
    ok(any(r["subject"] == "c.py::h" and r["state"] == "MISMATCH"
           and r["commit"] is None for r in rows),
       "a produced subject nobody pinned, reported UNPINNED")
    # per-metric count moved, same set
    rows = compare(pins, dict(ka, per={"a.py::f": 3, "b.py::g": 1}), rmst,
                   ["test_x"])
    ok(any(r["subject"] == "a.py::f" and r["state"] == "MISMATCH"
           for r in rows), "a per-metric count moving is a mismatch")
    # redirect cleared (the sense_as_match merge shape)
    rows = compare(pins, ka, {"redirect_missing": [], "violation": ["p/q.py"]},
                   ["test_x"])
    ok(any(r["kind"] == "rm.redirect_missing" and r["state"] == "MISMATCH"
           for r in rows), "a redirect clearing is a mismatch until re-pinned")
    # suite: not run -> NOT_CHECKED, not MATCH
    rows = compare(pins, ka, rmst, None)
    sr = [r for r in rows if r["kind"] == "suite.failing"]
    ok(sr and all(r["state"] == "NOT_CHECKED" for r in sr),
       "suite pins without --suite are NOT_CHECKED, not MATCH")
    ok(render(rows, {})[1] == 0, "NOT_CHECKED alone does not fail")
    ok("NOT_CHECKED is not a pass" in render(rows, {})[0],
       "NOT_CHECKED says it is not a pass")
    # a source that did not run is not a zero
    rows = compare(pins, None, rmst, ["test_x"])
    ok(all(r["state"] == "MISMATCH" for r in rows if r["kind"].startswith("ka")),
       "known_answer not running fails its pins rather than reading as zero")
    ok(parse_known_answer("garbage") is None, "no summary line -> None, not 0")
    ok(parse_known_answer("metrics registered: 4   expected: 4")
       == {"cases": 0, "metrics": 0, "per": {}},
       "summary present, no SKIPPED block -> a measured zero")
    ka_out = ("metrics registered: 51\n"
              "SKIPPED (NOT_RUN): 28 cases in 5 metrics   -- GATE RED\n"
              "  SKIPPED  6  assessor-coupling/conditions.py::pool_fraction\n"
              "             IndentationError: unexpected indent\n"
              "  SKIPPED  5  chain-position/load_class.py::stability_product\n")
    got = parse_known_answer(ka_out)
    ok(got["cases"] == 28 and got["metrics"] == 5 and len(got["per"]) == 2
       and got["per"]["chain-position/load_class.py::stability_product"] == 5,
       "the real SKIPPED block parses; the error line is not a row")
    ok(parse_suite("FAIL: test_a (x.Y)\nERROR: test_b (x.Z)\nRan 3 tests in 1s")
       == ["test_a", "test_b"], "suite FAIL and ERROR both read")
    ok(parse_suite("FAIL: test_a (x.Y)") is None,
       "no 'Ran N tests' -> None, not an empty failing set")

    # refusals
    def refuses(text, what):
        try:
            parse(text)
        except PinError:
            ok(True, what)
            return
        ok(False, what)
    refuses(BEGIN + "\nPIN ka.skipped.cases - 3\n" + END,
            "a pin with no @commit is refused")
    refuses(BEGIN + "\nPIN ka.skipped.cases - 3 @nothex\n" + END,
            "a non-hash commit is refused")
    refuses(BEGIN + "\nPIN ka.skipped.cases - three @abcdef1\n" + END,
            "a non-integer count is refused")
    refuses(BEGIN + "\nPIN suite.failing t MAYBE @abcdef1\n" + END,
            "a suite value outside INTENDED/UNINTENDED is refused")
    refuses(BEGIN + "\nPIN made.up - 1 @abcdef1\n" + END,
            "an unknown kind is refused")
    refuses(BEGIN + "\nPIN ka.skipped.cases - 1 @abcdef1\n"
            "PIN ka.skipped.cases - 2 @abcdef1\n" + END,
            "the same figure pinned twice is refused")
    refuses("no block here", "a file with no block is refused")
    refuses(BEGIN + "\nPIN\n" + END, "a bare PIN line is refused")

    # archived tag and compile dupes
    p2 = parse(BEGIN + "\nPIN rm.archived_target_missing archive/f/x.py - @abcdef1"
               "\nPIN cg.duplicate f/y.py::main - @abcdef1\n" + END)
    rm2 = {"redirect_missing": [], "violation": [],
           "archived_target_missing": ["archive/f/x.py"]}
    rows = compare(p2, None, rm2, None, ["f/y.py::main"])
    ok(all(r["state"] == "MATCH" for r in rows), "archived tag and dupe pins MATCH")
    rows = compare(p2, None, dict(rm2, archived_target_missing=[]), None,
                   ["f/y.py::main", "tools/k.py::_h"])
    ok(sum(r["state"] == "MISMATCH" for r in rows) == 2,
       "a cleared archived tag and an unpinned new dupe both mismatch")
    rows = compare(p2, None, rm2, None, None)
    ok(any(r["kind"] == "cg.duplicate" and r["state"] == "MISMATCH" for r in rows),
       "compile gate not loading fails its pins rather than reading as zero")
    rows = compare(pins, ka, dict(rmst, archived_target_missing=["a/b.py"]),
                   ["test_x"])
    ok(any(r["subject"] == "a/b.py" and r["state"] == "MISMATCH" for r in rows),
       "an archived miss nobody pinned is reported")

    print("known_red_check selftest: checks: %d   failed: %d"
          % (n[0], len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    text = io.open(KNOWN_RED, encoding="utf-8").read()
    try:
        rows, reach = check(text, with_suite="--suite" in argv)
    except PinError as e:
        print("PIN BLOCK REFUSED: %s" % e)
        return 1
    report, code = render(rows, reach)
    print(report)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
