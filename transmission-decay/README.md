# transmission-decay

An undergraduate-scale design for the decay rate of transmitted hazard
knowledge — at what generational distance an account shifts from
**mechanism** (actionable causal structure) to **story** (narrative
retained, causal structure lost).

`SOURCE_DROP.md` is delivered verbatim. `scheme.py` parses the M1–M8
coding scheme; `power.py` computes what one valley delivers;
`selftest_power.py` carries the checks; it prints its own count.

    python3 transmission-decay/power.py             # the report
    python3 transmission-decay/power.py --selftest

## This is the scheme the sibling folder was missing

`revision-mechanism` `RM_008` recorded M1–M8 as named, absent, and
**not reconstructed**, with the falsifier *"the companion study
landing."* It landed. That claim is now CLOSED and the scheme is
**imported** across, so the two cannot drift.

**The arrival is what shows the refusal was right.** The delivered
components are hazard-specific — *routing correct*, *precursor signs*,
*chained consequence* — a set no reasonable invention would have
produced, and every number keyed to an invented scheme would have been
about the invention.

## Not run, not simulated

The study needs fieldwork and collective consent, and its own ethics
section says *"A study that extracts a decay rate while accelerating
the extraction is self-defeating."* Nothing here models a valley, an
informant, an account, or a transmission chain. The only objects in
`power.py` are abstract retention probabilities and binomial noise.

The `M7` note binds harder still — *"the ACTION components may be more
sensitive than mechanism ones — do not assume publication is
neutral"* — and nothing here contains or invents an action rule.

## What is computed

**The most useful output is the expensive form of the question.** The
drop calls component order *"the most useful output"* and then asks two
questions that are not orderings: *does M7 outlive M3*, and *does M8
drop first*.

    n      full 8-order   M8 first (1 v 7)   one named pair
    5      0.000          0.360              0.754
    10     0.000          0.570              0.867
    20     0.007          0.753              0.919
    40     0.060          0.883              0.959
    80     0.167          0.960              0.997
    160    0.360          0.997              1.000

The full eight-component order is out of reach at any plausible
one-valley sample — 0.7% at twenty informants per chain position,
still about a third at a hundred and sixty. *"M8 drops first"* is one
component against seven, so seven comparisons must land, and it costs
around forty. **A single named pair — the form both headline questions
take — is affordable at ten to twenty.**

Actionable version: ask the pairs, report the ordering as unresolved,
and state which pairs were decidable at the n obtained. A twenty-point
retention gap between two named components decides at ten to twenty; a
ten-point gap takes eighty.

The retention profile behind the table is **arbitrary and declared**.
It is not a prediction about any component, because which component
drops first is the design's output.

**The half-life's resolution follows from the axis, not the sample.**

    levels                C0, C1, C2, C3+
    ordered positions     3
    open catch-all        C3+
    finest statement      "between C0 and C1"

Four levels give three intervals. A half-life read off this axis names
an interval and cannot be finer, whatever the sample size —
`reasoning-gate`'s `G-RES` with a half-life as the feature and a
four-point ordinal scale as the instrument. So `halflife_bracket()`
returns a bracket and **never interpolates**: chain position is
ordinal, and a value between C1 and C2 asserts a metric the design
does not define.

**And `C3+` is not a position.** C0–C2 count hops from a witness; C3+
is *"no traceable chain to a witness"* — the **absence** of a chain
position. An informant with four traceable hops and one with no
traceable chain both land there, and only the first is a distance. A
curve fitted across all four assigns coordinate `3` to a category that
has none. Cheap fix: fit C0–C2 and report C3+ as a separate stratum,
or split it — a lost chain and a long chain are different losses, and
that split is what the design's own `OUT-MIGRATION SURVIVORSHIP` point
needs.

## `M3` vs `M7` is asked twice, under two pressures

This study asks whether the **action rule outlives the mechanism**
under transmission decay. `revision-mechanism` comparison 3
**predicts** the opposite ordering under environmental change, and
names the reverse as the failure mode worth warning about.

Same pair, same scheme, two different selection pressures — and
neither document says whether the same ordering is expected under
both. There is no reason it must be: a component can be easy to
transmit and fragile under change. If `M7` outlives `M3` under
transmission *and* `M3` outlives `M7` under change, the two pressures
select oppositely on one pair, which is the most interesting outcome
available from running both, and neither design frames it as a
prediction.

## What the design gets right

**Two absences designed in.** *"Absence of C2/C3 informants is data,
not a sampling failure"* is the absent-vs-known-negative repair on the
sample. And `LANGUAGE AND REGISTER` is the same repair on the coding:
the drop says outright that `S1` conflates *no mechanism present* with
*mechanism present in a form I cannot read*, names it the largest
threat to validity, marks it not fully removable, and gives both the
remedy and what to do without one. Naming your own largest validity
threat and declining to claim it solved is rare.

**Chain position, not age.** *"A young informant who heard it directly
from a surviving witness is C1. Coding by age measures schooling, not
transmission."* The confound is designed out of the sampling frame
rather than controlled for afterward.

**The x-axis comes from outside.** Event dates from an independent
record, so the axis does not rest on any informant's dating — which is
the same move `investigation-sim` needed and `revision-mechanism`'s
`CHANGE AS FRAME` makes explicit.

## One cost worth stating

*"Correctness is checked against the instrumented record"* is the right
rule against the interviewer, and it makes the **physical channel the
arbiter of the knowledge channel** — the exact asymmetry the drop
opens by naming. A component the record has no field for scores as
incorrect, and `M8` (chained consequence) is the most exposed, because
process coupling is what `gap-markers` `SCR-05` records the hazard
literature as splitting on origin rather than behaviour. Cheap
addition: code *not in the record* as a third value alongside correct
and incorrect — the same third state `S1` and the empty strata already
get.

## Files

| | |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim |
| `scheme.py` | M1–M8, S1–S3 and C0–C3+, parsed from the drop |
| `power.py` | the half-life resolution, the three question forms and what each costs |
| `selftest_power.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `TD_001..TD_008` with a REFUTATION_PROTOCOL |
| `samples/` | pinned run |

Stdlib only, parses under Python 3.9, deterministic, CC0.

Siblings: `revision-mechanism/` (the companion, which imports the
scheme from here), `null-harness/` (the invariant behind the
stable-environment argument), `gap-markers/` (`SCR-05`, classification
splitting on origin rather than behaviour), `observer-exclusion/`
(survivorship in a transmission record), `investigation-sim/`
(`IS_001`, an x-axis that must come from outside the sample).
