#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
symmetry.py -- SYMMETRY-FAIL: two decisions with a matched profile that
went in different directions, where neither carries a named exception.

    profile     (U grade, C_permit grade, C_restrict grade) [CHOICE]: the
                three inputs RUS-0.2 reads to set a floor. C_restrict is
                read from the source sums ("src") or the registry's second
                coding ("reg"); both are reported.
    direction   relative to the bearer of the cost of caution, on the
                agency's own action (permissive = go_ahead | warn)
    exception   R1 (market-status scope), R3 (forced_action), R5 (emergency):
                the rules that set the floor without the matrix. A pair is a
                SYMMETRY-FAIL only if neither member carries one.

A SYMMETRY-FAIL is a pair the standard grades alike and the agencies did not;
it says nothing about which member was right. Each pair also shows both
members' cost-bearer groups under Rule S: a pair whose members differ in
group is where the cost-bearer reading would speak (a mark, not a finding).

Scope: coded sample only by default (NCR-N21); --all adds the R8 rows,
reported apart. Library + CLI; checks() is called by validate.py.
Stdlib only.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglib  # noqa: E402

PERMISSIVE = ("go_ahead", "warn")


def val(o, f):
    c = o["claims"].get(f)
    return None if c is None else c["value"]


def profile(o, side="src"):
    c = o["consequence"]
    cr = c["C_restrict"]["registry"] if side == "reg" else c["C_restrict"]["source"]
    if cr is None:
        cr = c["C_restrict"]["source"]
    return (val(o, "U_grade"), c["C_permit"]["grade"], cr["grade"])


def exceptions(o):
    out = []
    if val(o, "r1") not in (None, "none") and val(o, "r1_scope") == "market_status":
        out.append("R1")
    if val(o, "forced_action"):
        out.append("R3")
    if val(o, "r5"):
        out.append("R5")
    return out


def direction(o):
    return "permissive" if val(o, "action_direction") in PERMISSIVE else "restrictive"


def pairs(cases, side="src"):
    by = {}
    for o in cases:
        if "consequence" not in o:
            continue
        by.setdefault(profile(o, side), []).append(o)
    out = []
    for prof in sorted(by, key=lambda p: tuple(str(x) for x in p)):
        group = sorted(by[prof], key=lambda o: o["id"])
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                if direction(a) == direction(b):
                    continue
                ea, eb = exceptions(a), exceptions(b)
                out.append({"profile": prof, "a": a["id"], "b": b["id"],
                            "dir_a": direction(a), "dir_b": direction(b),
                            "exc_a": ea, "exc_b": eb,
                            "group_a": val(a, "cost_group_S"), "group_b": val(b, "cost_group_S"),
                            "fail": not ea and not eb})
    return out


def render(reg, include_r8=False):
    out = []
    frames = ("A", "B", "C", "D", "E") + (("R8",) if include_r8 else ())
    cases = [o for o in reg.cases() if o["frame"] in frames and "consequence" in o]
    for side in ("src", "reg"):
        ps = pairs(cases, side)
        fails = [p for p in ps if p["fail"]]
        out.append("== C_restrict %s: %d profile-matched pairs with different directions, %d SYMMETRY-FAIL (no named exception)"
                   % (side, len(ps), len(fails)))
        for p in ps:
            out.append("%-4s %-4s %-14s %s/%s  exceptions %s/%s  groups %s/%s  %s" % (
                p["a"], p["b"], "/".join(p["profile"]), p["dir_a"][:4], p["dir_b"][:4],
                ",".join(p["exc_a"]) or "-", ",".join(p["exc_b"]) or "-",
                p["group_a"], p["group_b"], "SYMMETRY-FAIL" if p["fail"] else "exception named"))
    return out


def checks(reg):
    errs, n = [], 0
    def mk(i, U, cp, cr, act, **kw):
        cl = {"U_grade": U, "action_direction": act, "r1": kw.get("r1", "none"),
              "r1_scope": "market_status", "forced_action": kw.get("forced", False),
              "r5": False, "cost_group_S": "concentrated"}
        return {"id": i, "claims": {k: {"value": v} for k, v in cl.items()},
                "consequence": {"C_permit": {"grade": cp},
                                "C_restrict": {"source": {"grade": cr}, "registry": None}}}
    # known answers on constructed cases
    fx = [mk("X1", "U3", "C3", "C2", "go_ahead"), mk("X2", "U3", "C3", "C2", "decline"),
          mk("X3", "U3", "C3", "C2", "decline", forced=True), mk("X4", "U2", "C3", "C2", "hold")]
    ps = pairs(fx)
    got = sorted((p["a"], p["b"], p["fail"]) for p in ps)
    want = [("X1", "X2", True), ("X1", "X3", False)]
    n += 1
    if got != want:
        errs.append("constructed fixture: %s, want %s" % (got, want))
    # on the registry: a pair is reported once, members share a profile, directions differ
    for side in ("src", "reg"):
        cases = [o for o in reg.cases() if o.get("in_sample")]
        seen = set()
        for p in pairs(cases, side):
            n += 1
            key = (p["a"], p["b"])
            if key in seen or (p["b"], p["a"]) in seen:
                errs.append("pair %s reported twice" % (key,))
            seen.add(key)
            a, b = reg.get(p["a"]), reg.get(p["b"])
            if profile(a, side) != profile(b, side) or direction(a) == direction(b):
                errs.append("pair %s does not meet the definition" % (key,))
    return n, errs


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("symmetry.py: checks run in reg-uncertainty-registry/tools/validate.py --selftest\n")
        return 2
    print("\n".join(render(reglib.Registry(), include_r8="--all" in argv)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
