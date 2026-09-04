#!/usr/bin/env python3
# gap_completeness.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# Does each gap entry carry everything a researcher would want in hand
# before starting -- not the eight template fields (those are 15 of 15)
# but the post-graduate essentials: a prior-art anchor, a provenance
# status, a secondary falsifier, a deliverable SCHEMA and a code consumer
# it drops into, a known-answer step, cross-gap coupling, an uncertainty
# requirement, and -- for one gap -- a consent step.
#
# Two layers, kept apart. The CENSUS is mechanical (regex over the
# delivered entries; a hit is a hit). The READING per gap is declared
# as data with a one-line basis so a reader can disagree row by row.
# Nothing here edits a delivered file.

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _read(name):
    return io.open(os.path.join(HERE, name), encoding="utf-8").read()


def entries(assembled=False):
    """Gap number -> entry text. Delivered: 1..13 from the delivered
    file, 14 and 15 from the two cards. Assembled: all fifteen from
    UNDERGRADUATE_RESEARCH_GAPS_V2.md (v1 + the cards + the addenda)."""
    if assembled:
        main = _read("UNDERGRADUATE_RESEARCH_GAPS_V2.md")
        parts = re.split(r"(?m)^## (\d+)\. ", main)
        out = {}
        for i in range(1, len(parts), 2):
            out[int(parts[i])] = parts[i + 1]
        return out
    main = _read("UNDERGRADUATE_RESEARCH_GAPS.md")
    parts = re.split(r"(?m)^## (\d+)\. ", main)
    out = {}
    for i in range(1, len(parts), 2):
        out[int(parts[i])] = parts[i + 1]
    out[14] = _read("GAP_14_mining_hydrology.md")
    out[15] = _read("GAP_15_bridge_impoundment.md")
    return out


# The eight fields the delivered template requires.
TEMPLATE = [
    ("gap statement", r"\*\*Gap:\*\*"),
    ("knowledge state", r"\*\*Knowledge state:\*\*"),
    ("research question", r"\*\*Research question:\*\*"),
    ("disciplines", r"\*\*Disciplines:\*\*"),
    ("data sources", r"\*\*Data sources:\*\*"),
    ("method", r"\*\*Method:\*\*"),
    ("deliverable", r"\*\*Expected deliverable:\*\*"),
    ("falsifier", r"\*\*Falsifier:\*\*"),
]

# What a researcher wants beyond the template. Each is a regex over the
# entry; the basis for the choice of pattern is in the README.
POSTGRAD = [
    ("prior-art table (do not re-derive)",
     r"already quantified|do not re-derive"),
    ("citation status / provenance flag",
     r"CITATION STATUS|PROVENANCE FLAG"),
    ("secondary falsifier", r"\*\*Secondary falsifier"),
    ("uncertainty bounds asked for", r"uncertainty bound"),
    ("known-answer / validation step",
     r"Validate against|reproduced on a second machine|"
     r"validation case|reproduce the 19|Known-answer step"),
    ("coupling to other gaps named", r"\bGaps? \d+"),
    ("what-would-move-it per parameter",
     r"names what would move it"),
    # step-form only: the bare word fires on gap 3, where 'tribal
    # consultation' is the quantity being MAPPED (method step 3), not a
    # step the researcher takes -- the word-list miss, kept narrow.
    ("consent / consultation step",
     r"obtain consent|with consent|free, prior|consult(?:ation)? "
     r"(?:with|before)|consent (?:from|of) the|initiate consultation"),
    ("deliverable schema (columns / fields)",
     r"\bcolumns?\b|\bfields?:|\bschema\b|Deliverable schema"),
]


def census(assembled=False):
    ents = entries(assembled)
    rows = []
    for name, pat in TEMPLATE + POSTGRAD:
        have = [g for g in sorted(ents) if re.search(pat, ents[g])]
        rows.append({"field": name, "have": have,
                     "count": len(have),
                     "template": (name, pat) in TEMPLATE})
    return {"rows": rows, "n": len(ents)}


# Where each gap says its deliverable goes, and whether that consumer
# exists as CODE in this folder (a name in the spec is not a drop-in).
CONSUMERS = {
    1: ("contributing_inflow.py", "contributing_inflow.py"),
    2: ("module_f.py (BURN_SEVERITY_MAX etc.)", "module_f.py"),
    3: ("eap_coverage.py (governance layer)", "eap_coverage_v2.py"),
    4: ("eap_coverage node table", "eap_coverage_v2.py"),
    5: ("Module A", None),
    6: ("Module B", None),
    7: ("Module C", None),
    8: ("Module D", None),
    9: ("Module E", None),
    10: ("validation report (no module)", None),
    11: ("exposure table (no module)", None),
    12: ("pipeline + manifest (no module)", None),
    13: ("validation report (module_f is the arithmetic)", "module_f.py"),
    14: ("contributing_inflow interface", "contributing_inflow.py"),
    15: ("Module F initiator interface", "module_f.py"),
}


def consumers():
    out = []
    for g in sorted(CONSUMERS):
        named, f = CONSUMERS[g]
        present = bool(f) and os.path.exists(os.path.join(HERE, f))
        out.append({"gap": g, "named": named, "code": f,
                    "code_present": present})
    return out


# The READING: what a post-graduate researcher would still lack, per
# gap, declared with a basis. "systematic" marks the omissions that are
# template-level (every one of 1-13 has them); the rest are per-gap.
READING = {
    1: ("systematic only", "has a known-answer step (validate against "
        "known storm events) and an uncertainty requirement; lacks the "
        "prior-art anchor and citation status every 1-13 entry lacks."),
    2: ("systematic only", "has a known-answer step (post-flood gage "
        "records) and names the tool; the consumer parameters exist in "
        "module_f.py."),
    3: ("consent step absent", "the method reads 'request or locate' "
        "records from six sovereign nations with no consultation or "
        "consent step; the repo's own field-study discipline makes that "
        "a precondition, not a courtesy. The route exists -- the "
        "deep-research doc's JEB note -- and is not in the entry."),
    4: ("systematic only", "the consumer (the node table) exists; a "
        "tier on NID and a route for the memoranda would close it."),
    5: ("no code consumer; no schema", "breach_params.csv is a "
        "filename: no column list, and Module A exists as a spec name, "
        "not as code. A drop-in has nothing to drop into."),
    6: ("no code consumer; no schema; pre-closure",
        "seismic_params.csv as above, plus the one bare 'if published' "
        "in the file."),
    7: ("no code consumer; no schema", "hydro_params.csv as above."),
    8: ("no code consumer; no schema", "cyber_params.yaml as above; "
        "UNDEFINED is the right state, and the deliverable is a "
        "definition, which is startable."),
    9: ("no code consumer; no schema", "compound_matrix.csv as above; "
        "the falsifier (all factors exactly 1.0) is a point, so it "
        "wants a tolerance."),
    10: ("gated on the model build", "reproducing 1948 presupposes the "
         "HEC-RAS model exists; this is the known answer for the whole "
         "spec, and it cannot start until Gaps 5-9 and 12 have."),
    11: ("gated on a hazard field", "the overlay consumes velocity "
         "bands the engine produces; startable on a published field."),
    12: ("systematic only", "the falsifier is its own known answer; the "
         "cleanest entry in the file."),
    13: ("gated on the model build; known answer is the deliverable "
         "name", "'validation report' names the output, not a positive "
         "control; module_f.py is the arithmetic it runs against."),
    14: ("none beyond the tier axis", "carries prior art, citation "
         "status, secondary falsifier, coupling, uncertainty, "
         "what-would-move-it, and a validation case; sources untiered."),
    15: ("known-answer step absent", "carries prior art, citation "
         "status, secondary falsifier and coupling; the Fjaerland case "
         "is a measured analogue, not a check the deliverable is run "
         "against."),
}


def reading():
    return [{"gap": g, "lack": READING[g][0], "basis": READING[g][1]}
            for g in sorted(READING)]


def tier_coverage_v2():
    """On the assembled file, every Data-sources bullet is paired with
    an addendum tier line naming the same source. Coverage is the
    paired count over the bullet count; UNKNOWN is a tier, not a gap."""
    import kill_audit as K
    ents = entries(assembled=True)
    total = paired = 0
    per_tier = {}
    for g in sorted(ents):
        bullets = K._source_bullets(ents[g])
        tiers = re.findall(r"^- (.+?) — \*\*(OPEN|REQUESTABLE|GATED|UNKNOWN)"
                           r"\*\*; route: ", ents[g], flags=re.M)
        named = dict((src.strip(), t) for src, t in tiers)
        for b in bullets:
            total += 1
            src = b[2:].strip()
            if src in named:
                paired += 1
                per_tier[named[src]] = per_tier.get(named[src], 0) + 1
    return {"bullets": total, "paired": paired, "per_tier": per_tier}


def _wrap(s, n=66):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines or [""]


def render():
    out = []
    w = out.append
    w("GAP COMPLETENESS -- what a researcher would still lack, per gap")
    w("")
    c = census()
    w("CENSUS (mechanical; a hit is a hit)")
    w("  %-40s " % "field" + " ".join("%2d" % g for g in range(1, 16)))
    for r in c["rows"]:
        marks = " ".join(" y" if g in r["have"] else " -"
                         for g in range(1, 16))
        tag = "T" if r["template"] else "P"
        w("  %-38s %s %s" % (r["field"], tag, marks))
    w("  T = template field, P = post-graduate essential")
    w("")
    c2 = census(assembled=True)
    w("CENSUS ON THE ASSEMBLED FILE (v1 + cards + addenda)")
    for r in c2["rows"]:
        if r["template"]:
            continue
        marks = " ".join(" y" if g in r["have"] else " -"
                         for g in range(1, 16))
        w("  %-38s P %s" % (r["field"], marks))
    tc = tier_coverage_v2()
    w("  data-source bullets paired with a tier line: %d of %d   %s"
      % (tc["paired"], tc["bullets"],
         " ".join("%s %d" % kv for kv in sorted(tc["per_tier"].items()))))
    w("")
    tmpl = [r for r in c["rows"] if r["template"]]
    post = [r for r in c["rows"] if not r["template"]]
    w("  template fields present in all 15:  %s"
      % all(r["count"] == 15 for r in tmpl))
    only_new = [r["field"] for r in post
                if set(r["have"]) and set(r["have"]) <= {14, 15}]
    w("  essentials carried ONLY by gaps 14/15: %d of %d"
      % (len(only_new), len(post)))
    for f in only_new:
        w("    - %s" % f)
    none = [r["field"] for r in post if r["count"] == 0]
    w("  essentials carried by NO gap: %s" % (none or "none"))
    w("")
    for ln in _wrap(
            "The split is clean: the eight template fields are 15 of "
            "15, and the post-graduate essentials are what the two "
            "newest cards added -- prior-art table, citation status, "
            "secondary falsifier, cross-gap coupling. Gaps 1-13 carry "
            "none of those. So what a researcher wants beyond the "
            "template is not a new list; it is the shape the author's "
            "own later entries already take, and the template grows by "
            "adopting those fields (the repo's growth rule: add a "
            "declared field, never widen an existing one)."):
        w("  " + ln)
    w("")

    w("DELIVERABLE CONSUMERS -- a name in the spec is not a drop-in")
    cons = consumers()
    for r in cons:
        w("  gap %2d  %-46s code: %s" % (
            r["gap"], r["named"],
            "present" if r["code_present"] else "ABSENT"))
    absent = [r["gap"] for r in cons if not r["code_present"]]
    w("  gaps whose consumer exists as code: %d of 15"
      % (15 - len(absent)))
    for ln in _wrap(
            "Gaps 5-9 deliver a CSV or YAML 'referenced by Module A-E', "
            "and Modules A-E exist as section headers in the delivered "
            "spec, not as code. No gap gives a column list. So the "
            "interface test the cold-start pass scored clean on NAMING "
            "fails on DROP-IN for five gaps: the deliverable is a "
            "filename, and there is nothing in the package for it to "
            "plug into. The three gaps that name a module which does "
            "exist (1, 2, 13-15 via module_f and contributing_inflow) "
            "are the ones a stranger can actually wire."):
        w("  " + ln)
    w("")

    w("THE READING -- per gap, what is still missing, with a basis")
    for r in reading():
        w("  gap %2d  %s" % (r["gap"], r["lack"]))
        for ln in _wrap(r["basis"], 62):
            w("          " + ln)
    w("")
    for ln in _wrap(
            "One instrument note first: a bare 'consult' pattern fires "
            "on gap 3, where 'tribal consultation' is the quantity being "
            "mapped, not a step taken -- the word-list miss this repo "
            "records elsewhere, so the census asks for a step form and "
            "gap 3 reads absent. "
            "Three findings are per-gap rather than template-level. "
            "Gap 3 (tribal EAP) has no consent or consultation step "
            "for records requested from six sovereign nations, while "
            "the repo's own field-study entries make collective consent "
            "a precondition -- an omission at the ethics layer, not the "
            "data layer, and the cheapest to close since the route is "
            "already named in the deep-research doc. Gaps 5-9 have no "
            "code consumer and no schema. And the known-answer step -- "
            "the repo's own rule that no metric ships without one -- is "
            "present in gaps 1, 2, 10, 12 and 14, and absent from the "
            "ten others, which hand a stranger a calibrated parameter "
            "with no positive control to run it against."):
        w("  " + ln)
    w("")
    w("This module computes; it does not conclude. Findings are in")
    w("AUDIT_NOTES.md as CCA_015..CCA_022. Nothing here is a hydraulic")
    w("result; every line is a property of the delivered text.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "gap_completeness.py has no checks of its own. The checks "
            "that exercise it live in selftest_kill.py.\n"
            "    python3 columbia-chain-cascade/selftest_kill.py\n")
        sys.exit(2)
    print(render())
