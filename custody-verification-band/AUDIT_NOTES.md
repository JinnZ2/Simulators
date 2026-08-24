# AUDIT NOTES — custody-verification-band

What is not established, written down before it can be forgotten.

## Nothing here is evidence

Six cases, all SEED. Four sources, none read. No case CITED. The SEED cases
are structural placeholders written to exercise the criterion, and two of them
(`owner_operator_trucking`, `cooperative_member`) were written specifically to
disagree with it. A constructed disagreement shows the two instruments CAN
differ. It does not show they differ on anything real. `extract.py` prints the
seed and unread counts on every run so the state cannot drift out of view.

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
