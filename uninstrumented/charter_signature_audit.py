#!/usr/bin/env python3
# charter_signature_audit.py -- CC0, stdlib only, parses under 3.9
#
# Audit of CHARTER_SIGNATURE.md, which is landed verbatim and edited
# by nothing here. The delivery declares itself an instrument at N=3,
# held for extension, parent of M-C (G-08) and sibling of M-A. This
# module computes what is computable about those declarations --
# the parent relation as a method diff rather than an assertion, the
# one instance reproducible against a landed record, the resolution
# of every cross-reference -- and prints the structural readings.
# Findings are UNI_169..UNI_175 in AUDIT_NOTES.md. The lag, the
# extension set, and the instrument's own hold are the author's and
# are not touched.

import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CS = os.path.join(HERE, "CHARTER_SIGNATURE.md")
OQ = os.path.join(HERE, "OPEN_QUESTIONS.md")
MARKER = os.path.join(ROOT, "notes", "markers", "HELD_2026_08_31.md")


def _read(path):
    return io.open(path, encoding="utf-8").read()


def _steps(block):
    """Numbered step texts out of a code block ('  1  ...' or '1. ...'),
    with continuation lines folded in."""
    out = []
    for line in block.split("\n"):
        m = re.match(r"^\s*(\d+)[.\s]\s*(\S.*)$", line)
        if m:
            out.append(m.group(2).strip())
        elif out and line.strip() and not line.strip().startswith(
                ("INPUT", "LAG", "HOLD", "reference")):
            out[-1] += " " + line.strip()
    return out


# ------------------------------------------ the parent relation

# The mapping is DECLARED (hand-coded pairs), and each pair's anchors
# are CHECKED to occur in the named step of the named document -- the
# declaration can be wrong but not vague, and a keyword scan deciding
# correspondence on its own would be nonidentity-census T1-1.
CORRESPONDENCE = [
    # (operation, anchor in CS section 5 step, anchor in G-08 step)
    ("extract the declared list", 1, "declared variable list", 1,
     "variable list"),
    ("derive the absence set", 3, "absence set", 2, "absence set"),
    ("separate per M-A", 4, "run M-A", 3, "liability-displaced"),
    ("date the later entry / failure", 6, "failure", 5,
     "triggering failure"),
    ("the lag", 6, "record the LAG", 6, "lag distribution"),
]
CS_ONLY = [
    (2, "mark the residual",
     "purpose-derivability with a marked residual"),
    (5, "boundary disputes",
     "boundary disputes as dated evidence"),
]


def relation():
    """'Parent of M-C, not a sub-case' checked as a method diff:
    section 5 carries every operation G-08's method carries, adds two
    G-08 lacks, and widens the input class from observer manuals to
    any chartered scope. A parent that contradicted a child step
    would be a different relation; none does."""
    cs = _read(CS)
    oq = _read(OQ)
    m5 = re.search(r"## 5\. METHOD.*?```(.*?)```", cs, re.S)
    cs_steps = _steps(m5.group(1))
    g08 = oq.split("## 4. METHODOLOGICAL")[1]
    g08_steps = _steps(re.search(r"\*\*Method:\*\*(.*?)\n\n\*\*",
                                 g08, re.S).group(1))
    shared = []
    for op, ci, ca, gi, ga in CORRESPONDENCE:
        shared.append((op,
                       ca.lower() in cs_steps[ci - 1].lower(),
                       ga.lower() in g08_steps[gi - 1].lower()))
    added = [(ci, an.lower() in cs_steps[ci - 1].lower(), desc)
             for ci, an, desc in CS_ONLY]
    # the additions must be absent from G-08's method entirely
    g08_all = " ".join(g08_steps).lower()
    absent = [an for _ci, an, _d in CS_ONLY
              if an.lower() not in g08_all]
    return {
        "cs_step_count": len(cs_steps),
        "g08_step_count": len(g08_steps),
        "shared_ops_anchored": all(a and b for _o, a, b in shared),
        "shared": shared,
        "cs_additions_anchored": all(ok for _i, ok, _d in added),
        "additions_absent_from_g08": len(absent) == len(CS_ONLY),
        "input_widened": "charter, statute, or constitutional"
                         in cs and "observer manuals" in g08,
    }


# ------------------------------ instance 1 against the record

def instance1():
    """'N=3 verified' splits by provenance. Instance 1 (weather) is
    the one row checkable against a landed record -- the marker
    file's M-C observed and absent sets -- and it reproduces, item by
    item. Instances 2 and 3 are new to this tree and carried."""
    cs = _read(CS)
    mk = _read(MARKER)
    # normalize whitespace: the delivered row wraps items across
    # indented lines ("growing\n           degree accumulation")
    row = " ".join(cs.split("DOMAIN     WEATHER")[1]
                   .split("```")[0].lower().split())
    mc = " ".join(mk.split("## M-C")[1]
                  .split("## M-D")[0].lower().split())
    declared = ["barometer", "thermometer", "wind velocity",
                "rain gauge", "dew point", "condition of", "cloud"]
    absent = ["soil moisture", "soil temperature", "groundwater",
              "streamflow", "snowpack", "evaporation",
              "growing degree", "phenology", "frost dates"]
    return {
        "declared_items_in_both":
            [d for d in declared if d in row and d in mc],
        "declared_all": all(d in row and d in mc for d in declared),
        "absent_items_in_both":
            [a for a in absent if a in row and a in mc],
        "absent_all": all(a in row and a in mc for a in absent),
        "instances_2_3_in_marker":
            "morrill" in mk.lower() or "national bank" in mk.lower(),
    }


# -------------------------------------------- cross-references

def cross_refs():
    cs = _read(CS)
    oq = _read(OQ)
    return {
        "mechanism_file":
            os.path.isfile(os.path.join(
                HERE, "MECHANISM_LIABILITY_DISPLACED.md")),
        "g08_entry": "(G-08)" in oq,
        "marker_mc": "## M-C" in _read(MARKER),
        "cites_g01_g03": "G-01 and G-03" in cs,
        # third instance of the author-numbering citation: under the
        # author's list G-01 is the detection-floor gap the seam-gaps
        # render tags G-02 (see notes/check_markers.py reading 3 and
        # WORK_ORDER_03 Task 4); G-03 carries the same id in both.
        "seam_g03_is_substitution":
            "Substitution reads as stability (G-03)"
            in _read(os.path.join(ROOT, "seam-gaps",
                                  "OPEN_QUESTIONS.md")),
    }


# ----------------------- the education row against falsifier c

def edu_row():
    """A structural reading, not a verdict. Falsifier (c) says: if
    boundary disputes show omitted variables CONSIDERED and declined
    on stated grounds, the absence is guarded, not unguarded. The
    education row's own second note documents a dispute about exactly
    the omitted territory -- a land-grant college arguing biology,
    geology and chemistry satisfied the charter -- closed by statute
    (Hatch 'passed partly to close that'). So one of the three rows
    carries, in its own notes, the evidence class the falsifier
    names, for part of its absence set. The ORDER OF OPERATIONS has
    two output states (displaced / genuinely held-constant) and this
    evidence produces a third: CONTESTED-AND-DECLINED. A stated
    falsifier with no slot in the instrument's own routing -- the
    MF_017 family shape, arriving on a falsifier rather than a
    field. The repair is one step after M-A separation; the
    delivered text is not modified."""
    cs = _read(CS)
    edu = cs.split("DOMAIN     KNOWLEDGE")[1].split("```")[0]
    fals = cs.split("## 6. FALSIFIER")[1].split("## 7.")[0]
    oo = cs.split("ORDER OF OPERATIONS")[1].split("```")[0]
    return {
        "dispute_note_present":
            "boundary contested on the record" in edu
            and "passed partly to close that" in edu,
        "falsifier_c_present":
            "CONSIDERED and\n     declined" in fals
            or "CONSIDERED" in fals,
        # the routing's two output states as written: present under
        # another encoding (the displaced branch), and genuinely
        # held-constant
        "order_of_ops_states":
            ["another encoding" in oo.lower(),
             "held-constant" in oo.lower()],
        "contested_state_in_order_of_ops":
            "contested" in oo.lower() or "declined" in oo.lower(),
        # section 5 step 5 reads the same observable as EVIDENCE of
        # visibility; 6(c) reads it as the falsifier. The
        # discriminator (was the dispute about the omitted variable,
        # and was it declined on stated grounds) is implied, not
        # stated:
        "disputes_used_both_directions":
            "dated evidence" in cs and "guarded, not unguarded"
            in cs,
    }


# --------------------------------------------------- the holds

def holds():
    """Two holds, two denominators, neither releasing the other:
    the instrument refuses a lag DISTRIBUTION at N=3 domains; G-08
    refuses a lag FIGURE below N>1 observation programs. The
    parent's three charters are not the child's programs, so the
    child's hold stands untouched by the parent's N."""
    cs = _read(CS)
    oq = _read(OQ)
    return {
        "cs_hold": "do not report a lag distribution at N=3" in cs,
        "g08_hold": "no lag figure until N>1 programs" in
                    oq.replace("\n", " ")
                    or "N>1 programs" in oq,
    }


# ------------------------- carried facts, coded by provenance

# Hand-coded DATA, printed not computed. This is the first delivery
# in the family whose occasion facts sit BEFORE the environment's
# knowledge horizon instead of after it, so a consistency reading
# from prior general knowledge is possible at all. CONSISTENT_PRIOR
# is consistency with knowledge held before the delivery -- it is
# NOT primary-source verification (the ANC_010 line); CARRIED is
# carried and uncheckable from here.
FACTS = [
    ("Morrill Act 1862; Hatch Act 1887", "CONSISTENT_PRIOR",
     "both statutes and dates match prior knowledge"),
    ("'useful plants' / 'manures' as statutory language",
     "CONSISTENT_PRIOR",
     "matches Hatch Act section 2 phrasing as known"),
    ("'industrial classes' / 'pursuits and professions'",
     "CONSISTENT_PRIOR", "matches Morrill Act phrasing as known"),
    ("National Bank Acts 1863-64; real-estate lending restriction",
     "CONSISTENT_PRIOR",
     "the chartering-act restriction held until the Federal "
     "Reserve Act era"),
    ("lag anchors: USDA transfer 1891, FFLA 1916, FDIC 1933, "
     "SCS 1935, NSF 1950, mining law 1866/1872",
     "CONSISTENT_PRIOR", "all six dates match prior knowledge"),
    ("soil moisture measurable in the period (the 6a counter-test's "
     "load-bearing premise)", "CONSISTENT_PRIOR",
     "gravimetric measurement predates the window"),
    ("McCulloch ABA address, October 1876, and the quoted line",
     "CARRIED",
     "the address and quote are not locatable from here; NOTE: "
     "the Comptrollership was 1863-65, a decade before the "
     "address date -- reads as identification by best-known "
     "office, recorded rather than adjudicated"),
    ("~30% of mortgages bank-held, early 1890s", "CARRIED",
     "no source reachable"),
    ("~35% of NYC loans callable on demand, 1900", "CARRIED",
     "no source reachable"),
    ("stations favored by urban elites to deflect populist "
     "demands", "CARRIED", "an attributed reading, no source"),
]


def _wrap(s, n=66, indent="     "):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return ("\n" + indent).join(lines)


def render():
    out = []
    w = out.append
    w("CHARTER SIGNATURE -- AUDIT")
    w("(the delivered file is edited by nothing here; the lag, the")
    w(" extension set and the hold are the author's)")
    w("")
    r = relation()
    w("PARENT RELATION, AS A METHOD DIFF")
    w("  section 5 steps %d, G-08 method steps %d"
      % (r["cs_step_count"], r["g08_step_count"]))
    w("  shared operations anchored in both: %s"
      % r["shared_ops_anchored"])
    w("  additions (in section 5, absent from G-08's method):")
    for _i, _ok, desc in [(a, b, c) for a, b, c in CS_ONLY]:
        w("    - %s" % desc)
    w("  additions anchored %s, absent from G-08 %s; input widened"
      % (r["cs_additions_anchored"], r["additions_absent_from_g08"]))
    w("  from observer manuals to any chartered scope: %s"
      % r["input_widened"])
    w("  'parent, not a sub-case' holds structurally.")
    w("")
    i1 = instance1()
    w("INSTANCE 1 AGAINST THE LANDED RECORD")
    w("  declared list reproduces the marker's M-C observed set:")
    w("  %d/%d items; absent list %d/%d items"
      % (len(i1["declared_items_in_both"]), 7,
         len(i1["absent_items_in_both"]), 9))
    w("  instances 2 and 3 are new to this tree (in the marker: %s)"
      % i1["instances_2_3_in_marker"])
    w("  so 'N=3 verified' splits: 1 reproduced against a landed")
    w("  record, 2 carried -- the first delivery in this family")
    w("  whose occasion sits before the knowledge horizon.")
    w("")
    e = edu_row()
    w("THE EDUCATION ROW AGAINST FALSIFIER (c)")
    w("  dispute note present %s; falsifier (c) present %s"
      % (e["dispute_note_present"], e["falsifier_c_present"]))
    w("  ORDER OF OPERATIONS output states: displaced %s,"
      % e["order_of_ops_states"][0])
    w("  held-constant %s; contested-and-declined: %s"
      % (e["order_of_ops_states"][1],
         e["contested_state_in_order_of_ops"]))
    w("  The row's own note carries the evidence class the")
    w("  falsifier names, and the routing has no state for it;")
    w("  disputes are read as evidence in 5.5 and as the falsifier")
    w("  in 6(c) with the discriminator implied (%s). UNI_171/172."
      % e["disputes_used_both_directions"])
    w("")
    h = holds()
    w("THE TWO HOLDS")
    w("  instrument: no lag distribution at N=3 (%s)" % h["cs_hold"])
    w("  G-08: no lag figure below N>1 programs (%s)" % h["g08_hold"])
    w("  different denominators; neither releases the other.")
    w("")
    c = cross_refs()
    w("CROSS-REFERENCES")
    for k, v in c.items():
        w("  %-28s %s" % (k, v))
    w("  the G-01 citation is the author's numbering, third")
    w("  instance; the seam-gaps ids yield to it per that README.")
    w("")
    w("CARRIED FACTS, BY PROVENANCE (declared codings, not")
    w("computations; CONSISTENT_PRIOR is not verification)")
    for fact, status, basis in FACTS:
        w("  %s" % _wrap(fact, 64, "  "))
        w("     %s -- %s" % (status, _wrap(basis)))
    w("")
    w("This module computes; it does not conclude. Findings are")
    w("UNI_169..UNI_175 in AUDIT_NOTES.md.")
    return "\n".join(out)


def selftest():
    n = [0]

    def check(name, ok):
        n[0] += 1
        if not ok:
            sys.stderr.write("FAIL %s\n" % name)
            sys.exit(1)

    before = hashlib.sha256(io.open(CS, "rb").read()).hexdigest()

    r = relation()
    check("cs six steps", r["cs_step_count"] == 6)
    check("g08 six steps", r["g08_step_count"] == 6)
    check("shared ops anchored", r["shared_ops_anchored"])
    check("additions anchored", r["cs_additions_anchored"])
    check("additions absent from g08", r["additions_absent_from_g08"])
    check("input widened", r["input_widened"])

    i1 = instance1()
    check("declared list reproduces", i1["declared_all"])
    check("absent list reproduces", i1["absent_all"])
    check("instances 2-3 not in marker",
          not i1["instances_2_3_in_marker"])

    e = edu_row()
    check("dispute note present", e["dispute_note_present"])
    check("falsifier c present", e["falsifier_c_present"])
    check("two order-of-ops states", all(e["order_of_ops_states"]))
    check("no contested state in routing",
          not e["contested_state_in_order_of_ops"])
    check("disputes read both directions",
          e["disputes_used_both_directions"])

    h = holds()
    check("instrument hold on page", h["cs_hold"])
    check("g08 hold on page", h["g08_hold"])

    c = cross_refs()
    check("mechanism file resolves", c["mechanism_file"])
    check("g08 entry resolves", c["g08_entry"])
    check("marker M-C resolves", c["marker_mc"])
    check("g01/g03 cited", c["cites_g01_g03"])
    check("seam g03 is substitution", c["seam_g03_is_substitution"])

    # every fact row carries a status from the fixed vocabulary and
    # a non-empty basis -- a coding without a basis is an assertion
    check("fact codings well-formed",
          all(s in ("CONSISTENT_PRIOR", "CARRIED") and b.strip()
              for _f, s, b in FACTS))
    check("both statuses occur",
          {s for _f, s, _b in FACTS} ==
          {"CONSISTENT_PRIOR", "CARRIED"})

    render()
    after = hashlib.sha256(io.open(CS, "rb").read()).hexdigest()
    check("delivered file untouched", before == after)

    print("charter_signature_audit selftest: %d/%d checks pass"
          % (n[0], n[0]))


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        print(render())
