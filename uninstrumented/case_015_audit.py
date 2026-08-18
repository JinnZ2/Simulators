#!/usr/bin/env python3
"""case_015_audit.py -- checks on the Case 015 drop.

Added, not delivered. `cases/case-015.md` is the entry as received and is
not modified. Findings recorded in AUDIT_NOTES.md as UNI_050..UNI_057.

    python3 case_015_audit.py

Case 015 proposes a new mechanism -- DEFINITIONAL PRECEDENCE -- and its
central claim is checkable in an unusual way: the field's own
classification vocabulary either has a slot for the finding or it does
not, and that is a matter of published record rather than of judgement.

LITERATURE CHECKS. Sections 1, 2, 3, 4 and 5 were run against the open web
on 2026-08-18 and are marked. They do NOT reproduce by running this
script, which does no network access. The arithmetic in section 5 does.

stdlib only, deterministic. CC0.
"""

import io
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CASE = io.open(os.path.join(HERE, "cases", "case-015.md"),
               encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


print("uninstrumented -- audit of the Case 015 drop")
print("delivered: cases/case-015.md")
print("mechanism candidate: DEFINITIONAL PRECEDENCE, not assigned")

# ---------------------------------------------------------------- UNI_050

head(1, "UNI_050", "the occasion verifies, with one word that moved  [web]")
print()
for claim, status, note in (
    ("five authors: Albright, Anil, Evans, Ntamubano, Kozik", "CONFIRMED",
     "Claire Albright, Gouri Anil, Jacob Evans, Souzane Ntamubano, "
     "Ariangela Kozik"),
    ("J. Bacteriology 2026, doi 10.1128/jb.00142-26", "CONFIRMED", "resolves"),
    ("bioRxiv 2026.01.19.700327", "CONFIRMED", "resolves"),
    ("University of Michigan", "CONFIRMED", "Kozik, U-M Medical School"),
    ("~100-year-old classification", "CONFIRMED",
     "the source's own phrase: 'a correction to the 100-year-old "
     "classification'"),
    ("growth limit between 5% and 8%", "CONFIRMED as an inference",
     "growth maintained at 2% and 5%; 8% was the next level tested, so "
     "the limit is bracketed exactly as stated"),
    ("robust aerotolerance at 21%", "CONFIRMED", "'robust aerotolerance "
     "in 21% O2'"),
    ("title: 'lung commensal'", "DRIFTS",
     "the bioRxiv preprint says 'Lung Commensal'; the Journal of "
     "Bacteriology version says 'lung symbiont'. The entry cites the JB "
     "doi and uses the preprint's word."),
):
    print("  %-24s %s" % (status, claim))
    for i in range(0, len(note), 56):
        print("                           %s" % note[i:i + 56])
block("""
Everything checks, and the one drift is small and pointed. Between
preprint and publication the relationship word for the organism changed
from COMMENSAL to SYMBIONT -- a categorical relabeling, inside the paper
whose subject is a categorical relabeling that took a century. Nothing
turns on it for the entry's argument; it is worth a line because the
entry's own QUANTITY line says "oxygen tolerance of a commensal organism",
and the published version no longer uses that word.

Also located and not in the entry: P. melaninogenica is reported at more
than 10% of microbial populations in both healthy and diseased lungs.
That is a stronger version of "prevalent" than the entry claims, and it
sharpens the contradiction the paper names.
""")

# ---------------------------------------------------------------- UNI_051

head(2, "UNI_051", "Q1's mechanism is refuted and its conclusion strengthened  [web]")
print()
print("  the field's oxygen vocabulary, as published:")
for i, (name, note) in enumerate((
    ("obligate aerobe", "requires O2, survives atmospheric"),
    ("facultative anaerobe", "uses O2 if present, otherwise not"),
    ("microaerophile", "requires O2 at about 1-10%, harmed at 21%"),
    ("aerotolerant anaerobe", "survives O2, does not use it for growth"),
    ("obligate anaerobe", "does not survive normal atmospheric O2"),
), 1):
    print("    %d. %-24s %s" % (i, name, note))
print()
print("  and the range documented WITHIN the obligate-anaerobe category:")
print("    'some obligate anaerobes can survive in up to 8% oxygen, while")
print("     others cannot survive unless the oxygen concentration is less")
print("     than 0.5%'")
block("""
Q1 opens: "Aerobe / anaerobe is a two-state classification."

It is five-state, and has been for as long as the textbook categories
have existed. One of the five -- **aerotolerant anaerobe** -- is named for
exactly the phenomenon the 2026 paper reports: survives oxygen, does not
use it for growth.

So the entry's stated mechanism does not hold. The category system did not
lack a slot. It had one, named for this, sitting between the two the entry
says are the only options.

**And that makes the entry's conclusion stronger, not weaker.** The claim
DEFINITIONAL PRECEDENCE is making is that the label outranked the
observation. If the vocabulary had genuinely been binary, the label
holding would be partly a tooling failure -- there would have been nowhere
to file the result. With five categories and one named for the finding,
the label held **despite** an available slot. That is a worse failure and
better evidence for the mechanism the case is proposing.

There is a second published figure that cuts the same way. The
obligate-anaerobe category's own documented range reaches **8% oxygen**.
The measured growth limit for P. melaninogenica -- between 5% and 8% --
sits INSIDE the range already published for the category it was assigned
to. What exceeds the category is the 21% aerotolerance, not the growth
limit.

So the finding is not "an organism turned out to be outside its category
by two orders of magnitude". It is closer to "an organism turned out to
sit at the documented top of its own category, and at a neighbouring
category on a second axis, and neither was checked for a century."
""")

# ---------------------------------------------------------------- UNI_052

head(3, "UNI_052", "Q1's falsifier partly fires, and the refinement beats the claim  [web]")
block("""
    Q1 fails if oxygen classifications are routinely established by
    gradient measurement and the binary is a reporting convention only.

The standard assay is a **thioglycollate broth tube**, and the located
description is explicit: the categories "can be distinguished
experimentally using thioglycollate broth tubes, where position in the
tube reflects the organism's oxygen preference."

A thioglycollate tube establishes an oxygen gradient down its length. The
standard method is a gradient method. So "standard anaerobic culture
reproduces the binary, not the gradient" is not right about the protocol.

What the assay does not do is **quantify**. It returns a POSITION, which
maps to a category NAME. It never returns a concentration.

That is the sharper form of the entry's own case, and it is a better
statement of the exclusion than the one Q1 gives:

    the numeric threshold attached to the label was never measured by
    the assay that assigns the label

A number like 0.05% cannot come out of a tube where you read a band's
depth. It has to come from somewhere else, get attached to the category
name, and then travel with every organism assigned that name by an assay
that could not have produced it. The real-time sensor platform matters
because it is a quantifying instrument, not because it is a gradient one
-- the gradient was already there.
""")

# ---------------------------------------------------------------- UNI_053

head(4, "UNI_053", "the titling claim verifies verbatim  [web]")
print()
print("  entry's VISIBLE AS: 'earlier work exists titled to the effect of")
print("  oxygen inducing mutation in a strict anaerobe, Prevotella'")
print()
print("  located, verbatim:")
print("    'Oxygen induces mutation in a strict anaerobe, Prevotella")
print("     melaninogenica' (2008)")
print()
print("  interval to the 2026 paper: 18 years")
block("""
Exact, including the word order. And the 2008 study's own findings make
the point harder than the entry does: oxygen exposure decreased cell
survival, increased oxidative DNA damage, and raised mutation frequency.

That is an oxygen-response measurement on the organism, published, with
the label retained in the title of the paper doing the measuring. The
mechanism the case proposes -- the label converts the observation rather
than being tested by it -- is instanced in a single title.
""")

# ---------------------------------------------------------------- UNI_054

head(5, "UNI_054", "Q3 is partly resolvable, and the two branches are not exclusive")
block("""
Q3 leaves open whether the binding constraint was the instrument or the
category, and says the two "have different implications for how many other
cases are currently sitting in this state."

The 2008 paper is evidence, and it lands on the **category** branch:
oxygen experiments were being run on this organism 18 years before the
sensor platform, and the classification survived them.

It does not settle the instrument branch, and this is the part worth
stating. The 2008 readout was mutation frequency and survival under
exposure -- not growth across intermediate concentrations. A study of that
design cannot produce a growth-limit number no matter how carefully it is
run, so its failure to revise the threshold is not evidence that the
instrument was available.

**The branches are not exclusive, and the 2008 paper shows both
operating**: the category held through oxygen experiments, and those
experiments used a readout incapable of producing the number that would
have challenged it. Q3's framing as an either/or is what needs the edit;
the open question underneath it -- how many other cases sit in this state
-- is unaffected, and the joint reading makes it worse, since it requires
both a missing quantifier and a holding label rather than either alone.
""")

# ---------------------------------------------------------------- UNI_055

head(6, "UNI_055", "the headline number rests on a figure that was not located")
print()
print("  entry: historical threshold 0.05%, measured limit 5-8%,")
print("         'roughly two orders of magnitude'")
print()
for thr, lo, hi in ((0.05, 5.0, 8.0), (0.5, 5.0, 8.0)):
    print("    threshold %.2f%%  ->  ratio to 5%% = %5.0fx   to 8%% = %5.0fx"
          "   (%.1f orders at 5%%)"
          % (thr, lo / thr, hi / thr, math.log10(lo / thr)))
block("""
At 0.05% the arithmetic is exact: 5 / 0.05 = 100, two orders of magnitude
on the nose.

The 0.05% figure itself was **not located**. What was located is the
general category description, which gives **0.5%** as the low-end figure
-- "others cannot survive unless the oxygen concentration is less than
0.5%". That is an order of magnitude above the entry's number.

If the operative historical figure for this organism were 0.5%, the gap is
one order of magnitude, not two, and "a wrong number that stood for
approximately 100 years" becomes a smaller wrong number. The entry may
well be quoting a Prevotella-specific threshold from the source paper,
which is a different quantity from the category's general low end, and
0.05% is a figure that appears in anaerobe handling literature.

Recorded as NOT LOCATED rather than as wrong. It is the one number in the
entry that the headline claim depends on, and the neighbouring published
figure differs from it by exactly the amount that halves the exponent.
Cheapest check for anyone with the paper: the threshold the source
attributes to the historical classification.
""")

# ---------------------------------------------------------------- UNI_056

head(7, "UNI_056", "DEFINITIONAL PRECEDENCE is a fourth state, and names an operation")
print()
print("  %-46s %s" % ("state", "named where"))
print("  " + "-" * 68)
for st, where in (
    ("an oversight", "README: 'gap'"),
    ("built into the apparatus before the first reading", "README: 'exclusion'"),
    ("apparatus exists, works, points elsewhere", "Case 013 Q4, Case 014 Q1 (UNI_042)"),
    ("observation made, recorded, re-explained by the label", "Case 015 (this)"),
):
    print("  %-46s %s" % (st, where))
block("""
`UNI_042` recorded that the register's founding binary had three states
delivered against it. This is a fourth, and it is different in kind from
the third.

The third state is an instrument pointed elsewhere -- nobody looked. This
one is: somebody looked, the result was recorded, published, and in the
same field, and the category converted it into a methods problem. The
entry's sentence for it is the whole mechanism:

    Once an organism is inside the category, an observation of it in
    oxygen does not read as evidence against the category -- it reads as
    contamination, a handling error, or a bad sample.

That is the strongest candidate for an actual new mechanism to come
through this drop family, and the reason is structural: the other
candidates name an ABSENCE -- capacity removed, derivation discarded, a
quantity with no register. This one names an **operation** that runs on
data that did arrive. It has a subject, a verb and an object, and the
object is evidence that exists.

It also has the best-instanced anchor of the four: a published title
(`UNI_053`) doing the operation in five words.
""")

# ---------------------------------------------------------------- UNI_057

head(8, "UNI_057", "the cross-links, and the confidence")
print()
links = [
    ("presented-binary", os.path.isdir(os.path.join(ROOT, "presented-binary"))),
    ("Mechanism 11", os.path.exists(os.path.join(
        ROOT, "derivation-discarded", "MECHANISM_11.md"))),
    ("Case 013", os.path.exists(os.path.join(HERE, "cases", "013compensationloadunattributed.md"))),
    ("Case 014", os.path.exists(os.path.join(HERE, "cases", "014offloadingevolutionaryframing.md"))),
]
for name, ok in links:
    print("    %-20s %s" % (name, "resolves" if ok else "ABSENT"))
block("""
Four of four. Second drop in the sequence with no dangling reference, after
Case 013 (`UNI_041`).

The presented-binary cross-link is accurate to what that folder is: an
option space constrained before the question is answered, with the
constrained result read as a property of the world. `UNI_051` sharpens
what it instances here -- the option space was not in fact constrained to
two, so the microbiology case is presented-binary's shape with a twist the
decision-framing version does not have. The alternatives were present and
documented, and were not reached for.

Confidence is split across the cluster again -- "Q2 is high as an audit.
Q1's magnitude unknown until the denominator is pulled" -- which is Case
012's state (`UNI_028`), now on its second appearance. Five states of the
one string field are in the wild and `entry()` stores a string
(`UNI_021`).
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_050..UNI_057")
print(BAR)
