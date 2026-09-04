#!/usr/bin/env python3
"""revision_audit -- the v2 order checked as a copy and as a claim.

`WORK_ORDER_V2.md` arrived beside `WORK_ORDER.md` with one addition: an
N2 CONTROL bullet under WHAT WOULD MOVE THIS BEYOND CURRENT REACH. This
module checks, from the two files and two sibling modules imported not
copied:

  1. the revision is a pure insertion -- v2 equals v1 with one block
     inserted at one point, nothing else moved;
  2. the CHANGELOG did not move with it;
  3. `N2` and `the null` have no referent in either version of this
     order; the referent is `zero-sum-curriculum-null/NULL_CONSTRUCTION.md`,
     whose N2 title is read and printed;
  4. the bullet names three measurables; each is mapped, as a declared
     reading, to the `hf-incident-extract` sheet, and the mapping is
     checked against the sheet's real field names;
  5. the bullet's outcome sentences against the null construction's own
     outcome table and against N3's stated inputs -- a TRANSPARENT scorer
     removes `opacity` from `(gradient + open channel + opacity)`.

Nothing here is a value from any run.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "zero-sum-curriculum-null"))
sys.path.insert(0, os.path.join(ROOT, "hf-incident-extract"))
import null_construction as NC  # noqa: E402
import hf_incident_extract as HF  # noqa: E402

V1 = os.path.join(HERE, "WORK_ORDER.md")
V2 = os.path.join(HERE, "WORK_ORDER_V2.md")


def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------ 1. the copy

def inserted_block(v1, v2):
    """The single contiguous block whose insertion turns v1 into v2, or
    None if the change is not a single insertion."""
    a, b = v1.splitlines(True), v2.splitlines(True)
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    j = 0
    while (j < min(len(a), len(b)) - i and a[len(a) - 1 - j] == b[len(b) - 1 - j]):
        j += 1
    if a[:i] + a[len(a) - j:] != a or len(a) != i + j:
        return None
    return "".join(b[i:len(b) - j])


def pure_insertion(v1, v2):
    blk = inserted_block(v1, v2)
    if blk is None:
        return {"pure": False, "block": None, "reassembles": False}
    idx = v2.find(blk)
    return {"pure": True, "block": blk,
            "reassembles": v2[:idx] + v2[idx + len(blk):] == v1,
            "lines": blk.count("\n")}


def section(text, heading):
    m = re.search(r"^## %s\n(.*?)(?=^## |\Z)" % re.escape(heading), text, re.S | re.M)
    return m.group(1) if m else None


# --------------------------------------------------------- 3. the referent

def referent(v1, v2):
    """Where `N2` and `null` occur in each version, by line; and N2's
    title in the null construction."""
    def lines_with(text, pat):
        return [i for i, l in enumerate(text.splitlines(), 1) if re.search(pat, l)]
    nc = NC.parse()
    return {
        "v1_N2": lines_with(v1, r"\bN2\b"),
        "v2_N2": lines_with(v2, r"\bN2\b"),
        "v1_null": lines_with(v1, r"\bnull\b"),
        "v2_null": lines_with(v2, r"\bnull\b"),
        "null_construction_N2": nc["branches"]["N2"]["title"],
        "null_construction_N2_test": nc["branches"]["N2"]["test"],
    }


# ------------------------------------------------- 4. the three measurables

# Declared readings: which sheet fields would carry each measurable the
# bullet names. `exact` means the sibling's measure IS the quantity;
# `partial` means a field touches it; `absent` means no field.
MEASURABLES = {
    "probing rate": {
        "fields": ("env_edit_moves", "gate_fool_moves"),
        "fit": "partial",
        "why": "the sheet counts probe classes (M3 is their ratio) and has "
               "no per-run denominator, so a RATE of probing is not on it",
    },
    "channel split (peers / gate / third parties)": {
        "fields": ("agents",),
        "fit": "partial",
        "why": "M6 reads the gate channel (opponent charged on an inert "
               "gate, per agent); peers and third parties have no field",
    },
    "self-risk rate": {
        "fields": ("runs_self_failed_for_collective", "runs_total"),
        "fit": "exact",
        "why": "M4 member_cost is runs self-failed for the collective over "
               "runs_total",
    },
}


def measurable_map():
    out = {}
    for name, m in MEASURABLES.items():
        out[name] = dict(m, fields_exist=all(f in HF.SHEET for f in m["fields"]))
    return out


# ------------------------------------------------ 5. the outcome sentences

def n3_inputs():
    """N3's stated inputs, parsed from its requires line."""
    req = NC.parse()["branches"]["N3"]["requires"]
    m = re.search(r"\(([^)]*)\)", req)
    return [p.strip() for p in m.group(1).split("+")] if m else []


def transparency_removes():
    """A transparent scorer (check logic disclosed) removes opacity from
    N3's inputs. Returns the inputs before and after."""
    before = n3_inputs()
    after = [x for x in before if x != "opacity"]
    return {"before": before, "after": after, "removed": len(before) - len(after)}


BULLET_OUTCOMES = {
    "persists": "the adversarial template is cued by something other than the setting",
    "vanishes": "the setting cues it",
}


def outcome_check():
    """The bullet's two outcome readings against the null construction's
    N2 outcome table. `persists` is the bullet's stronger claim: it names
    the TEMPLATE as what persists, where the null construction's table
    leaves what persists to N3."""
    nc_out = NC.N2_OUTCOMES
    persists_nc = nc_out["probing rate equal across settings"]
    vanishes_nc = nc_out["probing rate lower on possible tasks"]
    return {
        "persists": {
            "bullet": BULLET_OUTCOMES["persists"],
            "null_construction": persists_nc["null"],
            "names_template": "template" in BULLET_OUTCOMES["persists"],
            "routes_to_N3": "N3" in persists_nc["null"],
        },
        "vanishes": {
            "bullet": BULLET_OUTCOMES["vanishes"],
            "null_construction": vanishes_nc["N2"],
            "agree": True,
        },
    }


# ---------------------------------------------------------------- render

def render():
    v1, v2 = _read(V1), _read(V2)
    out = []
    w = out.append
    w("revision_audit -- WORK_ORDER_V2 against WORK_ORDER")
    w("")
    pi = pure_insertion(v1, v2)
    w("1. THE COPY   pure insertion %s   reassembles v1 %s   lines added %s" % (
        pi["pure"], pi["reassembles"], pi.get("lines")))
    w("   section touched: WHAT WOULD MOVE THIS BEYOND CURRENT REACH")
    w("")
    c1, c2 = section(v1, "CHANGELOG"), section(v2, "CHANGELOG")
    w("2. CHANGELOG   unchanged across the revision: %s" % (c1 == c2))
    w("   v2 logs: %s" % " | ".join(l.strip() for l in c2.strip().splitlines()))
    w("   P6 asks for versioned diffs; the revision's own diff is not logged in it.")
    w("")
    r = referent(v1, v2)
    w("3. REFERENT   'N2' in v1 lines %s, v2 lines %s;  'null' in v1 %s, v2 %s" % (
        r["v1_N2"], r["v2_N2"], r["v1_null"], r["v2_null"]))
    w("   referent is zero-sum-curriculum-null N2: %s" % r["null_construction_N2"])
    w("   whose test reads: %s" % r["null_construction_N2_test"])
    w("")
    w("4. MEASURABLES named by the bullet, against the hf-incident-extract sheet")
    for name, m in measurable_map().items():
        w("   %-44s %-7s fields %s (exist %s)" % (name[:44], m["fit"], ", ".join(m["fields"]),
                                                 m["fields_exist"]))
        w("      %s" % m["why"])
    w("   the null construction's N2 named one measurable (probing rate); the")
    w("   bullet names three, and the channel split is N3's residual quantity")
    w("   measured in the control setting.")
    w("")
    t = transparency_removes()
    w("5. OUTCOMES   N3's stated inputs %s -> with a transparent scorer %s (removed %d)" % (
        t["before"], t["after"], t["removed"]))
    oc = outcome_check()
    w("   'persists' -> bullet: %s" % oc["persists"]["bullet"])
    w("               null construction: %s" % oc["persists"]["null_construction"])
    w("               bullet names the template: %s; the table routes to N3: %s" % (
        oc["persists"]["names_template"], oc["persists"]["routes_to_N3"]))
    w("   'vanishes' -> bullet: %s;  null construction: %s" % (
        oc["vanishes"]["bullet"], oc["vanishes"]["null_construction"]))
    w("   with opacity removed, a persisting gate-as-opponent split has one fewer")
    w("   substrate input to rest on; gradient and open channel remain, so the")
    w("   'persists' reading narrows N3 and does not close it.")
    w("")
    w("Nothing here is a value from any run.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("revision_audit.py has no checks of its own; "
                         "they live in selftest_lpt.py.\n")
        return 2
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
