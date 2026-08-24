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

## Nothing here rests on a source yet

Twenty-two sources: five located, seventeen untouched, none extracted. Every
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
