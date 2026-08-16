#!/usr/bin/env python3
"""
check_gate_drift.py -- there is one gate. Find every copy of it.

CC0-1.0. Stdlib only. Run from anywhere in the repo.

    python3 tools/check_gate_drift.py [repo_root]

WHY THIS EXISTS
---------------
Five pre-repair copies of reasoning-gate files have arrived across three
drops -- gate.py, guards.json, make_docs.py, README.md, GUARDS.md -- each
missing repairs that were already made upstream. Recorded as
measurement-fork/CLAIM_TABLE.md MF_006 and MF_011.

A stale copy is worse than no copy. It runs, it produces plausible output,
and it silently lacks the guard behaviour the canonical version has: no
denial records, no claim scope, a registry that accepts a blank
fail_message, a G-FIT documented at the wrong stage. Nothing in the repo
noticed. This does.

THE RULE
--------
reasoning-gate/ holds the gate. Everything else IMPORTS it:

    GATE_SRC = os.environ.get("GATE_SRC", ".../reasoning-gate")
    sys.path.insert(0, GATE_SRC)
    from gate import Gate, Resolution, Control

msiaf-gdprf-bridge/, reasoning-dial/gate_dial.py and
measurement-fork/gate_fork.py all do this. A copy cannot drift if there is
no copy.

EXIT CODES
----------
    0   one canonical set, no copies, docs in sync
    1   drift found: a stale copy, or GUARDS.md out of sync with guards.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

CANONICAL_DIR = "reasoning-gate"
CANONICAL = ("gate.py", "guards.json", "GUARDS.md", "make_docs.py")

# Content markers. A file is a copy of the gate family if it carries BOTH
# markers for one of them, whatever it has been renamed to. Name matching
# alone misses `gate_2.py` and `guards_v1.json`.
#
# Two markers, not one, and one of each pair is a code construct. A README
# quoting the gate's docstring is not a copy of the gate; a file containing
# `class GateError(Exception)` is. The first version of this file matched on
# one marker and flagged itself, which is the check working and the rule
# being wrong.
MARKERS = {
    "gate.py": ("fail-closed reasoning gate for simulation harnesses",
                "class GateError(Exception)"),
    "guards.json": ('"id": "G-LAYER"', '"fail_message"'),
    "GUARDS.md": ("### G-LAYER - every quantity tagged with its origin layer",
                  "## POST - at report assembly"),
    "make_docs.py": ("render GUARDS.md from guards.json", "def render(reg)"),
}

SKIP_DIRS = {".git", "__pycache__", "node_modules", "runs", "legacy"}

RULE = "=" * 70


SELF_SIGNATURE = ("MARKERS = {", "CANONICAL_DIR = ")


def _defines_markers(text: str) -> bool:
    """True for this checker itself, identified by content not by path.

    Path-based self-skip breaks the moment the tool scans a tree that
    contains a copy of the tool -- which is exactly what it is for.
    """
    return all(sig in text for sig in SELF_SIGNATURE)


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def find_root(start: str) -> str:
    """Walk up until reasoning-gate/ is a child."""
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, CANONICAL_DIR)):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("no %s/ found above %s" % (CANONICAL_DIR, start))
        cur = parent


def scan(root: str) -> list[tuple[str, str, bool]]:
    """Return (relpath, which_canonical_file, is_identical) for every copy."""
    canon_dir = os.path.join(root, CANONICAL_DIR)
    digests = {}
    for name in CANONICAL:
        p = os.path.join(canon_dir, name)
        if not os.path.exists(p):
            raise SystemExit("canonical %s is missing from %s"
                             % (name, CANONICAL_DIR))
        digests[name] = sha(p)

    copies = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if os.path.abspath(dirpath) == os.path.abspath(canon_dir):
            continue
        for fn in filenames:
            if not fn.endswith((".py", ".json", ".md")):
                continue
            full = os.path.join(dirpath, fn)
            try:
                with open(full, "r", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            if _defines_markers(text):
                continue      # this checker, wherever it lives. It has to
                              # quote the markers, and matching itself is
                              # the same self-reference bug twice.
            for name, markers in MARKERS.items():
                if all(m in text for m in markers):
                    rel = os.path.relpath(full, root)
                    copies.append((rel, name, sha(full) == digests[name]))
                    break
    return copies


def docs_in_sync(root: str) -> bool:
    """GUARDS.md must be exactly what make_docs.py renders from guards.json."""
    canon = os.path.join(root, CANONICAL_DIR)
    sys.path.insert(0, canon)
    try:
        import make_docs
    except ImportError:
        return False
    with open(os.path.join(canon, "guards.json")) as fh:
        reg = json.load(fh)
    with open(os.path.join(canon, "GUARDS.md")) as fh:
        return fh.read() == make_docs.render(reg)


def importers(root: str) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            try:
                with open(full, "r", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            if ("from gate import" in text
                    and not all(m in text for m in MARKERS["gate.py"])):
                out.append(os.path.relpath(full, root))
    return sorted(out)


def main() -> int:
    root = find_root(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())

    print(RULE)
    print("GATE DRIFT CHECK  --  %s" % root)
    print(RULE)

    print("\ncanonical  %s/" % CANONICAL_DIR)
    for name in CANONICAL:
        print("    %-16s %s" % (name, sha(os.path.join(root, CANONICAL_DIR, name))))

    sync = docs_in_sync(root)
    print("\nGUARDS.md matches make_docs.py(guards.json):  %s"
          % ("yes" if sync else "NO -- regenerate"))

    imps = importers(root)
    print("\nimports the gate (%d):" % len(imps))
    for i in imps:
        print("    %s" % i)

    copies = scan(root)
    print("\ncopies of gate-family files outside %s/:" % CANONICAL_DIR)
    if not copies:
        print("    none")
    for rel, name, identical in copies:
        print("    %-46s copy of %-12s %s"
              % (rel, name, "IDENTICAL" if identical else "DRIFTED"))

    drifted = [c for c in copies if not c[2]]
    identical = [c for c in copies if c[2]]

    print("\n" + RULE)
    if not copies and sync:
        print("CLEAN. One gate, no copies, docs in sync.")
        return 0

    if drifted:
        print("DRIFT. %d stale cop%s of the gate family:"
              % (len(drifted), "y" if len(drifted) == 1 else "ies"))
        for rel, name, _ in drifted:
            print("    %s  differs from %s/%s" % (rel, CANONICAL_DIR, name))
        print()
        print("A stale copy runs, produces plausible output, and silently")
        print("lacks the guard behaviour the canonical version has. Delete")
        print("it and import instead:")
        print()
        print("    GATE_SRC = os.environ.get('GATE_SRC', '.../%s')"
              % CANONICAL_DIR)
        print("    sys.path.insert(0, GATE_SRC)")
        print("    from gate import Gate, Resolution, Control")
    if identical:
        print()
        print("REDUNDANT. %d byte-identical cop%s -- not stale yet, and the"
              % (len(identical), "y" if len(identical) == 1 else "ies"))
        print("only reason a copy is ever stale is that it started identical.")
    if not sync:
        print()
        print("DOCS. GUARDS.md is not what make_docs.py renders. Run:")
        print("    cd %s && python3 make_docs.py" % CANONICAL_DIR)
    print(RULE)
    return 1


if __name__ == "__main__":
    sys.exit(main())
