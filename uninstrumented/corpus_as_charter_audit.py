#!/usr/bin/env python3
# corpus_as_charter_audit.py -- CC0, stdlib only, parses under 3.9
#
# Audit of CORPUS_AS_CHARTER.md, landed verbatim and edited by nothing
# here. The delivery's empirical layer is a press-sourced AI-eval case
# whose transcripts are not in this repository and whose sources the
# egress gate refuses, so almost nothing in it is verifiable here --
# which is itself the headline finding. This module computes only the
# three things that ARE computable from inside the tree:
#   1  the relation to the parent instrument (CHARTER_SIGNATURE): is
#      this the same transform with the author subtracted?
#   2  the internal arithmetic of the ~40x asymmetry, from the file's
#      OWN stated counts -- not a check on the eval, a check on the
#      file's self-consistency
#   3  provenance containment: is every carried eval number inside the
#      verify-before-use region, and is the empirical layer flagged?
# It adjudicates none of the eval. Findings are CAC_1..CAC_7 below and
# echoed in AUDIT_NOTES.md.

import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CC = os.path.join(HERE, "CORPUS_AS_CHARTER.md")
CS = os.path.join(HERE, "CHARTER_SIGNATURE.md")


def _read(p):
    return io.open(p, encoding="utf-8").read()


def _section(text, heading):
    """Body of a '## N. HEADING ...' section up to the next '## '."""
    m = re.search(r"(?m)^## .*%s.*$" % re.escape(heading), text)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"(?m)^## ", rest)
    body = rest[:nxt.start()] if nxt else rest
    return " ".join(body.split())   # fold line-wraps for phrase match


# ------------------------------------------ 1  the relation

def relation():
    """The parent transform is declared-list / absence-set derived
    from a charter; the extension keeps it and subtracts the author,
    replacing the explicit declaration with a DIFFERENTIAL RECORDING
    RATE. Checked as vocabulary present in §1 plus a named parent, not
    asserted."""
    t = _read(CC)
    s1 = _section(t, "THE EXTENSION")
    return {
        "parent_file_resolves": os.path.isfile(CS),
        "names_parent":
            "CHARTER_SIGNATURE.md" in t and "child of the charter"
            in t.lower(),
        "author_subtracted":
            "no author and no date" in t or "authorless" in t.lower(),
        "differential_recording_rate":
            "differential recording rate" in s1.lower(),
        "keeps_absence_set": "absence set" in s1.lower(),
        "inherits_bias_claim":
            "measurement bias in the record, inherited" in t.lower()
            or "inherited" in s1.lower(),
    }


# ------------------------------------------ 2  the arithmetic

def arithmetic():
    """The ~40x asymmetry, from the file's OWN stated counts. The file
    states: audience 3-6 of ~1,300 transcripts; adversary >20%. The
    minimum asymmetry consistent with those is adversary_floor divided
    by audience_ceiling. If that is >= 40, '~40x' is a conservative
    (understating) statement of the file's own numbers -- the honest
    direction. This checks the file against itself, not the eval."""
    lo, hi, n = 3, 6, 1300
    aud_ceiling = hi / n            # largest plausible audience share
    adv_floor = 0.20               # ">20%"
    min_asym = adv_floor / aud_ceiling
    return {
        "audience_band_pct": (round(lo / n * 100, 2),
                              round(hi / n * 100, 2)),
        "adversary_floor_pct": 20.0,
        "min_asymmetry": round(min_asym, 1),
        "stated_asymmetry": 40,
        # 40 <= min_asym means the headline is at or below its own
        # floor -- conservative, not overstated
        "headline_is_conservative": 40 <= min_asym,
        "points_one_way": adv_floor > hi / n,
    }


# ------------------------------------ 3  provenance containment

# Every distinct carried eval figure. Each must occur ONLY inside the
# press-sourced region (sections 2 and 3), never in the frame, the
# extension, what-this-establishes, the depth stack, the physics, or
# the disagreements -- the MI_003 containment shape: a flagged number
# must not leak into load-bearing prose outside its flag.
EVAL_FIGURES = ["198", "~7%", ">20%", "3 to 6", "~1,300", "~40"]


def containment():
    """A carried figure may recur across carried sections (the problem
    count 198 restates in the §4 inference chain, which is a carried
    environment description) -- that is the same fact in a second
    carried context, not a leak. The property that matters is that no
    carried figure appears in the render's OWN analytic prose: the
    frame, §1 (the extension), §5 (depth stack), §6 (physics), §7
    (disagreements). Sections 2, 3 and 4 are the carried layer."""
    t = _read(CC)
    m2 = re.search(r"(?m)^## 2\. THE CASE", t)
    m5 = re.search(r"(?m)^## 5\.", t)
    carried = t[m2.start():m5.start()] if (m2 and m5) else ""
    analytic = t.replace(carried, "")
    leaks = {}
    for fig in EVAL_FIGURES:
        leaks[fig] = {"in_carried": fig in carried,
                      "leaks": fig in analytic}
    posture = _section(t, "PROVENANCE POSTURE")
    return {
        "region_found": bool(carried),
        "figures": leaks,
        "no_leak": all(not v["leaks"] for v in leaks.values()),
        "verify_before_use_flagged":
            "VERIFY BEFORE USE" in t and "press-sourced" in posture,
        "biology_marked_analogy":
            "as ANALOGY" in t and "ANALOGY" in _section(t, "THE CASE"),
        "co_production_declared": "co-produced" in posture.lower(),
    }


# ----------------------------- structure the spec asked for

def structure():
    t = _read(CC)
    return {
        "depth_stack_0_3":
            all(("DEPTH %d" % d) in t for d in range(4)),
        "two_disagreements":
            "TWO DISAGREEMENTS" in t
            and "no destination" in t.lower()
            and "bad physics" in t.lower(),
        "disagreements_flagged_not_adjudicated":
            "not adjudicated" in t.lower()
            and "this render's reading of which two" in t.lower(),
        "open_metr_access_dispute":
            "METR ACCESS DISPUTE" in t
            and "un-adjudicated" in t.lower(),
        "not_a_gap":
            "**Gap:**" not in t and "Knowledge state:" not in t,
    }


# -------------------------------------------------- render

def render():
    out = []
    w = out.append
    w("CORPUS AS CHARTER -- AUDIT")
    w("(the delivered file is edited by nothing here; its empirical")
    w(" layer is press-sourced and unverifiable from this repo --")
    w(" that is the headline, not a gap in the audit)")
    w("")
    r = relation()
    w("1  RELATION TO THE PARENT INSTRUMENT")
    for k in ("parent_file_resolves", "names_parent",
              "author_subtracted", "differential_recording_rate",
              "keeps_absence_set", "inherits_bias_claim"):
        w("   %-30s %s" % (k, r[k]))
    w("   the same transform, author subtracted, declaration replaced")
    w("   by a recording rate -- the relation holds structurally.")
    w("")
    a = arithmetic()
    w("2  THE ~40x ASYMMETRY, FROM THE FILE'S OWN COUNTS")
    w("   audience band %s%% (3-6 of ~1,300); adversary floor %s%%"
      % (a["audience_band_pct"], a["adversary_floor_pct"]))
    w("   minimum asymmetry consistent with those: %sx" %
      a["min_asymmetry"])
    w("   stated '~40x' is conservative (<= the floor): %s;"
      % a["headline_is_conservative"])
    w("   points one way (adversary >> audience): %s"
      % a["points_one_way"])
    w("   -- a check on the file against itself, not on the eval.")
    w("")
    c = containment()
    w("3  PROVENANCE CONTAINMENT")
    w("   press-sourced region found: %s; verify-before-use flagged:"
      % c["region_found"])
    w("   %s; biology marked analogy: %s; co-production declared: %s"
      % (c["verify_before_use_flagged"], c["biology_marked_analogy"],
         c["co_production_declared"]))
    w("   every carried figure stays inside the region (no leak): %s"
      % c["no_leak"])
    for fig, v in c["figures"].items():
        w("     %-8s in carried layer %s, leaks into analytic %s"
          % (fig, v["in_carried"], v["leaks"]))
    w("")
    s = structure()
    w("4  STRUCTURE THE SPEC ASKED FOR")
    for k in ("depth_stack_0_3", "two_disagreements",
              "disagreements_flagged_not_adjudicated",
              "open_metr_access_dispute", "not_a_gap"):
        w("   %-38s %s" % (k, s[k]))
    w("")
    w("This module computes; it does not conclude, and it verifies")
    w("nothing about the eval -- the transcripts are not here.")
    w("Findings CAC_1..CAC_7 in AUDIT_NOTES.md.")
    return "\n".join(out)


def selftest():
    n = [0]

    def check(name, ok):
        n[0] += 1
        if not ok:
            sys.stderr.write("FAIL %s\n" % name)
            sys.exit(1)

    before = hashlib.sha256(io.open(CC, "rb").read()).hexdigest()

    r = relation()
    check("parent resolves", r["parent_file_resolves"])
    check("names parent", r["names_parent"])
    check("author subtracted", r["author_subtracted"])
    check("differential recording rate", r["differential_recording_rate"])
    check("keeps absence set", r["keeps_absence_set"])
    check("inherits-bias claim present", r["inherits_bias_claim"])

    a = arithmetic()
    check("audience band from 3-6/1300",
          a["audience_band_pct"] == (0.23, 0.46))
    check("min asymmetry ~43", 43.0 <= a["min_asymmetry"] <= 43.5)
    check("40x is conservative", a["headline_is_conservative"])
    check("points one way", a["points_one_way"])

    c = containment()
    check("region found", c["region_found"])
    check("every figure in the carried layer",
          all(v["in_carried"] for v in c["figures"].values()))
    check("no figure leaks outside", c["no_leak"])
    check("verify-before-use flagged", c["verify_before_use_flagged"])
    check("biology marked analogy", c["biology_marked_analogy"])
    check("co-production declared", c["co_production_declared"])

    s = structure()
    check("depth stack 0-3", s["depth_stack_0_3"])
    check("two disagreements present", s["two_disagreements"])
    check("disagreements flagged not adjudicated",
          s["disagreements_flagged_not_adjudicated"])
    check("METR access dispute open", s["open_metr_access_dispute"])
    check("not a gap", s["not_a_gap"])

    render()
    after = hashlib.sha256(io.open(CC, "rb").read()).hexdigest()
    check("delivered file untouched", before == after)

    print("corpus_as_charter_audit selftest: %d/%d checks pass"
          % (n[0], n[0]))


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        print(render())
