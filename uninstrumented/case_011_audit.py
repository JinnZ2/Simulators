#!/usr/bin/env python3
"""case_011_audit.py -- checks on the Case 011 drop.

Added, not delivered. `cases/011rebuildabandonmentcycles.md` is the entry as received and is
not modified. Findings recorded in AUDIT_NOTES.md as UNI_020..UNI_026.

    python3 case_011_audit.py

Case 011 is the second consecutive delivered case the register's schema
cannot hold, and it strains it in a different place than Case 010 did.
Case 010 declined to name its mechanism; Case 011 declines to be one
quantity.

LITERATURE CHECKS. Four of the checks below were run against the open web
on 2026-08-18 and their results are recorded here as data. They are NOT
reproducible by running this script -- it does no network access -- and
they are marked. Everything computed from the register, from the entry
text, and from other folders in this repo is reproducible.

stdlib only, deterministic. CC0.
"""

import inspect
import io
import json
import os
import re

import uninstrumented as U

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CASE = io.open(os.path.join(HERE, "cases", "011rebuildabandonmentcycles.md"),
               encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


subq = re.findall(r"^### (Q\d) — (.*)$", CASE, re.M)

print("uninstrumented -- audit of the Case 011 drop")
print("delivered: cases/011rebuildabandonmentcycles.md")
print("register  : %d entries, %d mechanisms" % (len(U.ENTRIES),
                                                 len(U.MECHANISMS)))
print("cluster   : %d sub-questions" % len(subq))

# ---------------------------------------------------------------- UNI_020

head(1, "UNI_020", "the cluster is not constructible either, for a new reason")
print()
print("  entry() takes ONE of each:")
for f in ("quantity", "excluded_by", "would_measure"):
    print("    %s" % f)
print()
print("  Case 011 carries:")
for qid, title in subq:
    body = CASE.split("### %s" % qid, 1)[1].split("\n### ", 1)[0]
    has_ex = "EXCLUDED BY" in body
    has_wm = "WOULD MEASURE" in body
    print("    %-3s %-42s excluded_by=%-5s would_measure=%s"
          % (qid, title[:42], has_ex, has_wm))
block("""
Two delivered cases, two different refusals by the same schema.

  Case 010   declines to name its mechanism        -> excluded_by is closed
  Case 011   declines to be one quantity           -> quantity is scalar

`entry()` takes one `quantity`, one `excluded_by` and one `would_measure`.
Case 011 carries five sub-questions, four of which have their own
WOULD MEASURE and one its own EXCLUDED BY, and the entry states in its
first line that the quantity is not yet singular. (Q4's WOULD MEASURE is
the word "unclear", which is a filled field and not an empty one -- it
records that the instrument is not obvious, which is different from not
having looked.)

So the schema fits filed single-quantity entries and neither of the two
real cases that have actually been delivered to it. That is worth stating
plainly, because the eight entries it does hold were written by the same
author to fit it, and a schema fitted to its own examples is not yet
tested (`UNI_002`'s open question, from a different direction).

The `UNI_013` repair -- an `UNASSIGNED` sentinel -- does not cover this
one. A cluster needs sub-entries: a parent with `questions=[...]`, each
carrying its own `excluded_by` (possibly `UNASSIGNED`) and its own
`would_measure`, so that a question can be closed individually while the
cluster stays open. Q1 and Q3 below both narrow without closing, which is
exactly the state a scalar entry cannot record.
""")

# ---------------------------------------------------------------- UNI_021

head(2, "UNI_021", "a deliberately unstated confidence is stored as an omission")
print()
for val in ("", None):
    e = U.entry("q", "MODALITY", "v", "w", val, "hydrology")
    print("  entry(confidence=%-6r) -> accepted, stored as %r"
          % (val, e["confidence"]))
print()
print("  three states now exist in the wild:")
print("    high                      8 of 8 original entries")
print("    a gradient, ~40 percent    Case 010")
print("    deliberately not stated   Case 011, with the reason given")
print("  states the schema can tell apart: 2")
block("""
The register's own rule for this field is that confidence is "recorded
verbatim and not adjudicated". Case 011 does not state one, and says why:

    This is a cluster of open questions, and a scalar over a cluster would
    not carry usable information. Individual questions may take gradients
    once separated.

That is a reasoned refusal, and `entry()` accepts `""` and `None` without
comment, so it lands in the same cell as a field somebody forgot to fill.
Eleventh instance of the absent-versus-known-negative repair in this drop
family, and it is in the one field the register singles out as recorded
rather than judged.

Case 010 made the field non-constant (`UNI_014`). Case 011 shows the field
needs three states, not a wider range of one.
""")

# ---------------------------------------------------------------- UNI_022

head(3, "UNI_022", "Q5 is the strongest move in the drop and has no slot")
q5 = CASE.split("### Q5", 1)[1].split("## CROSS-LINKS", 1)[0]
print()
for line in [l for l in q5.splitlines() if l.strip()][1:]:
    print("  %s" % line.strip())
block("""
This is the register's own thesis applied to the register's own
vocabulary. `uninstrumented` exists because forcing a quantity through an
apparatus that cannot represent it is the operation that removes it; Q5
says the same of forcing an observation into the eight bins before it has
a shape, and refuses.

It is also the cheapest instruction in the drop to violate. Every
downstream reader -- human or model -- is under pressure to produce a
name, and "political and ownership structure of the affected area" is close
enough to several existing mechanisms that a plausible bin is easy to
supply. The entry pre-empts that with a direct instruction, which is the
only defence available to a document.

No schema slot. `note` would hold the text and would file it as a remark
rather than as an open axis with a count, so `Q5` would not appear in any
sort and nothing would show that this cluster has an unnamed member.
""")

# ---------------------------------------------------------------- UNI_023

head(4, "UNI_023", "the occasion, checked  [web, 2026-08-18, not reproducible here]")
CLAIMED = [
    ("Kiss, Viglione, Blöschl et al., Nature, 12 Aug 2026", "CONFIRMED",
     "published 12 Aug 2026"),
    ("title 'Cascading continental-scale floods across Europe in 1342-1343'",
     "CONFIRMED", "exact"),
    ("DOI 10.1038/s41586-026-10888-8", "CONFIRMED",
     "resolves to that article"),
    ("16 distinct flood events", "CONFIRMED",
     "reported as a sequence of 16 major flood events"),
    ("stated implication: management not built for sequences", "CONFIRMED",
     "reported as: current flood management is unprepared for such "
     "sequences"),
    ("'within roughly 18 months'", "DRIFTS",
     "coverage describes the sequence as spanning late 1341 to 1343, about "
     "two years. The entry is quoting the paper's own title window "
     "(1342-1343); the body window is wider than the title."),
]
print()
for claim, status, note in CLAIMED:
    print("  %-9s %s" % (status, claim))
    for i in range(0, len(note), 62):
        print("            %s" % note[i:i + 62])
block("""
Five of six exact, one drift, and the drift is inherited from the title
rather than introduced. Worth recording precisely because Q2 proposes
1342-1343 as a candidate corpus and the corpus boundary is the thing that
would be set by it: if the sequence starts in late 1341, an
inter-event-interval reconstruction that begins at 1342 drops the first
interval, which is the one that establishes the arrival rate.

Second consecutive occasion in this register that checks out against the
published record, after Case 010 (`UNI_015`).
""")

# ---------------------------------------------------------------- UNI_024

head(5, "UNI_024", "Q1 narrows: the hazard's antecedent state is instrumented, the system's is not")
block("""
Q1 bundles three things in one sentence:

    A second event arrives into saturated ground, unrepaired works, and
    spent response capacity.

They do not have the same status, and the falsifier fires on the first.

  SATURATED GROUND -- instrumented, and quantitatively dramatic.
  Antecedent moisture condition is a standard variable in flood frequency
  analysis. Reported effect sizes: under saturated soil a 7-year
  precipitation event can produce a 100-year flood, while a 200-year
  precipitation event on dry soil can produce a 15-year flood. That is the
  entry's own mechanism -- the second event is not the first one scaled up
  -- already measured, and measured to matter more than the rainfall
  return period.

  COMPOUND / SEQUENCE HAZARD -- an active quantified field. Compound storm
  events are modelled with published flooded-area figures by return
  period.

  UNREPAIRED WORKS, SPENT RESPONSE CAPACITY -- no design-standard variable
  located. The levee standards reached specify design frequency and storm
  duration; nothing representing pre-event repair completion was found.

So the general statement worth taking from Q1 is sharper than the one it
makes: the field instruments the antecedent state of the HAZARD and not
the antecedent state of the SYSTEM. Catchment wetness carries forward
between events; the condition of the works and of the people who operate
them does not.

Same shape as `UNI_017` on Case 010 one case earlier: the strong reading
of the falsifier fires, the narrow one survives, and the edit is to split
the sentence.
""")

# ---------------------------------------------------------------- UNI_025

head(6, "UNI_025", "Q3 narrows along the boundary of whoever keeps the record")
print()
print("  the entry's four pathways, against what a post-disaster record holds:")
rows = [
    ("residents decide", "ATTRIBUTED",
     "FEMA HMGP acquisitions are required to be voluntary; the owner "
     "agrees to sell and eminent domain is excluded"),
    ("state declines to fund works", "ATTRIBUTED",
     "state and local governments decide which properties to acquire, "
     "under federal restriction, and that selection is recorded"),
    ("insurer withdraws coverage", "NOT LOCATED",
     "a commercial decision, outside the program that keeps the record"),
    ("lender declines to finance rebuild", "NOT LOCATED",
     "same"),
]
for path, status, why in rows:
    print("    %-34s %s" % (path, status))
    for i in range(0, len(why), 58):
        print("      %s" % why[i:i + 58])
block("""
Q3's falsifier partially fires, and the split is not random: the two
pathways with attribution are the two inside the institution that keeps
the record, and the two without are the two outside it.

That is a boundary result rather than an oversight, and it is the register's
own subject. A post-disaster program records the decisions it makes and the
consent it obtains. An insurer's withdrawal and a lender's refusal are
decisions by parties the program does not administer, so they cannot appear
in its record whatever anyone intends -- and the site still ends up
unoccupied, logged the same way.

The entry's own cross-link is instanced by the same fact. "Voluntary" is a
truthful attribution of the final step, and the option set that step ranges
over is generated elsewhere -- which properties the administering authority
chose to fund, under federal restriction. That is
`../generation-capacity/MECHANISM_10.md` exactly: the choice is real, the
record is honest, and the generation happened upstream on a clock the
choosing party has no access to.
""")

# ---------------------------------------------------------------- UNI_026

head(7, "UNI_026", "the cross-links, resolved")
print()
links = [
    ("rate-mismatch-polytope", os.path.isdir(os.path.join(ROOT, "rate-mismatch-polytope"))),
    ("generation-capacity", os.path.isdir(os.path.join(ROOT, "generation-capacity"))),
    ("rural-conflation case", os.path.exists(os.path.join(
        ROOT, "category-weld", "welds", "rural.json"))),
    ("Case 010", os.path.exists(os.path.join(HERE, "cases", "010coupledperturbationbiohybrid.md"))),
]
for name, ok in links:
    print("    %-26s %s" % (name, "resolves" if ok else "ABSENT"))
rural = json.load(io.open(os.path.join(ROOT, "category-weld", "welds",
                                       "rural.json"), encoding="utf-8"))
print()
print("  rural weld, as delivered:")
print("    tracked_by_label : %s" % rural.get("tracked_by_label"))
print("    components       : %s"
      % ", ".join(c.get("id", "?") for c in rural.get("components", [])))
block("""
Three of four resolve, and the one that does not is named as though it
were a folder in this repo.

The rural cross-link is not only present but accurately characterised:
`rural` is tracked by `density` -- a headcount per area -- with
`self_support` as one of the welded components, which is exactly the
entry's "the instrument counts headcount, not what is holding".

`rate-mismatch-polytope` does not exist anywhere in the tree; the two
apparent hits under `../declared-frame/` are the phrase "separate mismatch
line" and are unrelated. Seventh instance of a reference naming an absent
artifact in this drop family (`CW_001`, `PB_001`, `GC_009`, `PB_015`,
`MD_001`, `DL_014`), three of which landed a drop later.

The nearest existing kin are worth naming, because Q2's hypothesis is
already modelled twice here in a different vocabulary.
`../rigidification-sensor/` runs on exactly Q2's comparison -- variance
suppressed faster than it regenerates, with `locked_at` recording the tick
where the cost of reversal passes the cost of continuation -- and
`../sustained-activation-gate/` holds the restore-versus-coupling
trade-off. Q2's "same total water across 40 years versus across 4 years" is
a repair-rate against an arrival-rate, which is the same crossing.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_020..UNI_026")
print(BAR)
