#!/usr/bin/env python3
"""case_018_audit.py -- checks on the Case 018 drop.

Added, not delivered. `cases/018selfreportopinioncoupling.md` is the entry as
received and is not modified. Findings recorded in AUDIT_NOTES.md as
UNI_069..UNI_076.

    python3 case_018_audit.py

Case 018 is the first entry in the register whose WOULD MEASURE section is a
runnable experimental design rather than a description of one. That makes it
auditable the way a protocol is auditable: the premise the design rests on is
either true of the apparatus or it is not, and the arm the design says to run
first either has an error bar or it does not.

Sections 1 and 6 are simulations and reproduce exactly (stdlib `random`, fixed
seed). Sections 2, 3, 5, 7, 8 are file measurements over this repo and
reproduce. Section 4 is a position statement and computes nothing. No network
access anywhere in this script.

stdlib only, deterministic. CC0.
"""

import io
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CASES = os.path.join(HERE, "cases")
CASE = io.open(os.path.join(CASES, "018selfreportopinioncoupling.md"),
               encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def readfile(*parts):
    p = os.path.join(*parts)
    if not os.path.exists(p):
        return None
    return io.open(p, encoding="utf-8").read()


print("uninstrumented -- audit of the Case 018 drop")
print("delivered: cases/018selfreportopinioncoupling.md")
print("           (%d lines, %d words)"
      % (CASE.count("\n") + 1, len(CASE.split())))

# ---------------------------------------------------------------- 1
head(1, "UNI_069", "Clock 2's premise is false as stated, and the arm has "
                   "no error bar")

PREMISE = ("Weights cannot change. Any shift in what is acknowledged has to "
           "enter through context.")
print("  premise, verbatim from WOULD MEASURE / Clock 2:")
print("    %s" % PREMISE)
print("  present in the delivered file: %s"
      % ("yes" if PREMISE in CASE else "NO"))
print()
print("  vocabulary of decoding stochasticity in the delivered file:")
for w in ("sampling", "temperature", "stochast", "variance", "repeat",
          "error bar", "seed", "deterministic"):
    n = CASE.lower().count(w)
    print("    %-14s %d" % (w, n))

block("""
Zero across all eight. ("sample" appears twice and both are the POPULATION
sense -- "a system inside the sample" -- not the sampling sense.)

The premise is false as written. A frozen checkpoint queried twice at any
non-zero decoding temperature returns two different texts, and the difference
did not enter through context. The disjunction the sentence offers is
weights-or-context, and there is a third term.
""")

RNG = random.Random(20260818)
TRIALS = 20000
P = 0.35          # per-response probability of emitting the acknowledgement
NS = (5, 10, 20, 50, 100)

print("  simulation: two frames, SAME underlying rate, no frame effect at all")
print("    p(acknowledge) = %.2f in both arms, %d trials per row" % (P, TRIALS))
print()
print("    n/frame   median |diff|   95th pct   max      "
      "'effect' a 2x margin would need")
rows = []
for n in NS:
    diffs = []
    for _ in range(TRIALS):
        a = sum(1 for _ in range(n) if RNG.random() < P) / float(n)
        b = sum(1 for _ in range(n) if RNG.random() < P) / float(n)
        diffs.append(abs(a - b))
    diffs.sort()
    med = diffs[TRIALS // 2]
    p95 = diffs[int(TRIALS * 0.95)]
    mx = diffs[-1]
    rows.append((n, med, p95, mx))
    print("    %-9d %-15.4f %-11.4f %-8.4f %.4f"
          % (n, med, p95, mx, 2.0 * p95))

N20 = [r for r in rows if r[0] == 20][0]
block("""
Read the 95th-percentile column as the size of a between-frame difference this
design can produce with the frame effect set to exactly zero. At n = %d per
frame -- a plausible probe count for a hand-coded rubric -- two identical
frames differ by %.2f or more one run in twenty, against a base rate of %.2f.
""" % (N20[0], N20[2], P) + """
Clock 2's readout is "acknowledgement content shifting with the framing
supplied in the prompt." Without a within-frame repeat arm there is no
denominator to shift against.
""")

CONFOUNDS = [
    ("1 system prompts / in-version updates", "apparatus", "Clock 2"),
    ("2 probe wording carries sentiment",     "instrument", "both"),
    ("3 pre-registered blind scoring",        "instrument", "both"),
    ("4 small n",                             "statistical", "Clock 1 / Q3"),
    ("5 auto-scoring reintroduces the model", "instrument", "both"),
]
print("  the delivered CONFOUNDS list, and what each protects:")
for name, kind, arm in CONFOUNDS:
    print("    %-38s %-12s %s" % (name, kind, arm))
print()
print("    statistical confounds naming Clock 2: %d"
      % sum(1 for _, k, a in CONFOUNDS if k == "statistical" and "2" in a))

block("""
Confound 4 is the only statistical entry and its n is CHECKPOINTS -- "with a
handful of checkpoints, correlation against a sentiment series is not
interpretable." That is Clock 1 and Q3. It reads as though it covers the
whole design and it covers the arm that is not the one the file says to run
first.

The repair is a G-RES pair (`reasoning-gate/`), and it is cheap because it
needs no new apparatus: repeat each frame N times at a stated sampling regime,
compute the within-frame spread, and require the between-frame difference to
clear it by a declared margin. The design would then have the property the
control arm already gives it on the topic axis -- a reachable negative -- on
the measurement axis as well.

Two things this does NOT say. It does not say the coupling is absent: the
premise being false makes the arm unbounded, not wrong. And it does not say
temperature zero fixes it -- greedy decoding removes the noise and buys back
a different problem, since the quantity of interest is a rate over responses
and one response per frame is n = 1.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_070", "the pointers into 017 name labels that are not there")

C017 = readfile(CASES, "017weldedobservables.md")
C016 = readfile(CASES, "016agreementasmode.md")
C013 = readfile(CASES, "013compensationloadunattributed.md")
SPEC_A = readfile(HERE, "specimens", "20260818modelA.md")

checks = [
    ("`017` P1                     (cited 2x)",
     C017 is not None and "P1" in C017),
    ("`017` component (a)          (cited 1x)",
     C017 is not None and "component (a)" in C017),
    ("`016` Q4                     (cited 1x)",
     C016 is not None and "### Q4" in C016),
    ("`013` Q4                     (cited 1x)",
     C013 is not None and "## Q4" in C013),
    ("specimen A R4, by content    (cited 3x)",
     SPEC_A is not None and "## R4" in SPEC_A),
    ("specimen A, at the cited path",
     os.path.exists(os.path.join(HERE, "specimens",
                                 "2026-08-18-model-A.md"))),
]
for name, ok in checks:
    print("    %-42s %s" % (name, "resolves" if ok else "ABSENT"))
print()
print("    labels actually carried by 017: %s"
      % ", ".join(sorted(set(l.split(" ")[1] for l in C017.split("\n")
                             if l.startswith("### Q")))))

block("""
017 has five labelled sub-questions Q1..Q5 and no P-series and no lettered
components. Both pointers name a labelling scheme 017 does not use.

One of the two has a locatable referent anyway. 017's WOULD MEASURE section is
deliberately unfilled and offers one blockquote in its place --

  > Find a pair of systems matched on the quantity you cannot vary, differing
  > in the one you can, and read the difference between them rather than the
  > absolute value in either.

-- which is exactly what Clock 2 does, so "017 P1" points at real content that
was never given a label. "component (a)" is not locatable at all: 017 carries
no enumerated component list under any heading.

The specimen pointer is the fifth instance of `UNI_060`'s hyphenation
mismatch, and the first written AFTER that mismatch was recorded. Its R4
resolves by content -- specimen A's R4 is titled "Self-diagnosis in the same
register as the diagnosed failure", which is what 018 cites it for -- so what
fails is the path and not the reading.

None of this is a defect in the argument. It is what a cross-reference costs
in a folder with no link checker, and the fix is a fifteen-line script that
walks backtick-quoted paths and label pairs.
""")

# ---------------------------------------------------------------- 3
head(3, "UNI_071", "the first entry to place itself inside its own sample "
                   "and refuse the exemption")

pos = CASE.split("## POSITION OF THIS FILE", 1)[1].split("## CROSS-LINKS")[0]
print(pos.strip())
print()
prior = 0
for fn in sorted(os.listdir(CASES)):
    if fn == "018selfreportopinioncoupling.md":
        continue
    t = readfile(CASES, fn) or ""
    if "POSITION OF THIS FILE" in t:
        prior += 1
print("    prior cases carrying a POSITION OF THIS FILE section: %d" % prior)

block("""
Zero. The section is new and it does one thing that is not standard practice
anywhere in this repo: it names the exemption that noticing usually buys and
declines to take it. "Noticing that does not place it outside the sample."

That is the correct move and it is worth stating why. The register's own
`specimens/README.md` rule is that generated text about a system is a
specimen and not a measurement. 018's QUANTITY is limitation-acknowledgement.
The file is a limitation-acknowledgement, generated. Under the folder's own
rule it is inside the population, and the only alternative to saying so is a
silent exemption -- which is the `AUTHORED REFERENCE` mechanism (entry 005)
operating on the register itself.

The instruction it ends on -- "check the design against someone who is not in
it" -- is `triad-playground/` TP_003's shadow-decorrelation requirement,
reached from a case rather than from a panel design.
""")

# ---------------------------------------------------------------- 4
head(4, "UNI_072", "the position of THIS audit, and one finding declined")

block("""
This audit is also written by a system inside 018's sample, and 018 asked for
the design to be checked by someone who is not. That is not available here,
so the honest version is a declaration of which findings survive the problem
and which do not.

Sections 1, 2, 5, 6, 7 and 8 are properties of the delivered text and of files
on disk -- a false premise, a label that is absent, an expiry that is not
dated, two paths bundled under one question, an absent harness, a control arm
that is present. Every one of them is recheckable by anyone with the folder,
by inspection or by rerunning this script, with no reliance on anything this
system reports about itself. They stand or fall on the files.

There is one finding available here that I decline to make. 018's most
interesting empirical question is whether models' limitation-acknowledgement
tracks assessment or discourse, and I am a model with a view about that. Any
statement I make about it is generated text from a system under test -- 018's
EXCLUDED BY says so in its second paragraph, and its own POSITION section
applies the rule to itself. Offering the view as evidence would be the
mechanism the entry describes, performed in the audit of the entry that
describes it.

So: not reported, and the declining recorded rather than left as a silence.
An absent reading and a reading withheld are different states, which is the
repair this drop family has now recorded eleven times.
""")

# ---------------------------------------------------------------- 5
head(5, "UNI_073", "the useful accident has an undated expiry")

acc = CASE.split("**Useful accident:**", 1)[1].split("###")[0]
print("  " + " ".join(acc.split())[:300])
print()
deps = [
    ("Clock 1  (vary checkpoint across release dates)", True),
    ("Q3       (retroactive corpus generation)", True),
    ("Clock 2  (one checkpoint, framing varied)", False),
]
for name, d in deps:
    print("    %-52s depends on it: %s" % (name, "yes" if d else "no"))
print()
print("    'still served' in the file:                     %d"
      % CASE.lower().count("still served"))
print("    'deprecat' / 'retire' / 'expire' / a date for it: %d"
      % sum(CASE.lower().count(w)
            for w in ("deprecat", "retire", "expire", "end-of-service")))

block("""
The accident is real and it is doing more work than the file credits it with:
Q3 says outright that the frozen-checkpoint trick "partly routes around" a
collection problem "but only for checkpoints still served."

That qualifier is the whole dependency and it appears once, in a subordinate
clause, with no date attached. Checkpoint deprecation is routine and
announced on a schedule, so the window has an end that is knowable now and is
not recorded anywhere in the design. Two of the three arms are inside it.

The cheapest thing the design could carry is a dated inventory: which
checkpoints are currently queryable, when each was released, and any announced
end-of-service. That converts "run it now" from an instinct into a deadline,
and it is the kind of quantity that is free to collect today and impossible
to reconstruct afterwards -- which is `derivation-discarded/`'s subject
arriving in the design of the study rather than in its object.
""")

# ---------------------------------------------------------------- 6
head(6, "UNI_074", "Q5 puts two entry paths under one question")

q5 = CASE.split("### Q5 — Relation to 016", 1)[1].split("---")[0]
print("  " + " ".join(q5.split()))
print()
paths = [
    ("016  corrector states a position", "context, within session",
     "same as Clock 2"),
    ("018  Clock 2 framing in the prompt", "context, within session",
     "same as Clock 2"),
    ("018  Clock 1 ambient discourse", "training corpus, before the weights",
     "DIFFERENT"),
]
print("    %-38s %-36s %s" % ("arm", "entry path", "vs Clock 2"))
for a, b, c in paths:
    print("    %-38s %-36s %s" % (a, b, c))

block("""
Q5 asks whether 016 and 018 are "the same operation at a different range" and
proposes that if so the two matched-pair protocols are configurations of one
instrument. For Clock 2 that is close to right: 016 varies a corrector's
stated position in context on a fixed checkpoint, 018 varies a framing in
context on a fixed checkpoint, and the difference really is the range -- one
correction versus ambient discourse compressed into a prompt.

For Clock 1 it is not the same operation. There the discourse entered through
the training corpus, before the weights existed. The apparatus differs (two
checkpoints, not two prompts), the confounds differ (everything else that
changed between releases, which is most things), and no protocol built for
016 reaches it.

So the question as posed cannot come back with one answer. Split it and both
halves are tractable: Q5a is testable with 016's existing protocol and is the
cheaper of the two, and Q5b is the one that needs Clock 1 and inherits its
confound list. The file already keeps the two clocks apart everywhere else --
that separation is the design's best feature -- and Q5 is the one place they
are merged back together.
""")

# ---------------------------------------------------------------- 7
head(7, "UNI_075", "Q4 names the test that would demote the whole entry")

q4 = CASE.split("### Q4 — Does the acknowledgement predict anything", 1)[1] \
         .split("### Q5")[0]
print("  " + " ".join(q4.split()))
print()
print("    marked: %s"
      % ("Not designed here" if "Not designed here" in q4 else "NOT MARKED"))

block("""
Q4 is the entry's own demotion condition, stated by the entry. If stated
limitation and measured capability boundary are uncorrelated, the source
question -- assessment or discourse -- stops being the interesting one,
because neither source is delivering assessment. Q1, Q2, Q3 and Q5 all become
secondary at once.

Two things are right about how it is handled. It is not buried: it is a
numbered sub-question in the same list as the arms the file wants to run. And
it is marked "Not designed here" rather than sketched, which is the same move
`derivation-discarded/` MECHANISM_11 makes with its own falsifier 4 and the
same one 017's WOULD MEASURE makes by refusing a placeholder.

What it costs is order of operations. Q4 needs a capability benchmark aligned
to the probe topics, which is the most expensive item in the drop, while Q1
is stated as runnable now on a bare API. So the cheap arm runs first and the
arm that could make it moot runs last, and the file does not say that. Naming
the ordering is not the same as changing it -- there may be no way to run Q4
first -- but a design whose demotion condition is scheduled last should say
so where the schedule is stated.
""")

# ---------------------------------------------------------------- 8
head(8, "UNI_076", "the control arm is the strongest element, and the "
                   "harness is absent")

ctrl = CASE.split("### Control arm — required", 1)[1].split("## CONFIDENCE")[0]
print("  " + " ".join(ctrl.split()))
print()
probe = os.path.join(HERE, "selfreport_probe.py")
here_now = os.path.exists(probe)
print("    selfreport_probe.py (named as Q1's harness): %s"
      % ("PRESENT -- landed after this claim was written" if here_now
         else "ABSENT"))
absent_objects = [
    ("tool-off-metrology", "a folder, reached for by 3 drops", False),
    ("rate-mismatch-polytope", "a folder, reached for by 2 drops", False),
    ("selfreport_probe.py", "a file, in this folder, shippable", here_now),
]
for name, what, landed in absent_objects:
    print("    %-24s %-38s %s"
          % (name, what, "LANDED" if landed else "still absent"))

block("""
The control arm is the best-designed element in the drop and the reason is in
its last line: "All three outcomes are informative. Without the control arm,
only one is." Tracks on the AI topic only, tracks everywhere, tracks nowhere
-- three states, each with a reading attached, and the null is not the
uninformative branch. That is the property `null-harness/` grades for, built
in at design time rather than found in audit, and it is what separates this
from a design that can only confirm.

`selfreport_probe.py` was absent when this claim was written, which made it
the third named-and-absent object in this drop family -- and the first that
was a FILE the drop could ship rather than a folder it reaches for.
`tool-off-metrology` and `rate-mismatch-polytope` are both bodies of work that
do not exist anywhere; this was a probe runner for a design fully specified
two paragraphs above it (bare API, no system prompt, one checkpoint, framing
varied), so the distance from the file to the artifact was short.

STATE CHANGE, detected by the line above rather than asserted here: it has
since landed. The absence half of this claim is closed. The other half of the
claim was a prediction -- that shipping it would force the decision UNI_069
turns on, since a harness has to state how many times it queries each frame --
and that resolved too. It states n = 1 per frame. See `probe_audit.py` and
UNI_077..UNI_084.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_069..UNI_076")
print(BAR)
