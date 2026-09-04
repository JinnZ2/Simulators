#!/usr/bin/env python3
"""stack_revision -- EXCLUSION_STACK v2 against v1, as a copy and as a claim.

`EXCLUSION_STACK_trucking_v2.md` arrived beside the first stack with
three additions: a CURRICULUM COVERAGE block inside L4 carrying the
stack's first per-layer falsifier, an ACCRETED, NOT ENGINEERED section,
and two open quantities S6 and S7. This module checks:

  1. the copy -- v2 is v1 with blocks inserted and nothing removed or
     moved; the CHANGELOG did not move with it;
  2. the L4 falsifier -- both arms of the prediction are present and
     the refuting observation is named; the evidence is one operator's
     training stack and the block says so;
  3. the four counts the ACCRETED section says "safety culture" reduces
     to (who holds, who returns, who is immune, who publishes) against
     the schema `readout_count.py` implements -- which have a field;
  4. "not fixable layer by layer" as arithmetic under the stack's own
     multiplicative survival: removing one layer from a product of
     twelve buys a factor of 1/r on that layer and leaves the rest;
  5. S1..S7 against the schema and the parent order -- which open
     quantity fills a schema column and which names a layer the schema
     has no column for;
  6. the two hosts S6's test would read, probed once.

The stack's sources were not read. Nothing here is a statement about
any regime, any curriculum, or any operator.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import readout_count as RC  # noqa: E402
import row_audit as RA  # noqa: E402
import stack_audit as SA  # noqa: E402

V1 = SA.DOC
V2 = os.path.join(HERE, "EXCLUSION_STACK_trucking_v2.md")


# ------------------------------------------------------------ 1. the copy

def insertions(v1, v2):
    """The blocks whose insertion turns v1 into v2, by a line diff that
    allows only additions. Returns (blocks, removed_lines)."""
    a, b = v1.splitlines(True), v2.splitlines(True)
    i = j = 0
    blocks, removed = [], []
    cur = []
    while j < len(b):
        if i < len(a) and a[i] == b[j]:
            if cur:
                blocks.append("".join(cur))
                cur = []
            i += 1
            j += 1
        else:
            cur.append(b[j])
            j += 1
    if cur:
        blocks.append("".join(cur))
    removed = a[i:]
    return blocks, removed


def pure_insertion(v1, v2):
    blocks, removed = insertions(v1, v2)
    reassembled = v2
    for blk in blocks:
        reassembled = reassembled.replace(blk, "", 1)
    return {"blocks": len(blocks), "removed_lines": len(removed),
            "reassembles_v1": reassembled == v1 and not removed,
            "lines_added": sum(blk.count("\n") for blk in blocks)}


def changelog_unchanged(v1, v2):
    return RA.section(v1, "CHANGELOG") == RA.section(v2, "CHANGELOG")


# ---------------------------------------------------- 2. the L4 falsifier

def l4_falsifier(v2):
    l4 = SA.layer_body(v2, "L4")
    return {
        "has_test": "TEST" in l4,
        "predict_both_arms": ("present in carrier-side" in l4) and ("absent in operator-side" in l4),
        "refutation_named": "this layer is refuted" in l4,
        "evidence_n1_declared": "one working operator's training stack" in l4,
        "cites_absent": all(x in l4 for x in ("390.6", "386.12", "31105")),
    }


# ------------------------------------------------ 3. the four counts

FOUR_COUNTS = {
    "who holds": ("holder",),
    "who returns": ("positions_returning", "return_count"),
    "who is immune": ("immunity",),
    "who publishes": (),
}


def four_counts():
    out = {}
    for k, fields in FOUR_COUNTS.items():
        present = [f for f in fields if f in RC.FIELDS]
        out[k] = {"fields": present, "has_field": bool(present)}
    return out


# ------------------------------------------- 4. layer-by-layer arithmetic

def remove_one(rates, layer):
    """Survival with one layer's filter removed (rate set to 1)."""
    r = dict(rates)
    r[layer] = 1.0
    return SA.survival(r)


def layer_by_layer(rates):
    """For a fully measured stack: baseline survival and the survival
    after removing each single layer. The gain from removing layer i is
    exactly 1/r_i; the product of the other eleven bounds it."""
    base = SA.survival(rates)
    out = {}
    for k in rates:
        after = remove_one(rates, k)
        out[k] = {"after": after, "gain": None if base in (None, 0) else after / base}
    return {"base": base, "per_layer": out}


# ---------------------------------------- 5. open quantities vs the schema

# Declared readings: which schema column or parent id each S fills.
OPEN_MAP = {
    "S1": ("layer L1", None, "employee classification has no column; the schema counts positions, not who is inside the statute"),
    "S2": ("layer L0", None, "filability of a readout item has no column; this is the row's `type` column again"),
    "S3": ("all layers", None, "per-layer survival is the stack's own quantity; no column"),
    "S4": ("the row's OPEN INSTANCE", None, "per-carrier reply rate; the schema has return_count per regime-year, not per carrier"),
    "S5": ("schema", ("intake_count", "return_count"), "filings vs investigations vs enforcement by year fills intake_count and return_count per regime-year"),
    "S6": ("layer L4", None, "a syllabus search; no column"),
    "S7": ("layer L4", None, "an awareness survey; the asymmetry is between two positions the schema does not separate"),
}


def open_map():
    out = {}
    for s, (target, fields, why) in OPEN_MAP.items():
        out[s] = {"target": target, "fields": fields, "why": why,
                  "fills_schema": bool(fields) and all(f in RC.FIELDS for f in fields)}
    return out


HOST_PROBE = {"oshacademy.com": "no response", "training.fema.gov": "no response"}


# ---------------------------------------------------------------- render

def _f(x):
    return "--" if x is None else ("%.6f" % x if isinstance(x, float) and x < 0.01 else "%.3f" % x if isinstance(x, float) else str(x))


def render():
    v1, v2 = SA._read(V1), SA._read(V2)
    out = []
    w = out.append
    w("stack_revision -- EXCLUSION_STACK v2 against v1")
    w("")
    pi = pure_insertion(v1, v2)
    w("1. THE COPY  blocks inserted %d, lines added %d, lines removed %d, reassembles v1: %s" % (
        pi["blocks"], pi["lines_added"], pi["removed_lines"], pi["reassembles_v1"]))
    w("   CHANGELOG unchanged: %s  (the revision is not logged in it)" % changelog_unchanged(v1, v2))
    w("")
    f = l4_falsifier(v2)
    w("2. L4 FALSIFIER  TEST present %s; PREDICT carries both arms %s; refuting observation named %s" % (
        f["has_test"], f["predict_both_arms"], f["refutation_named"]))
    w("   evidence declared as one operator's stack: %s; the three citations named as absent: %s" % (
        f["evidence_n1_declared"], f["cites_absent"]))
    w("   the first layer in the stack with its own falsifier; S6 is the test as a survey.")
    w("")
    fc = four_counts()
    w("3. THE FOUR COUNTS  'who holds, who returns, who is immune, who publishes' against the schema")
    for k, v in fc.items():
        w("   %-16s %s" % (k, ", ".join(v["fields"]) if v["has_field"] else "NO FIELD"))
    w("   three of four have a column; 'who publishes' is P2's third disjunct (RC_017) and has none.")
    w("")
    st = SA.unmeasured_stack(v2)
    w("4. LAYER BY LAYER  delivered stack: %d layers, survival %s (unmeasured)" % (len(st), SA.survival(st)))
    demo = {k: 0.5 for k in st}
    lb = layer_by_layer(demo)
    w("   constructed: every layer at 0.5 -> survival %s; removing any one layer -> %s (gain x%s)" % (
        _f(lb["base"]), _f(lb["per_layer"]["L0"]["after"]), _f(lb["per_layer"]["L0"]["gain"])))
    demo2 = dict(demo, L0=0.05)
    lb2 = layer_by_layer(demo2)
    w("   constructed: L0 at 0.05, others 0.5 -> survival %s; removing L0 -> %s (x%s); removing L7 -> %s (x%s)" % (
        _f(lb2["base"]), _f(lb2["per_layer"]["L0"]["after"]), _f(lb2["per_layer"]["L0"]["gain"]),
        _f(lb2["per_layer"]["L7"]["after"]), _f(lb2["per_layer"]["L7"]["gain"])))
    w("   under the stack's own arithmetic, removing one layer buys 1/r on that layer and")
    w("   leaves the other eleven; 'not fixable layer by layer' is the product, stated.")
    w("")
    om = open_map()
    w("5. OPEN QUANTITIES  S1..S7 against the schema")
    for s, v in om.items():
        w("   %s  %-26s fills schema %-5s %s" % (s, v["target"], v["fills_schema"], v["why"]))
    w("   one of seven fills schema columns; the other six name layers the schema has no column for.")
    w("")
    w("6. S6 HOSTS  " + ", ".join("%s %s" % kv for kv in HOST_PROBE.items()) + "  (allowlist egress; not read)")
    w("")
    w("Nothing here is a statement about any regime, curriculum or operator.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("stack_revision.py has no checks of its own; they live in selftest_rc.py.\n")
        return 2
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
