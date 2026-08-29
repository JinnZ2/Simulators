# dependency-ledger

A method for testing reconstruction claims by propagating them to
conserved quantities and checking closure against independent records —
**built as an instrument and run on one case, as the drop asks.**

`SOURCE_DROP.md` is delivered verbatim. `audit.py` is the method;
`selftest_audit.py` is 63 checks; `samples/` is the pinned run.

    python3 dependency-ledger/audit.py             # the report
    python3 dependency-ledger/audit.py --case watercraft-propulsion
    python3 dependency-ledger/audit.py --selftest

**Step 5 is CHECK against an INDEPENDENT record, and egress here is an
allowlist that refuses every archive.** So on the real case every
record-bounded cell comes back `UNMEASURED`. That is the run, not a
workaround, and it is the finding the drop predicted: *"The unmeasured
cells are the finding."*

## The run

    CASE: watercraft-propulsion   [REAL RUN]

    requirement                        bound   residual   verdict
    shaft_power_per_rower              LAW     8.71       GAP
    hull_drag_coefficient_at_loading   RECORD  --         UNMEASURED
    timber_volume_for_hull             RECORD  --         UNMEASURED
    crew_daily_calories                RECORD  --         UNMEASURED
    oar_replacement_rate               RECORD  --         UNMEASURED

    LAW      1 cell,  0 unmeasured
    RECORD   4 cells, 4 unmeasured

    MISSING COMPONENT SPEC
      subsystem     : oar / hull / load-distribution system
      required perf : 871.2 W
      constraints   : period materials, river reach, displacement D
      reachable?    : OPEN -- separate investigation

**The one cell that closes is the one whose independent record is
physiology rather than archaeology.** Sustained human mechanical output
is reachable from anywhere; granary capacity is not. And it closes as a
`GAP` — the drop's own predicted outcome for its own worked example.

**The residual is 75% built from unsourced coefficients** — six of
eight, each carrying a stated reason, including the oar propulsive
efficiency, *"exactly the one the reconstruction assumes without
stating."* It is a demonstration that the propagation runs, not a
measurement about any vessel, river, or period, and the
`SMUGGLED_CONSTANTS` guard prints the share in every report so the
number cannot be quoted without it.

`TIME AS SOLVENT` fires and is **left firing**: a 30-day duration
enters the propagation with nothing bounding it, and bounding it
requires occupation layers this environment cannot reach.

## The addition: LAW vs RECORD

Derived from running the method, not from reading it. **Steps 3 and 4
pull opposite ways.**

Step 3 says stop at conserved quantities — energy, mass, momentum,
time, material volume. Those are bounded by physical **law** and are
checkable from anywhere. Step 4 says expand each into its dependency
set — arable area, quarry volume, spoil heaps, pollen records. Those
are bounded by the **record** and are checkable only with archive
access.

The propagation crosses between the classes and the spec gives one
procedure with no marker for where it changes character, so a reader
cannot tell which cells they could have closed at a desk and which
required an excavation. Every terminal requirement here declares
`bound_by ∈ {LAW, RECORD}`, `close()` refuses one that declares
neither, and the table is split on it. The run above is that split
appearing as a property of a run rather than a distinction argued for.

## Three things the spec leaves open

**`residual = required / attested` is a ratio and nothing requires the
two to be the same quantity.** Step 4's own example propagates a
requirement in kcal/day toward a record in hectares. `G-DIM`. Enforced:
mismatched or undeclared units yield no residual and land on
`UNMEASURED`, with the units check saying which.

**`residual >> 1` has no value.** Declared as `FALSIFY_AT = 10.0` and
printed in every report. The watercraft case lands at **8.71**, so it
reads `GAP` — and at `FALSIFY_AT = 8` it would read `FALSIFIED`. The
verdict on the drop's own worked example sits inside the range one
undeclared symbol spans.

**Duration's independent bound is itself a measurement with a
resolution.** `TIME AS SOLVENT` fires on an unbounded duration and also
on a bound *coarser than the duration it bounds*, which cannot
constrain it — a `G-RES` pair the spec's prose implies and does not
state.

## What the spec gets right

**`attested undefined → NOT a pass`** is the absent-vs-known-negative
repair, stated before any code, on the field where it costs most — and
given its own named failure mode, so it is both a schema rule and a
guard. No other instance in this repository has been both. Implemented
three ways: `residual()` returns `None` never `0`, `verdict(None)` is
`UNMEASURED`, and an `attested` of literal **zero** is *refused*,
because a zero denominator is not a residual and is a different
statement from an absent one.

**"Do not aggregate residuals into one score"** is `domain-ledger`
`DL_001`'s no-composite discipline arrived at independently, and this
statement of it is better because it gives the reason: a mean over
subsystems names none of them. Enforced rather than instructed — the
selftest walks the AST asserting no residual is ever summed, maxed, or
averaged.

**COLLAPSED PROXIES is `fold-matrix`'s folded term.** That register
opens by defining one as *"a compact matrix wearing the costume of a
scalar"* and already carries `resources` — *"a stock and a flow,
welded"*. The guard **imports** the register rather than retyping it.

**The output is a specification, not a verdict**, and `reachable?` is
left open as a separate investigation. That converts *"knowledge was
lost"* into a search target, which is the drop's best move.

## What the run found in my own instrument

`guard_collapsed_proxies` tokenised names with `re.findall(r"[a-z_]+",
name)`. The underscore is **inside** the character class, so
`labor_required` is a single token, `labor` never appears, and the
guard returned `fired: False`. The guard whose job is to catch a term
hiding inside a name could not see a term inside a name — `UNI_009`'s
shape, in a tokenizer written after that finding was recorded. Caught
by the selftest arm requiring every guard to fire on a planted
violation.

## Files

| | |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim |
| `audit.py` | the method: propagation, three-valued closure, the LAW/RECORD split, five guards, the missing-component spec |
| `selftest_audit.py` | 63 checks; every guard null-tested both directions |
| `cases/` | one real run and two constructed, labelled in their own text |
| `CLAIM_TABLE.md` | `DLA_001..DLA_010` with a REFUTATION_PROTOCOL |
| `samples/` | pinned run |

The two constructed cases exist so the closure test can be shown to
return `SATISFIED` and `FALSIFIED` — without them a run of
all-`UNMEASURED` would not show the instrument can say anything else.
All four verdicts occur across the corpus and the selftest asserts it.

Stdlib only, parses under Python 3.9, phone-buildable, CC0.

Siblings: `fold-matrix/` (the folded term COLLAPSED PROXIES names, and
the imported vocabulary), `domain-ledger/` (`DL_001`, no composite),
`reasoning-gate/` (`G-DIM` at the residual, `G-RES` on the duration
bound), `gap-markers/` (record gaps as locations rather than findings),
`investigation-sim/` (`CALCULATED_UNCLOCKED` — a figure whose
conditions did not survive it).
