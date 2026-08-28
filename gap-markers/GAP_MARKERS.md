# GAP MARKERS

CC0. No rights reserved.

Marked gaps in hazard assessment, infrastructure evaluation, and disaster
response capability. Each entry records a place where a quantity is not
measured, a question is not asked, or an interface is not owned.

A marked gap is not a finding. It is a location.

---

## SCHEMA

Each gap entry carries these fields:

    GAP_ID          stable identifier
    DOMAIN          field(s) the gap sits between
    STATE           uncounted | unasked | unowned | assembly | undated
    WHAT_EXISTS     the instruments, data, or capability that ARE present
    WHAT_IS_MISSING the specific absence
    ENTRY_POINT     cheapest available first query, where one exists
    KIND            knowledge | boundary-artifact

### STATE values

    uncounted    population has no inventory; no bound in either direction
    unasked      data exists, collected for another purpose; question never posed
    unowned      every party competent, interface inside no party's scope
    assembly     all components present in separate literatures, never combined
    undated      record exists but currency unknown; a date field answers it

### KIND values

    knowledge          the physics or the measurement is genuinely not known
    boundary-artifact  known, but partitioned by budget, liability, or
                       jurisdiction, so no instrument spans it

KIND is the load-bearing distinction.

A boundary-artifact gap exists because of how institutions divide funding
and liability. Those divisions are contingent. They are not physics, and
there is no reason for a later system to inherit them.

A knowledge gap is a real absence and survives any reorganization.

Most entries here are boundary-artifact.

---

## READING RULE

Before treating any partition in this material as a constraint, sort it:

1. Does the boundary encode failure knowledge — a method that was found
   not to transfer, a correlation that breaks off its calibration range,
   a sampling assumption that does not hold? KEEP IT.

2. Does the boundary encode who pays, who is liable, or who holds
   jurisdiction? DO NOT INHERIT IT.

Both look identical from outside. The content differs.

---

## STANDING CAUTION

The following hold across all entries:

- Absence of a count is not evidence of a small population.
  "No one has a good idea of the extent" does not license "probably small."
  An uncounted population is unbounded in both directions.

- Design cases here are single-variable return periods estimated from
  short records under a stationarity assumption. They do not encode joint
  probability across hazard domains. A compound event is outside the frame,
  not outside the physics.

- Cost framing terminates branches silently. A variable priced out of an
  objective does not appear as a missing variable; it appears as a
  question already settled. Closed branches do not announce themselves.

- A correct output that contradicts an incentive is indistinguishable
  from an error to whoever checks it against the accepted result. The
  correction pressure runs one direction. Over enough cycles the pattern
  is not suppressed — it is not generated. There is no residue.

---

## INDEX

    gaps/substrate.md        ground, fill, water, deposition, voids
    gaps/structures.md       dams, bridges, dual-function assets, underground
    gaps/transport.md        rail, barge, air, road, staging
    gaps/capability.md       fabrication, response cadre, matching, stockpiles
    gaps/screens.md          computable screens not run; date fields not queried
