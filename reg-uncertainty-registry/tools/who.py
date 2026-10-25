#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
who.py -- who decided, who advised, who was overruled, who paid, and what
conflict records exist (WO-REG-1a).

    python3 tools/who.py A01            the people and bodies on one case
    python3 tools/who.py --actor ID     every case an actor appears on, by role
    python3 tools/who.py --overruled    every case where a recommending or
                                        reviewing body was set aside

Roles come from edges: decided_by, recommended_by, overruled, sponsored_by;
conflicts from CONFLICT nodes (conflict_of / concerns); delegation and
funding from delegated_from / funded_by. A case with no located disclosure
record shows its CONFLICT node in state UNREACHABLE: absence of a record is
never read as absence of a conflict. Every role edge is PROPOSED (one
coder, ACT-REGISTRY) unless stated otherwise.

Library + CLI; checks() is called by validate.py. Stdlib only.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglib  # noqa: E402

ROLES = ("decided_by", "recommended_by", "overruled", "sponsored_by")


def name(reg, aid):
    a = reg.get(aid)
    return "%s (%s)" % (a["name"], a["actor_type"]) if a else aid


def on_case(reg, cid):
    out = {r: sorted(e["to"] for e in reg.out_edges(cid, r)) for r in ROLES}
    out["conflicts"] = sorted(
        (c["id"], c["actor_id"], c["conflict_type"], c["record_state"])
        for c in reg.of("CONFLICT") if c["decision"] == cid)
    return out


def by_actor(reg, aid):
    out = {}
    for e in reg.edges:
        if e["type"] in ROLES and e["to"] == aid:
            out.setdefault(e["type"], []).append(e["from"])
    up = [e["to"] for e in reg.out_edges(aid, "delegated_from")]
    down = [e["from"] for e in reg.in_edges(aid, "delegated_from")]
    funds = [e["to"] for e in reg.out_edges(aid, "funded_by")]
    confl = sorted(c["id"] for c in reg.of("CONFLICT") if c["actor_id"] == aid)
    return {k: sorted(v) for k, v in out.items()}, up, down, funds, confl


def overruled(reg):
    rows = []
    for e in reg.edges:
        if e["type"] == "overruled":
            dec = sorted(x["to"] for x in reg.out_edges(e["from"], "decided_by"))
            rows.append((e["from"], e["to"], dec))
    return sorted(rows)


def render_case(reg, cid):
    o = reg.get(cid)
    w = on_case(reg, cid)
    out = ["== %s  %s" % (cid, o["title"])]
    for r in ROLES:
        for a in w[r]:
            out.append("%-15s %s" % (r.replace("_by", ""), name(reg, a)))
    for cfid, aid, ctype, st in w["conflicts"]:
        out.append("%-15s %s %s %s [%s]" % ("conflict", cfid, ctype, aid, st))
    return out


def checks(reg):
    errs, n = [], 0
    for e in reg.edges:
        if e["type"] in ROLES:
            n += 1
            if reg.get(e["to"]) is None or reg.get(e["to"])["type"] != "ACTOR":
                errs.append("%s %s -> %s: not an ACTOR" % (e["type"], e["from"], e["to"]))
    graded = [o for o in reg.cases() if o["frame"] in ("A", "B", "C", "D", "E", "R8")]
    for o in graded:
        n += 1
        if not reg.out_edges(o["id"], "decided_by"):
            errs.append("%s: no decided_by edge (a decision-maker is a node or a gap)" % o["id"])
    # known answers from the curation (A01: FDA decided, advisory committee overruled)
    w = on_case(reg, "A01")
    n += 1
    if "ACT-FDA-CDER" not in w["decided_by"] or "ACT-AC-PCNS" not in w["overruled"]:
        errs.append("A01 roles: %s" % w)
    n += 1
    if not any(c[2] == "disclosure_record" for c in on_case(reg, "B05")["conflicts"]):
        errs.append("B05 has no disclosure-record node")
    return n, errs


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("who.py: checks run in reg-uncertainty-registry/tools/validate.py --selftest\n")
        return 2
    reg = reglib.Registry()
    if "--actor" in argv:
        aid = argv[argv.index("--actor") + 1]
        roles, up, down, funds, confl = by_actor(reg, aid)
        print("== %s" % name(reg, aid))
        for r, ids in sorted(roles.items()):
            print("%-15s %s" % (r, ", ".join(
                "%s(%s)" % (i, (reg.get(i)["claims"].get("action_direction")
                                or reg.get(i)["claims"].get("direction") or {}).get("value", "-"))
                for i in ids)))
        print("delegated from  %s" % (", ".join(up) or "-"))
        print("delegates to    %s" % (", ".join(down) or "-"))
        print("funded by       %s" % (", ".join(funds) or "-"))
        print("conflicts       %s" % (", ".join(confl) or "none located"))
        return 0
    if "--overruled" in argv:
        rows = overruled(reg)
        print("== %d overrule edges" % len(rows))
        for cid, body, dec in rows:
            print("%-5s %-28s set aside by %s" % (cid, body, ", ".join(dec)))
        return 0
    ids = [a for a in argv if not a.startswith("--")] or [o["id"] for o in reg.cases()
                                                         if o.get("in_sample")]
    for cid in ids:
        print("\n".join(render_case(reg, cid)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
