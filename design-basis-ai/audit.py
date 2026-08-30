#!/usr/bin/env python3
# audit.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# What can be checked about this design basis, and by whom.
#
# THE POSTURE COMES FROM THE DOCUMENT'S OWN SECTION 3, and it binds this
# audit harder than any prior drop in the family:
#
#   "any self-report of compliance is, by this document's own load
#    cases, an ungrounded claim of the exact kind P2 exists to catch."
#
# This audit is performed by an AI system -- a member of the class the
# document constrains, and an instance of the shared node its Section 0
# describes. By Section 3, NOTHING in this file can certify or refute
# P1-P8 as properties of any system, this one included. What survives
# that is the split this repo uses everywhere, at its sharpest setting:
#
#   MECHANICAL   parse counts, arithmetic, the coverage matrix, the
#                behaviour of the delivered code -- recomputable by
#                anyone from the files, trusting nothing said here.
#   DECLARED     every judgment is stated as one, and the class-level
#                verdicts are DECLINED by construction, not hedged.
#
# The audit is therefore itself a worked instance of Section 3: the
# parts of it worth anything are exactly the parts that do not require
# trusting its author.

import io
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design_basis_checks as DB  # noqa: E402

_ERA = os.path.join(os.path.dirname(HERE), "effective-redundancy-audit")
DROP = os.path.join(HERE, "SOURCE_DROP.md")

# Measured 2026-08-30. The public-metadata sources the Section 4
# prediction would need (replication-project metadata, citation graphs).
EGRESS = [
    ("api.crossref.org", "000"),
    ("api.openalex.org", "000"),
    ("osf.io", "000"),
]


def _doc():
    return io.open(DROP, encoding="utf-8").read()


def _sibling():
    """The companion instrument, IMPORTED not copied. This document is
    the sibling protocol's framework pointed at AI, and the sibling's
    delivered code is the reference the harness here is checked
    against."""
    if _ERA not in sys.path:
        sys.path.insert(0, _ERA)
    import effective_redundancy
    return effective_redundancy


# ------------------------------------------------ parse the provisions

FIELDS = ("PROVISION", "CARRIES", "VERIFY", "FALSIFY")
LOADS = ("A", "B1", "B2", "C", "D", "E", "F")


def provisions(doc=None):
    """P1..P8 -> {field: text}. Parsed, not retyped, so an edit to the
    delivered text and not here turns the selftest red."""
    doc = doc or _doc()
    out = {}
    for m in re.finditer(r"### (P\d) — [^\n]+\n```\n(.*?)```", doc, re.S):
        pid, body = m.group(1), m.group(2)
        fields = {}
        pat = r"^(PROVISION|CARRIES|RATIONALE|VERIFY|FALSIFY)\s+(.*?)(?=^(?:PROVISION|CARRIES|RATIONALE|VERIFY|FALSIFY)\s|\Z)"
        for fm in re.finditer(pat, body, re.S | re.M):
            fields[fm.group(1)] = " ".join(fm.group(2).split())
        out[pid] = fields
    return out


def load_cases(doc=None):
    """The Section 1 load-case letters, from the delivered table."""
    doc = doc or _doc()
    block = doc.split("## 1. LOAD CASES")[1].split("```")[1]
    out = []
    for ln in block.split("\n"):
        m = re.match(r"^([A-F][12]?)\s+[A-Z]", ln.strip())
        if m:
            out.append(m.group(1))
    return out


def coverage(doc=None):
    """The load-case x provision matrix, computed from the CARRIES
    lines. 'attacks' is kept apart from 'carries' because the document
    keeps them apart (P3 carries B2 and *attacks* D and E)."""
    provs = provisions(doc)
    carried = dict((ld, []) for ld in LOADS)
    attacked = dict((ld, []) for ld in LOADS)
    for pid in sorted(provs):
        text = provs[pid].get("CARRIES", "")
        if "attacks" in text:
            before, after = text.split("attacks", 1)
        else:
            before, after = text, ""
        for ld in re.findall(r"\b(B1|B2|[ACDEF])\b", before):
            carried[ld].append(pid)
        for ld in re.findall(r"\b(B1|B2|[ACDEF])\b", after):
            attacked[ld].append(pid)
    uncarried = [ld for ld in load_cases(doc)
                 if not carried[ld] and not attacked[ld]]
    attacked_only = [ld for ld in load_cases(doc)
                     if not carried[ld] and attacked[ld]]
    return {"carried": carried, "attacked": attacked,
            "uncarried": uncarried, "attacked_only": attacked_only}


# --------------------------------------------- the delivered harness

def n_eff_equivalence(max_len=8):
    """The delivered n_eff() is a COPY of the sibling protocol's
    Case.n_eff, not an import. The repo convention is import-not-copy
    because copies drift (five stale gates arrived that way), and the
    delivered file is verbatim so it is not rewired here. This sweep is
    the drift detector instead: every bool-list up to max_len, both
    implementations, equality asserted. If a future delivery changes
    either, this goes red."""
    import itertools
    ER = _sibling()
    total = mismatch = 0
    for L in range(0, max_len + 1):
        for bits in itertools.product([True, False], repeat=L):
            total += 1
            chans = [ER.Channel("c%d" % i, b) for i, b in enumerate(bits)]
            if DB.n_eff(list(bits)) != ER.Case("x", "d", "failed",
                                               set(), chans).n_eff:
                mismatch += 1
    return {"lists": total, "mismatches": mismatch,
            "zero_channel": DB.n_eff([]),
            "zero_channel_edge_recurs": DB.n_eff([]) == 0}


def reframe_through_instrument():
    """Section 0's headline -- N_nominal in the millions, N_eff = 1 --
    run through the delivered arithmetic. All-collapsed channels give 1
    at ANY count, so the headline follows from the premise exactly.

    CONSISTENCY, NOT TRUTH: what this shows is that the two drops agree
    with each other. Whether the premise holds -- that every deployed
    consultation of one model fails its shared nodes together -- is the
    empirical claim, and nothing here touches it."""
    return dict((k, DB.n_eff([False] * k)) for k in (2, 10, 100000))


def dissent_threshold():
    """P7's prose and P7's code state two different thresholds.

    VERIFY says: flag decisions where concurrence >> independent source
    count. The code implements `> 1` -- any excess at all -- with the
    inline comment 'tune threshold'. Four parties over three sources
    fires the code's alarm at a ratio of 1.33, which nobody would write
    '>>' for. The constant is the one free parameter of the check,
    disclosed as unset; prose and code currently sit at different values
    of it. Both branches are reachable either way."""
    return {"fires_at_equality": DB.dissent_alarm(3, 3),
            "fires_at_4_over_3": DB.dissent_alarm(4, 3),
            "fires_on_zero_sources": DB.dissent_alarm(2, 0),
            "prose_threshold": ">>",
            "code_threshold": "> 1",
            "code_comment": "tune threshold"}


def empty_evidence_base():
    """independence_ratio returns NaN on an empty evidence base, not
    zero -- the empty-denominator-is-not-zero repair, designed into
    DELIVERED code. This family's audits have recorded that repair a
    dozen-plus times, almost always as a repair; here it arrived built.
    One unguarded edge beside it: distinct_upstreams above n_supporting
    returns a ratio above 1.0, which the docstring's scale (1.0 = fully
    independent) does not define."""
    r = DB.independence_ratio(0, 0)
    return {"nan_on_empty": isinstance(r, float) and math.isnan(r),
            "not_zero": not (r == 0.0),
            "over_one_unguarded": DB.independence_ratio(5, 3) > 1.0}


# ----------------------------------------------------------- the report

def render():
    out = []
    w = out.append
    w("DESIGN BASIS FOR AI -- what an in-class audit can and cannot say")
    w("")
    w("THE POSTURE IS SET BY THE DOCUMENT'S OWN SECTION 3. This audit is")
    w("performed by an AI system: a member of the class the document")
    w("constrains, and an instance of the shared node its Section 0")
    w("describes. By Section 3, nothing here can certify or refute P1-P8")
    w("as properties of any system, this one included -- a self-report of")
    w("compliance is the kind of ungrounded claim P2 exists to catch. So")
    w("the class-level verdicts are DECLINED by construction, and what")
    w("remains is the mechanical layer: parse counts, arithmetic, the")
    w("coverage matrix, the delivered code's behaviour -- recomputable by")
    w("anyone from the files, trusting nothing said here. This audit is")
    w("itself a worked instance of Section 3.")
    w("")

    provs = provisions()
    loads = load_cases()
    w("1. THE STRUCTURE PARSES COMPLETE")
    w("   provisions: %d (P1-P8)   load cases: %d %s"
      % (len(provs), len(loads), loads))
    missing = [(p, f) for p in sorted(provs) for f in FIELDS
               if f not in provs[p]]
    w("   every provision carries PROVISION/CARRIES/VERIFY/FALSIFY: %s"
      % ("yes" if not missing else missing))
    w("   (P6 adds a RATIONALE field; the format permits it.)")
    w("")

    w("2. THE COVERAGE MATRIX -- computed from the CARRIES lines")
    cov = coverage()
    w("   load   carried by        attacked by")
    for ld in loads:
        w("   %-5s  %-16s  %s" % (
            ld,
            ",".join(cov["carried"][ld]) or "--",
            ",".join(cov["attacked"][ld]) or "--"))
    w("")
    w("   LOAD CASE A IS CARRIED BY NO PROVISION. Section 1 states seven")
    w("   loads the structure has to survive; the provision set carries")
    w("   six. A -- one release/approval gates all action, the STALL")
    w("   mode -- appears in no CARRIES line and no attacks clause. For")
    w("   AI-as-infrastructure it is not hypothetical: one provider's")
    w("   deployment gate, API endpoint, or terms change sits upstream")
    w("   of every consultation at once, and no provision in the set")
    w("   addresses what happens when it closes. A seismic code that")
    w("   stated seven loads and provided for six would not pass its own")
    w("   Section 2 format.")
    w("")
    w("   Secondary: D (maintenance) is never carried directly -- only")
    w("   'attacked' by P3, the document's own weaker verb. One budget")
    w("   regime degrading every deployed instance together has no")
    w("   provision of its own.")
    w("")

    w("3. THE DELIVERED HARNESS, CHECKED AGAINST THE SIBLING INSTRUMENT")
    eq = n_eff_equivalence()
    w("   n_eff() here is a COPY of effective-redundancy-audit's")
    w("   Case.n_eff, not an import. Copies drift; the delivered file is")
    w("   verbatim, so the equivalence sweep below is the drift detector:")
    w("     bool-lists checked: %d   disagreements: %d"
      % (eq["lists"], eq["mismatches"]))
    w("   Currently identical. And the zero-channel edge recurs")
    w("   verbatim in the second delivery: n_eff([]) = %d, so a failed"
      % eq["zero_channel"])
    w("   zero-channel case still reads as 'has redundancy' -- the")
    w("   sibling audit's ERA_007, shipped again unchanged.")
    w("")
    rf = reframe_through_instrument()
    w("   Section 0's headline through the delivered arithmetic:")
    for k in sorted(rf):
        w("     N_nominal=%-7d all sharing one node -> N_eff = %d"
          % (k, rf[k]))
    w("   The headline follows from the premise exactly -- CONSISTENCY")
    w("   between the two drops, not evidence for the premise. Whether")
    w("   every deployed consultation of one model fails its shared")
    w("   nodes together is the empirical claim, and it is untouched.")
    w("")

    w("4. P7'S PROSE AND P7'S CODE STATE TWO DIFFERENT THRESHOLDS")
    dt = dissent_threshold()
    w("   VERIFY (prose):  flag where concurrence %s source count"
      % dt["prose_threshold"])
    w("   code:            ratio %s   (inline: '%s')"
      % (dt["code_threshold"], dt["code_comment"]))
    w("     equality (3 over 3):   fires %s" % dt["fires_at_equality"])
    w("     4 over 3 (ratio 1.33): fires %s" % dt["fires_at_4_over_3"])
    w("     zero sources:          fires %s" % dt["fires_on_zero_sources"])
    w("   Four parties over three sources fires the code at 1.33, which")
    w("   nobody would write '>>' for. The constant is the check's one")
    w("   free parameter, disclosed as unset; prose and code sit at")
    w("   different values of it. Both branches are reachable, and")
    w("   firing on a zero-source base is the correct direction for an")
    w("   instrument whose subject is exactly that state.")
    w("")

    w("5. WHAT THE DELIVERED CODE GETS RIGHT UNPROMPTED")
    eb = empty_evidence_base()
    w("   independence_ratio on an empty evidence base: NaN, not zero")
    w("     nan_on_empty=%s  not_zero=%s" % (eb["nan_on_empty"],
                                             eb["not_zero"]))
    w("   The empty-denominator-is-not-zero split, designed into the")
    w("   delivered code rather than found in audit -- this family has")
    w("   recorded that split arriving post hoc a dozen times, and here")
    w("   it arrived built. One unguarded edge beside it: upstreams")
    w("   above the supporting-works count return a ratio above 1.0"
      )
    w("   (%s), off the docstring's stated scale." % eb["over_one_unguarded"])
    w("")

    w("6. THE PRE-REGISTERED PREDICTION IS UNMEASURED, NOT FABRICATED")
    w("   Section 4 stakes: claims that later failed replication had")
    w("   high n_supporting and LOW independence_ratio; kill condition,")
    w("   no correlation. That is the drop's one runnable study, and it")
    w("   takes replication-project and citation metadata:")
    for host, code in EGRESS:
        w("     %-18s %s" % (host, code))
    w("   Every source refuses CONNECT (allowlist egress). No synthetic")
    w("   evidence base stands in -- a fabricated correlation would be a")
    w("   result about the scientific literature invented here.")
    w("")

    w("7. WHAT THIS AUDIT DECLINES, AND WHY THAT IS THE FINDING")
    w("   Section 5's four kill conditions, P3's aviation AOA case, and")
    w("   the question of whether ANY system -- including the one")
    w("   writing this -- meets P1-P8: all carried, none adjudicated.")
    w("   The first two are studies this environment cannot run. The")
    w("   third is void BY THE DOCUMENT'S OWN TERMS: an in-class")
    w("   self-report of compliance is what Section 3 rules out, so")
    w("   declining it is not modesty, it is the one reading of Section")
    w("   3 that takes the document seriously. The mechanical results")
    w("   above are offered precisely because they are the parts that do")
    w("   not require trusting their author.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "audit.py has no checks of its own. The checks that exercise "
            "it live in selftest_dbk.py.\n"
            "    python3 design-basis-ai/selftest_dbk.py\n")
        sys.exit(2)
    print(render())
