#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
_shared.py - the small amount every sim in this folder needs.

Wrapping, a runner, and the two cross-cutting readouts that every module must
expose: `confidence()` separate from the pattern and never resolved, and
`breaks()` naming where the module fails.

stdlib only, CC0.
"""

import argparse
import sys


def wrap(t, ind="  ", w=72):
    words, lines, cur = t.split(), [], ind
    for x in words:
        if len(cur) + len(x) + 1 > w and cur.strip():
            lines.append(cur.rstrip())
            cur = ind + x + " "
        else:
            cur += x + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def tail(mod):
    """Render the two mandatory readouts identically across modules."""
    L = ["", "-" * 72, "", "  CONFIDENCE, reported separately and not resolved"]
    c = mod.confidence()
    for k in sorted(c):
        L.append("    %-36s %s" % (k, c[k]))
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in mod.breaks():
        L.extend(wrap("- " + b, "    "))
    return L


def run(mod, name):
    ap = argparse.ArgumentParser(description=name)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return mod.selftest()
    print(mod.report())
    return 0


def checker():
    """Returns (ck, done). ck(label, cond) records; done() prints and rc's."""
    state = {"f": 0, "k": 0}

    def ck(label, cond):
        state["k"] += 1
        if not cond:
            state["f"] += 1
            print("FAIL %s" % label)

    def done():
        print("%d/%d checks passed" % (state["k"] - state["f"], state["k"]))
        return 1 if state["f"] else 0

    return ck, done
