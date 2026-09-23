#!/usr/bin/env python3
# run_manifest.py -- enumerate every entry point in this tree. Execute nothing.
#
# AGENTS.md section 1 names this as the first command, and says: "a lister, not a
# runner ... the manifest alone tells you what you are choosing not to measure."
# EXIT_CONTRACT.md sections 4 (R-2) and 5 both rest on the record it emits.
#
# WHY IT IS STATIC. A sweep that learns what a file is by running it has already
# spent the cost the manifest exists to let you decide about, and on a tree with
# 102 redirect stubs it collects 102 nonzero exits before it can tell you that
# none of them is a failure. So every classification here comes from the AST.
#
# WHAT IT DOES NOT DO, stated rather than implied:
#   - It runs no scanned module. No import, no exec, no eval. The only subprocess
#     is `git ls-files`, and a selftest check reads this module's own AST to
#     assert that every subprocess argv here begins with the literal "git".
#   - It does NOT perform the EXIT_CONTRACT section 5 check. That one compares a
#     VERDICT line against an exit code, and both are properties of a run. This
#     is the static half: it checks the exit code a redirect DECLARES, not the
#     one it produces. The two can disagree and only execution separates them.
#   - Classification can be wrong. Anything not matching a known shape is
#     UNCLASSIFIED and is never defaulted into a populated class, because a
#     misfiled entry point is the failure this file exists to prevent.
#   - It enumerates TRACKED files. `git ls-files` does not see an uncommitted
#     entry point, so on a dirty tree the manifest describes the committed tree
#     and is silent about your new work. Found by running it: this module was
#     absent from its own manifest until it was staged. The os.walk fallback
#     does see untracked files, and the summary line says which enumerator ran.
#   - redirect_target is a filename pulled out of a string literal by pattern.
#     That is a word-list-shaped operation and it can miss. A redirect whose
#     target cannot be extracted keeps class REDIRECT and target None.
#
# SELF-REFERENCE. This module is a tracked .py file, so it enumerates itself and
# appears in its own manifest as SELFTEST. Recorded rather than excluded: a path
# skip breaks on the one case that matters, a tree holding a copy of the tool.
#
# Stdlib only. Parses under 3.9. No network. CC0.

import ast
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# The classes. UNCLASSIFIED and UNPARSEABLE are states, not buckets of last
# resort: nothing is ever moved out of them by a default.
CLASSES = (
    "REDIRECT",      # refuses --selftest and names the real entry point
    "SELFTEST",      # --selftest runs checks
    "TEST_FILE",     # named test_* or selftest_*, no --selftest flag of its own
    "CLI",           # has a __main__ guard, no --selftest
    "LIBRARY",       # no __main__ guard, no --selftest
    "UNPARSEABLE",   # the AST could not be built; carries the reason
    "UNCLASSIFIED",  # matched no shape. Never defaulted into another class.
)

# EXIT_CONTRACT.md section 1: a redirect is state 2. Any other declared code on
# a redirect path is the redirect wearing another state's exit code.
REDIRECT_EXIT = 2

# Captures an optional directory prefix. A message naming
# `folder/tests/test_x.py` used to yield `test_x.py`, which then resolved
# beside the module and reported a live target as missing -- the first
# folder in the tree to put its test file in a subdirectory is what
# surfaced it. A flat layout hides the bug because the basename happens
# to resolve.
_PY_NAME = re.compile(r"\b((?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.py)\b")


def _literal_strings(node):
    out = []
    for n in ast.walk(node):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            out.append(n.value)
    return out


def _declared_exits(node):
    """Constant exit codes reachable in this subtree.

    sys.exit(<str>) is included as 1, because that is what CPython does with a
    string argument: print it to stderr and exit 1. A redirect written that way
    declares a failure it does not mean.
    """
    codes = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Return) and isinstance(n.value, ast.Constant):
            if isinstance(n.value.value, int) and not isinstance(n.value.value, bool):
                codes.add(n.value.value)
        if isinstance(n, ast.Call):
            name = getattr(n.func, "attr", None) or getattr(n.func, "id", None)
            if name in ("exit", "_exit") and n.args:
                a = n.args[0]
                if isinstance(a, ast.Constant) and isinstance(a.value, int) \
                        and not isinstance(a.value, bool):
                    codes.add(a.value)
                else:
                    # sys.exit("message") and friends: exits 1.
                    codes.add(1)
    return codes


def _selftest_branches(tree):
    return [n for n in ast.walk(tree)
            if isinstance(n, ast.If) and "--selftest" in ast.dump(n.test)]


def _has_main_guard(tree):
    for n in ast.walk(tree):
        if isinstance(n, ast.If) and "__main__" in ast.dump(n.test):
            return True
    return False


def classify(src, relpath):
    """Return a manifest record for one file. Reads only; runs nothing."""
    rec = {
        "path": relpath,
        "class": None,
        "invoke": None,
        "declared_exit": None,
        "redirect_target": None,
        "target_resolves": None,
        "contract_ok": None,
        "reason": "",
    }
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        rec["class"] = "UNPARSEABLE"
        rec["reason"] = "SyntaxError under python %d.%d: %s" % (
            sys.version_info[0], sys.version_info[1], e.msg)
        return rec
    except Exception as e:  # pragma: no cover - defensive
        rec["class"] = "UNPARSEABLE"
        rec["reason"] = type(e).__name__
        return rec

    branches = _selftest_branches(tree)
    if branches:
        codes = set()
        for b in branches:
            # b.body only, never b. Walking the If node sweeps in its orelse,
            # so a sys.exit(2) sitting in an unrelated `else:` on the same
            # if/elif chain was being attributed to the --selftest path. That
            # misfiled crediting-rate/crediting_rate.py, which runs 15 checks
            # and exits 0, as a REDIRECT -- telling a sweeper to skip a live
            # check. Found by running the file, not by reading the classifier.
            for stmt in b.body:
                codes |= _declared_exits(stmt)
        rec["invoke"] = ["python3", relpath, "--selftest"]
        if codes == set([REDIRECT_EXIT]):
            rec["class"] = "REDIRECT"
            rec["declared_exit"] = REDIRECT_EXIT
            rec["contract_ok"] = True
            rec["reason"] = "refuses --selftest, declares exit 2"
        elif codes and REDIRECT_EXIT not in codes and codes <= set([0, 1]):
            # A --selftest branch whose only constant exits are 0/1 and which
            # emits a message naming another .py is a redirect in intent.
            msgs = []
            for b in branches:
                for stmt in b.body:
                    msgs.extend(_literal_strings(stmt))
            target = _first_py_name(msgs, relpath)
            if target is not None:
                rec["class"] = "REDIRECT"
                rec["declared_exit"] = sorted(codes)[0]
                rec["contract_ok"] = False
                rec["reason"] = (
                    "redirect naming %s, but declares exit %d; "
                    "EXIT_CONTRACT section 1 reads that as a failure"
                    % (target, sorted(codes)[0]))
            else:
                rec["class"] = "SELFTEST"
                rec["declared_exit"] = sorted(codes)[0]
                rec["reason"] = "--selftest exits %s" % sorted(codes)
        elif not codes:
            rec["class"] = "SELFTEST"
            rec["reason"] = "--selftest dispatches to a call"
        else:
            rec["class"] = "UNCLASSIFIED"
            rec["reason"] = ("--selftest branch declares mixed exits %s; "
                             "no shape matched" % sorted(codes))
        if rec["class"] == "REDIRECT":
            msgs = []
            for b in branches:
                for stmt in b.body:
                    msgs.extend(_literal_strings(stmt))
            rec["redirect_target"] = _first_py_name(msgs, relpath)
        return rec

    base = os.path.basename(relpath)
    if base.startswith("test_") or base.startswith("selftest_"):
        rec["class"] = "TEST_FILE"
        rec["invoke"] = ["python3", relpath]
        rec["reason"] = "named as a test entry point, carries no --selftest flag"
    elif _has_main_guard(tree):
        rec["class"] = "CLI"
        rec["invoke"] = ["python3", relpath]
        rec["reason"] = "__main__ guard, no --selftest"
    else:
        rec["class"] = "LIBRARY"
        rec["reason"] = "no __main__ guard, no --selftest; not an entry point"
    return rec


def _first_py_name(strings, relpath):
    """Pull a .py filename out of redirect text, skipping the file's own name."""
    own = os.path.basename(relpath)
    for s in strings:
        for m in _PY_NAME.findall(s):
            if os.path.basename(m) != own:
                return m
    return None


def resolve_targets(records):
    """Mark whether each redirect's named target exists beside it.

    A redirect naming a file that is not there is D-4's shape one layer up: the
    pointer outlived the artifact.
    """
    for r in records:
        if r["class"] != "REDIRECT" or not r["redirect_target"]:
            continue
        target = r["redirect_target"]
        if "/" in target:
            # A message naming a path names it from the repo root, which is
            # how every redirect message in the tree is written.
            cand = os.path.join(ROOT, target)
        else:
            cand = os.path.join(ROOT, os.path.dirname(r["path"]), target)
        r["target_resolves"] = os.path.isfile(cand)


def tracked_files():
    """Enumerate tracked .py files. git if available, walk if not; say which."""
    try:
        out = subprocess.run(["git", "ls-files", "*.py"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
        paths = [p for p in out.split("\n") if p.strip()]
        if paths:
            return sorted(paths), "git ls-files"
    except Exception:
        pass
    paths = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", "__pycache__", "node_modules")]
        for fn in filenames:
            if fn.endswith(".py"):
                paths.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))
    return sorted(paths), "os.walk (git unavailable)"


def build():
    paths, source = tracked_files()
    records = []
    for p in paths:
        try:
            src = io.open(os.path.join(ROOT, p), encoding="utf-8").read()
        except Exception as e:
            records.append({"path": p, "class": "UNPARSEABLE", "invoke": None,
                            "declared_exit": None, "redirect_target": None,
                            "target_resolves": None, "contract_ok": None,
                            "reason": "unreadable: %s" % type(e).__name__})
            continue
        records.append(classify(src, p))
    resolve_targets(records)
    return records, source


def violations(records):
    out = []
    for r in records:
        if r["class"] == "REDIRECT" and r["contract_ok"] is False:
            out.append(r)
        if r["class"] == "REDIRECT" and r["target_resolves"] is False:
            out.append(r)
    return out


def summary(records, source):
    lines = []
    lines.append("run-manifest -- %d files enumerated via %s" % (len(records), source))
    lines.append("nothing was executed; every class below is read from the AST")
    lines.append("")
    counts = {}
    for r in records:
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    for c in CLASSES:
        lines.append("  %-14s %4d" % (c, counts.get(c, 0)))
    lines.append("")
    red = [r for r in records if r["class"] == "REDIRECT"]
    lines.append("REDIRECTS: %d. AGENTS.md section 4 and EXIT_CONTRACT section 1" % len(red))
    lines.append("both class these as NOT failures. A sweep that runs --selftest")
    lines.append("across the tree collects these as nonzero exits; they are the")
    lines.append("caller using the wrong door, and each one names the right one.")
    lines.append("")
    unres = [r for r in red if r["target_resolves"] is False]
    noname = [r for r in red if r["redirect_target"] is None]
    lines.append("  target named and resolves   %4d" % len([r for r in red if r["target_resolves"]]))
    lines.append("  target named, MISSING       %4d" % len(unres))
    lines.append("  target not extractable      %4d" % len(noname))
    lines.append("")
    v = violations(records)
    if v:
        lines.append("CONTRACT VIOLATIONS: %d" % len(v))
        for r in v:
            lines.append("  %s" % r["path"])
            lines.append("      %s" % r["reason"])
    else:
        lines.append("CONTRACT VIOLATIONS: 0")
    lines.append("")
    unp = [r for r in records if r["class"] == "UNPARSEABLE"]
    if unp:
        lines.append("UNPARSEABLE: %d (a state, not a failure and not a pass)" % len(unp))
        for r in unp:
            lines.append("  %s" % r["path"])
            lines.append("      %s" % r["reason"])
        lines.append("")
    lines.append("NOT DONE HERE: the EXIT_CONTRACT section 5 check compares a VERDICT")
    lines.append("line against a real exit code. Both are properties of a run. This")
    lines.append("file checks the code a redirect DECLARES, never the one it emits.")
    return "\n".join(lines)


# ---------------------------------------------------------------- selftest

def _fixtures():
    """Constructed sources, one per class, plus a planted violation.

    Built as strings rather than as files in the tree: a fixture .py checked in
    here would be enumerated by the very scan it exists to test.
    """
    return [
        ("redirect_ok.py",
         'import sys\ndef main(argv):\n'
         '    if "--selftest" in argv:\n'
         '        print("redirect_ok.py is the instrument; run test_thing.py")\n'
         '        return 2\n    return 0\n',
         "REDIRECT", True),
        ("redirect_exit2.py",
         'import sys\ndef main(argv):\n'
         '    if "--selftest" in argv:\n'
         '        sys.stderr.write("no selftest; run test_other.py\\n")\n'
         '        sys.exit(2)\n    return 0\n',
         "REDIRECT", True),
        ("redirect_bad.py",
         'import sys\ndef main(argv):\n'
         '    if "--selftest" in argv:\n'
         '        sys.exit("redirect_bad.py is a library; run: python3 score.py")\n'
         '    return 0\n',
         "REDIRECT", False),
        ("has_selftest.py",
         'def selftest():\n    return 0\ndef main(argv):\n'
         '    if "--selftest" in argv:\n        return selftest()\n    return 0\n',
         "SELFTEST", None),
        ("test_thing.py",
         'def go():\n    return 1\nif __name__ == "__main__":\n    go()\n',
         "TEST_FILE", None),
        ("plain_cli.py",
         'def main():\n    print("hi")\nif __name__ == "__main__":\n    main()\n',
         "CLI", None),
        ("plain_lib.py",
         'def helper(x):\n    return x + 1\n',
         "LIBRARY", None),
        ("broken.py",
         'def main(:\n    pass\n',
         "UNPARSEABLE", None),
        ("elif_else_exit2.py",
         'import sys\ndef main():\n'
         '    if "--selftest" in sys.argv:\n        selftest()\n'
         '    elif len(sys.argv) == 2:\n        go()\n'
         '    else:\n        print("usage: ...")\n        sys.exit(2)\n',
         "SELFTEST", None),
        ("mixed.py",
         'def main(argv):\n'
         '    if "--selftest" in argv:\n'
         '        if argv[0]:\n            return 2\n        return 7\n    return 0\n',
         "UNCLASSIFIED", None),
    ]


def selftest():
    checks = 0
    failed = 0

    def ck(cond, label):
        nonlocal checks, failed
        checks += 1
        if not cond:
            failed += 1
            print("FAIL  %s" % label)
        else:
            print("ok    %s" % label)

    print("-- classifier: fires on each shape, and does not fire on the others")
    seen_classes = set()
    for name, src, want_class, want_ok in _fixtures():
        rec = classify(src, name)
        ck(rec["class"] == want_class,
           "%-20s -> %s (got %s)" % (name, want_class, rec["class"]))
        seen_classes.add(rec["class"])
        if want_ok is not None:
            ck(rec["contract_ok"] is want_ok,
               "%-20s contract_ok is %s" % (name, want_ok))

    print("\n-- the null: every declared class is reached by some fixture")
    for c in CLASSES:
        ck(c in seen_classes, "class %s reached by a fixture" % c)

    print("\n-- the planted violation is caught, and its siblings are not")
    recs = [classify(s, n) for n, s, _c, _o in _fixtures()]
    v = violations(recs)
    ck(len(v) == 1, "exactly one fixture violates (got %d)" % len(v))
    ck(v and v[0]["path"] == "redirect_bad.py",
       "the violator is redirect_bad.py")

    print("\n-- redirect target extraction, and its stated limit")
    r = classify(_fixtures()[0][1], "redirect_ok.py")
    ck(r["redirect_target"] == "test_thing.py",
       "target extracted from the message")
    r2 = classify('def main(argv):\n'
                  '    if "--selftest" in argv:\n'
                  '        print("run the checks in the sibling folder")\n'
                  '        return 2\n    return 0\n', "quiet.py")
    ck(r2["class"] == "REDIRECT" and r2["redirect_target"] is None,
       "a redirect naming no .py stays REDIRECT with target None, not UNCLASSIFIED")
    r3 = classify('def main(argv):\n'
                  '    if "--selftest" in argv:\n'
                  '        print("solo.py carries no checks of its own")\n'
                  '        return 2\n    return 0\n', "solo.py")
    ck(r3["redirect_target"] is None,
       "a message naming only the file's own basename yields target None")

    r4 = classify('def main(argv):\n'
                  '    if "--selftest" in argv:\n'
                  '        print("run: python3 folder/tests/test_x.py")\n'
                  '        return 2\n    return 0\n', "folder/x.py")
    ck(r4["redirect_target"] == "folder/tests/test_x.py",
       "a target in a subdirectory keeps its path; taking the basename "
       "resolved it beside the module and reported a live file as missing")
    r5 = classify('def main(argv):\n'
                  '    if "--selftest" in argv:\n'
                  '        print("folder/solo.py carries no checks")\n'
                  '        return 2\n    return 0\n', "folder/solo.py")
    ck(r5["redirect_target"] is None,
       "the own-name skip compares basenames, so a path form of the file's "
       "own name is still skipped")

    print("\n-- absent is not a bucket")
    ck(classify('x = 1\n', "z.py")["contract_ok"] is None,
       "contract_ok is None where no contract applies, never True")
    ck(classify('x = 1\n', "z.py")["declared_exit"] is None,
       "declared_exit is None where none is declared, never 0")

    print("\n-- this module runs nothing it scans")
    own = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(own)
    bad = []
    subp = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            # The receiver matters. A first pass flagged re.compile, which is
            # the word-list failure this check exists to avoid, committed one
            # level down: it matched the NAME and ignored what it was called
            # on. Only a bare builtin call executes a string; re.compile does
            # not. So exec/eval/compile/__import__ are flagged as ast.Name
            # only, and import_module is flagged wherever it appears.
            if isinstance(n.func, ast.Name) and n.func.id in (
                    "exec", "eval", "compile", "__import__"):
                bad.append(n.func.id)
            if getattr(n.func, "attr", None) == "import_module":
                bad.append("import_module")
            nm = getattr(n.func, "attr", None) or getattr(n.func, "id", None)
            if nm in ("run", "Popen", "call", "check_output") and n.args:
                a = n.args[0]
                if isinstance(a, ast.List) and a.elts:
                    first = a.elts[0]
                    if isinstance(first, ast.Constant):
                        subp += 1
                        if first.value != "git":
                            bad.append("subprocess argv0=%r" % (first.value,))
    ck(not bad, "no exec/eval/import-by-name, and every subprocess argv0 is git")
    ck(subp == 1, "exactly one subprocess call site (got %d)" % subp)
    # the assertion above is read from the AST, not grepped: a substring scan
    # fires on this comment, which names the constructs it refuses.
    planted = ast.parse('import subprocess\nsubprocess.run(["python3", "x.py"])\n')
    hit = False
    for n in ast.walk(planted):
        if isinstance(n, ast.Call):
            nm = getattr(n.func, "attr", None) or getattr(n.func, "id", None)
            if nm == "run" and n.args and isinstance(n.args[0], ast.List):
                first = n.args[0].elts[0]
                if isinstance(first, ast.Constant) and first.value != "git":
                    hit = True
    ck(hit, "the subprocess check fires on a planted non-git argv0")

    def _exec_hits(source):
        got = []
        for q in ast.walk(ast.parse(source)):
            if isinstance(q, ast.Call):
                if isinstance(q.func, ast.Name) and q.func.id in (
                        "exec", "eval", "compile", "__import__"):
                    got.append(q.func.id)
                if getattr(q.func, "attr", None) == "import_module":
                    got.append("import_module")
        return got

    ck(_exec_hits('exec("x = 1")') == ["exec"],
       "the exec check fires on a planted bare exec")
    ck(_exec_hits('import importlib\nimportlib.import_module("m")')
       == ["import_module"], "and on a planted import_module")
    ck(_exec_hits('import re\nre.compile("x")') == [],
       "and stays silent on re.compile, the receiver that tripped the first pass")

    print("\n-- record shape is what a runner needs")
    keys = set(classify('x = 1\n', "z.py").keys())
    ck(keys == set(["path", "class", "invoke", "declared_exit",
                    "redirect_target", "target_resolves", "contract_ok",
                    "reason"]), "record carries exactly the declared fields")
    ck(json.loads(json.dumps(classify('x = 1\n', "z.py"))) is not None,
       "a record round-trips through json")

    print("\nchecks: %d   failed: %d" % (checks, failed))
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if failed == 0 else "FAIL", checks, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    records, source = build()
    if "--jsonl" in argv:
        for r in records:
            print(json.dumps(r, sort_keys=True))
        return 0
    if "--write" in argv:
        dest = os.path.join(ROOT, "run-manifest.jsonl")
        with io.open(dest, "w", encoding="utf-8") as fh:
            for r in records:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
        print("wrote %s (%d records)" % (dest, len(records)))
    print(summary(records, source))
    v = violations(records)
    print("")
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if not v else "FAIL", len(records), len(v)))
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
