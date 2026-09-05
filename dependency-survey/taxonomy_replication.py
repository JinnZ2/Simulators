#!/usr/bin/env python3
"""taxonomy_replication.py -- the cross-model replication RESULT
(ADDENDUM 01 §2, the taxonomy test) made checkable at the level the
delivered document fixes.

The RESULT compares two independent sorts of the same 19 SCOPE-DIFFERENT
cells (13 distinct): Kimi Run 2, which had produced the K-list, and a
Perplexity blind sort with no exposure to the K-list and no repo access.
The corpus itself is NOT in this repository -- it is external model
output -- so the underlying sort cannot be reproduced here. What CAN be
checked is the delivered §1 table's own structural claim:

  STRICTLY NESTED, ZERO CROSS-CUTTING -- every Perplexity group is a
  subset of exactly one Kimi kind.

That is a property of the delivered kimi-kind <- perplexity-group map,
verifiable as: the map is a FUNCTION (each group under exactly one kind).
This module transcribes that map from §1 (nothing invented; the per-record
memberships §1 does not print are not reconstructed) and checks it. It is
a transcription-consistency check, not a reproduction of the sort.

It also encodes §6's standing answer as a refusal: `kind_count()` does not
return an integer, because the document's own instruction is not to report
a kind count as a finding until a grain criterion is argued and adopted.
Report MEMBERSHIP.

    python3 taxonomy_replication.py         # the replication readout
Refuses --selftest (checks live in selftest_taxrep.py). Stdlib only,
parses under Python 3.9.
"""

import sys

# ---- transcribed from §1 of RESULT_taxonomy_replication.md, verbatim ----
# Kimi kind -> the Perplexity groups that cover it. Per-record memberships
# are not printed in §1 and are not invented here.
KIMI_COVERS = {
    "K1": ["G1", "G3", "G4", "G5"],   # conversion exists (unit/convention)
    "K3": ["G2", "G7"],               # no conversion in principle (homonym)
    "K2": ["G6"],                     # boundary difference
    "K5": ["G8", "G10", "G11"],       # reference-class re-baseline
}
# distinct records per Kimi kind (§1 "distinct" column)
KIMI_DISTINCT = {"K1": 4, "K3": 4, "K2": 1, "K5": 3}
STRAGGLER_GROUP = "G9"                # frame-relative refutation; NO NAME FOUND
STRAGGLER_DISTINCT = 1
# K4 had zero members on this transform set, under both sorters.
KIMI_KINDS_ZERO_MEMBERS = ("K4",)
DISTINCT_TOTAL = 13


def perplexity_groups():
    """All Perplexity groups named in §1, including the unassigned
    straggler."""
    gs = set(STRAGGLER_GROUP.split())
    for cover in KIMI_COVERS.values():
        gs.update(cover)
    return sorted(gs, key=lambda g: int(g[1:]))


def group_to_kinds():
    """Inverse of KIMI_COVERS: group -> [kinds that claim it]. Strict
    nesting means every entry has length 1 (a function). The straggler
    maps to no kind."""
    inv = {}
    for kind, cover in KIMI_COVERS.items():
        for g in cover:
            inv.setdefault(g, []).append(kind)
    inv.setdefault(STRAGGLER_GROUP, [])   # unassigned, by construction
    return inv


def strictly_nested(cover=None):
    """(ok, crosscutting) -- ok is True when every assigned Perplexity
    group is under exactly one Kimi kind (zero cross-cutting). Straggler
    (zero kinds) is not a cross-cut; a group under >= 2 kinds is."""
    inv = {}
    src = cover if cover is not None else KIMI_COVERS
    for kind, groups in src.items():
        for g in groups:
            inv.setdefault(g, []).append(kind)
    crosscut = sorted(g for g, ks in inv.items() if len(ks) > 1)
    return (len(crosscut) == 0, crosscut)


def kind_count():
    """§6: do NOT report a kind count as a finding until a grain criterion
    is argued and adopted. Returns the refusal, never an integer."""
    return "UNSETTLED (grain not fixed by anything in the records; report membership)"


def standing_answer():
    """§6, verbatim in structure: one or several / how many / what is
    fixed."""
    return {
        "one_or_several": "SEVERAL (three independent sorts, none returned one group)",
        "how_many": kind_count(),
        "fixed": "MEMBERSHIP (which records belong together replicated "
                 "across a sorter with no shared memory)",
    }


def grain():
    """The disagreement is entirely about grain (§2): 4 Kimi kinds with
    members vs 11 Perplexity groups over 13 distinct. Reported as a grain
    disagreement, NOT as a count of the thing."""
    return {
        "kimi_kinds_with_members": len(KIMI_COVERS),      # 4
        "perplexity_groups": len(perplexity_groups()),    # 11
        "distinct_records": DISTINCT_TOTAL,               # 13
        "note": "membership from the records; grain from the sorter, and "
                "nothing in the records settles it",
    }


def report():
    ok, crosscut = strictly_nested()
    inv = group_to_kinds()
    L = ["cross-model replication of the SCOPE-DIFFERENT taxonomy",
         "(ADDENDUM 01 §2; transcription-consistency check of the delivered §1 table,",
         " not a reproduction of the sort -- the 19-cell corpus is external model output)",
         "",
         "STRICTLY NESTED (zero cross-cutting): %s" % ("yes" if ok else "NO -- " + ", ".join(crosscut)),
         "  every Perplexity group is under exactly one Kimi kind:"]
    for g in perplexity_groups():
        ks = inv[g]
        under = ks[0] if len(ks) == 1 else ("(none -- straggler)" if not ks else "(" + ",".join(ks) + ")")
        tail = "  straggler: no kind, and no field name found" if g == STRAGGLER_GROUP else ""
        L.append("    %-4s under %s%s" % (g, under, tail))
    L.append("")
    gr = grain()
    L.append("GRAIN (the disagreement): %d Kimi kinds with members vs %d Perplexity groups, over %d distinct"
             % (gr["kimi_kinds_with_members"], gr["perplexity_groups"], gr["distinct_records"]))
    L.append("  %s" % gr["note"])
    L.append("K4: zero members under both sorters (Run-1-only, candidate artifact)")
    L.append("")
    sa = standing_answer()
    L.append("STANDING ANSWER (§6):")
    L.append("  one or several? %s" % sa["one_or_several"])
    L.append("  how many?       %s" % sa["how_many"])
    L.append("  what is fixed?  %s" % sa["fixed"])
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("taxonomy_replication has no selftest; run selftest_taxrep.py", file=sys.stderr)
        sys.exit(2)
    print(report())
