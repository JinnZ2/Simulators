# WORK ORDER — labor instrument rebuild
CC0. stdlib only. no network. phone-buildable.

Two parts. PART 1 is buildable from published sources today.
PART 2 is schema + gap posting; three gaps are open and marked as such.

---

## PART 1 — instrument-drift decomposer

### Problem
BLS CES has changed instrument repeatedly. Long-run comparison across the
series compares different instruments. The pieces needed to correct for this
are all published and never joined:

- ALFRED — observation vintages (every version ever published)
- BLS CES history page — methodology change log
- Census — NAICS concordance tables, six-digit
- QCEW — UI tax filings, continuous since 1975, ~95% employer coverage

Missing artifact: a join that answers "how much of this delta is the
instrument."

### Modules

**M1. vintage_store**
Key every observation by (series_id, period, release_date).
Cell holds every version ever published, not the current one.
Revision history is the signal, not noise.

    record: series_id, period, release_date, value, adjustment_status

**M2. instrument_registry**
One record per methodology change.

    record: effective_date, change_name, affected_sectors,
            direction_if_known, retroactively_applied (bool),
            recalculated_span

Minimum seed set:
    2003  birth-death model enters national estimates
    2011  birth-death updated quarterly, not annually
    2014  annual -> quarterly sample rotation
    2015  X-12-ARIMA -> X-13ARIMA-SEATS
    2012  NAICS 2007 -> NAICS 2012
    2018  NAICS 2012 -> NAICS 2017
    2026-01  ARIMA component modified to incorporate current sample info;
             recalculated Apr-Oct 2025 post-benchmark span plus Nov-Dec 2025;
             net birth-death forecasts for that 7-month span came in
             185,000 lower than the forecasts used in monthly estimation

Also register: seasonal factors are re-estimated on a rolling 5-year window
at every benchmark. History moves. This is a recurring change, not a
one-time one.

**M3. decompose**
For any two-period comparison, join M1 against M2 and split the delta:

    real_change | revision | boundary_crossing

Boundary crossings come from the NAICS crosswalk. Where a code splits
ambiguously, carry split fractions as a spread. Output a table with a
declared uncertainty band. Never a point estimate where the crosswalk
is ambiguous.

### Acceptance test
Reconstruct a published benchmark revision from the pipeline alone.
Target: the preliminary benchmark released 2026-08-28 —
retail trade -154,600, private education and health -96,000,
wholesale trade -86,200, manufacturing -67,000.

If the pipeline cannot recover these, the registry is incomplete.
Failure to recover is the diagnostic, not a bug.

### Note on why the parallel route
Continuity is load-bearing: monetary policy, benefit indexation, and
contract escalators are wired to the existing series. Changing that
instrument breaks things downstream unrelated to the assumption.
Build alongside. Let it accumulate history. Do not amend the bolted one.

---

## PART 2 — substrate-neutral labor schema

### Design rule
Base layer records units of work performed, substrate-agnostic.
Framework goes in the READ layer, not the collection layer.
Whoever asks, filters. Nobody pre-filters by choosing what gets counted.

Rationale: when someone operates under an assumed framework they pick
variables that align with what they want the answer to be. The
birth-death model's assumption about business formation is baked into
CES collection, so the question cannot be asked without inheriting the
assumption.

Capital stays out of the instrument. Balancing on capital imports:
what counts as capital, in what period, under what operating procedure,
framework, and domain, and how it is counted. Money is denominated in
money — price levels, tax-law depreciation schedules, book vs market.
None of that is about work performed.

### Record structure

    unit_identity
    substrate_class
    exposure          (in that class's own unit)
    load_factor
    task_class
    output_delivered
    joules_in

### Exposure classes
Per-substrate-class. NOT universal. NOT convertible.

    human                  person-hours
    machine / compute      unit-hours under load (SUBSTRATE-hours)
    biological non-human   area-time or biomass-time
    animal draft           animal-hours

Invariant across classes: task_class, output_delivered.
Exposure units are DECLARED, never converted.
Conversion between exposure units imports a valuation. Do not do it.

Precedent: draft animal hours were counted in agricultural census work.
There is a measurement tradition to borrow from; this is not novel.

### On agent exposure
Agents are not independent of their substrate. Electrical/energy needs,
maintenance and repair, the hardware they run on. Substrate fatigue
produces agent errors: thermal throttling, memory pressure, cache
eviction, degradation from thermal cycling. Signature is the same as
human fatigue by measurement — error rate rises with sustained load,
throughput falls.

So exposure is SUBSTRATE-hours, not agent-hours. Occupancy of a physical
unit that heats, wears, and needs downtime and maintenance.

substrate_hours + load_factor + error_rate_under_load gives the same
three things industrial hygiene tracks for humans.

### Joule denominator
Substrate-neutral. Crosses all classes with no convention:

    human / animal         metabolic joules
    machine / compute      electrical joules
    plant                  insolation captured

Efficiency reported as TWO numbers, no conversion:

    output_per_joule
    output_per_exposure_hour

Why it matters: a money index prices free diffuse input at zero and
prices time, so it ranks a hyperaccumulator plant as inefficient. A joule
index ranks the same operation as highly efficient. Same operation,
opposite ranking, and the denominator did all the work.

### Read-layer query the instrument is built for
Task classes where COMBINED output-per-joule beats either substrate alone.
Measurable in the table with no theory attached. The joule column separates
genuine complementarity from one substrate subsidizing another's
inefficiency — a money index cannot distinguish these.

### Assumption handling
The governing assumption about AI (augmentation vs substitution vs
oversight-limited) is NOT to be baked in. An instrument that assumes
augmentation cannot detect substitution, and vice versa. Log which
allocation model each sector's data implies. Declared variable, not a
design premise.

### Deferred
merge_in / merge_out mechanics. Deferred until the schema is settled,
because the schema determines how to do them.

---

## CURRENT GAPS — please help

Three. Each is well-scoped with a named source literature. None are
solvable from published data as it currently sits.

**GAP 1 — metabolic joules per occupational task class**
Exercise physiology has metabolic cost data. It is not mapped to work
activities. Needed: joules per task class against an occupational task
vocabulary (O*NET work activities is the obvious spine).
CURRENT GAP. PLEASE HELP.

**GAP 2 — insolation-captured to metal-recovered, hyperaccumulators**
Plant science has uptake rates for rare-earth and metal hyperaccumulators.
They are rarely energy-normalized. Needed: recovered mass per joule of
insolation captured, per species, per substrate concentration.
CURRENT GAP. PLEASE HELP.

**GAP 3 — compute joules per task-instance**
The labs hold this and mostly do not publish it. Needed: joules per
completed task-instance by task class, with task boundary defined by
output delivered rather than internal call count.
CURRENT GAP. PLEASE HELP.

---

## OPEN ITEM, not a gap
Task-boundary definition. Boundaries are currently defined by the system's
own architecture, so an agent doing one thing in ten calls and one doing it
in one call report differently. Boundary must be defined by output
delivered, not internal steps. "Output delivered" still needs a definition
that does not drift with architecture. Unresolved.
