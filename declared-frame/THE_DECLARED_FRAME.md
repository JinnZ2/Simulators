# The Declared Frame

Delivered document, verbatim. Analysis in [`README.md`](README.md) and
[`CLAIM_TABLE.md`](CLAIM_TABLE.md); the runnable check on the checker is
[`frame_audit.py`](frame_audit.py).

---

A six-field block to attach to any measurement, model, or claim.

CC0-1.0.

This is a marker — an idea being tested for fit, not a position under
defense. Test fit, extend it, or report where it breaks.

## Why

A result does not carry a frame-free number. A boundary was drawn, a horizon
was set, a sign convention was chosen, a formal system was used. All four
happened. In most reporting, none are stated.

The consequence is not bias. It is that frame disagreements get argued as
data disagreements, and they are unresolvable in that form, because the thing
in dispute was never in the numbers.

The fix is not to remove the frame. That is not available. The fix is to
declare it, so that two results become comparable-or-not mechanically rather
than by argument.

## The block

    frame:
      boundary:         what is inside the accounting
      horizon:          over what time the outcome is scored
      who_counts:       whose outcomes enter the total
      sign_source:      where "better" was set, and by whom
      logic:            which formal system
      observer_access:  unknown | partial | verified

## Field notes

**boundary** — Name what is inside and what is outside. Inputs, disposal
paths, maintenance, fabrication. A ratio that compares a closed budget to an
open one is a void ratio; declaring the boundary is what makes that visible.

**horizon** — The interval over which the outcome is scored. A configuration
optimal at one horizon is routinely pessimal at another. Horizon is not a
detail of the method, it is a term in the result.

**who_counts** — Whose outcomes enter the total. Individuals, a population,
a species, a system, downstream parties, future ones. Unstated, this defaults
to whoever commissioned the measurement.

**sign_source** — Where the outcome column's sign was set. "Better" is a
convention. It came from somewhere. Name it.

**logic** — Which formal system. Classical/Aristotelian, intuitionistic,
paraconsistent, fuzzy, relevance, modal. These are internally consistent and
disagree on which inferences are valid. No meta-system ranks them from
outside; the choice is fit-to-domain. Bivalence is the common default and is
a poor fit for graded states, for systems where measurement participates, and
for contradictory evidence held without collapse. A mismatch there gets
reported as lack of rigor rather than as mismatch.

**observer_access** — Whether the observer's own state and position were
checked, partially checked, or not at all. The neutral observer requires a
view with no boundary, no horizon, and no sign convention. A claim to it is a
frame with those set and not reported.

## UNKNOWN is a legal value

This is the load-bearing rule.

    unpopulated field  → visible gap, explorable
    omitted field      → invisible, reads as absence

Writing `unknown` costs nothing and preserves the gap as a place someone can
work. Omitting the field converts an open question into a settled one by
silence.

Never populate a field by inference to make the block look complete.
`unknown` is the correct entry for anything not measured.

## Comparability

Two results with declared frames can be checked mechanically:

    same boundary, same horizon, same who_counts
      → directly comparable

    differ on any of the three
      → not comparable as stated. The difference between
        them is a frame difference, not a finding.

    differ on logic
      → the inferences drawn from each are valid in
        different systems. The data may still compare;
        the conclusions do not.

    any field unknown on either side
      → comparability is undetermined, not false.
        Flag, do not resolve.

## Cost

Keeping the fields open costs more than not. The cost is fixed.

The cost of a narrow frame is conditional on the rate at which the world
departs from the frame's assumptions. That rate is usually assumed rather
than measured, and usually assumed from a period when it was lower.

As the change rate rises, the narrow frame gets more expensive while the
declared one does not. Whether the crossover has been passed in a given
domain is an empirical question that mostly has not been asked, because
efficiency was scored under an assumed rate nobody re-measured.
