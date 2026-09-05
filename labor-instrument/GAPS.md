# GAPS — labor instrument

The work order posts three current gaps and one open item. They are landed
here **as posted, not filled**. Each needs data that does not exist in
joined/published form, and the sources that hold the pieces are egress-blocked
in this environment (allowlist; ALFRED, BLS, and general web hosts answered no
on CONNECT, probed 2026-09-05T14:02Z). Nothing is fabricated to close any of
them.

---

## GAP 1 — metabolic joules per occupational task class   `OPEN`

```
have    exercise physiology has metabolic cost data
lack    it is not mapped to work activities
need    joules per task class against an occupational task vocabulary
        (O*NET work activities is the obvious spine)
status  CURRENT GAP. not solvable from published data as it sits.
feeds   PART 2 joule denominator for the `human` class; the read-layer
        complementarity query needs it to place human operations on the
        cross-class output_per_joule axis.
```

## GAP 2 — insolation-captured to metal-recovered, hyperaccumulators   `OPEN`

```
have    plant science has uptake rates for rare-earth / metal hyperaccumulators
lack    they are rarely energy-normalized
need    recovered mass per joule of insolation captured, per species, per
        substrate concentration
status  CURRENT GAP.
feeds   PART 2 joule denominator for the `biological` / `plant` class. The
        money-vs-joule ranking-flip in labor_schema.py is a CONSTRUCTED
        demonstration precisely because this real number is missing.
```

## GAP 3 — compute joules per task-instance   `OPEN`

```
have    the labs hold this and mostly do not publish it
lack    joules per completed task-instance by task class
need    task boundary defined by output delivered rather than internal
        call count (see the open item below)
status  CURRENT GAP.
feeds   PART 2 joule denominator for the `compute` / `machine` class.
```

---

## OPEN ITEM — task-boundary definition (not a gap)

```
Boundaries are currently defined by the system's own architecture, so an
agent doing one thing in ten calls and one doing it in one call report
differently. The boundary must be defined by OUTPUT DELIVERED, not internal
steps. "Output delivered" still needs a definition that does not drift with
architecture. UNRESOLVED.

Bearing on the build: GAP 3 cannot be filled cleanly until this is settled,
because "joules per task-instance" needs a task-instance boundary that does
not move when the architecture changes. The schema records `output_delivered`
as a first-class field for exactly this reason, but the field's DEFINITION is
the open item, not the field itself.
```

---

## What is NOT gapped

The machinery is built and runs on constructed data: M1 vintage_store, M2
instrument_registry (seed carried, unverified), M3 decompose (the three-way
split with a band where the crosswalk is ambiguous), and the PART 2 schema
with its invariants enforced. What is gapped is the DATA that would fill them
— and the acceptance test (reconstruct the 2026-08-28 benchmark) is NOT
RUNNABLE here for the same reason: no ALFRED vintages, no QCEW, egress-blocked.
