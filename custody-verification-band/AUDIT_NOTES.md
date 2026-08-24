# AUDIT NOTES — custody-verification-band

What is not established, written down before it can be forgotten.

## A finding of mine that did not survive its own data

The six invented SEED cases are gone, replaced by eleven real ones. With them
went `B4`. Over the seeds, the two-cut criterion and the full-cut reading
disagreed in both directions; over the eleven, they agree on every case. Two
of those six seeds had been written specifically to disagree, and the note
attached at the time said a constructed disagreement shows the instruments CAN
differ, not that they differ on anything real. That caveat was correct and the
finding it guarded is withdrawn.

The lesson is narrower than "seeds are bad": a fixture written to exercise a
rule will exercise it, and the result is a statement about the fixture. The
selftest now asserts the zero-disagreement result over the real corpus, so the
withdrawal cannot silently reverse.

## Why the omission costs nothing, which is the actual finding

`parallel_path` is a deterministic function of `custody` across all eleven
cases: `routed→no, mixed→partial, self→yes`. It carries no information custody
does not already carry, which is why a criterion that omits it loses nothing.

Undetermined whether that is a real regularity or the same judgement entered
twice under two names. `gaps.md` G-COLLINEAR states what separates them: a
case coded by someone who has not seen the custody column, or any case with
routed custody and a working parallel path. `extract.py check` reports the
collinearity every run.

This is the third time in this ecosystem that a folder's instrumentation has
carried a field with no discriminating power — after the readout baths in
`qrng-pair-search/` and the one-slot structural score in the shape-index. The
shape is the same each time: a quantity that does not vary independently looks
like rigour and adds nothing.

## Three defects in the delivered reader, named before fixed

    1. PHYSICS_REFS carry `extract` as a STRING. `for e in it["extract"]`
       iterated it per character; all five sources rendered as one letter
       per line.
    2. ARCHAEOLOGICAL items carry `measure`, not `extract`. The reader looked
       only for `extract`, so five sources printed titles and no content.
    3. `--custody self` substring-matched, so `self -> routed` answered to
       `self`. Four of six hits were conversion cases — systems that are no
       longer self-custodied. The filter returned the opposite of its
       question.

All three reproduced on the delivered data before being changed. Fixed by
normalising content across both keys and by parsing `a -> b` into a state
pair, so `--custody` reads the current state and `--was` reads the origin.
`table` marks transition rows with `>`.

## LIVE_CULTURES is a different corpus and the status vocabulary does not fit it

Seven sources added under a group whose method is observation, not reading:
practice still executing under current conditions. The status vocabulary —
`untouched / located / partial / extracted / dead_end` — is reading-shaped.
"Extracted" does not name what happens when you observe a system that is
still running, and nothing in the schema distinguishes a source you can read
from one you would have to go and watch. Left unfixed and recorded: the
vocabulary failing visibly is worth more than a term invented from one group.

The group carries two group-level keys the reader could not print —
`seed_bank_framing` and `strip`. Same defect class as the `measure` key: prose
attached to the data and invisible to the tool that reads it. `queue` now
prints every group-level key rather than only `why`.

## Gap coverage is thin and now counted

    4 of 9 gaps have a source pointing at them

    G-KNOWLEDGE-STATE   no source; its measures are residue, and residue
                        sits where nothing was logged
    G-SLACK             no source; measurable with current data, per its own
                        entry, but nothing in the corpus is aimed at it
    G-THRESHOLD         no source, and no candidate observable — uncoalesced
    G-REPAIRABILITY     S04 is aimed at case C08 but carries no for_gap link
    G-COLLINEAR         no source; it is a question about the coding, not
                        about the world, so it may never have one

`extract.py check` resolves every `for_gap` reference against the headings in
`gaps.md` and reports the uncovered gaps, so a gap cannot quietly acquire or
lose its evidence.

## G-COLLINEAR nearly vanished

The delivered `gaps.md` did not carry it. It came from the data rather than
from the drop, so it was re-appended rather than dropped, and a selftest now
asserts it is present. A gap that came from measurement should not be removed
by a document that predates the measurement.

## SHAPE_SPEC section 2 describes B7 verbatim

"Branching form applied to a system with no flux and no dissipation term looks
like insight and carries no information."

`branching.py` computes area-preserving and space-filling ratios and contains
no flux term and no dissipation term. It is pure geometry. Under SHAPE_SPEC
section 1 the shape is the constraint set and the geometry is only its readout,
so nothing in this folder licenses the step from vessel branching to economic
layers — the geometry was ported without checking whether the constraints came
with it.

Section 4 supplies the test this claim was recorded as lacking: name the
constraint whose removal changes the geometry, find a case where it is genuinely
absent, check the form differs. Not run. Section 4 also says a failed transfer
is a measurement rather than an embarrassment, so running it and getting a
different form would be output, not a retraction.

Section 9's note on cost lands on nothing here: the dissipation/enclosure group
is not computed in this folder, so there is no cost framing to replace. That is
the same absence stated from the other side.

## Nothing here rests on a source yet

Twenty-nine sources: five located, twenty-four untouched, none extracted. Every
case is a structural reading with a confidence and an `evidence_needed` list,
not a claim resting on the corpus. `extract.py check` prints the counts and
the open data problems every run.

## Two anchor labels named the wrong quantity

Recomputed in `branching.py`:

    delivered   "area-preserving junctions, r_ratio = 2^(-1/3) ~= 0.794"
    measured    2^(-1/3) = 0.7937 is the SPACE-FILLING LENGTH ratio, or
                equivalently the Murray's-law RADIUS ratio. The
                area-preserving radius ratio is 2^(-1/2) = 0.7071.

    delivered   "area-preserving ... => aggregate cross-section WIDENS
                every generation"
    measured    n*beta^2 = 1.0000 exactly under area preservation. Constant,
                by definition of the name. It widens by 2^(1/3) = 1.2599 per
                generation under Murray's law.

The values are real and correctly stated; what they are attached to is not.
Both regimes are present in real vasculature — area-preserving in large
vessels, Murray-like in small ones — so this is two regimes crossed, not a
number pulled from nowhere. The 3/4 exponent still falls out, and needs both
ratios: one number cannot stand for both, which is what the anchor block asked
it to do.

The conclusion the anchor was carrying, "trunk never wins by construction",
survives in the Murray regime and is neutral in the area-preserving one. The
route to it was wrong; the destination was not.

## The transfer is the unmeasured step, not the physics

`B7` in the claim table. The branching arithmetic is checked and reproduces.
Nothing in this folder licenses the step from vessel geometry to economic
layers, no measurement is proposed for it, and it is the largest unsupported
move in the folder. It is recorded as a claim with no falsifier rather than
carried implicitly inside the anchor block, where it reads as physics.

## The criterion reads two of five cuts

Not necessarily wrong — three may be diagnostics rather than criteria. It is
decidable, and `extract.py` computes the decision rather than arguing it.
What is not decided is which reading is correct: whether the three unread cuts
are missing conjuncts or gauges that should not gate. `gaps.md` G-CUTS states
what would settle it.

## Confidence numbers are carried, not resolved

Each case states a confidence between 0.3 and 0.6. These are taken as given
and are neither argued up nor discounted anywhere in this folder. They are not
combined into an aggregate, because averaging confidences over cases that are
all SEED would produce a number about the author's certainty and nothing about
the world.

## Q-PORT cannot be tested by the current case set

Every SEED case bundles proximity with verification, so none of them
distinguishes the two. The highest-priority open question has no case that
bears on it. That is the first gap to close and it is a data problem, not a
schema problem.
