#!/usr/bin/env python3
"""case_014_audit.py -- checks on the Case 014 drop.

Added, not delivered. `cases/014offloadingevolutionaryframing.md` is the entry as received and is
not modified. Findings recorded in AUDIT_NOTES.md as UNI_042..UNI_049.

    python3 case_014_audit.py

Case 014 is the fifth consecutive delivered case the schema cannot hold,
and the first whose EXCLUDED BY states that nothing excludes it -- which
runs against the register's own opening rule and is the sharpest thing in
the drop.

LITERATURE CHECKS. Sections 3, 4, 5 and 6 were run against the open web
on 2026-08-18 and are marked. They are NOT reproducible by running this
script -- it does no network access. Everything computed from the
register, the entry text and the repo tree is reproducible.

stdlib only, deterministic. CC0.
"""

import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CASE = io.open(os.path.join(HERE, "cases", "014offloadingevolutionaryframing.md"),
               encoding="utf-8").read()
README = io.open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


subq = re.findall(r"^## (Q\d) — (.*)$", CASE, re.M)
print("uninstrumented -- audit of the Case 014 drop")
print("delivered: cases/014offloadingevolutionaryframing.md")
print("cluster   : %d sub-questions, mechanism unassigned" % len(subq))

# ---------------------------------------------------------------- UNI_042

head(1, "UNI_042", "the register's founding binary cannot hold Q1")
print()
rule = README.split("Not a gap log", 1)[1].split("\n\n", 1)[0]
print("  the register's own opening rule:")
print("    Not a gap log%s" % " ".join(rule.split())[:58])
print("    %s" % " ".join(rule.split())[58:118])
q1 = CASE.split("## Q1", 1)[1].split("## Q2", 1)[0]
ex = q1.split("EXCLUDED BY:", 1)[1].split("\n\n", 1)[0]
print()
print("  Q1's EXCLUDED BY, in full:")
print("    %s" % " ".join(ex.split()))
block("""
By the register's own first rule that is a gap, not an exclusion. A gap is
an oversight; nothing prevents the audit and nobody has run it.

But the entry does not leave it there, and the next paragraph is the
interesting one:

    Same shape as the EIA denominator in Mechanism 11: the checking
    apparatus exists in a neighbouring field and is closed on its own
    inputs. [...] The target moved; the instrument did not follow.

That is a third state, and it is neither of the two the README names. The
apparatus exists. It is competent -- the evolution-education critique is
published, specific, and has a name for the exact failure mode. It is
aimed somewhere else. Nobody forgot, and nothing is constitutionally
incapable.

Case 013's Q4 named the same state one drop earlier -- "there, a record is
destroyed. Here the record is intact and unread" -- and Case 014's own
cross-links point at it. So the state has now been delivered twice and the
register's opening distinction is two-valued:

    gap          an oversight
    exclusion    built into the apparatus before the first reading
    ???          the apparatus exists, works, and points elsewhere

The third has no name in the README and no mechanism in the eight-tuple.
Whether it belongs in this register at all is a real question -- and it is
the register's own question, since admitting it widens the register's
subject from what an instrument cannot see to what an existing instrument
is not pointed at.
""")

# ---------------------------------------------------------------- UNI_043

head(2, "UNI_043", "a second absent artifact, now load-bearing across two drops")
print()
refs = re.findall(r"\[\[([^\]]+)\]\]", CASE)
print("  wiki-style references in this entry: %s" % ", ".join(sorted(set(refs))))
print("  cited %d times" % len(refs))
print("  folder ../%s exists: %s"
      % (refs[0], os.path.isdir(os.path.join(ROOT, refs[0]))))
c011 = io.open(os.path.join(HERE, "cases", "011rebuildabandonmentcycles.md"),
               encoding="utf-8").read()
print("  also named in 011rebuildabandonmentcycles.md Q4: %s"
      % ("tool-off" in c011 or "competence-residual" in c011))
block("""
`tool-off-metrology` does not exist anywhere in the tree. It is named
twice in this entry -- once as the BRIDGE under Q4 and once in
CROSS-LINKS -- and Case 011's Q4 already reached for it as "the tool-off /
competence-residual spine".

That makes **two** distinct named-but-absent artifacts, each now
load-bearing across two drops:

    rate-mismatch-polytope   Case 011 Q2, Mechanism 11 sub-q 4   (UNI_026, DD_008)
    tool-off-metrology       Case 011 Q4, Case 014 Q4 + links    (this)

The pattern is worth naming separately from either instance. A forward
reference cited once is a note to self. Two references, each cited by two
different drops for two different arguments, is a set of folders the
drop family keeps needing and has not written -- and both are about the
same thing from different ends: a rate or a baseline that the measurement
destroys.

The `[[...]]` syntax is new here. Prior cases name cross-links in prose.
Nothing in the repo resolves that form, so it reads as a link and behaves
as text.
""")

# ---------------------------------------------------------------- UNI_044

head(3, "UNI_044", "the occasion verifies, including the load-bearing detail  [web]")
print()
for claim, status, note in (
    ("Offloading Reduces Prospective Memory Learning, JEPLMC 2026",
     "CONFIRMED", "Fellers and Storm, Journal of Experimental Psychology: "
                  "Learning, Memory, and Cognition"),
    ("reminder users later remembered fewer future tasks",
     "CONFIRMED", "performance on the previously offloaded PM was "
                  "significantly impaired when reminders were removed"),
    ("BELOW the no-reminder baseline, not merely level with it",
     "CONFIRMED", "'falling below the baseline levels of performance "
                  "observed for participants who never used reminders'"),
    ("attributed to desirable difficulties", "CONFIRMED",
     "framed against the desirable-difficulties account"),
):
    print("  %-9s %s" % (status, claim))
    for i in range(0, len(note), 60):
        print("            %s" % note[i:i + 60])
block("""
Four for four, and the third is the one that matters. "Below the
no-reminder baseline, not merely level with it" is the difference between
a tool that does not help you learn and a tool that leaves you worse than
not having used it, and the source says the second.

Fifth consecutive occasion in this register that checks out
(`UNI_015`, `UNI_023`, `UNI_030`, `DD_002` on the practice, and this).
""")

# ---------------------------------------------------------------- UNI_045

head(4, "UNI_045", "Q1's corpus already exists; someone built it for another purpose  [web]")
block("""
Q1 states: "EXCLUDED BY: nothing prevents it. It has not been assembled."

The second sentence is the expensive one, and it is less true than it
looks. A meta-analysis of cognitive offloading exists -- "Meta-analytic
investigations of the effect of cognitive offloading on memory-based task
performance and interindividual variability" (PubMed 40500483) -- and a
meta-analysis ships an enumerated included-studies list with stated
inclusion criteria.

That list is the denominator Q1 needs. Q1 does not have to assemble a
literature; it has to score one that has already been assembled, for a
different question, by people with no stake in this one -- which is a
better provenance for a denominator than building it to fit the audit.

This changes Q1's cost from "define a corpus and defend the definition"
to "run three-way scoring over a published list", and it is the cheapest
thing this audit can hand back. Same shape as `DD_005` on Mechanism 11's
R2, and concrete rather than structural.

One caveat that has to travel with it: a meta-analysis on memory-based
task PERFORMANCE selects for studies reporting a performance effect,
which is not the same population as "instances where offloading is
described in evolutionary terms". The list is a starting corpus with a
known and statable bias, not the frame Q1 would ideally draw.
""")

# ---------------------------------------------------------------- UNI_046

head(5, "UNI_046", "the critique literature verifies; one attribution is broader than located  [web]")
print()
for claim, status, note in (
    ("Pobiner (2016)", "CONFIRMED",
     "'Accepting, understanding, teaching, and learning (human) "
     "evolution: Obstacles and opportunities', American Journal of "
     "Physical Anthropology"),
    ("need-based rationales assume within-lifetime change is heritable",
     "CONFIRMED", "the acquired-traits misconception -- use or disuse "
                  "leading to heritable change -- is documented in that "
                  "literature as an intuitive conception hindering "
                  "evolution understanding"),
    ("Kelemen, teleological default", "CONFIRMED",
     "'promiscuous teleology', described as a conceptual default all "
     "peoples share, which may be tamped down through enculturation"),
    ("not parental explanation, religiosity, or storybook convention",
     "BROADER THAN LOCATED",
     "the located framing is cross-cultural -- a shared default, "
     "modifiable by enculturation. The three-item negative list was not "
     "confirmed item by item."),
):
    print("  %-21s %s" % (status, claim))
    for i in range(0, len(note), 56):
        print("                        %s" % note[i:i + 56])
block("""
The two named sources are real, correctly attributed, and say what the
entry uses them for. The one item that runs ahead of what was located is
the negative list -- "not the product of parental explanation,
religiosity, or storybook convention". The located characterisation is
compatible with it and is not the same statement: a default shared across
peoples and tamped down by enculturation is a claim about universality,
not a rule-out of three specific sources.

Compatible, not identical, and the distinction matters for the use the
entry makes of it. "It is a default reading mode, which is why it survives
in people who would disavow it if asked directly" needs the negative list
to be load-bearing; universality alone does not get there, since a
universally-taught thing is also universal.
""")

# ---------------------------------------------------------------- UNI_047

head(6, "UNI_047", "Q2 holds against what was located, and its falsifier misses half of it")
block("""
Q2 makes two claims and attaches one falsifier.

  claim A   the reference population is smuggled -- unstated rather than
            misstated, so the generalization is never made explicit
  claim B   this error has no name in the sources found, unlike the
            pinnacle error which is documented

  falsifier "Q2 fails if reference populations are stated in the sources
            and the generalization is explicit rather than smuggled"

The falsifier tests claim A. Claim B -- that the critique does not exist
-- has no falsifier attached, and it is the one the entry leans on
("only one is documented", "the one with no name in the sources found").

On what was located: the evolution-education literature studies
populations of LEARNERS -- religiosity, education, age and political
affiliation as predictors of evolution acceptance -- and not the implicit
reference population of the narrative being taught. So claim B is
consistent with the corpus reached here.

Not searched, and named as the cheapest next check: the history-of-science
and decolonial-paleoanthropology literature, where a critique of
Eurocentric framing in human-origins narratives plausibly exists under a
different name. Claim B is a negative about a literature, and a negative
about a literature is only as good as the search behind it -- which is
`UNI_006`'s rule applied to a claim rather than to a register.
""")

# ---------------------------------------------------------------- UNI_048

head(7, "UNI_048", "the attribution tag at scale, and what it tracks")
print()
tags = re.findall(r"^## (Q\d) — (.*)$", CASE, re.M)
print("  %-4s %-34s %-10s %s" % ("q", "title", "attributed", "instrument"))
print("  " + "-" * 72)
for qid, title in tags:
    body = CASE.split("## %s" % qid, 1)[1].split("\n## ", 1)[0]
    tagged = "[stated by" in body
    wm = body.split("WOULD MEASURE:", 1)[1].split("\n\n", 1)[0].strip() \
        if "WOULD MEASURE:" in body else "(none stated)"
    wm = " ".join(wm.split())
    kind = ("none" if wm.startswith("unclear") or
            wm.startswith("no instrument") else "stated")
    if qid == "Q1":
        kind = "stated"
    print("  %-4s %-34s %-10s %s" % (qid, title[:34],
                                     "yes" if tagged else "-", kind))
block("""
Three tags, up from one in Case 013 (`UNI_035`). The device is now used at
scale rather than as a one-off, and its distribution inside the entry is
informative: the single untagged question is the one with an independent,
runnable instrument and a stated high confidence, and instrumentability
falls off across the tagged ones -- Q2's measurement depends on Q1 having
run, Q3's is "unclear", Q4's is "no instrument proposed".

That is not a criticism of the tagged questions. It is a description of
what the tag is doing: marking the parts of the entry that are somebody's
position rather than a procedure, in an entry whose own reading protocol
says it holds markers and not positions. The tag is how those two things
coexist in one document, and it is doing real work.

`entry()` still has no field for it (`UNI_035`), so all of this lives in
free text.
""")

# ---------------------------------------------------------------- UNI_049

head(8, "UNI_049", "the withheld slot, third instance -- and Q3 states the register's thesis")
print()
for src in ("../uninstrumented/cases/011rebuildabandonmentcycles.md  Q5",
            "../derivation-discarded/MECHANISM_11.md  sub-question 4",
            "cases/014offloadingevolutionaryframing.md  Q3"):
    print("    %s" % src)
block("""
Third instance in three drops. `DD_007` recorded it as "a recurring
device" at two; at three it is a construct with a stable form and still no
schema slot anywhere in the family.

Q3 adds something the prior two did not, and it is the sharpest sentence
in the drop:

    the non-separability may be the finding rather than the obstacle. If
    the channels are not separable in the system, any study isolating one
    is measuring an artifact of its own isolation, and the isolation is a
    property of the instrument.

That is `uninstrumented`'s own thesis stated in general form, by an entry,
about a domain -- and stated as a conditional with the condition named,
rather than as an assertion. It also supplies the shape of Q3's own
falsifier from the other side: a design that separates the channels
"without assuming their independence" is exactly a design whose isolation
is not a property of the instrument.

The NOT CLAIMED HERE section is worth recording alongside it. "No intent.
The drift direction is arguable from evidence; a party steering it is not,
and the case does not require one." That pre-empts the reading that would
convert Q4 into a claim about somebody's plan, and it does it by naming
what the argument does NOT need -- which is the same discipline
`../rigidification-sensor/` states about itself ("names no actor, motive,
or plan by construction") arriving in a one-page case.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_042..UNI_049")
print(BAR)
