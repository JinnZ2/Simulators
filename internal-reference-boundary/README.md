# internal-reference-boundary

A boundary drawn by the party inside it, measured from inside.

`HANDOFF.md` is delivered verbatim and is not edited. Everything else is
built to it. Nothing here is a reading of any real field, body,
institution, practice, treatment or person; every case is CONSTRUCTED and
every empirical figure is CARRIED from the handoff and checked against
nothing.

## Shape

```
                        ANCHOR INVARIANT
        a boundary drawn by the party inside it, measured from inside
                               |
        +----------------------+----------------------+
        |                                             |
   RADIALS (radials.py)                    TIME (gap_transfer.py)
   one boundary, statically                one gap, across hosts
        |                                             |
   R1 encounter rate        per occasion of need   host_1 --+
   R2 measurand ownership   ladder 0.0 .. 1.0               | inherits
   R3 sanction base rate    band, two time bases            |  population
   R4 routability           + damage capacity               |  + horizon
   R5 exemption provenance  breadth | benefit-corr          v
   R6 transfer survival     n_eff origins, 4 routes    host_2  CARRIER
   R7 permeability          2 metrics, 2 denominators       |
        |                                                   | direction
        |                                                   v
   ASSEMBLY ORDER                                      host_3  same gap,
   invariant -> cases -> EXEMPTIONS AS A SEPARATE LAYER        other way
```

Three non-value states on every radial, kept apart:

```
   UNDECLARED      the record does not state the input
   NEEDS_CORPUS    the method is complete, no corpus supplied
   NOT_EVALUABLE   the input is present, the quantity has no value
```

The handoff marks R1-R5 READY and R6, R7 method-complete-and-needing-a-
corpus. R6 and R7 therefore refuse to emit a number without one, naming
the input they want.

## Run

```
python3 radials.py            # the radial reading over the constructed corpus
python3 radials.py --mean     # [CHOICE 7] dilute the R6 coupling combination
python3 radials.py --choices  # every open parameter, 1..8
python3 gap_transfer.py       # the gap-transfer reading
python3 gap_transfer.py --choices        # 9..10
python3 test_boundary.py      # the checks; prints its own count
```

Both modules refuse `--selftest` with rc 2 rather than exiting 0 on an
invocation that runs nothing.

## Files

```
HANDOFF.md        delivered verbatim, never edited
radials.py        R1..R7, the fold test, the R7 x R6 cell, assembly
gap_transfer.py   the second instrument: track the gap, not the host
cases.py          six constructed boundary cases, one per instance
gap_cases.py      the handoff's worked case CARRIED + two constructed
test_boundary.py  the checks, in 20 sections
CLAIM_TABLE.md    IRB_001..IRB_022
samples/          one pinned run of each renderer and of the suite
```

## What the instrument does not do

- **It does not adjudicate whether a pariah is correct.** R7 scores the
  field's stated REASON for rejecting -- METHOD or CONCLUSION -- which is
  the design move that removes the need. A field correctly identifying
  bad method scores as permeable. No identifier in either module holds a
  correctness verdict on rejected work; the scan is null-tested on a
  plant.
- **It does not record how any intervention went.** `gap_transfer.py`
  has no efficacy field and refuses a host carrying one at intake. An
  instrument holding an efficacy column is one somebody will sort by.
- **It does not rank boundaries.** There is no composite score, no
  function sums or averages across radials, and `locate_carrier` returns
  its candidates in the order given.
- **It does not read free text.** `what_the_boundary_is` and
  `who_draws_it` are carried and reported; replacing both moves no
  radial.

## Three things the build found

**R3's own anchor sits on two time bases.** `~1 finding per 10,000
researchers/yr` is per person-year; `25-50% self-reported incidence` is a
share over an unstated window. The ratio is a band spanning about 60x
until the window is declared, so the radial returns a band and no point.
One word closes it. (`IRB_001`)

**R6's rule needs no eigensolver.** The effective number of independent
origins is the participation ratio, and for a symmetric coupling matrix
with unit diagonal that is `n^2 / sum_ij C_ij^2` exactly -- standard
library, both extremes exact, monotone in coupling. Four nominal origins
on the worked case come back at 1.93. (`IRB_003`)

**The worked case cannot reach its own sharpest reading.** *Same defect
running the other way* requires the accounting horizon shown to be the
same one in both hosts, and the delivered case declares it in neither.
At its delivered resolution both transfers return NOT_EVALUABLE. One
field closes it, and nothing here fills it in. (`IRB_016`)

## Open, from the handoff, none of it run

```
  fold-test R2 vs R5                  instrument built, corpus UNRESOLVED
  R7 x R6 interaction cell            NAMED_UNINSTRUMENTED
  psychosurgery governance            NOT_RUN  (R5 on a live case)
  elite-memoir content analysis       NOT_RUN  (method exists, never run
                                                on this population)
```

The fold test's discriminating cell -- an externally-held metric with a
self-designated exemption -- is deliberately absent from `cases.py`.
Authoring it would close the handoff's own open item by writing the
answer down.

CC0. Stdlib only. Parses under 3.9. Phone-buildable.
