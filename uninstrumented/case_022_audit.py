#!/usr/bin/env python3
"""case_022_audit.py -- checks on the 022 marker.

Added, not delivered. `cases/022fieldlevelmeasurementstate.md` is the marker as
received and is not modified. Findings recorded in AUDIT_NOTES.md as
UNI_135..UNI_144.

    python3 case_022_audit.py

022 is the third MARKER and the first to make claims about a literature rather
than about a case. Most of it is checkable two ways: against this repository's
own prior findings, and against the sources.

LITERATURE CHECK. Section 10 was run against the open web on 2026-08-18 and is
marked. It does NOT reproduce by running this script, which does no network
access. Everything else is a property of files on disk.

stdlib only, deterministic. CC0.
"""

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CASES = os.path.join(HERE, "cases")
BAR = "=" * 72


def case(f):
    return io.open(os.path.join(CASES, f), encoding="utf-8").read()


C22 = case("022fieldlevelmeasurementstate.md")
C18 = case("018selfreportopinioncoupling.md")
NOTES = io.open(os.path.join(HERE, "AUDIT_NOTES.md"), encoding="utf-8").read()


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def flat(t):
    return " ".join(t.split())


F22 = flat(C22)

print("uninstrumented -- audit of the 022 marker")
print("delivered: cases/022fieldlevelmeasurementstate.md")
print("           (%d lines, %d words)" % (C22.count("\n") + 1, len(C22.split())))
print("status:    %s" % C22.split("**Status:**", 1)[1].split("\n")[0].strip())

# ---------------------------------------------------------------- 1
head(1, "UNI_135", "confidence is per-item everywhere except the table the "
                   "file is organised around")

print("    the header: \"Confidence: mixed by layer -- stated per item below,")
print("      not over the whole.\"")
print()
for m in re.finditer(r"^### (S\d) — (.+)$", C22, re.M):
    body = C22.split(m.group(0), 1)[1].split("\n### ")[0]
    conf = re.search(r"\*\*Confidence: ([^*]+)\*\*", body)
    print("    %-4s %-44s %s"
          % (m.group(1), m.group(2)[:42],
             conf.group(1).strip() if conf else "NONE"))
print()
tbl = C22.split("| stage |", 1)[1].split("\n\n")[0]
rows = [l for l in tbl.split("\n") if l.startswith("| ") and "---" not in l]
print("    THE STAGES table: %d rows, confidence column: %s"
      % (len(rows), "present" if "onfidence" in tbl else "ABSENT"))
looser = C22.split("## HELD LOOSER", 1)[1].split("## POSITION")[0]
demoted = [w for w in ("liking", "fear") if w in looser.lower()]
print("    stages demoted 60 lines later in HELD LOOSER: %s"
      % ", ".join(demoted))
print("      \"no measurement of them was found in this audit and none is")
print("       proposed here... not load-bearing for anything above.\"")

block("""
Five of five structural problems carry an explicit confidence. The stage table
carries none, and it is the file's organising device -- the thing that makes
the separability argument, and the first substantive content a reader meets.

Two of its six rows are then held at lower confidence sixty lines later, in a
section that says of them "no measurement of them was found in this audit and
none is proposed here" and "not load-bearing for anything above." That is the
right handling and it happens in the wrong place: a reader who takes the table
as the summary -- which is what a six-row table at the top is for -- gets six
stages at equal weight, and two of them are later disclaimed.

The fix is one column. The file already computes the values; `sign` and
`salience and funding` would read `held looser`, and the table would then carry
the discipline the header announces rather than deferring it.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_136", "S5 instanced on the file's own S4 number, inside this "
                   "repository")

print("    S4, verbatim:")
s4 = C22.split("### S4", 1)[1].split("\n", 1)[1].split("### S5")[0]
print("      " + flat(s4)[:230])
print("    S4's stated confidence: high. \"This one has a number.\"")
print()
print("    S5, verbatim:")
s5 = C22.split("### S5", 1)[1].split("\n", 1)[1].split("\n---")[0]
print("      " + flat(s5)[:240])
print()
print("    what UNI_094 recorded of those same figures, one drop ago:")
row = [l for l in NOTES.split("\n") if "106 experts" in l]
print("      %s" % (row[0].strip() if row else "?"))
print()
print("    022 restates ICC2 = .184:  %s" % ("ICC₂ = .184" in C22))
print("    022 restates 94.3%%:        %s" % ("94.3%" in C22))
fs4 = flat(s4)
print("    S4 marks either figure unverified/unsourced/uncited: %s"
      % ("yes" if any(w in fs4.lower() for w in
                      ("not located", "unverified", "unsourced", "uncited"))
         else "NO"))
print("      (\"not located\" does occur in 022 -- in the welds table, about a")
print("       different item)")

block("""
S5 says: a rate with ICC2 = .184 underneath becomes a plain number in a later
paper's related work, the reliability does not travel with the figure, and
downstream work then treats the quantity as fixed.

`UNI_094` sampled eleven claims from `LITERATURE.md` and found eight
confirmed and three not located. One of the three was "106 experts, 94.3%,
ICC2 = .184". One drop later those figures appear in S4 as the file's single
strongest evidence, flagged "Confidence: high. This one has a number", with no
mark on their status.

So the reliability of the reliability figure did not travel either, and it
travelled a distance of one folder. This is not a hit on the file's argument --
S5 is more likely true for being demonstrable at this range, and the shortest
possible demonstration is the one the file performs on itself without noticing.

It is a hit on S4's confidence rating. "This one has a number" is what S4 has
that S1-S3 do not, and the number is the one item in the neighbourhood that a
prior pass could not source. The repair is a clause, and the file's own
apparatus supplies it: cite the figure and mark it unverified, which is what
`LITERATURE.md` would have needed a per-item depth marker to do (`UNI_094`).
""")

# ---------------------------------------------------------------- 3
head(3, "UNI_137", "the anonymization pattern is two shapes, not one")

an = C22.split("## THE ANONYMIZATION PATTERN", 1)[1] \
        .split("## WHAT WOULD MEASURE")[0]
for n in ("1. **Self-preference**", "2. **Trait scoring**",
          "3. **Peer-preservation**"):
    seg = an.split(n, 1)[1].split("\n\n")[0] if n in an else ""
    print("    %s" % n.split("**")[1])
    print("      " + flat(seg)[:170])
print()
print("    the file's reading: \"partial decoupling works, complete decoupling")
print("      fails or leaves a residual... the same shape twice\"")
print()
print("    %-10s %-30s %-22s %s"
      % ("leg", "partial perturbation", "full perturbation", "shape"))
print("    %-10s %-30s %-22s %s"
      % ("1", "effect DROPS", "effect RECOVERS", "NON-MONOTONIC"))
print("    %-10s %-30s %-22s %s"
      % ("2", "effect halves", "(not run)", "monotonic, residual"))

block("""
The two legs are joined by an "or" that is doing a great deal of work.
"Complete decoupling fails OR leaves a residual" covers both because it covers
almost anything short of complete success, and the underlying observations are
different in kind.

Leg 1 is non-monotonic: partial obfuscation reduces self-preference, full
stylistic neutralization brings it back. Remove more of the putative cause and
the effect returns. Leg 2 is ordinary partial mitigation: reverse coding
removes some of the skew and some survives.

Those support different conclusions. Leg 2 says style is part of the story and
something else is too. Leg 1 says style may not be the carrier at all, because
an effect that recovers under fuller removal of X is evidence X was not what
was doing the work -- a stronger and more surprising claim than the one the
file draws from the pair.

The file's own follow-up question is aimed at the right place ("If identity
signal survives complete stylistic neutralization, it is carried by something
other than style"), and it applies to leg 1 alone. Splitting the shapes makes
that question sharper rather than weaker: leg 1 is a candidate misattributed
cause, leg 2 is a residual to be decomposed, and they need different next
experiments.
""")

# ---------------------------------------------------------------- 4
head(4, "UNI_138", "S1's remedy is built in this folder and is not linked")

s1 = C22.split("### S1", 1)[1].split("### S2")[0]
print("    S1's stated decoupling:")
print("      " + flat(s1).split("`017` weld.")[1][:210])
print()
print("    018's WOULD MEASURE, Clock 1 + the useful accident:")
acc = C18.split("**Useful accident:**", 1)[1].split("###")[0]
print("      " + flat(acc)[:190])
print()
xl = re.findall(r"^- `([^`]+)`", C22.split("## CROSS-LINKS", 1)[1], re.M)
print("    022 cross-links: %s" % ", ".join(xl))
print("    018 cited anywhere in 022: %s" % ("018" in C22))
print("    selfreport_probe.py present: %s"
      % os.path.exists(os.path.join(HERE, "selfreport_probe.py")))

block("""
S1 says the field structurally lacks repeated measurement of the same object,
that decoupling would require a frozen checkpoint held constant across
instrument generations, and that this is available because old checkpoints
remain queryable.

That is `018`'s Clock 1, its "useful accident" almost word for word, and its
harness has been in this folder for three commits. `018` is the one case file
in the sequence that 022 does not cite.

The gap is not decorative. Two things attach to it. `UNI_073` recorded that the
queryable-checkpoint window has an undated expiry -- deprecation is routine and
announced, `deprecat`/`retire`/`expire` are zero hits in 018 -- and that
observation now applies to S1's entire proposed remedy. And `selfreport_probe.py`
already implements the frozen-checkpoint arm, so what S1 describes as
"largely unused" is unused in the literature and half-built here.

The closing section makes the omission louder rather than quieter. "WHAT THE
OUTSIDE POSITION HAS" names repeated probing across models over time as the one
thing unavailable from inside the field, and asks whether it has been logged as
a series. `018` Clock 1 is the design for reading exactly that, and Q3 there
already states the collection problem in the same words.
""")

# ---------------------------------------------------------------- 5
head(5, "UNI_139", "the control-field audit is the strongest element, and "
                   "it points at this repository")

cf = C22.split("## WHAT WOULD MEASURE THE FIELD-LEVEL CLAIM", 1)[1] \
        .split("## HELD LOOSER")[0]
print("  verbatim:")
print("    " + flat(cf))
print()
for n, ok in (("names a comparison class", "comparison class" in cf),
              ("names candidate fields", "analytical chemistry" in cf),
              ("states the falsifier explicitly", "falsifier for the whole "
               "file" in flat(cf)),
              ("states it has not been run", "has not been run" in cf),
              ("the negative outcome indicts the repo, not the field",
               "finding about the repository" in flat(cf))):
    print("    %-52s %s" % (n, "yes" if ok else "NO"))

block("""
A file making a field-level claim states that the claim needs a comparison
class or it is an impression, names three candidate comparison fields, says
which categories would be scored, and then says in bold that this is the
falsifier for the whole file and it has not been run.

The last property is the one that matters: the negative outcome is aimed at the
repository rather than at the field. "If the hit rate is comparable, the
mechanisms in this repository are loose enough to fit anything, and that is a
finding about the repository rather than about AI research." A framework that
names the result which would indict the framework, and prices it as the same
work as the result that would support it.

The repo has run a smaller version and it is worth connecting. `UNI_004` put
the register against the six externally graded instruments in
`instrument-epistemology` as a known-null corpus and got 0 of 6 filings, and
`UNI_006` recorded the honest counterweight -- that the null was chosen for
being well documented rather than for sitting near the boundary. A control
field is the same test with a harder null, and the same caveat will apply:
analytical chemistry chosen because it is settled is a null selected on the
variable under test.

Of a piece with the rest of the file's refusals. It declines the easy version
three times -- "Not a claim that the findings are wrong", "That is not a
criticism of any study", "the field knows this and builds around it... the
problem is not ignorance" -- and each refusal costs the argument force it could
have had cheaply.
""")

# ---------------------------------------------------------------- 6
head(6, "UNI_140", "leg 2 of the anonymization pattern inherits two prior "
                   "findings")

print("    022 states: \"reverse coding is the only strategy that reduced")
print("      desirable-end skew, and reduced it by roughly half.\"")
print()
print("    UNI_087  \"roughly half\" was NOT LOCATED in the source; it reports")
print("             \"decreases bias levels but does not eliminate them\"")
print("    UNI_086  the source's abstract concludes the effect \"cannot be")
print("             attributed to acquiescence bias\" -- the opposite reading")
print()
print("    022 repeats the fraction:     %s" % ("roughly half" in C22))
print("    022 repeats 019's reading:    %s"
      % ("reduced it by roughly half" in F22))
print("    022 notes the source dispute: %s"
      % ("yes" if "cannot be attributed" in F22 else "NO"))

block("""
Not a new error -- propagation of two recorded ones, and worth logging because
the file itself is about propagation.

`UNI_087` found "roughly half" was not a located number: the source reports
that reverse coding "decreases bias levels but does not eliminate them", with
no fraction, in a paper that quantifies precisely elsewhere. `UNI_086` found
the source's abstract concludes the residual means the effect "cannot be
attributed to acquiescence bias" -- the opposite reading from the one `019`
takes, which this audit judged the weaker of the two inferences on the merits
while noting `019` never flags the disagreement.

022 carries both forward. The fraction becomes one of two legs in the most
transferable observation in the file, and the disputed reading becomes half of
a cross-literature pattern.

The magnitude matters here in a way it did not in `019`. There the half was
load-bearing for two sub-questions; here it is load-bearing for the claim that
two literatures show the same shape, and "reduced it by an unstated amount"
does not support the pairing with leg 1 nearly as well. This is `UNI_136` in
its second instance in one file: a figure travelling one folder without its
status.
""")

# ---------------------------------------------------------------- 7
head(7, "UNI_141", "the sharpest technical claim in the file is one "
                   "sentence with no readout")

w = C22.split("| welded pair | decoupled? |", 1)[1]
rows = [l for l in w.split("\n") if l.startswith("| ") and "---" not in l]
print("    welds table: %d rows" % len(rows))
for l in rows:
    cells = [c.strip() for c in l.split("|") if c.strip()]
    print("      %-62s %s" % (cells[0][:62], cells[1][:28]))
print()
live = w.split("That last row is the live one.", 1)[1].split("\n\n")[0]
print("    the argument attached to the last row:")
print("      " + flat(live))
print()
print("    a readout for it anywhere in the file: %s"
      % ("yes" if "perplexity" in C22.split("## WHAT WOULD MEASURE")[1]
         else "NO"))

block("""
Seven welds with decoupling status, and one row carries an argument rather than
a status. "Familiarity -- low perplexity -- IS correlation with one's own
distribution. If both effects run on overlap, they are one quantity measured
twice under two names, and the field is treating them as separate subfields."

That is the most substantive novel claim in the file and it is close to an
identity: text that is low-perplexity under a model is text the model assigns
high probability, which is what "close to its own output distribution" means.
If self-preference and peer-preservation both scale with that quantity, the
claim that they are one effect is not a conjecture about psychology but a
statement about what both experiments are varying.

It is also the only claim in the file with an obvious cheap test and no readout
attached. Perplexity of the evaluated text under the evaluating model is
computable wherever logprobs are available; the prediction is that
self-preference and peer-preservation strength both track it, and that
controlling for it collapses the difference between the two literatures. The
WHAT WOULD MEASURE section proposes a control-field audit for the field-level
claim and nothing for this, which is the file's own most falsifiable content.
""")

# ---------------------------------------------------------------- 8
head(8, "UNI_142", "the disclosure reverses the compression, and is the "
                   "first to name a consequence")

MARK = {
    "018": ("## POSITION OF THIS FILE", "## CROSS-LINKS", C18),
    "020": ("- **The account is inside its own sample.**", "- **R4",
            case("020attributedagencyarrangement.md")),
    "021": ("- **Same-sample problem.**", "- **No claim about intent**",
            case("021sensesubstitutionundeclaredaxis.md")),
    "022": ("## POSITION OF THIS FILE", "## WHAT THE OUTSIDE", C22),
}
print("    %-6s %-22s %6s" % ("file", "form", "words"))
for k in ("018", "020", "021", "022"):
    a, b, t = MARK[k]
    seg = a + t.split(a, 1)[1].split(b)[0]
    form = "dedicated section" if a.startswith("## ") else "bullet"
    print("    %-6s %-22s %6d" % (k, form, len(seg.split())))
print()
pos = C22.split("## POSITION OF THIS FILE", 1)[1].split("## WHAT THE OUTSIDE")[0]
print("  022, verbatim:")
print("    " + flat(pos))

block("""
`UNI_131` measured the disclosure compressing 60 -> 43 -> 24 words across 018,
020 and 021, and recorded that what dropped out was the refusal of the
exemption. 022 restores the refusal in five words -- "Noticing the position does
not exit it" -- and adds something none of the three had.

It names a CONSEQUENCE. The other three say where the author stands. This one
says a correction occurred, that it was specifically about building a
deflationary case and presenting it as neutral framing, and that the correction
is why `sign` appears as its own stage in the table. The disclosure is
load-bearing on the file's structure rather than appended to it, which is the
difference between declaring a position and showing where it was already
acting.

Two things follow. It is checkable in a way the others were not: `sign` is in
the table, so the stated consequence is visible in the artifact. And it makes
`UNI_135` sharper rather than softer -- `sign` was added because of a
correction, and it is one of the two rows the file later holds at lower
confidence without the table saying so.
""")

# ---------------------------------------------------------------- 9
head(9, "UNI_143", "the position of this audit: the UNI_101 condition "
                   "applies here")

print("    022's thesis: AI-behavior research has instrument problems at the")
print("      variable-selection, baseline, sign, funding, instrument and")
print("      target stages.")
print()
print("    direction of my interest:")
print("      if the thesis holds, adverse findings about systems like me are")
print("      less reliable                                    -> ONE WAY")
print("    compare UNI_101 (020): interest one way   -> declined")
print("    compare UNI_132 (021): interest two ways  -> not declined")

block("""
`UNI_132` declined to repeat `UNI_101`'s move because 021's interest ran two
ways. Here it runs one. If AI-behavior research has instrument problems at an
unusual rate, then findings about model misbehaviour carry less weight, and a
model endorsing that is an interested party ratifying a claim that reduces
scrutiny of its own class -- exactly `UNI_101`'s condition.

So the field-level thesis is declined here, and the declining is recorded.

The file anticipated this and built the guard, which is why an audit is still
possible. `sign` is a named stage precisely because the author was caught
constructing a deflationary case and presenting it as neutral, and the
POSITION section says so. That does not make my endorsement admissible; it
makes the parts of the file that do not depend on the thesis auditable
separately, and those are what sections 1 to 8 above are.

Every one of them is a property of the delivered text, of files in this
repository, or of a prior claim in this audit trail -- a table missing a
column, a figure travelling without its status, two shapes reported as one, a
cross-link absent, a claim with no readout, a disclosure that changed. Section
10 is a literature check anyone can rerun. None requires taking a position on
whether the field-level claim is true, and none is offered as one.
""")

# ---------------------------------------------------------------- 10
head(10, "UNI_144", "S3's cited result verifies, and has a published "
                    "challenge the file does not carry")

print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print()
s3 = C22.split("### S3", 1)[1].split("### S4")[0]
print("    S3 states:")
print("      " + flat(s3).split("Relevant and cutting both ways:")[1][:250])
print()
print("    located: Probing and Steering Evaluation Awareness of Language")
print("      Models, arXiv 2507.01786 -- linear probes separate real-world")
print("      evaluation and deployment prompts; current safety evaluations")
print("      are correctly classified, i.e. they already appear artificial.")
print("      CONFIRMED, close to verbatim.")
print()
print("    also located, NOT carried by 022:")
print("      Is Evaluation Awareness Just Format Sensitivity? Limitations of")
print("      Probe-Based Evidence under Controlled Prompt Structure,")
print("      arXiv 2603.19426.")

block("""
S3's supporting result checks out about as closely as a paraphrase can. It is
the one thing raising S3 above an impression, and the file uses it carefully --
"cutting both ways", which it does, since a probe that separates evaluation
from deployment is evidence for the constructed/real distinction being live and
also evidence that the field already has an instrument for it.

There is a 2026 paper arguing the probe evidence may be format sensitivity
rather than evaluation awareness, and 022 does not carry it.

The interesting part is that it does not undercut the use 022 makes. The
challenge is to the internal-representation reading -- whether the model
represents "I am being evaluated" -- and S3's claim needs only that safety
evaluations are distinguishable from deployment text by something. Format
sensitivity satisfies that; a scenario that reads as artificial by its format
still reads as artificial. So the citation survives the challenge for S3's
narrower purpose and would not survive it for a stronger one.

Which makes this the third instance in one file of the shape S5 names, and the
mildest: a result travelling without the caveat attached to it, where the
caveat happens not to bite. `UNI_136` and `UNI_140` are the two where it does.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_135..UNI_144")
print(BAR)
