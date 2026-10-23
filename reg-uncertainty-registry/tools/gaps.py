#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
gaps.py -- every gap in the registry, as the nodes that carry it. Gaps are
nodes, never blanks (WO-REG-1a): each line below is an object a query can
reach, with the reason it is a gap.

    absences          ENDPOINT_ABSENCE (NOT_ASSESSED / NOT_REQUIRED /
                      NOT_RESOLVED / NOT_LOCATED)
    non-decisions     NON_DECISION cases: no agency decision on the question
    unmapped ids      SUBSTANCE / ENDPOINT with only a local id
    authority gaps    AUTHORITY citations UNREACHABLE, and the cases whose
                      chains pass through them
    unlocated inputs  inputs relied on and not located (EV-U...)
    frames            frames named and not loaded
    disclosure        cases with no located disclosure record (a CONFLICT
                      node in state UNREACHABLE: never 'no conflict')
    ledger            claim rows not searched in this session (UNREACHABLE)
                      and rows searched and corrected

Library + CLI (python3 tools/gaps.py [--section NAME]); checks() is called by
validate.py. Stdlib only.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglib  # noqa: E402


def collect(reg):
    out = {}
    out["absences"] = [(a["id"], "%s x %s" % (a["substance"], a["endpoint"]), a["state"], a["note"])
                       for a in sorted(reg.of("ENDPOINT_ABSENCE"), key=lambda x: x["id"])]
    out["non_decisions"] = [(c["id"], c["frame"], c["title"], "")
                            for c in reg.cases() if c["type"] == "NON_DECISION"]
    out["unmapped_ids"] = [(o["id"], o["type"], o["id_state"], "")
                           for o in sorted(reg.of("SUBSTANCE", "ENDPOINT"), key=lambda x: x["id"])
                           if o["id_state"] == "LOCAL_ONLY"]
    auth_gap = sorted(a["id"] for a in reg.of("AUTHORITY")
                      if a["verification"]["state"] == "UNREACHABLE")
    users = {}
    for e in reg.edges:
        if e["type"] == "authorized_by" and e["to"] in auth_gap:
            users.setdefault(e["to"], []).append(e["from"])
    out["authority_gaps"] = [(a, reg.get(a)["level"], reg.get(a)["citation"],
                              "used by " + (", ".join(sorted(users.get(a, []))) or "no case"))
                             for a in auth_gap]
    out["unlocated_inputs"] = [(o["id"], o["kind"], o["statement"][:60], o.get("unlocated_reason", ""))
                               for o in sorted(reg.of("EVIDENCE"), key=lambda x: x["id"])
                               if o["kind"] == "unlocated_input"
                               or (o["id"].startswith("EV-U") and o["kind"] == "absence")]
    out["frames"] = [(o["id"], "gap", o["statement"][:60], o["verification"]["reason"])
                     for o in sorted(reg.of("EVIDENCE"), key=lambda x: x["id"]) if o["kind"] == "gap"]
    out["disclosure"] = [(c["id"], c["decision"], c["record_state"], "")
                         for c in sorted(reg.of("CONFLICT"), key=lambda x: x["id"])
                         if c["conflict_type"] == "disclosure_record" and c["record_state"] != "FOUND"]
    led = [o for o in reg.of("EVIDENCE") if o["verification"].get("ledger_row")]
    out["ledger_unsearched"] = [(o["id"], o["verification"]["state"], o["statement"][:60], "")
                                for o in sorted(led, key=lambda x: x["id"])
                                if o["verification"]["reached"] == "N"]
    out["ledger_corrected"] = [(o["id"], o["verification"]["state"], o["statement"][:60],
                                (o["verification"]["corrected_value"] or "")[:80])
                               for o in sorted(led, key=lambda x: x["id"])
                               if o["verification"]["state"] == "CORRECTED"]
    return out


def render(reg, section=None):
    out = []
    for name, rows in collect(reg).items():
        if section and name != section:
            continue
        out.append("== %s: %d" % (name, len(rows)))
        if name in ("ledger_unsearched", "unmapped_ids") and section is None:
            out.append("   (list with --section %s)" % name)
            continue
        for r in rows:
            out.append("   " + "  ".join(str(x) for x in r if x != ""))
    return out


def checks(reg):
    errs, n = [], 0
    g = collect(reg)
    for name, rows in g.items():
        n += 1
        ids = [r[0] for r in rows]
        if len(ids) != len(set(ids)):
            errs.append("%s lists an id twice" % name)
        for r in rows:
            if reg.get(r[0]) is None:
                errs.append("%s: %s is not an object" % (name, r[0]))
    # every gap carries a reason
    for o in reg.of("ENDPOINT_ABSENCE"):
        n += 1
        if not o.get("note"):
            errs.append("%s: absence without a note" % o["id"])
    for r in g["unlocated_inputs"]:
        n += 1
        if not r[3]:
            errs.append("%s: unlocated input without a reason" % r[0])
    # known answers: the work order's example absence, and the five retyped rows
    n += 1
    ea = [r for r in g["absences"] if r[0] == "EA-01"]
    if not ea or ea[0][2] != "NOT_ASSESSED" or "glyphosate" not in ea[0][1]:
        errs.append("EA-01 glyphosate x gut microbiome not NOT_ASSESSED")
    n += 1
    nd = {r[0] for r in g["non_decisions"] if r[1] != "R8"}
    if nd != {"B07", "B08", "C08", "C10", "E01"}:
        errs.append("non-decisions in the sample %s, want B07 B08 C08 C10 E01" % sorted(nd))
    return n, errs


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("gaps.py: checks run in tools/validate.py --selftest\n")
        return 2
    section = argv[argv.index("--section") + 1] if "--section" in argv else None
    print("\n".join(render(reglib.Registry(), section)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
