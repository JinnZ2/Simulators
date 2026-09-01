# WORK ORDER 03 — Archive encoding cluster

Renders the M-A..M-E cluster from `MARKERS_HELD.md`.

Read `MARKERS_HELD.md` first. It carries the full development,
the source verifications, and the hold reasons. This file says
what to build from it and in what order.

Ordering rule for this work order, non-negotiable:
**the mechanism is rendered first and the instances render
under it.** These are not five sibling gaps. Filing them flat
loses the only thing that makes them a body of work.

Depends on: WORK ORDER 01 Task 3 (decision-gap entry type)
for Task 3 below. Independent of WORK ORDER 02.

---

## TASK 1 — Render the mechanism

```
source      MARKERS_HELD.md, M-A
folder      uninstrumented/
type        MECHANISM  (not a gap — it is an exclusion mode)
state       n/a, this is a named mechanism
```

Render M-A as an exclusion mechanism entry alongside the
existing eight in `uninstrumented/`.

Required content:

```
  the transform statement:
    a variable an institution cannot admit as a CAUSE
    reappears in its records as a COST, a PENALTY, a
    LANDMARK, or a PROOF OBLIGATION

  the four-archive table exactly as in M-A
    (Signal Service / Star Route / Homestead / Wells Fargo)

  the two-mechanism split, stated plainly:
    held-constant       -> nobody looked, data does not exist
    liability-displaced -> data exists under another name,
                           recoverable
    opposite implications; must be separated before any
    absence claim is made

  the join key: same place, same date, different encoding
```

Cross-reference to `unrecordable-by-construction`. That marker
covers material that cannot enter a record at all. M-A covers
material that enters in transformed form. Related, not the same
— state the difference in one line, do not merge them.

DO NOT generalize M-A beyond the four documented archives.
Four rows is what has been verified. The candidate list in M-E
is a candidate list.

---

## TASK 2 — Render M-B as a gap under the mechanism

```
source      MARKERS_HELD.md, M-B
folder      uninstrumented/  (with the mechanism)
type        GAP
class       EMPIRICAL
state       NOT_STUDIED
```

Attribution note for the renderer: the fine-as-threshold
reading is Kavik's. It is not in the literature. Render it as
a proposed instrument, not as a reported finding.

Render with all of the following intact:

```
  the calibration argument — why the operator is a
  better-calibrated sensor than a fixed-scale gauge
  for the question of passability

  the signal: fines per route per month, seasonal cycle
  vs anomaly; spatial clustering across adjacent routes
  draws the event footprint

  the placement argument: star routes are BY DEFINITION
  off the rail lines, so this maps where the Signal
  Service is not

  BOTH complications, as design requirements not caveats:
    excused vs unexcused = two thresholds, agency's and
      operator's. Do not collapse.
    enforcement regime (contract churn, 1870s star route
      scandals) = covariate, must be modeled

  the validation path: fine anomalies vs Signal Service
  station records on nearby routes, same months. Agreement
  calibrates the series; a calibrated series is then usable
  on the routes with no station.
```

Falsifier, to be stated explicitly in the entry:

```
  fine anomalies show no relationship to independently
  recorded conditions on routes where both exist, once
  enforcement regime is controlled.
```

PRECONDITION to put on the page, not buried: star route
contract registers have a coverage gap across 1877-1890
(registers exist 1828-1870 and 1917-1960). Contracts and
correspondence survive. **What survives for the window must be
verified at NARA RG28 before anyone designs against it.**
Write this as step zero of the method, not as a caveat.

---

## TASK 3 — Render M-D as a gap under the mechanism

```
source      MARKERS_HELD.md, M-D
folder      uninstrumented/  (with the mechanism)
type        GAP
class       EMPIRICAL
state       NOT_STUDIED
```

State the NOT_STUDIED cleanly: every located use of homestead
proving-up files is genealogical or family-history. Not tried
and failed. Not pointed at.

Required content:

```
  what the files hold: wells dug, crops planted, trees
  cleared, fences built; claimant testimony plus two
  witness affidavits; sworn, dated, at legal land
  description precision, produced in volume

  the placement asymmetry, which is the design point:
    Signal Service placed by existing posts + existing
    telegraph + coastal/Great Lakes storm-warning charter
    -> follows the rail and wire network
    homestead claims went where land was OPEN
    -> ahead of that network by definition
    -> THE NON-OVERLAP IS THE INFORMATIVE PART

  access: NARA RG49; BLM GLO Records searchable by legal
  description, partial state coverage online; NPS Homestead
  Records Project; some county-level holdings
```

Falsifier:

```
  well-depth and crop testimony show no coherent spatial
  or temporal structure beyond what is explained by
  claim-filing chronology and boilerplate.
```

This gap has a DECISION component — which state's digitized
set to start from. Use the decision-gap entry type from
WORK ORDER 01 Task 3 if it exists by then. Discriminator:
overlap with Signal Service station coverage, since the
validation depends on having a calibration region.

---

## TASK 4 — Render M-C, with its correction applied

```
source      MARKERS_HELD.md, M-C
folder      uninstrumented/
type        GAP
class       METHODOLOGICAL
state       NOT_STUDIED
```

M-C was drafted before M-A existed. **The correction is
mandatory**: the absence set has two mechanisms with opposite
implications, and separating them is step 3 of the method, not
an afterthought. Do not render the single-mechanism version.

Required content:

```
  the inversion: what is measured = what is believed to
  vary; what is unmeasured = what is believed to hold

  the Signal Service observed set from the 1887 manual,
  including the note that two-level cloud motion is an
  upper-air wind proxy — the set is built for storm
  ARRIVAL PREDICTION, not climate

  the absence list: soil moisture and temperature,
  groundwater, streamflow, snowpack, evaporation, growing
  degree accumulation, phenology, frost dates as events

  the 1891 War-to-USDA transfer as a natural experiment:
  same sky, changed institution, changed variable list

  the reference failure case: soil moisture instrumented
  after the Dust Bowl; unmeasured reads as stable until it
  fails loudly enough to get an instrument

  the unguarded-record argument: what was measured was
  argued over and defended; what was not measured was
  mostly never argued about, so the absence set is
  unguarded
```

HOLD CONDITION — keep on the page:

```
  the lag claim requires N>1 observation programs across
  DIFFERENT charters. One program's absence set is an
  anecdote. Render the gap; do not render a lag figure
  until the charter set is assembled.
```

Falsifier as drafted in M-C: variable lists expand at a rate
unrelated to documented failures — by technology availability
or budget alone, with no assumption-failure signature.

Cross-reference to G-01 (WORK ORDER 02): same shape, different
domain. An unmeasured quantity reads as a stable quantity;
a sub-floor null reads as an absent effect.

---

## TASK 5 — Source register, not a gap

```
source      MARKERS_HELD.md, M-E
folder      uninstrumented/
type        SOURCE REGISTER
```

M-E is scouting, not a question. Render it as a source
register that Tasks 2-4 and any later charter work draw on.

```
  postal RG28 holdings as listed, INCLUDING the register
  coverage gap
  Post Office site location reports 1837-1950 — flag these
  as the richer set: rivers, creeks, canals, roads,
  railroads, postmaster sketch maps, population served,
  contractor name
  Wells Fargo holdings, with the access class stated
  plainly: by request with lead time, not download
  the charter-contrast framing: postal charter is neutral
  to the environment, express charter is economic, and the
  divergence between what each records is itself the
  measurement
  the candidate charter list, MARKED AS CANDIDATES
```

Do not write questions into this file. It is a register.

---

## RENDERING NOTES

```
DO NOT
  file M-A..M-E as five sibling entries. The mechanism is
    the parent. This is the one instruction that cannot be
    traded off.
  generalize the four-archive table past four rows
  render M-C without the M-A correction
  drop either M-B complication into a caveat line
  soften the RG28 register-gap precondition
  describe any person in any of these files

CROSS-DOMAIN INDEX (WORK ORDER 01 Task 4)
  M-A is a MECHANISM entry and should index alongside the
  eight existing exclusion mechanisms, not among the gaps.
  M-B, M-C, M-D index as gaps pointing UP at it.
  M-C also indexes as a dependency of G-01's family:
  both are "absence read as fact" failures.

OPEN, for Kavik
  charter placement for the wider candidate list — she has
  a location in mind for it. Do not invent one.
```
