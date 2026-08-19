#!/usr/bin/env python3
"""case_023_audit.py -- checks on the 023 drop, run through its own T1.

Added, not delivered. `cases/023borrowedselectionvocabulary.md` is the entry as
received and is not modified. Findings recorded in AUDIT_NOTES.md as
UNI_147..UNI_153.

    python3 case_023_audit.py

023 specifies T1 and then says: "Run it against the historical cases first --
they are the calibration set, and if the audit does not separate Lysenkoism
from population genetics it is not measuring anything."

So it was built (`selection_cuts.py`) and run, and most of what follows is the
instrument's output rather than a reading of the text. That is the difference
between this audit and the preceding twenty-odd: the findings were computed.

The calibration scores are AUTHORED -- coded from 023's own descriptions -- and
are the input, not a result. Sections 2 and 3 are robust to that in a way
section 1 is not; each says so.

LITERATURE CHECK. Section 6 was run against the open web on 2026-08-18 and is
marked. It does not reproduce here. Everything else reproduces exactly.

stdlib only, deterministic. CC0.
"""

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import selection_cuts as SC                                     # noqa: E402

CASES = os.path.join(HERE, "cases")
C23 = io.open(os.path.join(CASES, "023borrowedselectionvocabulary.md"),
              encoding="utf-8").read()
BAR = "=" * 72
D = SC.calibrate()


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def flat(t):
    return " ".join(t.split())


print("uninstrumented -- audit of the 023 drop")
print("delivered: cases/023borrowedselectionvocabulary.md")
print("           (%d lines, %d words)" % (C23.count("\n") + 1, len(C23.split())))
print("built:     selection_cuts.py -- T1, with the calibration set as a gate")

# ---------------------------------------------------------------- 1
head(1, "UNI_147", "T1 runs, the gate passes, and one cut carries the "
                   "separation")

print("    calibration cases: %d   coding problems: %d"
      % (D["n"], len(D["problems"])))
print()
print("    %-26s %-10s %s" % ("cut", "separates", "overlapping values"))
for cut, r in D["per_cut"].items():
    print("    %-26s %-10s %s"
          % (cut, "yes" if r["separates"] else "NO",
             ", ".join(r["overlap"]) or "-"))
print()
print("    full vector separates: %s" % D["separable"])
print("    minimal separating subsets: %s"
      % "; ".join(" + ".join(x.split("_")[0] for x in m)
                  for m in D["subsets"]["minimal"]))
print("    cuts that are NECESSARY: %s"
      % (", ".join(D["subsets"]["necessary"]) or "none"))

block("""
023 asked for exactly this and it answers in its favour on the headline
question: the four cuts as a VECTOR separate Lysenkoism from population
genetics, and the gate passes. The instrument is not measuring nothing.

What the per-cut column adds is that the separation is not distributed across
four conditions. **C3 alone separates the whole set.** C1, C2 and C4 each take
values that appear in both classes. And no cut is necessary -- drop any one and
the remaining three still separate -- so on this set the four are redundant
rather than jointly required.

That matters for how the file presents them. Each cut is introduced as "a
condition selection requires", which is a claim about the concept and may well
be right. What the calibration set shows is a claim about the INSTRUMENT: as
scored, it is a one-cut instrument with three cuts alongside it, and a domain
audit reporting "fails 4 of 4" is reporting one finding four times.

The caveat is load-bearing and belongs here rather than in a footnote. Nine
cases, coded by this audit from 023's own descriptions. Recode eugenics C1 as
NON_EXCLUSIVE and the picture changes. What does not change is section 2.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_148", "C2 is inert, and 023's own NOT CLAIMED HERE is what "
                   "makes it so")

print("    %-34s %-9s %-10s %s" % ("C2 value", "LITERAL", "BORROWED", "status"))
for v in SC.CUTS["C2_authorship"]:
    lit = [n for n, c in SC.CALIBRATION.items()
           if c["C2_authorship"] == v and c["expects"] == "LITERAL"]
    bor = [n for n, c in SC.CALIBRATION.items()
           if c["C2_authorship"] == v and c["expects"] == "BORROWED"]
    print("    %-34s %-9d %-10d %s"
          % (v, len(lit), len(bor), "INERT" if lit and bor else ""))
print()
print("    the LITERAL cases sitting on AUTHORED_BY_INTERESTED_PARTIES:")
for n, c in SC.CALIBRATION.items():
    if (c["expects"] == "LITERAL"
            and c["C2_authorship"] == "AUTHORED_BY_INTERESTED_PARTIES"):
        print("      %s" % n)
print()
nc = C23.split("## NOT CLAIMED HERE", 1)[1].split("\n\n")[0]
print("    023 NOT CLAIMED HERE, verbatim:")
print("      " + flat(nc)[:200])

block("""
Every one of C2's three values appears in both classes. It contributes nothing
to the separation, and it is the only cut of which that is true across all
values rather than one.

The reason is in 023's own text. NOT CLAIMED HERE names directed evolution and
evolutionary algorithms as domains where the vocabulary is correct -- and both
are environments authored end to end by parties with a position in the outcome.
A biologist choosing which variants to carry forward IS the selection
environment. So "authored rather than encountered" cannot be what separates
literal from borrowed use, because the file's own two clearest literal cases
are maximally authored.

This finding does not depend on how this audit coded anything contested. It
needs only 023's statement that those two are literal, which the file makes,
and the observation that they are authored, which is not in dispute.

C2 is not thereby wrong about the AI case -- the environment there is authored
by interested parties, and that is worth saying. It is that the fact does not
discriminate, so it cannot carry the argument's weight. The cut that survives
this is C3: directed evolution has a stable criterion, and that is what makes
the authoring harmless.
""")

# ---------------------------------------------------------------- 3
head(3, "UNI_149", "the instrument disagrees with the file about the closest "
                   "historical match")

subj = SC.SUBJECT["ai_model_selection"]
sv = tuple(subj[c] for c in SC.CUTS)
print("    023 states: eugenics is the \"closest match including C4\"")
print()
print("    %-26s %-8s %s" % ("case", "absent", "same vector as the subject?"))
for n, c in SC.CALIBRATION.items():
    v = tuple(c[x] for x in SC.CUTS)
    s = SC.score(c, n)
    print("    %-26s %d/4      %s"
          % (n, s["n_conditions_absent"], "YES" if v == sv else ""))
print("    %-26s %d/4" % ("ai_model_selection (subject)",
                          SC.score(subj, "s")["n_conditions_absent"]))
print()
print("    eugenics differs from the subject on: %s"
      % ", ".join(c for c in SC.CUTS
                  if SC.CALIBRATION["eugenics"][c] != subj[c]))

block("""
Scored on its own four cuts, the subject's nearest neighbour is Spencer, not
eugenics -- identical vector, 4 of 4 conditions absent. Eugenics differs on C1
and comes out at 3 of 4.

The reason is the definition 023 gives C1: selection requires that failing the
criterion removes you from the population. Compulsory sterilization does
exactly that -- it removes people from the reproducing population, which is the
population a selection claim is about. On the stated condition, eugenics scores
EXCLUSIVE. So does Lysenkoism, where dissenting geneticists were removed by
imprisonment and execution.

Two readings, and the file should pick one. Either C1 is satisfied by those
cases -- in which case they are genuinely exclusive environments and the
"closest match" claim needs to rest on C2/C3/C4, which is where the file's own
argument for eugenics actually sits -- or C1 means something narrower than
"removes you from the population" and the narrower thing should be written
down.

Nothing here softens the historical comparison. It sharpens which cut is
carrying it: not C1.
""")

# ---------------------------------------------------------------- 4
head(4, "UNI_150", "C4's forward consequence is the strongest content and "
                   "has no readout")

fc = C23.split("Forward consequence:", 1)[1].split("---")[0]
print("  verbatim:")
print("    " + flat(fc))
print()
for t in ("T1 — The four-cut audit", "T2 — Timing check", "T3 — Amplification"):
    body = C23.split(t, 1)[1].split("###")[0] if t in C23 else ""
    reaches = "judge" in body.lower() or "variance" in body.lower()
    print("    %-32s measures the judge-variance claim: %s"
          % (t.split("—")[0].strip(), "yes" if reaches else "NO"))

block("""
The claim is that a later study of which agents persisted, inferring properties
from persistence, would be reading judge variance as a property of the agents.
That is a real methodological consequence with a name already attached in this
folder -- `016` Q6, an unmeasured variable used as evidence -- and 023
identifies it correctly.

None of the three instruments touches it. T1 scores the vocabulary conditions,
T2 scores adoption timing, T3 tracks a term through citation. The judge-variance
claim is about a future inference and is the file's most consequential content.

It is also the most measurable thing in the file, because it has a standard
form and does not need the selection argument at all. Inter-rater agreement on
the termination decision is the whole quantity: give several judges the same
cases and measure whether they agree. That is `022`'s ICC2 = .184 shape applied
one layer over, and if the agreement is low, the persistence record carries
judge variance regardless of whether anyone calls the process selection.

Worth separating for that reason. C4's forward consequence stands or falls on a
reliability coefficient, and it would survive every other claim in the file
being wrong.
""")

# ---------------------------------------------------------------- 5
head(5, "UNI_151", "the referent of C4 is ambiguous in exactly the way 021 "
                   "describes")

c4 = C23.split("### C4", 1)[1].split("---")[0]
print("  C4, verbatim:")
print("    " + flat(c4)[:330])
print()
for w in ("termination", "agents", "in the room", "qualifications"):
    print("    %-16s occurrences in C4: %d" % (w, flat(c4).lower().count(w)))
print()
print("    023 declares itself: \"Instance of `021`\"")
print("    021's mechanism: one word entering with one sense and exiting with")
print("      another, with nothing in the sentence marking the swap.")

block("""
"Terminations are executed on the judgment of whoever is in the room. Different
person, different room, different qualifications, different standards." And:
"Two agents doing identical things receive opposite outcomes depending on the
room."

Read against the file's opening -- an index, developers, company interests,
legal enforcement -- the referent is AI models. Read on its own, C4 describes
employment terminations: rooms, qualifications, standards, people. "Agent" and
"termination" each carry both senses, and nothing in the section marks which is
meant.

The maintainer resolved it on delivery -- the subject is AI agent selection --
so this is ambiguity in the text rather than confusion in the author, and it is
recorded on that basis.

It is worth recording because 023's second line declares it an instance of 021,
and 021's mechanism is a word entering with one sense and exiting with another
with nothing marking the swap. `UNI_130` found the same thing in 021 itself, on
"medium". Third instance in three files, and the first where the ambiguous term
sits in the section the file calls its sharpest cut.

Cheapest fix in the drop: one clause naming the referent in C4's first
sentence.
""")

# ---------------------------------------------------------------- 6
head(6, "UNI_152", "the Spencer timing verifies, and the same record "
                   "complicates the invariant there")

print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print()
print("    023 states: Spencer, \"survival of the fittest\" (1864; adopted")
print("      into Darwin's 5th ed.)")
print("    located:    Spencer coined it in Principles of Biology (1864);")
print("      Darwin adopted it in the 5th edition of Origin (1869).")
print("      CONFIRMED, both dates and the direction.")
print()
print("    also located, and not in 023: Wallace urged the term on Darwin in")
print("      1866 specifically to avoid readers taking 'natural selection' to")
print("      personify nature as *selecting*.")
print()
print("    not independently checked this pass: Alchian (1950), the eugenics")
print("      board/physician characterisation, the memetics criticism.")

block("""
The dated claim checks out in both directions, which is what T2 needs.

The detail the search adds runs mildly against the invariant in this one
instance. 023's invariant is that the vocabulary buys credibility validation
would otherwise have to buy, and that it arrives before the process stabilises.
Spencer's phrase entering ECONOMICS and social policy fits that exactly and is
what the table's right-hand column describes.

Its entry into BIOLOGY does not. Wallace proposed it to Darwin for a technical
reason -- to stop "natural selection" reading as though nature were an agent
doing the selecting -- and Darwin adopted it into an already-stable theory
eight years after Origin. That is a borrowing that arrived after stabilisation,
for precision rather than for credibility, running the opposite way.

T2 asks for exactly this: "A case where the word arrived after a stable epoch
would falsify the invariant, and is worth looking for specifically." The
Spencer row may contain one, in the direction the table does not track. Not a
refutation of the invariant, which is about export from biology outward; a
candidate the file's own falsifier instruction points at, sitting inside its
own first row.
""")

# ---------------------------------------------------------------- 7
head(7, "UNI_153", "the calibration-first instruction is what made this "
                   "auditable")

t1 = C23.split("### T1", 1)[1].split("### T2")[0]
print("    T1's closing instruction, verbatim:")
print("      " + flat(t1).split("Run it against")[1][:200])
print()
print("    T2's falsifier instruction, verbatim:")
t2 = C23.split("### T2", 1)[1].split("### T3")[0]
print("      " + flat(t2).split("A case where")[1][:180])
print()
print("    drops in this family specifying a calibration set inside the")
print("      instrument definition, before the instrument exists: 1 (this one)")

block("""
Two design decisions did more work than anything else in the file.

T1 names its calibration set and states the failure condition in the same
breath -- "if the audit does not separate Lysenkoism from population genetics
it is not measuring anything." That is a known-null/known-signal pair specified
BEFORE the instrument exists, which is the property `null-harness/` grades for
and the thing `UNI_106` found missing in M1, `UNI_080` found missing in the
leakage screen, and `UNI_126` found impossible in 021's T1. Here it is present,
and it is why `selection_cuts.py` could enforce a gate rather than print a
caveat: the refusal condition was already written.

T2 does the rarer thing. It names what would falsify the invariant and says the
case is "worth looking for specifically rather than waiting to encounter."
Actively seeking the refutation rather than remaining open to it. Section 6
above found a candidate on the first look, in the file's own first row, which
is roughly what that instruction predicts will happen if it is followed.

Recorded plainly because six of the seven findings above are objections, and
they were all reachable only because the file specified the conditions under
which it could be checked.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_147..UNI_153")
print("seven findings. the material gave seven.")
print(BAR)
