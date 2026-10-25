#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
chain.py -- for one decision, every chain it rests on, with the
verification state at each hop, and the single-failure flags.

    authority   statute -> regulation/guidance -> decision, in the order the
                authorized_by edges carry; each AUTHORITY's ledger state
    evidence    EVIDENCE nodes supporting the case, each with its SOURCE(s)
                and state; forcing evidence (forced_by) marked
    actors      decided_by / recommended_by / overruled / sponsored_by
    unlocated   inputs relied on and not located (EV-U..., UNREACHABLE)

Single-failure flags (WO Part A: flag any conclusion resting on one source
or one coder):
    ONE_CODER          every PROPOSED field on the case has one coder and no
                       second coding covers the case
    ONE_SOURCE         the located (VERIFIED or CORRECTED) evidence behind
                       the case comes from at most one SOURCE
    NO_LOCATED_SOURCE  no located evidence at all
    AUTHORITY_GAP      an authority hop whose citation is UNREACHABLE
    ORIGINATOR_ONLY    the direction the case is graded on is the source
                       originator's coding with no independent check

Library + CLI (python3 tools/chain.py A01 | --flags); checks() is called by
validate.py. Stdlib only.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglib  # noqa: E402

LOCATED = ("VERIFIED", "CORRECTED")


def second_coded(reg=None):
    path = os.path.join(reglib.FOLDER, "second_coder", "coding.jsonl")
    if not os.path.exists(path):
        return set()
    import json
    with open(path, "r", encoding="utf-8") as fh:
        return {json.loads(l)["id"] for l in fh if l.strip()}


def chain(reg, cid):
    o = reg.get(cid)
    auth = sorted(reg.out_edges(cid, "authorized_by"), key=lambda e: e.get("order", 0))
    hops = [(e["to"], reg.get(e["to"])["level"], reg.get(e["to"])["verification"]["state"])
            for e in auth]
    ev = []
    for e in reg.in_edges(cid, "supports"):
        x = reg.get(e["from"])
        if x["type"] != "EVIDENCE":
            continue
        ev.append((x["id"], x["kind"], x["verification"]["state"], tuple(x["sources"])))
    forced = sorted(e["to"] for e in reg.out_edges(cid, "forced_by"))
    actors = {r: sorted(e["to"] for e in reg.out_edges(cid, r))
              for r in ("decided_by", "recommended_by", "overruled", "sponsored_by")}
    return {"case": o, "authority": hops, "evidence": sorted(ev), "forced_by": forced,
            "actors": actors}


def flags(reg, cid, coded2=None):
    ch = chain(reg, cid)
    o = ch["case"]
    coded2 = second_coded() if coded2 is None else coded2
    out = []
    coders = {c["coder"] for c in o["claims"].values() if c["status"] == "PROPOSED"}
    if len(coders) == 1 and cid not in coded2:
        out.append("ONE_CODER (%s)" % next(iter(coders)))
    srcs = {s for _, _, st, ss in ch["evidence"] if st in LOCATED for s in ss}
    if not any(st in LOCATED for _, _, st, _ in ch["evidence"]):
        out.append("NO_LOCATED_SOURCE")
    elif len(srcs) <= 1:
        out.append("ONE_SOURCE (%s)" % (", ".join(sorted(srcs)) or "located evidence cites no URL"))
    gaps = [a for a, lvl, st in ch["authority"] if st == "UNREACHABLE"]
    if gaps:
        out.append("AUTHORITY_GAP (%s)" % ", ".join(gaps))
    d = o["claims"].get("action_direction") or o["claims"].get("direction")
    if d and d.get("independence") == "ORIGINATOR" and cid not in coded2 and "history" not in d:
        out.append("ORIGINATOR_ONLY (action direction)")
    return out


def render(reg, cid):
    ch = chain(reg, cid)
    o = ch["case"]
    out = ["== %s  %s (%s, %s, frame %s)" % (cid, o["title"], o["agency"], o["year"], o["frame"])]
    out.append("authority  " + (" -> ".join("%s[%s %s]" % h for h in ch["authority"]) or "none recorded"))
    for eid, kind, st, ss in ch["evidence"]:
        out.append("evidence   %-9s %-12s %-20s %s%s" % (eid, st, kind, ", ".join(ss) or "-",
                   "  (forcing)" if eid in ch["forced_by"] else ""))
    for r, ids in sorted(ch["actors"].items()):
        if ids:
            out.append("%-10s %s" % (r.replace("_by", ""), ", ".join(ids)))
    out.append("flags      " + ("; ".join(flags(reg, cid)) or "none"))
    return out


def flag_table(reg):
    coded2 = second_coded()
    out, tally = [], {}
    for o in reg.cases():
        if o["frame"] not in ("A", "B", "C", "D", "E", "R8"):
            continue
        f = flags(reg, o["id"], coded2)
        for x in f:
            tally[x.split()[0]] = tally.get(x.split()[0], 0) + 1
        out.append("%-5s %s" % (o["id"], "; ".join(f) or "-"))
    head = ["== single-failure flags over graded cases: " +
            ", ".join("%s %d" % kv for kv in sorted(tally.items()))]
    return head + out


def checks(reg):
    errs, n = [], 0
    for o in reg.cases():
        n += 1
        auth = sorted(reg.out_edges(o["id"], "authorized_by"), key=lambda e: e.get("order", 0))
        if [e["to"] for e in auth] != o["authority_chain"]:
            errs.append("%s: authority_chain differs from its authorized_by edges" % o["id"])
        if auth and reg.get(auth[0]["to"])["level"] not in ("statute", "international_instrument"):
            errs.append("%s: authority chain does not start at a statute" % o["id"])
    # known answers
    n += 1
    if "ONE_CODER (ACT-REGISTRY)" not in flags(reg, "D03", set()):
        errs.append("D03 (one-coder R8 row) not flagged ONE_CODER")
    n += 1
    if "EV-U01" not in [e[0] for e in chain(reg, "A01")["evidence"]]:
        errs.append("A01: the unlocated sponsor input EV-U01 is not on its chain")
    n += 1
    if any(f.startswith("ONE_CODER") for f in flags(reg, "A01", {"A01"})):
        errs.append("a second-coded case still flagged ONE_CODER")
    return n, errs


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("chain.py: checks run in reg-uncertainty-registry/tools/validate.py --selftest\n")
        return 2
    reg = reglib.Registry()
    ids = [a for a in argv if not a.startswith("--")]
    if "--flags" in argv or not ids:
        print("\n".join(flag_table(reg)))
    for cid in ids:
        print("\n".join(render(reg, cid)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
