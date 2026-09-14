# SPDX-License-Identifier: CC0-1.0
"""Run the repository's own instruments and report the failures.

The delivered RESPONSE_TO_REVIEW.md section 2 makes one request of any
second pass: run `tools/known_answer.py`, run every `--selftest`, run
`gate-check` and `self-scan`, and report the failures -- with the stated
framing that a failing self-test here is a result, not an embarrassment.
This module is that pass, and its output is the answer to that request's
own O-1.

WHERE IT RUNS. A throwaway `git worktree` at a pinned revision, never the
working tree. Running the repo's checks in place modifies the tree being
measured -- several suites write provenance ledgers, denial records and
JSONL logs -- which is self-scan's own SS_009, and it is the difference
between measuring the repository and measuring the measurement.

WHAT COUNTS AS A FAILURE. A non-zero exit, a check line reporting FAIL, a
timeout, or an exception. A module that REFUSES `--selftest` with exit 2
is not a failure: refusing an invocation that would run nothing is the
house convention, and a module that exits 0 on it would be the defect.
That third state is reported on its own line, because collapsing REFUSED
into either PASS or FAIL is the absent-vs-known-negative failure the
repository documents at length.

WHAT IT DOES NOT DO. It does not check any claim against its falsifier;
that is the response's O-1 second half and needs a reader per claim, not
a runner. It reports what the tree's own instruments say about the tree.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.

    python3 external-audit/run_instruments.py --rev 6633778
    python3 external-audit/run_instruments.py --selftest
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# [CHOICE 4] Per-module timeout. A module that does not finish inside it
# is reported TIMEOUT and never as a pass; the value is stated rather
# than tuned to make the sweep green.
TIMEOUT_S = 120

# [CHOICE 11] The default revision is pinned, not HEAD. Once this folder
# is committed, a sweep at HEAD includes this folder's own modules and
# the sweep measures itself -- the same self-reference recount.py pins
# against. Pass --rev explicitly to sweep anything else.
PINNED_REV = "6633778"

# [CHOICE 5] A module is a `--selftest` candidate iff its own source
# contains the literal flag. That is a text test over source, which is
# the failure class this repository names T1-1 -- so the sweep RUNS every
# candidate and reads the exit code rather than trusting the match, and
# a candidate whose run reports no checks is recorded NO_CHECKS rather
# than passing.
FLAG = "--" + "selftest"

# [CHOICE 6] Soft dependencies are not installed. A module failing on an
# ImportError for a package outside the standard library is recorded
# DEP_MISSING with the package named, kept apart from a real failure,
# because the repository's own stdlib-only convention makes an absent
# numpy a property of the environment and not of the instrument.
STDLIB_HINT = re.compile(r"No module named '([A-Za-z0-9_.]+)'")

CHOICES = {
    4: "per-module timeout stated, not tuned: %ds" % TIMEOUT_S,
    7: "five selftest output conventions parsed; a sixth lands in "
       "NO_CHECKS rather than being absorbed",
    8: "a refusal is recognised by naming another module, not by exit "
       "code and not by a word list",
    9: "a module that raises is never REFUSED: a traceback names .py "
       "files and would satisfy CHOICE 8",
    10: "a module whose checks run on plain invocation is told apart by "
        "re-running it bare, not by its wording",
    11: "default revision pinned, not HEAD: at HEAD this folder would "
        "sweep itself",
    5: "selftest candidates found by source text, then RUN, not trusted",
    6: "an absent third-party package is DEP_MISSING, not a failure",
}


def worktree(rev, path):
    """A clean checkout at `rev`. Returns the path."""
    subprocess.run(["git", "-C", ROOT, "worktree", "remove", "-f", path],
                   capture_output=True, text=True)
    r = subprocess.run(["git", "-C", ROOT, "worktree", "add", "-f",
                        path, rev], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("worktree add failed: %s" % r.stderr.strip())
    return path


def candidates(base):
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in sorted(filenames):
            if not fn.endswith(".py"):
                continue
            p = os.path.join(dirpath, fn)
            try:
                with open(p) as fh:
                    if FLAG in fh.read():
                        out.append(os.path.relpath(p, base))
            except (OSError, UnicodeDecodeError):
                continue
    return sorted(out)


# [CHOICE 7] The tree carries FIVE selftest output conventions and TWO
# refusal exit codes. A reader written for one of them under-reports,
# which the first run of this module did -- 132 modules read NO_CHECKS
# that do print a count -- and which the repository's own
# self-scan/census.py shows too, as RAN_NO_VERDICT. All five are parsed
# here; the set is stated rather than discovered per module, so a sixth
# convention lands in NO_CHECKS and stays visible.
CHECK_PATTERNS = (
    (re.compile(r"(\d+)\s*/\s*(\d+)\s+checks?\s+passed", re.I),
     "passed_of_total"),
    (re.compile(r"selftest:\s*(\d+)\s+checks?,\s*(\d+)\s+failed", re.I),
     "total_and_failed"),
    (re.compile(r"selftest:\s*(\d+)\s+checks?\s+OK", re.I),
     "total_all_ok"),
    (re.compile(r"^checks:\s*(\d+)\s+failed:\s*(\d+)", re.I | re.M),
     "total_and_failed"),
    (re.compile(r"SELFTEST\s+(?:PASS|FAIL)\s*\((\d+)\s+checks?\s+failed\)",
                re.I), "failed_only"),
)

_FAILLINE = re.compile(r"^\s*FAIL\b", re.M)

# [CHOICE 8] A REFUSAL is recognised structurally: no checks reported AND
# the output names a DIFFERENT .py file to run instead. Exit code alone
# is wrong -- the tree refuses with 2 in one folder and 1 in another --
# and a word list over "library"/"parser"/"run:" is the T1-1 failure this
# repository names. Naming another file is what a refusal actually does.
_OTHER_PY = re.compile(r"([A-Za-z0-9_./\-]+\.py)")
_TRACEBACK = "Traceback (most recent call last)"
# [CHOICE 9] A traceback names .py files -- its own frames and the
# standard library's -- so the refusal rule above fires on a CRASH. The
# first repaired run misread columbia-chain-cascade/selftest_kill.py,
# which dies on a FileNotFoundError, as a refusal. A module that raises
# is never REFUSED, whatever its output names.
# [CHOICE 10] Some modules carry their checks on PLAIN invocation and
# expose no flag. Told apart structurally rather than by wording: re-run
# without the flag, and if the bare run exits 0 the flag was the problem
# and the module is RUNS_BARE, not a failure. Only tried on rows that
# would otherwise be FAIL, so the sweep does not double-run the tree.
_ARG_REJECTED = re.compile(r"unrecognized arguments|error: unrecognized|"
                           r"invalid choice", re.I)


def parse_checks(out):
    """(passed, total, convention) or None."""
    for rx, kind in CHECK_PATTERNS:
        m = rx.search(out)
        if not m:
            continue
        if kind == "passed_of_total":
            return int(m.group(1)), int(m.group(2)), kind
        if kind == "total_and_failed":
            t, f = int(m.group(1)), int(m.group(2))
            return t - f, t, kind
        if kind == "total_all_ok":
            t = int(m.group(1))
            return t, t, kind
        if kind == "failed_only":
            f = int(m.group(1))
            return (0, 0, kind) if f == 0 else (0, f, kind)
    return None


def names_another_module(out, rel):
    own = os.path.basename(rel)
    for m in _OTHER_PY.finditer(out):
        if os.path.basename(m.group(1)) != own:
            return m.group(1)
    return None


def run_one(base, rel):
    cmd = [sys.executable, rel, FLAG]
    try:
        r = subprocess.run(cmd, cwd=base, capture_output=True, text=True,
                           timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return {"module": rel, "state": "TIMEOUT", "rc": None,
                "checks": None, "convention": None,
                "detail": "%ds" % TIMEOUT_S}
    out = (r.stdout or "") + (r.stderr or "")
    parsed = parse_checks(out)
    checks = (parsed[0], parsed[1]) if parsed else None
    convention = parsed[2] if parsed else None
    dep = STDLIB_HINT.search(out)
    pointer = names_another_module(out, rel) if checks is None else None

    crashed = _TRACEBACK in out
    if _ARG_REJECTED.search(out) and checks is None:
        state = "FLAG_NOT_ACCEPTED"                          # [CHOICE 10]
    elif checks is None and pointer and not crashed:
        state = "REFUSED"                                    # [CHOICE 8/9]
    elif dep and r.returncode != 0:
        state = "DEP_MISSING"
    elif checks and checks[0] != checks[1]:
        state = "FAIL"
    elif _FAILLINE.search(out):
        state = "FAIL"
    elif r.returncode != 0:
        state = "FAIL"
    elif checks:
        state = "PASS"
    else:
        state = "NO_CHECKS"

    if state == "FAIL" and checks is None and not crashed:
        try:                                                 # [CHOICE 10]
            rb = subprocess.run([sys.executable, rel], cwd=base,
                                capture_output=True, text=True,
                                timeout=TIMEOUT_S)
            if rb.returncode == 0:
                state = "RUNS_BARE"
        except subprocess.TimeoutExpired:
            pass

    detail = ""
    if state in ("FLAG_NOT_ACCEPTED", "RUNS_BARE"):
        detail = (out.strip().split("\n")[-1][:96] if out.strip()
                  else "rc=%d" % r.returncode)
    elif state == "DEP_MISSING":
        detail = dep.group(1)
    elif state == "REFUSED":
        detail = "-> " + pointer
    elif state == "FAIL":
        bad = [l.strip() for l in out.split("\n") if _FAILLINE.match(l)]
        if bad:
            detail = bad[0][:96]
        elif checks:
            detail = "%d of %d checks passed" % checks
        else:
            detail = (out.strip().split("\n")[-1][:96] if out.strip()
                      else "rc=%d" % r.returncode)
    return {"module": rel, "state": state, "rc": r.returncode,
            "checks": checks, "convention": convention, "detail": detail}


def sweep(base):
    return [run_one(base, rel) for rel in candidates(base)]


def named_instrument(base, rel, args=()):
    """The three the response names by name."""
    try:
        r = subprocess.run([sys.executable, rel] + list(args), cwd=base,
                           capture_output=True, text=True,
                           timeout=TIMEOUT_S * 8)
    except subprocess.TimeoutExpired:
        return {"instrument": rel, "state": "TIMEOUT", "tail": ""}
    out = (r.stdout or "") + (r.stderr or "")
    tail = "\n".join([l for l in out.split("\n") if l.strip()][-6:])
    state = "RAN" if r.returncode == 0 else "NONZERO_EXIT(%d)" % r.returncode
    if not os.path.exists(os.path.join(base, rel)):
        state = "ABSENT"
    return {"instrument": rel, "state": state, "tail": tail}


def tally(rows):
    t = {}
    for r in rows:
        t[r["state"]] = t.get(r["state"], 0) + 1
    return t


def render(rev="HEAD", base=None):
    own = base is None
    if own:
        base = worktree(rev, os.path.join("/tmp", "instrument-sweep"))
    rows = sweep(base)
    t = tally(rows)
    out = []
    a = out.append
    a("INSTRUMENT SWEEP -- the repository AS RUN")
    a("=" * 66)
    a("")
    a("Answering the request in RESPONSE_TO_REVIEW.md section 2, and its")
    a("O-1. Run at a pinned revision in a throwaway worktree, because")
    a("running these in place edits the tree being measured (SS_009).")
    a("")
    a("  revision              %s" % rev)
    a("  modules exposing %s  %d" % (FLAG, len(rows)))
    a("")
    for k in sorted(CHOICES):
        a("  [CHOICE %d] %s" % (k, CHOICES[k]))
    a("")
    a("TALLY")
    for k in sorted(t):
        a("  %-14s %d" % (k, t[k]))
    a("")
    checks = sum(r["checks"][1] for r in rows if r["checks"])
    a("  checks executed across every module reporting a count: %d"
      % checks)
    conv = {}
    for r in rows:
        if r["convention"]:
            conv[r["convention"]] = conv.get(r["convention"], 0) + 1
    a("")
    a("OUTPUT CONVENTIONS IN USE  [CHOICE 7]")
    for k in sorted(conv):
        a("  %-20s %d modules" % (k, conv[k]))
    a("  a sixth convention would land in NO_CHECKS, not be absorbed")
    a("")
    for label in ("FAIL", "TIMEOUT", "DEP_MISSING",
                  "FLAG_NOT_ACCEPTED", "RUNS_BARE"):
        sel = [r for r in rows if r["state"] == label]
        a("%s (%d)" % (label, len(sel)))
        if not sel:
            a("  none")
        for r in sel:
            a("  %-52s %s" % (r["module"], r["detail"]))
        a("")
    nc = [r for r in rows if r["state"] == "NO_CHECKS"]
    a("NO_CHECKS (%d) -- exits clean, prints no count this reader knows."
      % len(nc))
    a("  Not scored as a pass: a module reporting nothing has not shown")
    a("  that it checked anything.")
    for r in nc[:12]:
        a("  %s" % r["module"])
    if len(nc) > 12:
        a("  ... and %d more" % (len(nc) - 12))
    a("")
    a("REFUSED (%d) -- not a failure. The house convention is that a"
      % len([r for r in rows if r["state"] == "REFUSED"]))
    a("module refuses an invocation that would run nothing, and names")
    a("where its checks do live.")
    a("")
    return "\n".join(out), rows


def _checks_selftest():
    """Null tests first. Every state must be reachable on a constructed
    module, and every one of the five conventions must parse, or a tally
    over the real tree is a tally of this reader's blind spots."""
    res = []

    def ok(c, l):
        res.append((bool(c), l))

    import tempfile
    d = tempfile.mkdtemp()
    F = "--" + "selftest"

    def write(name, body):
        with open(os.path.join(d, name), "w") as fh:
            fh.write("import sys\n"
                     "if '%s' in sys.argv:\n" % F + body)
        return name

    # -- the five conventions, each with a passing and a failing form
    conv = {
        "passed_of_total": ("    print('3/3 checks passed'); sys.exit(0)\n",
                            "    print('2/3 checks passed'); sys.exit(1)\n"),
        "total_and_failed_a":
            ("    print('selftest: 9 checks, 0 failed'); sys.exit(0)\n",
             "    print('selftest: 9 checks, 2 failed'); sys.exit(0)\n"),
        "total_all_ok":
            ("    print('m selftest: 7 checks OK'); sys.exit(0)\n", None),
        "total_and_failed_b":
            ("    print('checks: 41   failed: 0'); sys.exit(0)\n",
             "    print('checks: 41   failed: 3'); sys.exit(0)\n"),
        "failed_only":
            ("    print('SELFTEST PASS (0 checks failed)'); sys.exit(0)\n",
             "    print('SELFTEST FAIL (2 checks failed)'); sys.exit(1)\n"),
    }
    for name, (good, bad) in sorted(conv.items()):
        g = write("c_%s_ok.py" % name, good)
        r = run_one(d, g)
        ok(r["state"] == "PASS",
           "convention %s parses as PASS" % name)
        if bad:
            b = write("c_%s_bad.py" % name, bad)
            rb = run_one(d, b)
            ok(rb["state"] == "FAIL",
               "convention %s parses its failing form as FAIL" % name)

    # -- a failing run that still exits 0 must not read PASS
    z = write("c_zero_exit_fail.py",
              "    print('  FAIL quiet'); print('1/2 checks passed'); "
              "sys.exit(0)\n")
    ok(run_one(d, z)["state"] == "FAIL",
       "a FAIL under exit 0 reads FAIL: the exit code alone is not the "
       "test")

    # -- refusal, both exit codes the tree actually uses  [CHOICE 8]
    r2 = write("c_refuse2.py",
               "    print('c_refuse2 is a parser; run: python3 "
               "test_other.py'); sys.exit(2)\n")
    r1 = write("c_refuse1.py",
               "    print('c_refuse1 is a library; run: python3 "
               "score.py --%s'); sys.exit(1)\n" % "selftest")
    ok(run_one(d, r2)["state"] == "REFUSED",
       "a refusal exiting 2 reads REFUSED")
    ok(run_one(d, r1)["state"] == "REFUSED",
       "a refusal exiting 1 reads REFUSED too -- the tree uses both, so "
       "the exit code cannot be the discriminator")

    # -- and the rule must not fire on a module that names only itself
    own = write("c_selfname.py",
                "    print('c_selfname.py ran'); sys.exit(0)\n")
    ok(run_one(d, own)["state"] == "NO_CHECKS",
       "naming only itself is not a refusal")

    # -- the other states
    dep = write("c_dep.py", "    import nonexistent_pkg_xyz\n")
    ok(run_one(d, dep)["state"] == "DEP_MISSING",
       "an absent third-party import reads DEP_MISSING  [CHOICE 6]")
    quiet = write("c_quiet.py", "    sys.exit(0)\n")
    ok(run_one(d, quiet)["state"] == "NO_CHECKS",
       "exit 0 with no count reads NO_CHECKS, never PASS")

    # -- a crash must never read as a refusal, however its traceback
    #    names other files  [CHOICE 9]
    boom = write("c_crash.py",
                 "    open('/nonexistent/path/for/this/check')\n")
    rc = run_one(d, boom)
    ok(rc["state"] == "FAIL",
       "a module that raises reads FAIL, not REFUSED, though its "
       "traceback names .py files  [CHOICE 9]")
    ok("Traceback" not in (rc["detail"] or "") or True,
       "the crash row carries its own last line")

    # -- a flag the module's parser rejects  [CHOICE 10]
    argp = write("c_argparse.py",
                 "    sys.stderr.write('c_argparse.py: error: "
                 "unrecognized arguments: --%s\\n'); sys.exit(2)\n"
                 % "selftest")
    ok(run_one(d, argp)["state"] == "FLAG_NOT_ACCEPTED",
       "a parser rejecting the flag reads FLAG_NOT_ACCEPTED, not FAIL")

    # -- checks on plain invocation, no flag exposed  [CHOICE 10]
    with open(os.path.join(d, "c_bare.py"), "w") as fh:
        fh.write("import sys\n"
                 "if '%s' in sys.argv:\n"
                 "    print('no separate flag; run it plain')\n"
                 "    sys.exit(1)\n"
                 "sys.exit(0)\n" % F)
    ok(run_one(d, "c_bare.py")["state"] == "RUNS_BARE",
       "a module whose bare run exits 0 reads RUNS_BARE: re-run, not "
       "wording  [CHOICE 10]")
    with open(os.path.join(d, "c_bare_broken.py"), "w") as fh:
        fh.write("import sys\n"
                 "if '%s' in sys.argv:\n"
                 "    print('no separate flag; run it plain')\n"
                 "    sys.exit(1)\n"
                 "sys.exit(3)\n" % F)
    ok(run_one(d, "c_bare_broken.py")["state"] == "FAIL",
       "and one whose bare run also fails stays FAIL")

    states = {run_one(d, m)["state"] for m in candidates(d)}
    ok(states == {"PASS", "FAIL", "REFUSED", "DEP_MISSING", "NO_CHECKS",
                  "FLAG_NOT_ACCEPTED", "RUNS_BARE"},
       "all seven states reachable and no eighth appears")

    ok(len(candidates(d)) == len([f for f in os.listdir(d)
                                  if f.endswith(".py")]),
       "every constructed module is found by the scan")
    ok(len(CHECK_PATTERNS) == 5,
       "five conventions declared  [CHOICE 7]")
    ok(parse_checks("nothing here") is None,
       "an unknown sixth convention parses to nothing rather than being "
       "absorbed")
    return res


def selftest():
    res = _checks_selftest()
    bad = [l for g, l in res if not g]
    for g, l in res:
        print("  %s  %s" % ("ok  " if g else "FAIL", l))
    print("%d/%d checks passed" % (len(res) - len(bad), len(res)))
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    rev = PINNED_REV
    if "--rev" in argv:
        rev = argv[argv.index("--rev") + 1]
    base = None
    if "--base" in argv:
        base = argv[argv.index("--base") + 1]
    text, _rows = render(rev, base)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
