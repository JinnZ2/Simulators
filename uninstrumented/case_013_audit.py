#!/usr/bin/env python3
"""case_013_audit.py -- checks on the Case 013 drop.

Added, not delivered. `cases/013compensationloadunattributed.md` is the entry as received and is
not modified. Findings recorded in AUDIT_NOTES.md as UNI_034..UNI_041.

    python3 case_013_audit.py

Case 013 is the fourth consecutive delivered case the register's schema
cannot hold, and the first that does not know whether it is one entry or
two. Its Q3 makes a technical transfer -- the NIST dimming effect applied
to a sorting key -- which is simulable, so section 5 simulates it instead
of arguing about it.

LITERATURE CHECKS. Sections 3, 4 and part of 5 were run against the open
web on 2026-08-18 and are marked. The simulations in section 5 are stdlib,
seeded and reproducible by running this script.

CC0.
"""

import io
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CASE = io.open(os.path.join(HERE, "cases", "013compensationloadunattributed.md"),
               encoding="utf-8").read()
C010 = io.open(os.path.join(HERE, "cases", "010coupledperturbationbiohybrid.md"),
               encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def ols(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    return (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            / sum((x - mx) ** 2 for x in xs))


print("uninstrumented -- audit of the Case 013 drop")
print("delivered: cases/013compensationloadunattributed.md")
print("filename supplied by the author in a later delivery; the drop")
print("instructs that the one-or-two question must not be RESOLVED to get")
print("a cleaner filename, and the name used is its own working handle")

# ---------------------------------------------------------------- UNI_034

head(1, "UNI_034", "a fourth refusal, and the first about the entry's own identity")
print()
print("  %-8s %-38s %s" % ("case", "declines", "schema field"))
print("  " + "-" * 74)
for c, d, f in (
    ("010", "to name its mechanism", "excluded_by, closed vocabulary"),
    ("011", "to be one quantity", "quantity, scalar"),
    ("012", "to carry one confidence", "confidence, one string"),
    ("013", "to be one entry, or two", "the entry itself"),
):
    print("  %-8s %-38s %s" % (c, d, f))
block("""
The first three strain a field. This one strains the record.

    Q1-Q3 (unattributed compensation load) and Q4 (existing unread
    solution) are the same situation from either end. They take different
    measurements and may want different names. Not resolved here.
    Recorded as open because forcing the split now would fix a boundary
    before there is a reason to put it anywhere.

`entry()` returns one dict. There is no representation for "this may be
two entries and the question of which is open", and the `UNI_020` repair
does not reach it either: sub-entries let a cluster hold several questions
under one parent, which presumes the parent is one thing.

The drop also anticipates the pressure the filename itself applies, and
says so in its second paragraph -- the one-or-two question "should not be
resolved to get a cleaner filename".

It first landed here as `case-013.md` -- the register's own numbering,
which takes no position. The author then re-delivered all five cases as
files, with descriptive filenames, and this one arrives as
`013compensationloadunattributed.md`. That is the entry's own declared
working handle, which the entry itself labels as naming "the first half
only", so the name is provisional by the entry's own statement rather
than a resolution of the split. The instruction was against resolving the
QUESTION for filename convenience, not against using the provisional
handle, and the author supplied the name.

Worth stating because the difference is easy to lose: the filename now
names Q1-Q3 and not Q4, and if the split happens Q4 leaves without a name
of its own.
""")

# ---------------------------------------------------------------- UNI_035

head(2, "UNI_035", "per-item attribution inside an entry, with no field for it")
m = re.search(r"\[stated by ([^\]]+)\]", CASE)
print()
print("  found in Q4: [stated by %s]" % m.group(1))
print("  entry() provenance fields: none")
print("  entries in the register carrying an attribution: 0 of 8")
block("""
First provenance tag inside a register entry, and it is attached to one
sub-question rather than to the entry.

`../held-open-uncertainty/OPEN_QUESTIONS.md` does this per entry --
`HO_001` recorded that three of nine entries name whose position they are,
and that the one marked Claude's carries its own retraction. This is the
same discipline one level finer, and it lands on the half that the SPLIT
IS OPEN section says may become a separate case. If the split happens, Q4
leaves with its attribution attached, which is the reason to record it at
this granularity.

`entry()` has `quantity`, `excluded_by`, `also`, `visible_as`,
`would_measure`, `confidence`, `field`, `note` and `worked_in`. None of
them carries who said it.
""")

# ---------------------------------------------------------------- UNI_036

head(3, "UNI_036", "the anchor is fresher and more concrete than stated  [web, 2026-08-18]")
print()
print("  located:")
for line in (
    "5-digit SATCAT exhausted 2026-07-11 with the addition of Saramago",
    "official USSF SATCAT now at 100365; new objects get 6-digit 100000+",
    "Alpha-5: alphanumeric first character, described as a STOPGAP,",
    "  capacity to 339,999, letters I and O omitted to avoid confusion",
    "  with the digits 1 and 0",
    "9-digit catalogue numbers in GP/OMM formats, introduced 2020",
    "legacy fixed-width TLE/3LE still in use alongside both",
):
    print("    %s" % line)
block("""
Every structural element the entry describes is present and dated. The
overflow is six weeks old at the time of this audit, which makes Q1's
"per year since the overflow" denominator start essentially now rather
than decades ago -- a better measurement position than the entry claims,
because the compensation layer can be watched from its first year instead
of reconstructed.

Three coexisting representations -- legacy fixed-width TLE, Alpha-5, and
9-digit GP/OMM -- is the "parallel schemes, reconciliation routines
between them" the entry names, running now and documented.

One detail is worth more than the entry gets from it. Alpha-5 omits the
letters I and O to avoid confusion with 1 and 0: the compensation layer
gives up capacity to prevent a legibility failure it introduced. And it
is called a stopgap by its own publisher, with a stated ceiling of
339,999 -- so the compensation layer is itself a fixed-width scheme with
a design-time population assumption, which is Q2's asymmetry recurring
one level up rather than being resolved.
""")

# ---------------------------------------------------------------- UNI_037

head(4, "UNI_037", "'objects recategorised' is not what was located, and Q3's falsifier partly fires")
block("""
The entry's overflow paragraph says high number blocks are opened "and
objects recategorised", and treats that reassignment as the event that
moves the key.

What was located is narrower. New objects receive numbers at 100000+;
Alpha-5 changes the ENCODING of numbers at or above 100000 so they fit a
five-character field. Neither operation renumbers an existing object. If
existing catalog numbers do not move, the analysed key does not move for
the existing population -- which is Q3's own falsifier condition, met from
a direction the entry does not consider.

Reassignments do occur, and for a different reason: corrections "when
tracking data reveals merged or split objects, often from refined sensor
observations resolving initial ambiguities". That is a physical-resolution
event, not an overflow event.

**Two distinct sources of key movement, and the entry attributes to
overflow what is documented for object resolution.** Both are real; they
have different rates, different causes, and different populations
affected, and Q1's WOULD MEASURE would need to separate them because only
one of them is caused by the design-time omission the case is about.

The other half of Q3's falsifier -- "if reassignment is in practice
handled by stable internal identifiers" -- also partly fires. The COSPAR
International Designator encodes launch year, that year's launch number,
and a piece letter, and is published alongside the NORAD number. It does
not overflow on a fixed field width the way a sequential counter does, so
a population analysed by COSPAR ID is stable against the overflow source.
It is NOT stable against the resolution source: splitting one object into
two adds a piece letter.

So the falsifier fires against one source of movement and not the other,
and a stable-against-overflow key already exists in the same records.
""")

# ---------------------------------------------------------------- UNI_038

head(5, "UNI_038", "Q3's transfer, simulated  [NIST citation web-checked; sims reproducible]")
block("""
The citation checks out: Adam Pintar (mathematical statistician) and
Samuel Stavis (physical scientist), NIST, August 2026, the "dimming
effect" in nanoparticle sizing, with a correction that reverses it. The
entry's one-line characterisation is accurate.

The transfer is the checkable part, and it is checkable by simulation
rather than by argument. Three regimes, because a catalog number can be
used in more than one way and they are not the same statistics.
""")
rng = random.Random(7)
N = 20000
print()
print("  regime 1 -- classical errors-in-variables, continuous X")
print("  (the NIST case: a measured quantity with random additive error)")
print("    %-10s %-12s %-12s %s" % ("sd(err)", "slope", "predicted", "ratio"))
xt = [rng.gauss(0, 1) for _ in range(N)]
y1 = [2.0 * x + rng.gauss(0, 0.5) for x in xt]
for se in (0.0, 0.5, 1.0, 2.0):
    xo = [x + rng.gauss(0, se) for x in xt]
    b = ols(xo, y1)
    print("    %-10.2f %-12.4f %-12.4f %.3f"
          % (se, b, 2.0 / (1.0 + se ** 2), b / 2.0))

print()
print("  regime 2 -- non-differential misclassification of a grouping key")
print("  (the join case: records attached to the wrong identifier)")
print("    %-10s %-12s %-12s %s" % ("p_swap", "obs diff", "predicted", "ratio"))
for p in (0.0, 0.1, 0.25, 0.4):
    a, b_ = [], []
    for _ in range(N):
        g = rng.random() < 0.5
        val = (1.0 if g else 0.0) + rng.gauss(0, 1.0)
        gobs = (not g) if rng.random() < p else g
        (a if gobs else b_).append(val)
    d = sum(a) / len(a) - sum(b_) / len(b_)
    print("    %-10.2f %-12.4f %-12.4f %.3f" % (p, d, 1 - 2 * p, d))

print()
print("  regime 3 -- order-preserving block reassignment, key as a covariate")
print("  (the overflow case: a subset moved into a distant high block)")
idx = list(range(N))
y3 = [1e-4 * i + rng.gauss(0, 0.5) for i in idx]
print("    %-34s %-12s %s" % ("remap", "slope", "ratio"))
print("    %-34s %-12.3e %.3f" % ("none", ols(idx, y3), ols(idx, y3) / 1e-4))
for label, cut, shift in (("top 20% moved to +100000", 0.8, 100000),
                          ("top 20% moved to +1000000", 0.8, 1000000)):
    c = int(N * cut)
    xo = [i + shift if i >= c else i for i in idx]
    b = ols(xo, y3)
    print("    %-34s %-12.3e %.3f" % (label, b, b / 1e-4))
k = int(N * 0.2)
pick = set(rng.sample(idx, k))
xo, c = [], 0
for i in idx:
    if i in pick:
        xo.append(100000 + (c % 200))
        c += 1
    else:
        xo.append(i)
b = ols(xo, y3)
print("    %-34s %-12.3e %.3f" % ("20% gathered into a 200-wide block",
                                  b, b / 1e-4))
block("""
**All three flatten toward zero.** Q3's direction claim survives in every
regime tested, and I expected it not to -- an order-preserving remap looked
like it could bias either way, and regime 3 was built to show that. It does
not: moving a subset into a distant block inflates var(X) far more than it
adds covariance, so the slope collapses. Reported because the
pre-registered expectation was wrong and the simulation is what settled it.

What does NOT transfer is the mechanism.

  regime 1  classical errors-in-variables. Attenuation is exactly the
            reliability ratio var(true)/(var(true)+var(err)); measured
            ratios track it to three decimals. This is the NIST case and
            it needs a continuous X with random additive error.
  regime 2  non-differential misclassification. Attenuation is exactly
            (1-2p). Different derivation, same direction. This is the
            right analogue for a reassigned identifier used as a JOIN
            key, which is how a catalog number is mostly used.
  regime 3  variance inflation from a block remap. Attenuation is severe
            -- down to 1% of the true slope, against 50% for a classical
            error of sd equal to the spread of X.

So "structurally the same as the NIST dimming effect" is true of the
direction and of nothing else. The three mechanisms are distinct, and the
catalog cases are worse than the nanoparticle case rather than analogous
to it, which strengthens Q3 rather than weakening it.

One caution the entry does not state: regime 3 assumes the key is used as
a numeric covariate, and regressing an outcome on a catalog number is
rarely a meaningful thing to do. The strongest form of Q3 is regime 2 --
mis-joins across reconciled schemes -- because that is the operation the
compensation layer performs constantly.
""")

# ---------------------------------------------------------------- UNI_039

head(6, "UNI_039", "the Case 010 cross-link lands, and it corrects UNI_019")
seg = C010.split("COMPARATOR", 1)[1].split("READOUT", 1)[0]
print()
print("  Case 010's comparator, as delivered:")
print("    %s" % " ".join(seg.split())[:64])
print("    %s" % " ".join(seg.split())[64:128])
flat = " ".join(("If the margin is **flat**"
                 + C010.split("If the margin is **flat**", 1)[1]
                 ).split(".", 1)[0].split())
print()
print("  Case 010's flat branch reads:")
for i in range(0, len(flat), 62):
    print("    %s" % flat[i:i + 62])
block("""
Case 013's claim is that Case 010 "reads it as a geometric constraint on
silver placement; that reading may be incomplete", because the sequence is
the address.

**It lands, and it corrects a finding recorded in this file.** `UNI_019`
called Case 010's comparator "the load-bearing element" and a known-null
in `../null-harness/` terms, on the grounds that matched spacing and
matched Ag loading isolate *organic* from *periodic scaffold with silver
in it*. That holds on the organic-versus-inorganic axis and is too
generous on a second axis the comparator does not control.

A periodic scaffold has one spacing repeated; positions are
interchangeable. A sequence-addressed scaffold has positions
distinguishable from one another -- that is what "the structure is the
address" means. If the DNA layer's contribution depends on
distinguishability rather than on pitch, then matched pitch is not a
matched control: the comparator differs from the hybrid in the dimension
under test.

The consequence is specific and it is a false negative. Case 010's flat
branch is read as "the organic layer is functioning as a geometric ruler
and any periodic scaffold of matched pitch substitutes". Under the
addressing reading, a flat margin would be reached whenever the coupling
depends on addressability, because the comparator cannot express it --
so the branch that is supposed to mean "geometry was enough" would also
fire when addressing is everything.

Repair is one arm: a comparator with matched pitch AND aperiodic,
position-distinguishable structure -- an aperiodic sequence with the same
spacing statistics and the same Ag loading. That separates pitch from
addressing, which the delivered two-arm design cannot.

The entry's instruction "do not collapse them" is right for the reason it
gives: evidence in either case propagates. This finding is an instance --
a claim in Case 013 changed the reading of a claim about Case 010.
""")

# ---------------------------------------------------------------- UNI_040

head(7, "UNI_040", "Q4's comparison class survives, in a narrower form")
block("""
Q4's falsifier: "fails if object-carried identification schemes turn out
to have their own bounded capacity under a different name."

It does not fail, and it does not survive as stated either.

A DNA sequence of length L over four letters addresses 4^L states, which
is bounded. So "no block to overflow" is not literally true -- the
capacity is finite. What is true, and is the statable version, is that
**capacity scales with the object rather than being fixed by a register**.
Adding one base multiplies capacity by four, at the cost of one base; a
fixed-width counter cannot be widened without rewriting every consumer of
the field, which is precisely the compensation load Q1 is about.

The satellite case supplies the middle term and it was in the record the
whole time. The COSPAR designator is compositional -- launch year, launch
number within the year, piece letter -- so the year field is open-ended
and capacity grows with time rather than being drawn down from a fixed
pool. It sits between the sequential counter and the sequence-as-address
family, in the same records as the counter, and nothing in the entry
mentions it.

That is the cheapest available next step for Q4: the comparison class does
not have to be reached for across substrates, because a partial instance
of it is already published alongside the anchor.
""")

# ---------------------------------------------------------------- UNI_041

head(8, "UNI_041", "the cross-links, and the confidence")
print()
links = [
    ("Case 010", os.path.exists(os.path.join(HERE, "cases", "010coupledperturbationbiohybrid.md"))),
    ("Case 011", os.path.exists(os.path.join(HERE, "cases", "011rebuildabandonmentcycles.md"))),
    ("Case 012", os.path.exists(os.path.join(HERE, "cases", "012fuelincidencesubstrategoods.md"))),
    ("Mechanism 11", os.path.exists(os.path.join(
        ROOT, "derivation-discarded", "MECHANISM_11.md"))),
]
for name, ok in links:
    print("    %-16s %s" % (name, "resolves" if ok else "ABSENT"))
print("    %-16s %s" % ("rate-mismatch-polytope", "not cited this time"))
block("""
Four of four resolve -- the first drop in this sequence with no dangling
reference. `rate-mismatch-polytope`, named by Case 011 and again by
Mechanism 11 (`UNI_026`, `DD_008`), is not cited here.

On confidence: "Not stated as a scalar... Q3 alone could take a gradient
once Q1's data exists." That is Case 011's deliberate absence plus
something new -- a stated DEPENDENCY between sub-questions, where one
question's confidence is gated on another question's data.

Four cases, four states of one string field: high (the eight originals),
a gradient (010), a reasoned absence (011), a split (012), and now an
absence with a stated unlock condition (013). `entry()` stores a string
and cannot tell any of them apart from an omission (`UNI_021`).
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_034..UNI_041")
print(BAR)
