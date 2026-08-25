# CLAIM TABLE — claim-record

Claims from building the seven-field record and filling it with six real
claims. `SOURCE_DROP.md` is untouched.

**REFUTATION PROTOCOL.** The schema is the claim. A check that fails
updates the schema or the claim, never the record that failed it. Where
a finding is a property of the corpus rather than of the schema, it says
so and names what corpus would settle it.

---

### CR_001 — the schema has no way to say nothing, and that is rule two taken seriously

Rule two read as a required-fields list gives a form. Read as *optional
is how the domain of validity disappeared* it gives something stronger:
every field that could be absent has a **stated sentinel that carries a
reason** instead — `UNTESTED`, `UNQUANTIFIED` with a `why`, an empty
parent list with a `root_reason`.

`UNQUANTIFIED` without a `why` is refused, because a sentinel with no
reason is an omission wearing one, which is rule two's own failure
arriving one level down.

**Falsifier:** a field where an omission and a stated absence produce the
same validator output.

**Status: SUPPORTED. Three sentinels, each with its reason required.**

---

### CR_002 — the coupling between fields 2 and 7 is the part that does work a required-field list does not

- `lo == hi` under `NOT_COLLAPSED` → `POINT_WITHOUT_BASIS`
- `lo != hi` under `EXACT` → `INTERVAL_MARKED_EXACT`

A point arrives either from a distribution or from a count. Field 2 says
*interval, not a point*; field 7 is where a point earns the exception.
Without the coupling, a record can satisfy both fields independently and
still be the failure the drop describes — a distribution silently reduced
to its upper quartile.

Both directions are pinned.

**Falsifier:** a legitimate point measurement that is neither collapsed
nor exact.

**Status: SUPPORTED.**

---

### CR_003 — rule two is null-tested per field, and the positive control comes first

Seven arms, one per field: drop it, require `INVALID` with
`MISSING_FIELD` naming that field. All seven fire.

**A validator that refuses everything passes all seven**, so the first
check in the file is that a complete record validates, and eleven further
checks require specific well-formed variants to validate rather than
merely to be refused: `UNQUANTIFIED` with a reason, `UNTESTED`
`outside_this`, a point from a named statistic, a resolvable parent.

39 checks, both directions on every rule that has two.

**Falsifier:** a well-formed record the validator refuses — F1.

**Status: SUPPORTED.**

---

### CR_004 — rule one holds against the registry, and a cycle is reported as a cycle

An unresolvable parent gives `PARENT_UNRESOLVED` and `INVALID`. A cycle
gives `PARENT_CYCLE` with the loop printed, rather than recursion depth.

The load path is the payoff and is demonstrable on the real corpus:

```
SSS_022b
  SSS_017
  SSS_020
    SSS_017
    SSS_021
      SSS_017
```

**Every claim in the corpus traces to `SSS_017`**, the reader repair. If
that is refuted, five claims above it are exposed, and the schema is what
makes that visible rather than something someone has to remember.

**Falsifier:** F4 — a load path that misses a real dependency, since
field 6 records what the author recorded and not what the claim rests on.

**Status: SUPPORTED for what is recorded. F4 is not testable from inside
the registry.**

---

### CR_005 — there is no denominator field, and 6 of 6 records smuggle one into `units`

| record | `units` |
|---|---|
| SSS_017 | `formula cells resolved, of 825 present` |
| SSS_019 | `1 (share of non-empty cells)` |
| SSS_020 | `sheets with a pure-derived factors column, of 11 carrying that label` |
| SSS_021 | `occurrences, of 4 differing per group` |
| SSS_022a | `cells, of 22 flagged` |
| SSS_022b | `cells, of 22 flagged` |

**6 of 6.** Every measurement in the first corpus is a count against a
population, and the population has nowhere to go but a free-text string
beside the unit.

This is `measurement-fork`'s VOID RATIO at design time: a ratio needs
both operands named, and a denominator that lives in prose is one nobody
can compare across records. The repair is a `measurement.of` field with a
value and a description, which would also make `129 of 825` and
`22 of 22` comparable as shares without re-reading the string.

**Falsifier:** a corpus where denominators are rare enough that the field
would sit empty — which would then need a sentinel, and the sentinel is
the cheaper half of the repair.

**Status: SUPPORTED, unrepaired. The schema is the delivery's and this is
a proposed eighth sub-field, not a defect in what was specified.**

---

### CR_006 — field 7's stated purpose has zero instances in the first corpus

`collapse_record.state` across the six records:

| state | count |
|---|---|
| `EXACT` | **6** |
| `COLLAPSED` | **0** |
| `NOT_COLLAPSED` | 0 |

The drop names field 7 *"the upper-quartile field"* — its purpose is the
distribution silently reduced to a point. **No record exercises it.** The
selftest does, in both directions, so the branch is not dead code; the
corpus does not, so the branch has never met a real case.

The reason is not carelessness and is worth stating, because it bounds
the finding: **every instrument in this corpus is deterministic and every
artifact is a fixed file**, so every measurement is an exact count and
`EXACT` is the correct state in all six. Field 2's *interval, not a
point* and field 7's collapse record are both aimed at measurements with
sampling error, and this folder has not yet made one.

So the corpus is unrepresentative in a specific, nameable way, and what
would test the schema properly is **one claim whose measurement is a
distribution** — from a sampled process rather than from arithmetic on a
file.

`null-harness` calls this shape `CONSTANT_SILENT`. Here the branch fires
in the selftest and not in the wild, which is the weaker version and
still worth recording before anyone reads six validating records as six
tests of the schema.

**Falsifier:** a record with `state: COLLAPSED`.

**Status: SUPPORTED. Field 7 is untested by the corpus and tested by the
selftest, and those are different things.**

---

### CR_007 — three more columns are single-valued, so the fields are present and not yet informative

| field | values in the corpus |
|---|---|
| `instrument.error.kind` | `systematic` × 6. No `random`, no `UNQUANTIFIED` |
| `domain_of_validity.outside_this` | contains `UNTESTED` × 6 |
| `clock.next_check` | one date × 6, chosen in one sitting |

`outside_this` is the sharpest of the three: **the sentinel is doing all
the work in the field the drop calls the one that always gets stripped.**
The field is present in every record, which is what rule two buys, and
carries no information about any of them yet, which rule two does not
buy and cannot.

A required field that is always filled with the same sentinel is a field
that has survived rule two and not yet earned its place. Recorded rather
than repaired: the repair is to measure something outside the conditions,
which is work, not schema.

**Falsifier:** a second corpus where these columns vary.

**Status: SUPPORTED.**

---

### CR_008 — there is no sibling relation, and the missing edge was written as a parent before it was caught

`SSS_022a` (unit present on 22 of 22) and `SSS_022b` (variance sibling
absent on 22 of 22) are **one observation from one run of one scan**.
They are separate records because field 2 holds one interval, which is
the schema forcing decomposition and is arguably right.

The first version gave `SSS_022b` the parent `SSS_022a`. That is a false
edge: b does not rest on a, they were measured together. **The schema has
a parent relation and no sibling one**, so co-measured claims either
invent a hierarchy or are given the same parents — and inventing the
hierarchy is what happened first, in the file, by the author of the
schema, within minutes of writing rule one.

Corrected to shared parents. Recorded rather than quietly fixed, because
it is evidence about how the missing relation gets filled: not left
blank, but populated with the nearest available edge.

**Falsifier:** a co-measured pair that a reader finds correctly ordered
by a parent edge.

**Status: SUPPORTED. The repair is a `siblings` or `co_measured` field,
which is a change to the delivered schema and is not made here.**

---

### CR_009 — field 1 is the one field enforced lexically, and a paraphrase steps around it

38 hedge words, screened both ways: a hedge-free assertion must come back
clean, and `mayor`, `somewhere` and `thereabouts` must not fire — the
substring-bleed failure this repository recorded as `UNI_009`.

*"This may hold"* is caught. *"This holds in the cases examined so far,
though the sample is what it is"* is not, and asserts less than it
appears to. The limit is at the top of `record.py` rather than the
bottom, with `DF_010` and `ACL_017` named as the same limit on other
substrates.

What the screen buys is the fluent failure — reaching for *may*,
*appears*, *roughly* without noticing. That is the one that happens.

**Falsifier:** F3 — a hedge that survives the screen and changes what the
assertion licenses.

**Status: SUPPORTED for the vocabulary. The paraphrase channel is open by
construction.**

---

### CR_010 — `due --on DATE` read the date as the records directory and printed an empty table with rc 0

The argument parser dropped `--`-prefixed tokens and kept the rest as
positionals, so `record.py due --on 2026-08-25` loaded `2026-08-25` as a
directory, found nothing, and rendered a well-formed table with **zero
rows and exit status 0.**

Same shape as `domain-ledger` `DL_005`: a report whose denominator is
zero, rendered as though it had one, in a tool about denominators. Found
by running the command, not by reading the parser.

Repaired: a flag's value is no longer a positional, and both `validate`
and `due` refuse an empty registry on stderr with rc 2 rather than
printing an empty table. Both pinned.

**Falsifier:** a third command path that renders an empty registry as a
result.

**Status: REPAIRED, both branches pinned.**

---

### CR_011 — the clock is about the instrument wherever the claim is arithmetic on a fixed artifact

Six records, six identical `next_check` dates, chosen by one author in
one sitting. The honest reading of field 5 for these claims: **a
byte-identical file does not decay, so the timescale is the reader's, not
the claim's.**

`SSS_017`'s `holds_for` says so outright — *"as long as both the file and
that reader revision are unchanged; the file is fixed, the reader is
not"* — which is the field being filled correctly and revealing that for
this class of claim it is measuring the instrument.

That is not a defect. It is what field 5 looks like when the claim is
arithmetic: the check date is a reminder to re-run against a changed
tool. For a claim about a world that moves, it would mean something else,
and no record here is one.

**Falsifier:** a claim in this registry whose subject changes while its
instrument does not.

**Status: SUPPORTED.**

---

## Claims from section 2, the derived clock

Delivered 2026-08-25: three sub-fields, all derived rather than
asserted; shelf life is the time constant weighted by coupling; a clock
asserted rather than derived does not validate.

---

### CR_012 — the coupling has to be a dimensionless elasticity, or the shelf life is not a time

Section 2 calls the third sub-field *the partial derivative*. Taken
literally, `dY/dX` carries the units of the result over the units of the
neglected term, and

    shelf_life = time_constant / coupling

is then years divided by (kg CO2e per kWh per kWh), which is not a
duration and does not compare between two claims.

The quantity that works is the **elasticity**, `(dY/Y)/(dX/X)`:
dimensionless, comparable across claims, and exactly what
`sheet-structure-scan/coupling.py` measures by perturbation. So the
schema requires `clock.coupling.units == "1"` and refuses anything else.

This is `reasoning-gate`'s `G-DIM` applied before the number is produced
rather than after it is quoted.

**Falsifier:** a coupling with units that still divides a time correctly.

**Status: SUPPORTED. The sub-field is enforced dimensionless.**

---

### CR_013 — all three behaviours the order names are realized on real records

| record | clock | shelf life | next check |
|---|---|---|---|
| `UNF_GRID_IRAQ` | **DERIVED** | **3.40 yr** | 2030-01-18 |
| `UNF_PALESTINE` | **UNDERIVABLE** | — | — |
| `SSS_017` | **UNBOUNDED_BY_THIS_TERM** | — | — |

**The grid factor: derived and short**, as predicted. It holds the
generation mix fixed; the mix time constant is 3 years and the coupling
is **0.8815, measured by perturbation** on the file rather than
asserted — `+0.1%` on `Electricity, heat, cooling!B193`, elasticity of
`Report!E25` under a stated case.

**The Palestine factor: no clock, and no default emitted.** It holds
fixed that five neighbours resemble the target. That resemblance was
never measured, so `time_constant` is `UNMEASURED` with the reason, and
the derivation returns `UNDERIVABLE` with `next_check: None`. There is
no branch in `derive_clock` that can produce a date from an unmeasured
sub-field.

**`SSS_017`: the weak-coupling rule, instanced.** Its neglected term is
the reader revision, which moved **twice in one day** — a time constant
of 0.003 years, the fastest in the registry. Its `domain_of_validity`
names the commit, so the claim does not move when the reader does:
coupling 0, and the state is `UNBOUNDED_BY_THIS_TERM`. *Weak coupling
means a fast-moving neglected term doesn't shorten it* — the fastest
term in the corpus dates nothing.

**Falsifier:** a record whose derived clock a reader judges wrong in
direction.

**Status: SUPPORTED, three of three.**

---

### CR_014 — rule 3 is enforced against the literal, and the sub-fields are enforced one level down

`holds_for`, `next_check`, `shelf_life` and `shelf_life_years` are
**refused as literals** in the clock — `CLOCK_ASSERTED`. That is rule 3
directly.

The rule is also enforced where it would otherwise be evaded: a
sub-field carrying a value with **no `basis`** is refused, because a
number typed in with nothing behind it is the clock asserted one level
down. `UNMEASURED` without a `why` is refused for the same reason.

**Falsifier:** a way to get a date out of the schema without three
derived sub-fields behind it.

**Status: SUPPORTED. Four literal names, both sub-field evasions.**

---

### CR_015 — the rate ceiling refines the reading and does not gate the date

`rate_ceiling` gives the regime — `ADIABATIC` when the neglected term
moves slower than the ceiling, `SUDDEN` when faster — and it is **not**
required for the shelf life, which needs only the time constant and the
coupling.

That split is deliberate: a claim whose ceiling nobody has established
still has a derivable shelf life, and forcing the ceiling would make
`UNDERIVABLE` the common case for a reason section 2 does not give.
**8 of 9 records carry `rate_ceiling: UNMEASURED`** and the one derived
clock still derives.

**Falsifier:** a case where the regime changes what the shelf life
should be, making the split wrong.

**Status: SUPPORTED. `REGIME_UNKNOWN` on 9 of 9, which is a corpus
statement — see `CR_017`.**

---

### CR_016 — `COLLAPSED_UPSTREAM`, the fourth state the three fixtures forced

The three worked cases separate on exactly one axis, and the schema had
only two boxes for three answers:

| record | state | which point | stated by |
|---|---|---|---|
| `UNF_HOTEL_AR` | `COLLAPSED` | **`upper_quartile`** | the workbook, at `Info and sources!E19` |
| `UNF_PALESTINE` | `COLLAPSED` | **`mean`** | computed in the workbook, verified to **1.1e-16** |
| `UNF_GRID_IRAQ` | **`COLLAPSED_UPSTREAM`** | **unstated** | nobody |

The grid factor arrived as a point from a cited dataset that the
workbook does not describe. That is not `COLLAPSED` (the statistic is
unknown), not `EXACT` (there was plainly something to collapse), and not
`NOT_COLLAPSED`. The new state requires `source` and `what_is_unstated`,
so the gap is named rather than defaulted into one of the other three.

The hotel case is `CR_006` closed: **field 7's stated purpose, the
upper-quartile field, now has an instance**, and it is a real one — the
workbook says so in its own words.

**Falsifier:** a fifth arrangement these four cannot hold.

**Status: SUPPORTED. Field 7 has 4 states and the corpus now uses 3.**

---

### CR_017 — the corpus is still uniform in the fields the sentinels cover

| field | 9 records |
|---|---|
| `clock.rate_ceiling` | `UNMEASURED` **8** |
| `clock` regime | `REGIME_UNKNOWN` **9** |
| `domain_of_validity.outside_this` | contains `UNTESTED` **9** |
| `collapse_record.state` | `EXACT` 6, `COLLAPSED` 2, `COLLAPSED_UPSTREAM` 1 |

`CR_006` is closed and `CR_007` is not. **No record in the registry
carries a measured rate ceiling**, so the adiabatic-versus-sudden
distinction section 2 asks for has been implemented, is exercised in the
selftest in both directions, and has never fired on a real record.

That is the same shape `CR_006` had one drop earlier, one field over,
and it is stated before anyone reads nine validating records as nine
tests of the clock.

**Falsifier:** a record with a measured `rate_ceiling`.

**Status: SUPPORTED. The regime column is untested by the corpus.**

---

### CR_018 — the coupling sub-field is measured on the file, which is the join between sections 2 and 4

`UNF_GRID_IRAQ` and `UNF_HOTEL_AR` both carry a coupling produced by
`sheet-structure-scan/coupling.py` — 0.8815 and 0.9247 — with the
perturbation, the target and the case written into `basis`.

That is what makes rule 3 more than a formatting rule: for a claim about
a workbook, **the third sub-field is not a judgement at all.** It is a
measurement anyone can repeat by running the named command against the
named file.

Both were `NOT_COMPUTABLE` until `VLOOKUP` was implemented, because both
worked cases in the delivery are consumed by a lookup. The order's two
sections failed at the same cell for the same reason, and unblocking one
unblocked the other.

**Falsifier:** a claim whose coupling cannot be measured on any
instrument, making the sub-field a judgement again.

**Status: SUPPORTED for workbook claims. For the six `SSS_*` records the
coupling is 0 by construction and says so in its basis.**

---

### CR_019 — the no-labelling constraint is imported, not re-implemented

The order states it: the tool reports structure and never labels a
record as wrong. `record.py` imports `no_severity` from
`sheet-structure-scan/` rather than copying it — one screen, and
`MF_019` is what copying costs — and screens its own emitted report,
returning non-zero if a word lands.

It fired immediately, on this file's own disclaimer prose (*"a record
should have been written"*, then *"what anyone ought to do"*). Reworded
twice rather than loosening the screen. Second instance of `SSS_024`'s
use-and-mention boundary, in the second tool.

The verdict vocabulary is stated rather than assumed: **`VALID` and
`INVALID` are about conformance to the record schema**, never about
whether a claim is true or how much weight a measurement carries, and
the report says so above the table.

**Falsifier:** a labelling reaching the report in words the screen does
not hold — open by construction, as `CR_009` states.

**Status: SUPPORTED.**

---

## Claims from the frame layer

Three base principles and an acceptance test, delivered 2026-08-25.
Implemented in `frames.py` and `frames/*.json`. The reasoning is
recorded verbatim in both, and is the reason the work happened before
anything needed it:

> this is being specified before it's needed because retrofit cost is
> the entire reason the fold detector exists. Building the fold in now,
> knowing it's a fold, would be the same error the tool was written to
> find.

---

### CR_020 — the format had four frame leaks and every one was in the code, not the records

Found by grep, before the principles were implemented:

| leak | where |
|---|---|
| `units_expected="years"` | the time-constant check |
| `units_expected="per_year"` | the rate-ceiling check |
| `365.2425` | inside the next-check derivation |
| `shelf_life_years` | the **name** of the returned field |

Not one was in a record. Every record already declared its unit, so the
data was frame-tagged and the **code** was frame-welded — which is why
the acceptance test passes without editing any of them, and why it would
have failed against the implementation of an hour earlier.

**Falsifier:** a frame token in a record that the registry cannot
resolve, which would put a leak in the data.

**Status: REPAIRED. No unit is named in `record.py` outside the
deliberately-leaked control and the selftest's explicit frame arguments.**

---

### CR_021 — the identity transform had to be registered, and it turned up as a break

Principle 1 says no frame is the default. The obvious reading is about
`years`. The implementation showed a second one: `coupling` declares
`units: "1"`, and until `frames/dimensionless.json` existed, **all nine
records went `UNDERIVABLE` at once.**

Leaving `1` implicit would have made it the one unit the format resolved
without asking — a privileged frame wearing a unit string. It is now a
versioned object like the rest, and its `basis` records that it arrived
as a failure rather than as a design note.

**Falsifier:** another quantity the registry resolves without a frame
object behind it.

**Status: SUPPORTED. Six frames registered, no special cases.**

---

### CR_022 — the acceptance test passes, and the control is what makes that mean anything

```
added                    venus_days (10087200.0 s per unit), not on disk
records read             9
records needing an edit  0
records still validating 9 of 9
errors                   0
```

The added frame is **deliberately not one of the files in `frames/`**,
because adding a frame that is already registered tests nothing.

**The control is the load-bearing half.** A test that adds a frame
nothing reads would pass on a format that had leaked everywhere, so the
same claim is written in the added frame and must clear three bars:

| | |
|---|---|
| validates under the frame-aware implementation | **True** |
| refused by an implementation with `years` welded in | **True** |
| derives the same shelf life in base units | **True** |

The third is not decoration: without it, a second frame that silently
changed the quantity would pass the first two.

Run inside **both** selftests rather than left as a command someone
remembers.

**Falsifier:** a frame whose addition requires an edit — F8.

**Status: SUPPORTED.**

---

### CR_023 — principle 1 reaches the reader, not only the format

`due` has **no default frame**. A reader that did not have to name its
frame would make one of them the default in everything but the
specification, so `record.py due` without `--in` refuses and lists what
is registered.

The same applies inside a record: `measured_on` now requires
`measured_on_frame`, because an instant with no declared calendar is the
Gregorian one by assumption. All nine records were edited to declare it —
**that is a schema tightening, not a frame addition**, and it is the
distinction the acceptance test turns on. Adding `venus_days` needed no
edit; requiring every instant to name its calendar needed nine.

**Falsifier:** a path that yields a duration or an instant without a
frame being named.

**Status: SUPPORTED. `FRAME_UNDECLARED` and `FRAME_UNREGISTERED` are
separate codes, because a frame nobody named and a frame nobody
registered are different repairs.**

---

### CR_024 — working in base units makes the regime comparison frame-free

`rate_ceiling` and `time_constant` are converted to base on the way in,
so `1/tau <= ceiling` compares a rate in `per_year` against a time
constant in `sols` **without either being expressed in the other's
frame.**

That falls out of principle 3 rather than being designed: if nothing is
stored converted, everything is converted once at read time, and the
comparison happens where both are in the same base.

**Falsifier:** a comparison in the derivation that needs one operand
rendered in the other's frame.

**Status: SUPPORTED.**

---

### CR_025 — the first run of the acceptance test failed on the harness, not the format

Arm A reported **3 of 9 validating** with six `PARENT_UNRESOLVED`
findings. The cause was that the harness validated each record in a
one-record registry, so rule 1 could not see any parent by construction.

Recorded rather than quietly fixed, because it is a specific way an
acceptance test can report a failure that belongs to itself: the
test-time registry was not the registry the format uses, and a reader who
took the first output at face value would have gone looking for a frame
leak in six records that did not have one.

**Falsifier:** another harness-level state the test reports as a format
failure.

**Status: REPAIRED. The test now validates against the full registry.**

---

## Claims from work order 3, S5 — the adjustment history

Fields 8, 9 and 10 amend the schema. The discriminator that reads them
is in `residual-direction/`.

---

### CR_026 — field 8 is the first column in this registry that varies

`CR_007` and `CR_017` recorded that every sentinel-bearing field came
back single-valued. Field 8 does not:

| value | records |
|---|---|
| `unadjusted` | **6** |
| `unknown` | **3** |

The six are counts this session computed from a file, where nothing was
subtracted and the history is known. The three are values read from a
published dataset and a published index whose own production the
workbook does not describe — which is `COLLAPSED_UPSTREAM` seen from a
second side, and the same three records carry both.

Field 10 splits with it: depth `0` on six, `UNKNOWN` with a reason on
three.

So the standing finding narrows rather than closing. `outside_this` and
`rate_ceiling` are still uniform; field 8 is not, and it is the first
field whose values say something about the corpus rather than about the
schema.

**Falsifier:** a record whose status a reader would assign differently.

**Status: SUPPORTED.**

---

### CR_027 — zero and unknown are different in field 10, and a missing field is neither

`correction_depth: 0` says nothing was inherited. `{"state": "UNKNOWN",
"why": ...}` says nobody looked. An absent field is refused rather than
read as zero.

The absent-versus-known-negative repair, now designed in at the fourth
field of this schema — `error.kind`, `outside_this`, the clock
sub-fields, and now this one. It costs one branch at construction and is
unrecoverable later, which is why it keeps being worth writing down.

**Falsifier:** a third state these two conflate.

**Status: SUPPORTED.**

---

### CR_028 — the uninterpretable state is a record-layer function, not a report string

`interpretable(record, lean_present)` returns a boolean and a reason, and
the discriminator in `residual-direction/` calls the same logic on the
series side. Both arms are checked: unknown history with no lean is
uninterpretable, unknown history **with** a lean is readable — because a
lean that survived an adjustment is still a lean — and a known history
with no lean is readable.

That middle case matters. A blanket rule on `unknown` would refuse to
read a series that has something to say.

**Falsifier:** an unknown-history series with a lean that a reader
judges unreadable.

**Status: SUPPORTED.**

---

### CR_029 — a coupling in this registry was transferred rather than measured, and it was wrong

`UNF_PALESTINE` carried **0.8815** with the basis *"measured by
perturbation on the neighbouring Iraq cell under the same case; the
Palestine row is consumed by the same lookup and carries the same
elasticity to the reported total."*

Measured on the Palestine cell itself, under a case that selects
Palestine, it is **0.8194**.

The transfer reasoning was about the **lookup**, not about the cell. The
elasticity of a sum with respect to one term is that term's share of the
total; Palestine's factor is 0.569 against Iraq's 0.934, so the shares
differ and no argument about shared consumption makes them equal.

The word *measured* in that basis was doing work it had not earned. The
record is corrected with the real number, the command that produced it,
and the correction stated in the field rather than in a commit message.

**It changes no verdict.** `UNF_PALESTINE`'s time constant is
`UNMEASURED`, so its clock was and remains `UNDERIVABLE` — which is
worth saying, because a correction that moved nothing is still a
correction, and the alternative was leaving a wrong number in a field
whose whole purpose is that it be measured.

The record also gains a condition recording what the per-cell run
established: **`B296` is a hardcoded constant**, so the mean-of-five
relationship the workbook states in prose is not maintained by any
formula.

**Falsifier:** a case under which the two cells do carry the same
elasticity, which would make the transfer sound after all.

**Status: CORRECTED. The error was mine and it was in a `basis` field.**
