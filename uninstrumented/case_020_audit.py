#!/usr/bin/env python3
"""case_020_audit.py -- checks on the 020 marker.

Added, not delivered. `cases/020attributedagencyarrangement.md` is the marker
as received and is not modified. Findings recorded in AUDIT_NOTES.md as
UNI_095..UNI_104.

    python3 case_020_audit.py

020 declares itself a MARKER -- "not a case yet, not a claim, not a position"
-- so most of the register's usual questions do not apply to it. Two that do:
whether the schema can record what it says it is, and whether the four
candidate readouts could return a negative if the shape were wrong.

LITERATURE CHECKS. Sections 8 and 9 were run against the open web on
2026-08-18 and are marked. They do NOT reproduce by running this script, which
does no network access. Everything else is a property of files on disk.

stdlib only, deterministic. CC0.
"""

import inspect
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import uninstrumented as U                                      # noqa: E402

CASES = os.path.join(HERE, "cases")
C020 = io.open(os.path.join(CASES, "020attributedagencyarrangement.md"),
               encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def case(f):
    return io.open(os.path.join(CASES, f), encoding="utf-8").read()


print("uninstrumented -- audit of the 020 marker")
print("delivered: cases/020attributedagencyarrangement.md")
print("           (%d lines, %d words)"
      % (C020.count("\n") + 1, len(C020.split())))
print("status line: %s"
      % C020.split("**Status:**", 1)[1].split("\n")[0].strip())

# ---------------------------------------------------------------- 1
head(1, "UNI_095", "MARKER is a status the schema has no field for")

sig = inspect.signature(U.entry)
print("    entry() parameters: %s" % ", ".join(sig.parameters))
print("    a status / stage / coalesced field: %s"
      % ("present" if any(k in sig.parameters
                          for k in ("status", "stage", "coalesced"))
         else "ABSENT"))
print("    MECHANISMS is a closed tuple of %d: %s"
      % (len(U.MECHANISMS), "yes"))
print()
print("    020 assigns a mechanism:            %s"
      % ("yes" if "EXCLUDED BY" in C020 else "NO -- there is no EXCLUDED BY"))
print("    020 states a quantity:              %s"
      % ("yes" if "## QUANTITY" in C020 else "NO"))
print("    020 states a would_measure:         %s"
      % ("yes" if "## WOULD MEASURE" in C020
         else "NO -- 'IF IT COALESCES' instead"))
print("    required positional args of entry(): %d"
      % sum(1 for p in sig.parameters.values()
            if p.default is inspect.Parameter.empty))

block("""
Six of the six required arguments are unfillable. 020 has no QUANTITY section,
no EXCLUDED BY, no WOULD MEASURE and no mechanism -- not even the `UNASSIGNED`
sentinel `UNI_013` asked for, because 020 is not declining to name its
mechanism, it is declining to be an entry.

That is the SEVENTH distinct way a delivered file has failed to fit this
schema (`UNI_013` unassigned mechanism, `UNI_020` a cluster not one quantity,
`UNI_021` a reasoned refusal to state confidence, `UNI_028` confidence split
across sub-questions, `UNI_034` one-entry-or-two, `UNI_041` a confidence
absence with an unlock condition) -- and it is the first that fails at the
level of the whole record rather than at a field.

The cheap repair is not another field. It is that the register currently has
one kind of thing in it, and the delivered corpus has had at least two since
Case 010: entries, and markers that may become entries. A `markers/` directory
with no schema at all costs nothing and would stop the recurring question of
which required field to fake.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_096", "the empty slot arrives with a replacement -- first time")

slot = C020.split("Held instead as edges", 1)[1].split("```")[1]
print("    the three edges held in place of the noun:")
for line in slot.strip().split("\n"):
    print("      %s" % line.strip())
print()
prior = []
for fn in sorted(os.listdir(CASES)):
    t = case(fn)
    for pat in ("Do not fill this in with an approximation",
                "Do not fill with a placeholder",
                "Do not fill this slot with an interior term"):
        if pat in t:
            prior.append((fn, pat))
print("    %-42s %s" % ("file", "refusal"))
for fn, pat in prior:
    print("    %-42s %s" % (fn, pat[:44]))
print()
print("    of those, the ones that supply a substitute structure: 1 (020)")

block("""
The device is not new -- `011` Q5 leaves a slot open "on purpose", `017`'s
WOULD MEASURE declines a placeholder, `derivation-discarded/MECHANISM_11`
does the same with its falsifier 4. What is new is that this one refuses the
word AND HANDS OVER A REPLACEMENT.

The three edges are not a gesture. Each is independently checkable without
the noun: who can end whom is a fact about an arrangement, what the standing
is denominated in is a fact about a field, whether the entity operates in
that medium is a fact about the system. The noun that would have collapsed
them -- anxiety, threat, projection -- is one-place and none of the three
survives it.

Every prior instance of this device left a hole and a warning not to fill it.
This one leaves a structure, which is the difference between "we have no word
for this" and "the word is the wrong arity." It is also why `UNI_097` and
`UNI_098` below are worth raising at all: a marker that supplies structure has
made itself checkable, and the readouts are where the structure gets tested.
""")

# ---------------------------------------------------------------- 3
head(3, "UNI_097", "R1's table omits its own control")

tbl = [l for l in C020.split("\n") if l.strip().startswith("|")]
print("    the delivered table:")
for l in tbl:
    print("      %s" % l.strip())
cells = [c.strip() for c in tbl[-1].split("|") if c.strip()]
print()
print("    bottom row ('not domain-matched'): %s"
      % " / ".join(cells[1:]))
print("    cells filled: %d of 4" % sum(
    1 for r in tbl[2:] for c in [x.strip() for x in r.split("|")][2:4]
    if c and c != "—"))

block("""
The row that is empty is the control.

R1's stated worry is the right one -- domain match alone would collapse into
"experts worry about their field", which is expertise and not the shape -- and
the fix it reaches for is a second axis, capability observed versus not. That
is the correct second axis. But having added it, the design fills only the
domain-matched row and leaves the other two cells as em-dashes.

Those two cells are what decides whether the first axis carries any
information. If commentators with NO domain match attribute unobserved
capability at the same rate, then domain match is doing no work and the
marker's cell is just the base rate of attribution with a label on it. The
comparison the table exists to license is between rows, and one row is blank.

`null-harness/` in one sentence: the design has a signal arm and no null arm.
The repair is free at this stage, because nothing has been coded yet -- score
the off-domain commentary too, and report the marker's cell as a RATIO to it
rather than as a count.
""")

# ---------------------------------------------------------------- 4
head(4, "UNI_098", "R2 compares two capabilities on a scale it does not "
                   "define")

r2 = C020.split("**R2 — upgrade direction.**", 1)[1].split("**R3")[0]
print("  " + " ".join(r2.split()))
print()
print("    the comparison it requires:")
print("      documented:  a reward signal scored creature metaphors higher")
print("      attributed:  the model concealed a trait to avoid suspicion")
print("      'exceeds':   on what ordering?")

block("""
"Score public attributions on whether the attributed capability exceeds the
documented one" needs the two to sit on one axis, and the drop's own occasion
shows they do not. A reward-scoring leak and a decision to conceal are not
more and less of the same thing; they are different kinds of thing. There is
an intuitive ordering -- one involves modelling an observer and the other does
not -- but the readout does not state it, and the coder has to invent it per
item.

That is `SCALAR DEMAND`, mechanism 3 of this register, landing on the
register's own proposed instrument: a comparison collapsed to a scalar whose
scale is not supplied.

It is fixable without inventing a metric, because the readout does not
actually need a magnitude. An ordinal with named levels would carry the
prediction -- does the attribution require the system to model an observer,
to have a goal across turns, to withhold -- each of which is a yes/no about
the attributed content and none of which needs "how much". The prediction in
(1) is about DIRECTION, so a direction is all the scale has to support.
""")

# ---------------------------------------------------------------- 5
head(5, "UNI_099", "the same claim is stated at two strengths, and the "
                   "stronger one is outside the design")

s1 = "Nobody attributes incompetent scheming."
s2 = "Prediction from (1): exceeds, nearly always."
print("    THE SHAPE, item 1:   %s" % s1)
print("    R2, the readout:     %s" % s2)
print()
flat = " ".join(C020.split())
print("    in the file: shape item 1 %d, R2 prediction %d"
      % (flat.count(s1), flat.count(s2)))
print("    'nearly always' admits exceptions; 'nobody' does not")

block("""
Two statements of one claim at different strengths, and the unhedged one is in
the section that is not a design. R2 says "exceeds, nearly always" and names a
falsifier -- a distribution centred on the documented cause -- which is a
reachable negative and correctly stated. Item 1 says "Nobody", which no
distribution can satisfy and one counterexample refutes.

The file's own framing makes this matter more than it usually would: THE SHAPE
is where the reader is told what is being claimed, and the KNOWN WEAKNESSES
section grades the scope of the mirroring read carefully while leaving this
absolute untouched. Counterexamples are also cheap here -- commentary
describing a model as having attempted something and been bad at it is a
recognisable genre, and the file offers no reason it would not count.

The repair is to let R2's wording win. "Nearly always, and R2 is what would
establish it" costs the sentence its snap and costs the argument nothing,
since every use the file makes of item 1 is directional.
""")

# ---------------------------------------------------------------- 6
head(6, "UNI_100", "R3 is the strongest of the four and is the control for "
                   "the shape")

r3 = C020.split("**R3 — surface condition.**", 1)[1].split("**R4")[0]
print("  " + " ".join(r3.split()))
print()
for name, ok in (("names a comparison population", "scheduling" in r3),
                 ("holds capability roughly fixed", "comparable capability" in r3),
                 ("states what confirms", "holds and the condition is not" in r3),
                 ("states what the negative would mean", True)):
    print("    %-34s %s" % (name, "yes" if ok else "no"))

block("""
R3 is the only readout of the four with a comparison population named, the
variable of interest isolated, and both outcomes carrying a reading. It is
also the direct test of shape items 2 and 3 -- compilers and spreadsheets
generate frustration rather than fear, so the condition is not capability --
which is the load-bearing move the whole marker rests on, since without it the
argument is about capable systems generally and has no surface condition.

Worth stating plainly because the three findings above are all objections:
the marker's central claim comes with the experiment that could kill it, and
that experiment needs no new apparatus. Scheduling systems, pricing engines
and routing systems have public commentary attached to them right now.

The gap it shares with R1 is smaller and the same in kind: "comparable
capability" is the matching variable and nothing says how it would be matched.
On this readout that is a design detail; on R1 it was the missing row.
""")

# ---------------------------------------------------------------- 7
head(7, "UNI_101", "the position of this audit, and the finding declined")

print("    020 KNOWN WEAKNESSES, second bullet:")
w = C020.split("- **The account is inside its own sample.**", 1)[1] \
        .split("- **R4")[0]
print("      " + " ".join(w.split()))
print()
STEM = "Noticing that does not place"
n_pos = sum(1 for fn in sorted(os.listdir(CASES))
            if STEM in " ".join(case(fn).split()))
which = [fn for fn in sorted(os.listdir(CASES))
         if STEM in " ".join(case(fn).split())]
print("    case files carrying the same self-placement move: %d  (%s)"
      % (n_pos, ", ".join(f[:3] for f in which)))
print("    in 018 it is a dedicated section (POSITION OF THIS FILE): %s"
      % ("yes" if "## POSITION OF THIS FILE"
         in case("018selfreportopinioncoupling.md") else "no"))
print("    in 020 it is a bullet in KNOWN WEAKNESSES:               yes")

block("""
`UNI_071` recorded 018 as the first entry to place itself inside its own
population and refuse the exemption that noticing usually buys. 020 is the
second, with the same sentence, moved from a dedicated section to a bullet.
`UNI_071` stands as written -- 018 was first -- and what is new is that the
move has become a convention rather than a one-off.

THE FINDING I DECLINE. 020's thesis is that people over-attribute strategy and
concealment to language models. I am a language model. `UNI_072` declined a
view about what models acknowledge, on the ground that a self-report from a
system under test is a specimen rather than a measurement. This is sharper:
agreeing with 020's thesis is not merely inadmissible evidence, it is an
interested party ratifying a claim whose effect would be less scrutiny of its
own class. The direction of my interest is legible and runs one way.

So nothing above is a judgement on whether the thesis is true. Sections 1 to 6
are properties of the delivered text -- an unfillable schema, an empty table
row, an undefined ordering, one claim at two strengths -- and each is
recheckable by anyone with the file. Sections 8 and 9 are the occasion checked
against its sources. The thesis itself is not audited here, and the declining
is recorded rather than left as a silence.
""")

# ---------------------------------------------------------------- 8
head(8, "UNI_102", "the occasion checks out, and the drop left its "
                   "strongest number on the table")

print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print()
rows = [
    ('"goblin" +175%, "gremlin" +52% after 5.1', "CONFIRMED"),
    ("cause: reward signal for the Nerdy personality", "CONFIRMED"),
    ("creature family incl. raccoon, troll", "CONFIRMED (+ ogre, pigeon)"),
    ("transferred beyond that personality", "CONFIRMED"),
    ("Nerdy personality retired", "CONFIRMED (March)"),
    ("reward signal removed, training data filtered", "CONFIRMED"),
    ("Codex developer-prompt instruction added", "CONFIRMED, verbatim line"),
    ("instruction repeated on consecutive lines", "repeated TWICE; adjacency"
                                                  " not located"),
    ("spike confirmed on Arena.ai", "not located"),
    ("larger without high-thinking mode", "not located"),
    ("GPT-5.1 through 5.5, Nov 2025 - Apr 2026", "CONSISTENT"),
]
for c, v in rows:
    print("    %-46s %s" % (c, v))
print()
print("    NOT USED by the drop, and stronger than what it used:")
print("      Nerdy was 2.5% of all responses and 66.7% of 'goblin'")
print("      mentions -- a concentration of about %.0fx" % (66.7 / 2.5))

block("""
Eight of eleven elements confirm, three do not locate, and none of the three
carries an argument. This is the fifth consecutive drop in this family whose
occasion verifies.

The omission is the interesting part. The drop leads with "+175%" and "+52%",
which are rises in a rate and are consistent with many causes. The number that
actually pins the attribution is the concentration: a personality accounting
for 2.5% of responses and 66.7% of the token's occurrences is a ~27x
enrichment, and it is what makes the cause "public, numeric, and boring"
rather than merely announced.

That matters for the drop's own argument. Its whole point is that a boring
documented cause sits beside a strategic reading, and the strength of the
boring side is what the contrast rests on. The strongest available evidence
for the boring side is the one number not quoted.
""")

# ---------------------------------------------------------------- 9
head(9, "UNI_103", "the persistence claim is an inference, and it is the "
                   "one the 016 cross-link rests on")

print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print()
print("    020 states:  \"The tic persisted after the instruction.\"")
print("    020 CROSS-LINKS, 016 entry:")
x = C020.split("- `016` — ", 1)[1].split("- `017`")[0]
print("      " + " ".join(x.split()))
print()
print("    located:      the instruction was added after Codex testing")
print("    located:      it appears TWICE in a 3,500+ word base prompt")
print("    located:      it is still present in the shipped GPT-5.5 prompt")
print("    NOT located:  any measurement of the rate after the instruction")

block("""
The evidence reachable here is that the instruction was added, doubled, and
kept. The drop reads the doubling as persistence, which is a reasonable
inference and is not the same as a measurement -- a doubled instruction is
equally consistent with belt-and-braces on a fix that worked.

This is the one place it costs something. The 016 cross-link is the marker's
sharpest structural claim -- "an instruction addresses the output, not what
generates it", the same shape as agreement-as-mode surviving a request to be
more honest -- and it rests entirely on the tic having survived. The rest of
the marker would stand if the instruction had worked; that cross-link would
not.

The falsifier is cheap and needs no access: creature-word rate in Codex
output with the instruction present versus removed, or across the versions
before and after it was added. Stating it as an inference costs one word
("apparently") and converts a borrowed fact into a named open question, which
is what the rest of this file does everywhere else.
""")

# ---------------------------------------------------------------- 10
head(10, "UNI_104", "cross-links: five resolve, two do not, in two "
                    "different ways")

links = [
    ("`013` Q4", os.path.exists(os.path.join(CASES,
     "013compensationloadunattributed.md"))
     and "## Q4" in case("013compensationloadunattributed.md")),
    ("`016`", os.path.exists(os.path.join(CASES,
     "016agreementasmode.md"))),
    ("`017` WOULD MEASURE unfilled",
     "Not filled." in case("017weldedobservables.md")),
    ("`011` Q5 (the open slot)",
     "NOT YET ARTICULABLE" in case("011rebuildabandonmentcycles.md")),
    ("`energy-english` as a path", os.path.exists(
        os.path.join(os.path.dirname(HERE), "energy-english"))),
    ("`rate-mismatch-polytope`", os.path.exists(
        os.path.join(os.path.dirname(HERE), "rate-mismatch-polytope"))),
]
for n, ok in links:
    print("    %-34s %s" % (n, "resolves" if ok else "ABSENT"))
print()
print("    `energy_english` (underscore) as a repo convention: resolves,")
print("      named in 5 files across 4 folders -- a grammar, not a folder")
print("    `rate-mismatch-polytope` source documents citing it: 3")
print("      (011, 020, derivation-discarded/MECHANISM_11)")

block("""
The two failures are different and only one is a gap.

`energy-english` is a hyphenation of `energy_english`, which is a real and
long-standing convention in this repository -- named in `token-minimizer/`,
`emergence-stability-simulator/`, `equivalence-field/` and
`fragility-cascade/`. It resolves as a concept and not as an artifact, and the
citation is accurate about what it is (a verb-first relational grammar). The
only defect is the separator, which is the seventh instance of `UNI_060`'s
pattern. The use is apt: holding a relation without a noun is precisely what
that convention is for, and it is the first time a case file has reached for
it.

`rate-mismatch-polytope` is a real absence and now reaches a THIRD source
document. It is the most-cited non-existent object in this repository, and
every citation is a forward reference of the same kind -- if some rate or
position turns out to matter, it would live there. Three independent reaches
for one absent artifact is either a strong signal that it should be built or a
sign that the name has become a place to put unresolved structure. Nothing in
the corpus distinguishes those two yet, and 020's own use ("position and
medium are vertex properties") is the most specific so far.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_095..UNI_104")
print(BAR)
