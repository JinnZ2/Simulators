#!/usr/bin/env python3
"""mechanism_11_audit.py -- checks on the Mechanism 11 drop.

Added, not delivered. `MECHANISM_11.md` is the drop as received and is not
modified. Findings recorded in AUDIT_NOTES.md as DD_001..DD_008.

    python3 mechanism_11_audit.py

Mechanism 11 is the third proposed exclusion mechanism for
`../uninstrumented/`, after CATEGORY WELD (9, `../category-weld/`) and
GENERATION CAPACITY REMOVED (10, `../generation-capacity/`). Like
mechanism 10's first drop it arrives as a document with no scorer and no
cases, so nothing here is reconstructed.

LITERATURE CHECKS. Sections 2-4 were run against the open web on
2026-08-18 and are marked. They are NOT reproducible by running this
script -- it does no network access. Section 3's arithmetic IS
reproducible, on the figures recorded there.

stdlib only, deterministic. CC0.
"""

import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = io.open(os.path.join(HERE, "MECHANISM_11.md"), encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


print("derivation-discarded -- audit of the Mechanism 11 drop")
print("delivered: MECHANISM_11.md")
print("not delivered: scorer, cases, README, claim table")

# ---------------------------------------------------------------- DD_001

head(1, "DD_001", "the distinguishing test is the sharpest in the family, and is modal")
block("""
    after the removal, can any party -- including one who wanted to --
    recover what was lost? If the loss is uncountable in principle rather
    than uncounted in practice, it is mechanism 11.

Against the three mechanisms it separates itself from, the distinctions
hold and each names a different object:

  PROXY SUBSTITUTION (6)   a stand-in IS measured. Here nothing stands in.
  SCORED AS WASTE (8)      the quantity is seen and valued at zero or
                           below. Here it is not seen; the value is not
                           low, it is absent from the schema.
  GENERATION CAPACITY (10) the capacity to PRODUCE is removed. Here the
                           record of a COMPLETED computation is destroyed.

That last distinction is the one worth keeping. Mechanism 10 is about a
future that cannot be generated; mechanism 11 is about a past that cannot
be re-derived. Same direction of loss, opposite side of the clock.

**Where it is weaker than it reads.** "Uncountable in principle" is a
MODAL claim, and modal claims are not decided by looking. Every other
distinguishing test in this family resolves against a document or a
count -- mechanism 10's R1 is a recall ratio, `category-weld`'s test is a
divergence spread. This one asks whether a recovery is possible, which is
answered by failing to think of a way, and failing to think of a way is
what `../uninstrumented/`'s own `UNI_005` warns is an absence rather than
a result.

The drop half-anticipates this. Open sub-question 3 asks for "a class of
structure for which the derivation IS recoverable post-removal" and says
the boundary is worth more than the central case, which is correct and is
the operational form of the same question. The test would become decidable
if it were stated as: is the constraint set documented anywhere outside the
structure? That is checkable per case, and the fourth falsifier already
says so -- "the 'only copy' claim fails for any structure whose constraint
set is independently documented."

So the decidable version is already in the document, in the falsifiers,
and the distinguishing test is stated in the undecidable form.
""")

# ---------------------------------------------------------------- DD_002

head(2, "DD_002", "the anchor case verifies as a practice; the figures do not match  [web]")
print()
print("  entry states: 152 of the auditable predictions deemed accurate,")
print("                roughly 73 percent, spread about 38-92 by project type")
print()
print("  located, three separate post-audit studies:")
rows = [
    ("UK, 28 projects", 865, 488, 383, "79% of auditable accurate/nearly"),
    ("second study", 366, None, None, "57% auditable, ~three-quarters accurate"),
    ("third study", 311, 166, 129, "78% of auditable accurate"),
]
print("    %-18s %8s %10s %9s  %s"
      % ("study", "predns", "auditable", "accurate", "as reported"))
print("    " + "-" * 74)
for name, tot, aud, acc, note in rows:
    print("    %-18s %8s %10s %9s  %s"
          % (name, tot, aud if aud else "-", acc if acc else "-", note))
block("""
The practice is exactly as described: post-auditing is a named, published
activity with decades of review literature, and the accuracy figures sit
in a 73-79% band. The mechanism's setup is not invented.

The specific triple the drop quotes -- 152 accurate, ~73%, 38%-92% by
project type -- was NOT located. The figures that surfaced are 383/79%,
~75%, and 129/78%. It may come from a review not surfaced here, so this is
recorded as not-located rather than as wrong, and the characterisation it
supports ("roughly three-quarters, varying by project type") is borne out
by every study found.

Fourth consecutive occasion in this drop family whose practice checks out
(`UNI_015`, `UNI_023`, `UNI_030`), and the first where the specific
numbers attached to it did not.
""")

# ---------------------------------------------------------------- DD_003

head(3, "DD_003", "the literature reports THREE narrowings and never composes them")
TOTAL, AUDITABLE, ACCURATE = 865, 488, 383
UNQUAL = 0.30
print()
print("  from one UK study, all figures as published:")
print("    predictions made                     %4d" % TOTAL)
print("    auditable                            %4d   (%.0f%% of made)"
      % (AUDITABLE, 100.0 * AUDITABLE / TOTAL))
print("    'accurate' or 'nearly accurate'      %4d   (%.0f%% of auditable)"
      % (ACCURATE, 100.0 * ACCURATE / AUDITABLE))
print("    unpredicted impacts recorded            6")
print()
print("    reported separately: 'only 30% of the impacts were unqualifiedly")
print("    close to their forecasts, with almost as many rated accurate")
print("    principally by virtue of the vagueness of the forecasts'")
print()
print("  the headline figure                    %.0f%%" % (100.0 * ACCURATE / AUDITABLE))
print("  accurate as a share of predictions made %.0f%%" % (100.0 * ACCURATE / TOTAL))
print("  unqualifiedly close, if 30%% of auditable %.0f%% of predictions made"
      % (100.0 * UNQUAL * AUDITABLE / TOTAL))
print("  ratio, headline to strict reading       %.1fx"
      % ((ACCURATE / AUDITABLE) / (UNQUAL * AUDITABLE / TOTAL)))
block("""
The drop names one narrowing -- the prediction list as denominator, A'
scored against itself. The published numbers show three, stacked, each
running the same direction:

  1. all impacts        -> predictions made        the drop's point
  2. predictions made   -> auditable               56%, and NOT random:
                                                   the stated reasons are
                                                   lack of data, vague or
                                                   ambiguous predictions,
                                                   and time dependency
  3. 'accurate'         -> unqualifiedly close     ~30%, with almost as
                                                   many scored accurate BY
                                                   VIRTUE OF vagueness

Narrowing 2 is the sharpest addition, because the filter selects against
exactly the predictions most likely to be scored wrong -- a vague
prediction is unauditable, and a vague prediction that survives to be
audited is scored accurate for being vague. The same property removes a
prediction at step 2 or earns it a pass at step 3.

**This makes the anchor case stronger than the drop states it, and for a
different reason.** The drop says the instrument "is constituted so that
[the gap] cannot appear." The literature is more interesting than that:
the gap DOES appear, in pieces -- 56%, ~30%, six unpredicted impacts, the
vagueness caveat -- all published, in the same reviews. What never happens
is the multiplication. No study composes them into one number, so each
piece reads as a caveat on the ~79% headline (78.5% from the counts)
rather than as a factor in a product.

That is `../thermal-sensor-degradation-audit/`'s result on a different
substrate: corruption(trend) = corruption(measurement) x
corruption(framework), multiplicative, and invisible while each term is
reported alone.

The 30% figure's base is not stated unambiguously in what was located, so
the composition above is labelled and should be treated as illustrative
arithmetic on published components rather than as a recovered statistic.
""")

# ---------------------------------------------------------------- DD_004

head(4, "DD_004", "falsifier 1 does not fire; R1's numerator exists and is 6  [web]")
block("""
    Fails if post-audit literature is found that scores against total
    observed impacts rather than against the prediction list.

Not located. Every study surfaced scores against the prediction list, and
one review states the constraint directly -- the denominator is reduced by
data quality and methodological limits, not widened to total observed
impacts. The falsifier stands unfired.

But R1's numerator is not as missing as the drop says. The drop states
"published audits report the numerator inconsistently and often not at
all"; at least one reports it plainly -- **six unpredicted impacts** in the
UK study of 865 predictions across 28 projects.

Six is small, which engages the third falsifier: "weakens substantially if
R1 comes back small -- i.e. if unanticipated impacts really are rare rather
than merely unlooked-for." The literature answers that ambiguously, and in
its own words:

    the reported incidence of such impacts varies greatly across studies
    ... unanticipated impacts often only become apparent while
    investigating actual impacts during post-auditing

A count that varies greatly across studies of the same kind of object is
the signature of a quantity set by search intensity rather than by the
world, and a count that only appears "while investigating actual impacts"
is a count conditioned on someone having looked outside the prediction
list. So R1-small is not yet evidence that unanticipated impacts are rare.
It is evidence that R1 is not yet a measurement.

That is the honest state, and it is neither the drop's expected null nor
its feared refutation.
""")

# ---------------------------------------------------------------- DD_005

head(5, "DD_005", "R2 is the runnable one, and it is also the null test's control")
print()
for tag in ("R1", "R2", "R3"):
    seg = DOC.split("**%s —" % tag, 1)[1].split("\n\n", 1)[0]
    first = " ".join(seg.split())[:150]
    print("  %s  %s" % (tag, first[:66]))
    print("      %s" % first[66:132])
block("""
The drop's own ranking is right: R2 is a documentation audit and needs
library access rather than field data, and the other two need someone to
re-read source EISs against monitoring records or to sample removal
approvals.

Worth adding that R2 does a second job the drop does not claim for it.
THE NULL TEST expects a structural null -- no term for unmodelled function
of the removed structure, anywhere -- and a search that returns nothing has
the problem `../uninstrumented/`'s `UNI_006` names: it has not been shown
that the search would find the thing if it were there.

R2 is the positive control for that. It runs over the same corpus and asks
for something that plainly does exist in some documents -- an explicit
statement of what the denominator is -- so a fraction strictly between 0
and 1 demonstrates the reading protocol can distinguish present from
absent. If R2 also returns zero, the instrument is the problem and not the
field.

That relationship is not stated in the drop and costs nothing to add.
""")

# ---------------------------------------------------------------- DD_006

head(6, "DD_006", "R3's calibration constraint arrives pre-flagged, and inherits a known limit")
print()
cal = DOC.split("Calibration constraint:", 1)[1].split("\n\n", 1)[0]
for line in [l for l in cal.splitlines() if l.strip()]:
    print("  %s" % line.strip())
gc = os.path.join(ROOT, "generation-capacity", "capacity.py")
n = io.open(gc, encoding="utf-8").read().count("scored_against") if os.path.exists(gc) else 0
print()
print("  ../generation-capacity/capacity.py mentions scored_against: %d times" % n)
block("""
Same shape as mechanism 10's CALIBRATION CONSTRAINT, which
`../generation-capacity/capacity.py` implements as a `scored_against`
field that invalidates center-scored readings and drops them from the
slope. `GC_003` recorded what that implementation actually buys: it is a
DECLARATION, not a unit check -- nothing derives the scoring frame from
the data, so a case that declares the right frame and uses the wrong one
passes clean.

Mechanism 11 states the constraint before any code exists, which is the
cheapest point to state it and is a real improvement in sequencing. It
inherits the limit unchanged: "score against the document's own
uncertainty vocabulary" is a judgement about which words in a document
constitute an uncertainty vocabulary, and no rule is given for it.

The three-state readout is right and matches this family's convention --
documented / asserted / absent, no verdict computed, which is
`../presented-binary/binary_audit.py`'s vocabulary exactly. `PB_008`
recorded that its defaults all run toward `absent`, which is the safe
direction, and R3 as specified would want the same.
""")

# ---------------------------------------------------------------- DD_007

head(7, "DD_007", "'do not fill in with an approximation' is now a recurring device")
print()
for src, txt in (
    ("../uninstrumented/cases/case-011.md  Q5",
     "Do not fill this in with an approximation. It is left open on purpose."),
    ("MECHANISM_11.md  sub-question 4",
     "Not articulated. Do not fill in with an approximation."),
):
    print("  %s" % src)
    print("      %s" % txt)
block("""
Second appearance in two drops, and in both it guards the same kind of
slot: an axis the author can see is there and cannot yet separate into a
question.

It is worth naming as a device because it is the only defence a document
has against its own readers, and because there is still no schema slot
behind it anywhere in this family. `UNI_022` recorded that for Case 011:
`entry()` has `note`, which would file an open axis as a remark, so it
would not appear in any sort and nothing would show that the cluster has
an unnamed member.

Mechanism 11's instance is inside a numbered sub-question list, so it is
at least counted -- sub-question 4 of 4 exists as an item even though its
content is withheld. That is a slightly better containment than Case 011's
Q5 achieved, and it happened without a schema change: the numbering did
the work.
""")

# ---------------------------------------------------------------- DD_008

head(8, "DD_008", "the cross-links, and one named twice")
print()
links = [
    ("Case 011", os.path.exists(os.path.join(ROOT, "uninstrumented", "cases",
                                             "case-011.md"))),
    ("Case 012 Q5", os.path.exists(os.path.join(ROOT, "uninstrumented",
                                                "cases", "case-012.md"))),
    ("Mechanism 10", os.path.exists(os.path.join(ROOT, "generation-capacity",
                                                 "MECHANISM_10.md"))),
    ("rural-conflation case", os.path.exists(os.path.join(
        ROOT, "category-weld", "welds", "rural.json"))),
    ("rate-mismatch-polytope", os.path.isdir(os.path.join(
        ROOT, "rate-mismatch-polytope"))),
]
for name, ok in links:
    print("    %-26s %s" % (name, "resolves" if ok else "ABSENT"))
block("""
Four of five resolve, and the fifth is the same one Case 011 named.

`UNI_026` recorded `rate-mismatch-polytope` as absent when Case 011 cited
it for Q2's rate term. It is now cited again, for per-layer clock speeds,
in a different drop. A reference named once is a forward pointer; a
reference named twice across two drops, by two different arguments, is
load-bearing -- both drops are reaching for the same missing object.

What exists instead, and is worth naming for whoever builds it:
`../rigidification-sensor/simulator.py` returns per-tick continuation and
reversal costs with `locked_at` marking the crossing, and
`../sustained-activation-gate/` holds the restore-versus-coupling
trade-off. Sub-question 4's nesting question -- does removal at one layer
have a signature at the layers above, and on what delay -- is a
multi-timescale version of the same crossing, and
`../grounding-layers/temporal_dysrhythmia` already runs six timescales from
microseconds to millennia with translator-switch coupling.

So the missing folder has at least three existing pieces of machinery
aimed at its subject, and none of them is what either drop asked for.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as DD_001..DD_008")
print(BAR)
