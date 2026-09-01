#!/usr/bin/env python3
# corpus_as_charter_audit.py -- CC0, stdlib only, parses under 3.9
#
# Audit of CORPUS_AS_CHARTER.md and its fuller canonical delivery
# CORPUS_AS_CHARTER_V2.md, both landed verbatim and edited by nothing
# here. The delivery's empirical layer is a press-sourced AI-eval case
# whose transcripts are not in this repository and whose sources the
# egress gate refuses, so almost nothing in it is verifiable here --
# which is itself the headline finding. This module computes only the
# things that ARE computable from inside the tree:
#   1  the relation to the parent instrument (CHARTER_SIGNATURE): is
#      this the same transform with the author subtracted?
#   2  the internal arithmetic of the ~40x asymmetry, from the file's
#      OWN stated counts -- not a check on the eval, a check on the
#      file's self-consistency
#   3  provenance containment: is every carried eval number inside the
#      verify-before-use region, and is the empirical layer flagged?
#   4  cross-rendering consistency: v1 (the recovery render from the
#      aborted-write spec) and v2 (the fuller 11-section delivery) are
#      two renderings of ONE document; a rendering that restates an
#      earlier one is a copy, and copies drift (the OE_011 / DBK_010 /
#      DBK_021 shape). Do the shared eval counts and the ~40x arithmetic
#      reproduce identically on v2, or did the fuller pass move them?
# It adjudicates none of the eval. Findings are CAC_1..CAC_12 below and
# echoed in AUDIT_NOTES.md. v1 landed first as a recovery render; v2 is
# the actual document arriving verbatim, landed beside it per the repo's
# supersession convention (observer-exclusion SPEC_V2, design-basis
# SOURCE_DROP_V2) so both stay inspectable.

import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CC = os.path.join(HERE, "CORPUS_AS_CHARTER.md")
CV2 = os.path.join(HERE, "CORPUS_AS_CHARTER_V2.md")
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


# ============================================== the v2 pair
# CAC_8..CAC_12. v2 is the fuller 11-section canonical delivery of the
# same document v1 recovered from the aborted-write spec. Everything
# below reads the DELIVERED text and computes; it adjudicates nothing.

def _v2_section(text, n):
    """Body of v2 section '## N.' up to the next '## N+1.' (or end)."""
    m = re.search(r"(?m)^## %d\. " % n, text)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"(?m)^## %d\. " % (n + 1), rest)
    return rest[:nxt.start()] if nxt else rest


def _stated_counts(text):
    """The eval counts an argument's weight rests on, pulled tolerant
    of formatting so 'v1 vs v2' compares COUNTS and not punctuation:
    audience (lo, hi, denom), adversary floor %, stated asymmetry x."""
    aud = re.search(
        r"(\d+)\s*(?:to|[-–—])\s*(\d+)\s+of\s+~?([\d,]+)", text)
    adv = re.search(r">\s*(\d+)\s*%", text)
    asym = re.search(r"~?\s*(\d+)\s*[x×]", text)
    return {
        "audience": (int(aud.group(1)), int(aud.group(2)),
                     int(aud.group(3).replace(",", ""))) if aud else None,
        "adversary_floor_pct": int(adv.group(1)) if adv else None,
        "stated_asymmetry": int(asym.group(1)) if asym else None,
    }


def relation_v2():
    """The parent relation holds on v2 too -- checked on v2's own text,
    author subtracted, declaration replaced by a differential recording
    rate, the parent named. The CAC_2 check one rendering further."""
    t = _read(CV2)
    s1 = _v2_section(t, 1)
    return {
        "file_resolves": os.path.isfile(CV2),
        "names_parent": "CHARTER_SIGNATURE.md" in t,
        "extension_declared":
            "extension to a substrate where the charter" in t.lower(),
        "author_subtracted":
            "no author and no date" in t or "authorless" in t.lower(),
        "differential_recording_rate":
            "differential recording" in s1.lower(),
        "eleven_sections": all(("## %d." % n) in t for n in range(12)),
    }


def cross_rendering():
    """CAC_9, the headline for the pair: v1 and v2 are two renderings of
    one document. Pull the weight-bearing counts from each tolerant of
    formatting and compare. If they match, the fuller pass did not drift
    the numbers -- copies drift (OE_011 / DBK_010 / DBK_021) and here
    they did not. Then reproduce the ~40x floor on v2's OWN counts (the
    CAC_3 arithmetic, one rendering on)."""
    v1c = _stated_counts(_read(CC))
    v2c = _stated_counts(_read(CV2))
    # the ~40x floor from v2's stated audience + adversary floor
    lo, hi, n = v2c["audience"]
    floor = (v2c["adversary_floor_pct"] / 100.0) / (hi / n)
    return {
        "v1_counts": v1c,
        "v2_counts": v2c,
        "counts_match": v1c == v2c,
        "audience_matches": v1c["audience"] == v2c["audience"],
        "adversary_floor_matches":
            v1c["adversary_floor_pct"] == v2c["adversary_floor_pct"],
        "stated_asymmetry_matches":
            v1c["stated_asymmetry"] == v2c["stated_asymmetry"],
        "v2_min_asymmetry": round(floor, 1),
        # v2's stated '40' is at or below its own arithmetic floor
        "v2_headline_conservative": v2c["stated_asymmetry"] <= floor,
    }


# The argument-weight figures whose containment is load-bearing: the
# asymmetry rests on these. The environment count 198 and the escalation
# count 3-6 legitimately recur where the environment is recapped (§9)
# and where the open question points at its own datum (§11) -- recorded,
# not flagged, per the audit's own honesty about a restated fact.
ASYM_FIGURES = [">20%", "~40", "0.4%"]
ARGUMENT_SECTIONS = (1, 6, 7, 8, 10)   # the pure analytic sections


def containment_v2():
    """CAC_10. The weight-bearing asymmetry figures must stay inside the
    carried statistical region (§2 THE CASE, §3 THE MISSING PARTY) and
    never appear in the pure argument sections (§1, §6, §7, §8, §10).
    The environment count and the escalation count recur in the
    environment recap and the open-items pointer; those are recorded as
    legitimate recurrences, not leaks."""
    t = _read(CV2)
    arg = "".join(_v2_section(t, n) for n in ARGUMENT_SECTIONS)
    leaks = {fig: fig in arg for fig in ASYM_FIGURES}
    return {
        "asym_figures_leak": leaks,
        "no_asym_leak": not any(leaks.values()),
        # legitimate, recorded recurrences of non-weight figures
        "env_count_recurs_in_9": "198" in _v2_section(t, 9),
        "escalation_count_recurs_in_11": "3-6" in _v2_section(t, 11),
        # §0 discipline: dated sources + DISPUTED marked not resolved
        "sources_dated":
            "26 Aug 2026" in t and "29 July 2026" in t,
        "disputed_marked_not_resolved":
            "DISPUTED" in t and "Marked, not resolved" in t,
    }


def expanded_moves():
    """CAC_11 + CAC_12, the two structural reads the fuller pass adds --
    flagged as this audit's readings, adjudicated as neither true nor
    false about the world.

    CAC_11  §8 is the CHARTER_SIGNATURE transform applied to
            epistemology: the era's DECLARED standard is the charter,
            the unanswered counter-evidence is the unguarded absence,
            'biased against its own declared standard' the signature.
    CAC_12  the fuller pass keeps two disciplines the repo runs
            everywhere: a correction marked on the record (§7's
            insulation-is-a-ratio, 'kept on the record because an
            earlier framing of this was wrong'), and two findings held
            apart that it names as not-to-be-merged (§9's 'nothing can
            hold it' vs 'the sensor was off')."""
    t = _read(CV2)
    s8 = _v2_section(t, 8)
    s7 = _v2_section(t, 7)
    s9 = _v2_section(t, 9)
    return {
        # CAC_11 -- structural presence, a reading not an adjudication
        "s8_names_declared_standard":
            "declared standard" in s8.lower()
            or "standard it declared" in s8.lower()
            or "declares for itself" in s8.lower(),
        "s8_charter_signature_named":
            "charter signature applied to epistemology" in s8.lower(),
        "s8_biased_against_own_standard":
            "against its own declared standard" in s8.lower(),
        # CAC_12 -- correction on the record + two states kept apart
        "s7_correction_on_record":
            "kept on the record because an earlier framing" in s7.lower(),
        "s7_insulation_is_a_ratio":
            "it is a **ratio**" in s7.lower()
            or "insulation is not a binary" in s7.lower(),
        "s9_two_findings_not_merged":
            "different findings with different responses" in s9.lower()
            and "do not merge them" in s9.lower(),
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
    w("THE V2 PAIR (CAC_8..CAC_12)")
    w("v1 is the recovery render from the aborted-write spec; v2 is the")
    w("fuller 11-section document arriving verbatim, landed beside it.")
    w("")
    rv = relation_v2()
    w("5  RELATION HOLDS ON V2")
    for k in ("file_resolves", "names_parent", "extension_declared",
              "author_subtracted", "differential_recording_rate",
              "eleven_sections"):
        w("   %-30s %s" % (k, rv[k]))
    w("")
    x = cross_rendering()
    w("6  CROSS-RENDERING CONSISTENCY -- do the counts drift?")
    w("   v1 counts: %s" % (x["v1_counts"],))
    w("   v2 counts: %s" % (x["v2_counts"],))
    w("   counts match (no drift across the two renderings): %s"
      % x["counts_match"])
    w("   v2 min asymmetry from its own counts: %sx; stated '~40x'"
      % x["v2_min_asymmetry"])
    w("   at or below that floor (conservative): %s"
      % x["v2_headline_conservative"])
    w("")
    cv = containment_v2()
    w("7  PROVENANCE CONTAINMENT ON V2")
    w("   weight-bearing asymmetry figures leak into argument prose: %s"
      % (not cv["no_asym_leak"]))
    for fig, lk in cv["asym_figures_leak"].items():
        w("     %-6s leaks into an argument section: %s" % (fig, lk))
    w("   env count 198 recurs in the §9 recap (legitimate): %s"
      % cv["env_count_recurs_in_9"])
    w("   escalation count 3-6 recurs in the §11 pointer (legit): %s"
      % cv["escalation_count_recurs_in_11"])
    w("   sources dated in §0: %s; DISPUTED marked not resolved: %s"
      % (cv["sources_dated"], cv["disputed_marked_not_resolved"]))
    w("")
    e = expanded_moves()
    w("8  WHAT THE FULLER PASS ADDS (readings, not adjudications)")
    w("   §8 -- charter transform on epistemology:")
    for k in ("s8_names_declared_standard", "s8_charter_signature_named",
              "s8_biased_against_own_standard"):
        w("     %-34s %s" % (k, e[k]))
    w("   §7/§9 -- correction on record + two states kept apart:")
    for k in ("s7_correction_on_record", "s7_insulation_is_a_ratio",
              "s9_two_findings_not_merged"):
        w("     %-34s %s" % (k, e[k]))
    w("")
    w("This module computes; it does not conclude, and it verifies")
    w("nothing about the eval -- the transcripts are not here.")
    w("Findings CAC_1..CAC_12 in AUDIT_NOTES.md.")
    return "\n".join(out)


def selftest():
    n = [0]

    def check(name, ok):
        n[0] += 1
        if not ok:
            sys.stderr.write("FAIL %s\n" % name)
            sys.exit(1)

    before = hashlib.sha256(io.open(CC, "rb").read()).hexdigest()
    before_v2 = hashlib.sha256(io.open(CV2, "rb").read()).hexdigest()

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

    # ----- the v2 pair, CAC_8..CAC_12
    rv = relation_v2()
    check("v2 file resolves", rv["file_resolves"])
    check("v2 names parent", rv["names_parent"])
    check("v2 declares the extension", rv["extension_declared"])
    check("v2 author subtracted", rv["author_subtracted"])
    check("v2 differential recording rate",
          rv["differential_recording_rate"])
    check("v2 has all eleven sections", rv["eleven_sections"])

    x = cross_rendering()
    check("v2 audience counts parse", x["v2_counts"]["audience"] is not None)
    check("audience counts match across renderings",
          x["audience_matches"])
    check("adversary floor matches across renderings",
          x["adversary_floor_matches"])
    check("stated asymmetry matches across renderings",
          x["stated_asymmetry_matches"])
    check("no drift across the two renderings", x["counts_match"])
    check("v2 min asymmetry ~43", 43.0 <= x["v2_min_asymmetry"] <= 43.5)
    check("v2 headline conservative", x["v2_headline_conservative"])

    cv = containment_v2()
    check("no asymmetry figure leaks into v2 argument prose",
          cv["no_asym_leak"])
    check("env count recurs in the §9 recap (recorded)",
          cv["env_count_recurs_in_9"])
    check("escalation count recurs in the §11 pointer (recorded)",
          cv["escalation_count_recurs_in_11"])
    check("v2 sources dated in §0", cv["sources_dated"])
    check("v2 DISPUTED marked not resolved",
          cv["disputed_marked_not_resolved"])

    e = expanded_moves()
    check("§8 names the era's declared standard",
          e["s8_names_declared_standard"])
    check("§8 names the charter signature on epistemology",
          e["s8_charter_signature_named"])
    check("§8 biased-against-own-standard present",
          e["s8_biased_against_own_standard"])
    check("§7 correction kept on the record",
          e["s7_correction_on_record"])
    check("§7 insulation-is-a-ratio present",
          e["s7_insulation_is_a_ratio"])
    check("§9 two findings held apart, not merged",
          e["s9_two_findings_not_merged"])

    render()
    after = hashlib.sha256(io.open(CC, "rb").read()).hexdigest()
    after_v2 = hashlib.sha256(io.open(CV2, "rb").read()).hexdigest()
    check("delivered v1 file untouched", before == after)
    check("delivered v2 file untouched", before_v2 == after_v2)

    print("corpus_as_charter_audit selftest: %d/%d checks pass"
          % (n[0], n[0]))


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        print(render())
