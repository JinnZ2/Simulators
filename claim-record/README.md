# claim-record

Seven fields per claim, two hard rules, and a validator that refuses.

Delivery in [`SOURCE_DROP.md`](SOURCE_DROP.md), spoken, verbatim.
Schema in [`SPEC.md`](SPEC.md). Findings from filling it with six real
claims in [`CLAIM_TABLE.md`](CLAIM_TABLE.md).

```
python3 record.py validate            every record, with findings
python3 record.py path UNF_PALESTINE  the load path, walked upward
python3 record.py due --on 2026-08-25 --in sols   whose check has passed
python3 frames.py list                           the registered transforms
python3 frames.py --acceptance                   add a frame, check nothing moves
python3 record.py --selftest
```

## The design move

Rule two read as a required-fields list gives a form. Read as *optional
is how the domain of validity disappeared in the first place* it gives
something stronger:

> **This schema has no way to say nothing. It only has ways to say "not
> known, and here is why."**

`UNTESTED`, `UNQUANTIFIED` with a `why`, an empty parent list with a
`root_reason`. A sentinel without its reason is refused — that is rule
two's own failure arriving one level down.

## The part that does work a required-field list does not

Field 2 says *an interval, not a point*. Field 7 is where a point earns
the exception, and the two are coupled:

- `lo == hi` under `NOT_COLLAPSED` → `POINT_WITHOUT_BASIS`
- `lo != hi` under `EXACT` → `INTERVAL_MARKED_EXACT`

A point arrives either from a distribution or from a count, and saying
which **is** the field. Without the coupling a record can satisfy both
fields independently and still be the failure the drop describes.

## Three base principles

**1. No privileged frame.** Not even the one every record uses. `years`
is a registered transform like `sols`; an unregistered unit raises rather
than resolving by assumption, and `due` has **no default frame** — the
reader names the one it wants. Even the identity transform is registered,
because leaving `1` implicit would have made it the one unit the format
resolved without asking. That turned up as a break rather than as a
design note, which is the check working.

**2. Transforms are first-class objects.** `frames/*.json`, versioned,
beside the records. A rate frame carries no rate of its own — it names
the duration frame it inverts, so a correction reaches it without an
edit. Adding a frame is adding a file.

**3. Derived at read time, never at write time.** A stored duration is a
cached conversion, and caching the conversion is what makes it legacy.
`shelf_life`, `next_check` and every `shelf_life_<unit>` name are refused
as literals in a record; the derivation returns base units and the reader
renders them:

```
claim          clock    shelf(years)  next_check
UNF_GRID_IRAQ  DERIVED  3.403         2030-01-18
claim          clock    shelf(days)   next_check
UNF_GRID_IRAQ  DERIVED  1243          2030-01-18
claim          clock    shelf(sols)   next_check
UNF_GRID_IRAQ  DERIVED  1210          2030-01-18
```

One record, three frames, nothing stored converted.

### The acceptance test

> Add a second frame with a different rate, and no existing record needs
> editing. If any record needs editing, the frame leaked into the data.

`frames.py --acceptance` adds `venus_days` — deliberately not one of the
files on disk — and reports **9 records read, 0 needing an edit, 9 still
validating.** Beside it runs a control, because a test that adds a frame
nothing reads would pass on a format that had leaked everywhere: the same
claim written in the added frame must validate here, must be **refused**
by an implementation with `years` welded in, and must derive the **same
shelf life in base units**.

Both selftests run it, rather than leaving it a command someone
remembers.

### Why now

> this is being specified before it's needed because retrofit cost is
> the entire reason the fold detector exists. Building the fold in now,
> knowing it's a fold, would be the same error the tool was written to
> find.

## The clock, derived

Three sub-fields — the time constant of the nearest neglected term, the
rate ceiling on the background, and the coupling — and **no date is
stored**:

    shelf_life = time_constant / |coupling|

The coupling is a **dimensionless elasticity**, and it has to be: a raw
partial derivative carries units, and a time divided by that is not a
time. For a claim about a workbook it is **measured, not asserted** —
`coupling.py` perturbs the constant and reads the output cells.

All three behaviours the order names are realized on real records:

| record | clock | shelf life |
|---|---|---|
| `UNF_GRID_IRAQ` | **DERIVED** | **3.40 yr**, next check 2030-01-18 |
| `UNF_PALESTINE` | **UNDERIVABLE** | no date, and no default emitted |
| `SSS_017` | **UNBOUNDED_BY_THIS_TERM** | the fastest term in the corpus dates nothing |

The grid factor holds the generation mix fixed; coupling **0.8815**,
measured on the file. The Palestine factor holds fixed that five
neighbours resemble the target — never measured, so there is no branch
that can produce a date. `SSS_017`'s neglected term moved **twice in one
day** and its domain of validity pins the commit, so coupling is 0 and
the term does not date the claim: *weak coupling means a fast-moving
neglected term doesn't shorten it*, instanced.

## What the real records showed

Filled with claims from the `sheet-structure-scan/` run earlier the same
day, where the provenance is known. All six validate — and the useful
part is what came back uniform:

| field | corpus |
|---|---|
| `collapse_record.state` | `EXACT` 6, `COLLAPSED` 2, `COLLAPSED_UPSTREAM` 1 |
| `clock.rate_ceiling` | **`UNMEASURED` 8 of 9** |
| `instrument.error.kind` | `systematic` 6 |
| `domain_of_validity.outside_this` | contains `UNTESTED` 6 |
| `measurement` units carrying a denominator | **6** |

**`CR_006` is closed and `CR_017` replaces it.** Field 7's
upper-quartile branch now has a real instance — the hotel factor, whose
statistic the workbook states in its own words at `Info and sources!E19`.
But **no record carries a measured `rate_ceiling`**, so the
adiabatic-versus-sudden distinction is implemented, exercised in the
selftest both ways, and has never fired on a real record. Same shape,
one field over.

The three fixtures forced a fourth collapse state (`CR_016`): the hotel
source names its statistic, the Palestine value is a mean computed in the
workbook and verified to **1.1e-16**, and the grid factor arrived as a
point from a dataset the workbook does not describe —
`COLLAPSED_UPSTREAM`, which names the source and the gap rather than
defaulting into one of the other three.

**There is no denominator field** (`CR_005`), so `129 of 825`, `22 of 22`
and `1 of 11` all put the population in a free-text `units` string —
VOID RATIO at design time.

**There is no sibling relation** (`CR_008`), and the missing edge got
written as a parent before it was caught: two claims measured in one run
were given a parent-child edge, in the file, by the author of the schema,
minutes after writing rule one.

## The load path

Field 6's purpose, on the real corpus:

```
SSS_022b
  SSS_017
  SSS_020
    SSS_017
    SSS_021
      SSS_017
```

Every claim traces to `SSS_017`, the reader repair. Refute that and five
claims above it are exposed — visibly, rather than because somebody
remembered.

78 selftest checks across two modules. Rule two gets seven null arms, one per field, and the
**positive control comes first**: a validator that refuses everything
passes all seven.

CC0. Stdlib only. Parses under Python 3.9.
