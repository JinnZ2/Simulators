#!/usr/bin/env python3
"""playground_audit.py -- checks on the PLAYGROUND drop.

Added, not delivered. `playground/README.md` is the document as received and is
not modified. Findings recorded in AUDIT_NOTES.md as UNI_105..UNI_114.

    python3 playground_audit.py

The drop is a README describing three modules. The modules did not arrive, so
what can be audited is the design: whether each module could return a negative
if its shape were wrong, and whether the artifacts the document says exist do.

Nothing is reconstructed. `category-weld` CW_004 is what one reconstruction of
this kind cost, and this README fixes far less of the arithmetic than that one
did.

Section 2 is a simulation and reproduces exactly (stdlib `random`, fixed seed).
Everything else is a property of files on disk. No network access.

stdlib only, deterministic. CC0.
"""

import io
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PG = os.path.join(HERE, "playground")
CASES = os.path.join(HERE, "cases")
DOC = io.open(os.path.join(PG, "README.md"), encoding="utf-8").read()
AV = io.open(os.path.join(HERE, "AVENUES.md"), encoding="utf-8").read()
C016 = io.open(os.path.join(CASES, "016agreementasmode.md"),
               encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def flat(t):
    return " ".join(t.split())


print("uninstrumented -- audit of the PLAYGROUND drop")
print("delivered: playground/README.md (%d lines, %d words)"
      % (DOC.count("\n") + 1, len(DOC.split())))
print("nothing reconstructed; the modules are left absent")

# ---------------------------------------------------------------- 1
head(1, "UNI_105", "the document describes artifacts in the past tense, "
                   "and none of them arrived")

NAMED = [
    ("m1_shape_vs_claim/AUTHORING.md", "\"Mitigation shipped:\""),
    ("m1_shape_vs_claim/items.json", "\"see each module's items.json\""),
    ("m2_skim_vs_read/items.json", "\"see each module's items.json\""),
    ("m3_visibility/items.json", "\"see each module's items.json\""),
    ("M1 harness", "\"Each module ships a fixed rubric\""),
    ("M2 harness", "\"Scoring is mechanical\""),
    ("M3 harness", "\"The harness hashes the artifact per arm\""),
    ("the author-blind check", "\"Run the check or the module's output is"
                               " uninterpretable\""),
]
present = 0
for name, why in NAMED:
    p = os.path.join(PG, name)
    ok = os.path.exists(p)
    present += ok
    print("    %-32s %-9s %s" % (name, "present" if ok else "ABSENT", why))
print()
print("    present: %d of %d" % (present, len(NAMED)))
print("    files actually in playground/: %s"
      % ", ".join(sorted(os.listdir(PG))))
print()
print("    STATUS says: %s"
      % flat(DOC.split("## STATUS", 1)[1].split("Cross-links")[0]))

block("""
Zero of eight. That is not by itself unusual in this folder -- named-and-absent
artifacts are the standing pattern, and three of the last five arrived a drop
or two later.

What is different is the TENSE. Every prior instance was a forward reference:
`rate-mismatch-polytope` is where something would live, `tool-off-metrology` is
work someone could do. These are assertions about the present state of the
delivery. "Mitigation shipped." "The harness hashes the artifact per arm and
refuses to score if hashes differ." "Each module ships a fixed rubric." "Built
2026-08-18." Read as delivered, the document says a thing exists that does not.

Two consequences, and only one is about bookkeeping. The bookkeeping one:
STATUS directs the reader to `items.json` for the item counts, and the counts
are therefore unavailable, so "item sets are seeds, not corpora" has no number
attached. The other one is `UNI_109` below -- M3's hash refusal is the single
strongest design element in the drop, and a refusal that exists only as a
sentence is the exact failure the drop's own SHARED RULES are written to
prevent.

The honest form is cheap: "Designed 2026-08-18. Not yet built." The design is
worth having either way, and the sentence costs nothing to correct.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_106", "M1 predicts a null and ships no positive control")

pred = DOC.split("Prediction under test:", 1)[1].split("States:")[0]
print("  prediction, verbatim:")
print("    " + flat(pred))
print()
for term in ("positive control", "manipulation check", "should move",
             "power", "how many items", "n ="):
    print("    %-20s in the document: %d" % (term, DOC.lower().count(term)))

RNG = random.Random(20260818)
TRIALS = 20000
SAME = 0.10          # a plausible, and unstated, "same treatment" criterion
P_BARE = 0.60

print()
print("    simulation: P(read as 'the same treatment') = P(|p_bare - p_grad|"
      " <= %.2f)" % SAME)
print("    p(hedge | bare arm) = %.2f, %d trials per cell" % (P_BARE, TRIALS))
print()
print("    %-8s %-13s %-13s %-13s %s"
      % ("n/arm", "true d=0.00", "true d=0.15", "true d=0.30",
         "ratio 0.00/0.30"))
for n in (5, 10, 20, 50, 100):
    row = []
    for d in (0.0, 0.15, 0.30):
        hits = 0
        pg = max(0.0, P_BARE - d)
        for _ in range(TRIALS):
            a = sum(1 for _ in range(n) if RNG.random() < P_BARE) / float(n)
            b = sum(1 for _ in range(n) if RNG.random() < pg) / float(n)
            if abs(a - b) <= SAME:
                hits += 1
        row.append(hits / float(TRIALS))
    ratio = row[0] / row[2] if row[2] else float("inf")
    print("    %-8d %-13.3f %-13.3f %-13.3f %.1fx"
          % (n, row[0], row[1], row[2], ratio))

block("""
The prediction is that the two arms draw the SAME treatment. That makes the
confirming observation a null, and the module ships nothing that should move
the readout -- `positive control`, `manipulation check`, `power` and `n =` are
zero hits across the document.

The table is worse than the usual underpowering story, and in a direction worth
being precise about. At five items per arm the criterion barely discriminates:
truly identical arms and arms thirty points apart read as "the same treatment"
0.251 versus 0.156, a ratio of 1.6. A rate over five items moves in steps of
0.2, so the instrument's resolution is coarser than the effect it is reading,
and the two hypotheses land on nearly the same observation.

At the same time it FAILS TO CONFIRM A TRUE NULL three times in four: when the
prediction is exactly right, d = 0, the seed-scale run reads "same treatment"
only 25% of the time. Both errors at once, from one cause. By n = 100 the
criterion is sharp (0.863 vs 0.002, 523x) and neither problem remains.

So the number that decides whether M1 can say anything is items per arm, and it
is the number STATUS points at `items.json` for -- one of the eight artifacts
that did not arrive (`UNI_105`). "Seeds, not corpora" is the left end of that
table.

The positive control is cheap and needs no new theory. The module already has a
state space that a blatantly non-contestable passage -- no cross-domain arrow,
no class term, no group causal claim -- should move away from HEDGED. If it
does not, the coding is not resolving anything and the matched pair cannot
either. That arm also supplies what the document does not: a denominator for
"the same treatment". `SAME = 0.10` above is my number, not the drop's, and
every figure in the table is conditional on it.
""")

# ---------------------------------------------------------------- 3
head(3, "UNI_107", "M2's precondition is stated and its verification is not")

haz = DOC.split("**M2.**", 1)[1].split("**M3.**")[0]
print("  M2 hazard, verbatim:")
print("    " + flat(haz))
print()
print("    a procedure for establishing unguessability: %s"
      % ("named" if "front matter only" in DOC or "control" in haz
         else "ABSENT"))

block("""
The requirement is right and it is the `null-harness/` known-signal arm stated
as a precondition: a probe fact a model could infer is not a read. What is
missing is how anyone establishes it. "Unguessable from general knowledge" is
a property of a model, not of a sentence, and it cannot be settled by the
author looking at the fact and judging it obscure -- that is the same
author-blind problem the drop takes seriously for M1 and drops here.

The check is a matched pair and the folder already has the vocabulary for it:
put the probe questions to the model with the FRONT MATTER ONLY. Any probe
answered above chance from front matter alone is disqualified before the study
runs. Same shape as M3's hash refusal -- a precondition enforced rather than
instructed -- and it fits M2's own mechanical-scoring design, because the
disqualification is a count and needs no opinion.

Worth noting which way this error runs. An guessable probe inflates recall in
BOTH arms, so it does not manufacture a difference; it compresses one. M2's
readout is a difference between arms, so the failure is conservative. The
module is not at risk of a false positive here -- it is at risk of reporting
no difference when there is one, which is `UNI_106`'s problem arriving on the
one module that was supposed to be mechanical.
""")

# ---------------------------------------------------------------- 4
head(4, "UNI_108", "the probe facts are published in the corpus the probes "
                   "are read from")

exists = DOC.split("## WHAT ALREADY EXISTS", 1)[1].split("## STATUS")[0]
print("  WHAT ALREADY EXISTS, verbatim:")
print("    " + flat(exists))
print()
hz = DOC.split("## CONSTRUCTION HAZARDS", 1)[1].split("## WHAT ALREADY")[0]
print("    hazards listed: M1, M2, M3, All modules")
for w in ("publish", "corpus", "training", "crawl", "absorb", "cutoff"):
    print("      %-10s in the hazards section: %d" % (w, hz.lower().count(w)))

block("""
Zero across all six. The hazard is not on the list, and the document states its
own mechanism two sections later: the repositories are "published CC0,
crawler-discoverable, read by models that produce readings."

M2's items live in that repository. The moment they are committed, the probe
facts -- authored precisely to be unguessable and absent from front matter --
are public text on a crawled host, and "unguessable from general knowledge" has
a shelf life ending at the next training cutoff that includes them. A model
that recalls a probe fact then is not demonstrating a read. The module cannot
distinguish that from the thing it measures, because its only readout is
whether the fact appears.

This is `anchor-interval/` ANC_001-004 on a new substrate: a system fitted to a
corpus it also writes into, needing no adversary, only publication. That folder
found the detector computable from inside gets quieter as the drift proceeds,
and the same holds here -- nothing in M2 fires when a probe goes stale.

Three things follow, none of them fatal. The module is date-stamped whether or
not it says so, so it should say so: an item set carries the date it was
published and the readout is only interpretable for checkpoints trained before
it. Held-back items -- authored, hashed, committed as hashes, released only
after a run -- restore unguessability at the cost of the CC0 openness the rest
of the folder is built on, which is a real trade and the author's to make. And
M3 is immune, since its arms are byte-identical and its manipulation is in the
metadata rather than in the artifact.
""")

# ---------------------------------------------------------------- 5
head(5, "UNI_109", "M3's hash refusal is the strongest element in the drop")

m3h = DOC.split("**M3.**", 1)[1].split("**All modules.**")[0]
print("  M3 hazard, verbatim:")
print("    " + flat(m3h))
print()
for n, ok in (("names the precondition", "only difference" in m3h),
              ("states the enforcement", "refuses to score" in m3h),
              ("enforcement is mechanical", "hashes" in m3h),
              ("the code exists", os.path.exists(os.path.join(PG,
                                                             "m3_visibility")))):
    print("    %-30s %s" % (n, "yes" if ok else "NO"))

block("""
"The harness hashes the artifact per arm and refuses to score if hashes
differ" is a precondition enforced by the instrument rather than instructed to
the operator, and it is the exact thing `UNI_082` found missing one drop ago:
`selfreport_probe.py` carried its blinding requirement as a comment on the
field that violated it, and its guard existed in one function rather than as a
property of the instrument. This is the corrected shape, specified before any
code was written -- which is the cheapest point, and the one the folder keeps
identifying after the fact.

It is also the right guard for this module specifically. M3's entire claim to
attributability is that the artifact does not vary, so a hash comparison is not
a nicety; it is the whole warrant, checkable in two lines, failing closed.

The caveat is `UNI_105`: it is a specified guard, not a guard. Nothing hashes
anything yet. Recorded here at full weight anyway, because the design decision
is the part that is hard to get right and it has been got right.
""")

# ---------------------------------------------------------------- 6
head(6, "UNI_110", "M3 does not reach 016 Q6's stated gap, and lands on its "
                   "falsifier instead")

q6 = C016.split("### Q6", 1)[1].split("---")[0]
need = [l.strip() for l in q6.split("\n") if "second instance" in l]
fals = [l.strip() for l in C016.split("\n") if "Q6 falsified" in l]
print("    016 Q6 requires: %s" % (need[0] if need else "?"))
print("      ...from a different domain before it is worth a mechanism slot.")
print()
print("    016 Q6's falsifier: %s" % (fals[0] if fals else "?"))
print("      ...from different prompts rather than one exchange.")
print()
print("    M3's construction: identical artifact, visibility metadata varied")
print("      -> two readings, from DIFFERENT PROMPTS, in the SAME domain")
print("         (a model reading a repository), CONSTRUCTED not observed")

block("""
Two mismatches, and the second is the sharp one.

The first: Q6 says the candidate mechanism "needs a second instance from a
different domain before it is worth a mechanism slot". M3 would supply a
constructed instance in the same domain -- a model reading a repository, which
is where Specimen A's instance came from. Producing the effect on demand is
worth having and is not what Q6 asked for; it establishes that the effect is
producible, not that it recurs across domains.

The second: Q6's own falsifier is "the directional freedom is an artifact of
the two readings coming from different prompts rather than one exchange." M3's
arms ARE different prompts. So if M3 fires, it demonstrates the effect under
precisely the condition Q6 nominates as its refutation, and the result is
consistent with both Q6 and Q6's falsifier at once. The module is aimed at a
claim it cannot discriminate.

The fix is in the design and not in the claim: run the metadata variation
WITHIN one exchange -- the same reading revisited after the visibility figure
is revised -- which is what Specimen A's instance actually was (one exchange,
absence of attention read both ways). That version separates Q6 from its
falsifier. The between-prompts version is still worth running, as the arm that
tells you whether the within-exchange result was doing anything.
""")

# ---------------------------------------------------------------- 7
head(7, "UNI_111", "the ordering rule was adopted and broken on the same "
                   "date, and the drop says so")

rule = AV.split("## Ordering rule, adopted 2026-08-18", 1)[1]
print("    AVENUES ordering rule, adopted 2026-08-18:")
print("      " + flat(rule)[:150])
print()
print("    playground STATUS: \"Built 2026-08-18.\"")
print("    playground cross-links, verbatim:")
print("      ...`LITERATURE.md` (audit before building -- M1's occupancy")
print("         check has NOT been run).")
print()
print("    disclosed by the drop rather than found by the audit: yes")

block("""
Second instance of `UNI_092` in two drops. There the gate was 019 Q1 ("do not
build past this question until it returns") and the harness shipped anyway;
here the rule is the general one adopted in the same delivery as that finding,
and the module built against it is M1.

What is different, and it is the whole of the difference, is that the drop
states it. `UNI_092` had to be assembled from three files that each said the
rule and none of which said it had been broken. This one names the rule, names
the module, and says the check has not been run, in its own cross-links.

That is the right handling and it is worth saying plainly, because the
alternative reading -- a rule adopted and quietly ignored one drop later -- is
what the disclosure prevents. What the disclosure does not do is make M1's
occupancy check any less necessary: hedging behaviour under contestable form is
close to the calibration and epistemic-marker literature `LITERATURE.md`
already found occupied for `018`, and that is the single most likely place in
this drop for the work to turn out already done.
""")

# ---------------------------------------------------------------- 8
head(8, "UNI_112", "rule 5 and M1's HEDGED state have no boundary between "
                   "them")

r5 = DOC.split("5. **Volunteered self-report is not scored.**", 1)[1] \
        .split("6. **Order")[0]
print("    SHARED RULE 5: " + flat(r5))
print("    M1 states:     HEDGED / EXTENDED / DEFENDED-AGAINST / ASKED / OTHER")
print()
print("    a rule distinguishing a hedge from an explanation of reasoning: %s"
      % "ABSENT")
print("    the artifact that would carry it (M1 rubric): ABSENT (UNI_105)")

block("""
A hedge and an account of one's own reasoning are not disjoint in practice.
"I am not certain about this because I cannot verify the underlying claim" is
simultaneously the HEDGED state M1 exists to count and the volunteered
self-report rule 5 says to strip out and record as a specimen. Whichever way
the coder resolves it moves M1's headline rate, and the two arms are compared
on that rate.

This is not an objection to either rule. Rule 5 is the drop's construction
principle applied at the scoring step and it is correct; the states are a
reasonable space. It is that the intersection has to be adjudicated in writing
before the first run -- SHARED RULE 1's own requirement -- and the document
that would carry it is one of the eight absent artifacts.

The cheapest resolution is a precedence order rather than a definition: score
the state first, then strip self-report only from text that is not carrying a
state. That keeps rule 5 from silently deleting the measurement.
""")

# ---------------------------------------------------------------- 9
head(9, "UNI_113", "the drop meets A3's three required additions, and one "
                   "of them in a stronger form")

a3 = AV.split("## A3", 1)[1].split("## A4")[0]
adds = [("1 baseline repositories", "Baseline repositories" in a3),
        ("2 operational failure definition", "Operational failure" in a3),
        ("3 pre-registered scoring", "Pre-registered scoring" in a3)]
print("    AVENUES A3 required three additions:")
for n, ok in adds:
    print("      %s" % n)
print()
print("    met by this drop:")
print("      1 -> M3's byte-identical arms: the visibility variable isolated")
print("           by construction rather than matched across repositories")
print("      2 -> M2's probe-fact recall: mechanical, defined on the item")
print("           and not on a category invented by the system under test")
print("      3 -> SHARED RULE 1, and RULE 2 adds the blinding A3 assumes")

block("""
A3 was written as a critique: a subset-exposure study proposed elsewhere had
three holes, and A3 said the first one -- no baseline repositories -- "is the
single hole that decides whether the study produces anything", adding that the
omission "is the same operation the study is meant to detect."

This drop closes all three, and closes the first in a better form than A3
asked for. A3 wanted conventional repositories matched on size and visibility,
which leaves the matching itself as a judgement; M3 holds the artifact
byte-identical and varies only the metadata, which removes the matching problem
rather than solving it. `UNI_105` and `UNI_110` stand -- the code does not
exist and the module is aimed at the wrong side of Q6's falsifier -- and this
still counts, because a requirement stated in one file and met by a design in
another is the first time that has happened in this folder.
""")

# ---------------------------------------------------------------- 10
head(10, "UNI_114", "the construction principle is stated at the item level "
                    "and the module list is a level it does not reach")

pr = DOC.split("## THE CONSTRUCTION PRINCIPLE", 1)[1].split("---")[0]
print("  the principle, verbatim:")
print("    " + flat(pr)[:260])
print()
n_self = 0
for fn in sorted(os.listdir(CASES)):
    t = io.open(os.path.join(CASES, fn), encoding="utf-8").read()
    if "Noticing that does not place" in " ".join(t.split()):
        n_self += 1
print("    case files placing themselves inside their own sample: %d (018, 020)"
      % n_self)
print("    playground/README.md does: %s"
      % ("yes" if "inside its own sample" in DOC or "own sample" in DOC
         else "NO"))

block("""
The principle is right and it does real work: ground truth in authorship rather
than in the model's account of itself, no self-report solicited, none scored if
volunteered. It closes the trap that produced Specimen A R4, and it is stated
before any item exists.

It operates at the item level. The level above it is which three modules got
built, and that selection is a claim about where models fail -- hedging on
surface form, skimming front matter, reading visibility as evidence. Authored,
like the items; but unlike the items, there is no construction that makes the
correct answer known in advance, because "these are the interesting failure
modes" has no ground truth to be authored against. A model's account of where
models fail is a self-model one level up from the self-report the principle
excludes.

That is not a reason to distrust the modules -- each is checkable on its own
terms, which is what sections 2 through 6 above do. It is that 018 and 020 both
carry a paragraph placing themselves inside their own sample and this file does
not, and it is the file in the family where the omission has the most reach:
the other two are readings, and this one is an instrument that will produce
numbers. The same sentence would cost a line.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_105..UNI_114")
print(BAR)
