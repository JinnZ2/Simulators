# SPEC — the seven-field claim record

Written to the delivery in `SOURCE_DROP.md`, spoken 2026-08-25.
Runnable form: `record.py`. CC0, stdlib only, parses under Python 3.9.

---

## 0. THE DESIGN MOVE

Rule two says no field is optional, *because optional is how the domain
of validity disappeared in the first place*. Taken literally that is a
required-fields list. Taken seriously it is stronger:

> **This schema has no way to say nothing. It only has ways to say "not
> known, and here is why."**

A field that cannot be filled is filled with a **stated sentinel** that
carries a reason — `UNTESTED`, `UNQUANTIFIED`, an empty parent list with
a `root_reason` — never left out, and never left blank. An omission and a
known negative are different states, and every field that can carry
either keeps them apart.

That is the repair this repository has recorded more than a dozen times
across other folders and implemented at construction only a handful of
times, which is the only point in the cycle where it is free.

---

## 0b. THREE BASE PRINCIPLES

Stated plainly, because the file is the place for them.

**1. No privileged frame.** The format does not treat any frame as the
default, **including the one every current record uses.** `years` is a
registered transform on the same terms as `sols`; nothing falls back to
it, an unregistered unit raises rather than resolving by assumption, and
a reader that wants a duration in a frame has to name the frame. Even
the identity transform is registered — leaving `1` implicit would have
made it the one unit the format resolved without asking.

**2. Transforms are first-class objects.** They live in `frames/` as
versioned records beside the claims, not as conversion code inside an
application. Each names its base, its rate, and the basis for that rate.
A rate frame carries no rate of its own: it names the duration frame it
inverts, so a correction to that frame reaches it without an edit.
Adding a frame is adding a file.

**3. Derived at read time, never at write time.** A stored duration is a
cached conversion, and caching the conversion is what makes it legacy.
Nothing is written back converted. `shelf_life`, `next_check`,
`holds_for` and every `shelf_life_<unit>` name are **refused as literals
in a record**; the derivation returns base units and the reader renders
them in the frame it asked for.

### The acceptance test

> Add a second frame with a different rate, and no existing record needs
> editing. If any record needs editing, the frame leaked into the data.

`frames.py --acceptance` runs it. It adds `venus_days` — deliberately
**not** one of the files in `frames/`, since adding a frame already
registered tests nothing — re-reads all nine records, and checks that
none changed on disk and all still validate.

**And it runs a control beside it**, because a test that adds a frame
nothing reads would pass on a format that had leaked everywhere. The
control writes the same claim in the added frame and requires three
things: it validates under the frame-aware implementation, it is
**refused** by an implementation with `years` welded in, and it derives
the **same shelf life in base units** — or the second frame changed the
claim rather than re-expressing it.

### The reasoning, verbatim from the order

> this is being specified before it's needed because retrofit cost is
> the entire reason the fold detector exists. Building the fold in now,
> knowing it's a fold, would be the same error the tool was written to
> find.

## 1. THE SEVEN FIELDS

| # | field | required shape |
|---|---|---|
| 1 | `assertion` | non-empty, and screened for hedges |
| 2 | `measurement` | `lo`, `hi`, `units` — an interval, not a point |
| 3 | `instrument` | `name`, and `error` with a `kind` and a magnitude |
| 4 | `domain_of_validity` | ≥1 named `condition`, and `outside_this` |
| 5 | `clock` | `holds_for`, and a parseable `next_check` |
| 6 | `derivation` | `parents`, a list; empty needs a `root_reason` |
| 7 | `collapse_record` | a `state`, and what that state requires |
| 8 | `correction_status` | `unadjusted` / `adjusted` / `unknown` |
| 9 | `correction_method` | what was subtracted, by whom, on what decision |
| 10 | `correction_depth` | generations of adjustment inherited, or `UNKNOWN` with a why |

### 1 — assertion, stated without hedges

The assertion states the thing; **the interval in field 2 carries the
imprecision.** A hedge in field 1 is imprecision stated twice — once
where it can be measured, once where it cannot — and the second copy is
what survives when the first is dropped.

Enforced by a 38-word screen. **This is the one field enforced
lexically, and any paraphrase steps around it.** The limit is stated
here, not in a footnote, alongside `UNI_009`, `DF_010` and `ACL_017`,
which are the same limit on other substrates. What it catches is the
fluent failure — reaching for *may*, *appears*, *roughly* without
noticing — which is the one that happens. Screened both ways: a
hedge-free assertion must come back clean, and `mayor`, `somewhere` and
`thereabouts` must not fire.

### 2 — measurement, an interval

`lo`, `hi`, `units`. An inverted interval is refused. **Blank units are
refused: dimensionless is a value and is written as one.**

`lo == hi` is legal only under the field 7 coupling below.

### 3 — instrument, and its known error characteristics

Half of this field is the error, and that half is not optional.
`error.kind` is one of `random`, `systematic`, `both`, `UNQUANTIFIED`.

`UNQUANTIFIED` **carries a `why`**. Without one it is an omission
wearing a sentinel, which is the failure rule two exists to prevent
arriving one level down.

### 4 — domain of validity, the field that always gets stripped

At least one condition, each a `name` and a `value`. Plus
`outside_this`: what is known to happen outside the conditions.
`UNTESTED` is a legal value; an omission is not.

### 5 — the clock, DERIVED and never asserted

Three sub-fields, plus what the claim held fixed and when it was
measured. Nothing else, and in particular **no date**.

| sub-field | is | units |
|---|---|---|
| `neglected_term.held_fixed` | what this claim held fixed | — |
| `measured_on` + `measured_on_frame` | the anchor, and the calendar it is written in | an `instant` frame |
| `time_constant` | how fast that thing changes | any `duration` frame |
| `rate_ceiling` | the fastest background change the claim survives | any `rate` frame |
| `coupling` | sensitivity of the result to the neglected term | the `dimensionless` frame |

**No unit is named in the code.** Each sub-field declares its frame and
the registry resolves it; the derivation works in base units throughout,
so a rate in `per_year` and a time constant in `sols` compare without
either being converted into the other's frame. The calendar is a frame
too and names its own implementation.

Each is a value **with a `basis`**, or `UNMEASURED` **with a `why`**. A
value with no basis is refused: a number typed in with nothing behind it
is the clock asserted one level down.

**Derived, not stored:**

    shelf_life = time_constant / |coupling|
    next_check = measured_on + shelf_life
    regime     = ADIABATIC if 1/time_constant <= rate_ceiling else SUDDEN

**The coupling has to be dimensionless.** A raw partial `dY/dX` carries
the units of the result over the units of the term, and years divided by
that is not a duration. The quantity that works is the elasticity
`(dY/Y)/(dX/X)`, which is what `sheet-structure-scan/coupling.py`
measures by perturbing the constant and reading the output cells — so
for a claim about a workbook the third sub-field is **a measurement, not
a judgement.** `units` must be `"1"`.

**Weak coupling does not shorten the shelf life, and at zero it does not
bound it.** That is a state, `UNBOUNDED_BY_THIS_TERM`, not a large
number — a number would sort.

**A clock that cannot be derived emits nothing.** If the time constant
or the coupling is `UNMEASURED`, the state is `UNDERIVABLE`,
`next_check` is `None`, and there is no branch that can produce a date.
That is the Palestine case and it is the reason the field exists.

**The rate ceiling refines the reading and does not gate the date.**
It gives the regime; the shelf life needs only the time constant and the
coupling. Forcing it would make `UNDERIVABLE` the common case for a
reason section 2 does not give.

### 6 — derivation

`parents`, a list of claim ids. An **empty list is a claim to be a root**
and carries a `root_reason` — without one it cannot be told from parents
that were never recorded, which is rule two again.

`record.py path ID` walks it upward. That is the field's purpose: if a
parent is later refuted, everything resting on it is visible.

### 7 — the collapse record

Three states, and the choice among them is the field's whole content:

| state | means | requires |
|---|---|---|
| `NOT_COLLAPSED` | the measurement is an interval as measured | — |
| `COLLAPSED` | a distribution was reduced, and the statistic is known | `from`, `point`, `why` |
| `COLLAPSED_UPSTREAM` | a point arrived as a point, and the source did not say what it collapsed | `source`, `what_is_unstated` |
| `EXACT` | a count or a definition, so a point *is* the measurement | `basis` |

`point` comes from a **closed vocabulary** — `mean`, `median`, `mode`,
`min`, `max`, `lower_quartile`, `upper_quartile`, `interquartile_range`,
`percentile`, `single_draw`, `other`. Closed, because "a statistic" as
free text is exactly how an upper quartile becomes "the value". With an
`other` escape that must name what it is, because
`uninstrumented/UNI_013` recorded what a vocabulary closed on purpose
costs when a real case does not fit, and the repair it asked for was
this one.

### 8, 9, 10 — the adjustment history

Added by work order 3, S5.

**Field 8 vocabulary.** S5 names the values `raw | corrected | unknown`;
S6 of the same order replaces the state vocabulary with
`adjusted / unadjusted`. **S6 governs** — it is the naming constraint —
and S5's two spellings load as aliases, so a record written to the letter
of S5 still validates and nothing is renamed underneath its author.

**`unknown` is legal and expected.** It is not a gap. A symmetric
residual set whose adjustment history is `unknown` is **uninterpretable**:
a claim that left no lean and one whose lean was removed are the same
artifact from the record, and the schema emits that rather than
defaulting to clean. `interpretable(record, lean_present)` is where it
lives.

**Field 9 has field 7's shape**: what was subtracted, by whom, on what
decision. S5's validation rule — **`adjusted` with a null method does not
validate** — plus each of the three parts required individually, because
a method naming only what was subtracted leaves the decision unrecorded.

**Field 10 keeps zero and unknown apart.** `0` says nothing was
inherited; `{"state": "UNKNOWN", "why": ...}` says nobody looked. A
missing field is neither and is refused.

### THE COUPLING BETWEEN 2 AND 7

Stated separately because it is the part that does work no required-field
list does:

- `lo == hi` under `NOT_COLLAPSED` → **`POINT_WITHOUT_BASIS`.** A point
  arrives either from a distribution or from a count, and saying which
  is the field.
- `lo != hi` under `EXACT` → **`INTERVAL_MARKED_EXACT`.**

Both directions are pinned in the selftest.

---

## 2. THE TWO HARD RULES, AND HOW THEY ARE TESTED

**Rule 3 — a clock asserted rather than derived does not validate.**
`holds_for`, `next_check`, `shelf_life`, `shelf_life_years`,
`shelf_life_base`, `shelf_life_days` and `shelf_life_sols` are refused as
literals in the clock — principle 3, enforced by name. So is a sub-field with a value and no
basis, and `UNMEASURED` with no reason — the two ways to assert it one
level down.

**Rule 1 — a claim with an unresolvable parent does not validate.**
Enforced against the registry, not against the file. A cycle is reported
as `PARENT_CYCLE` with the loop printed, not as recursion.

**Rule 2 — no field is optional.** Seven null arms, one per field: drop
it, and the result must be `INVALID` with `MISSING_FIELD` naming that
field.

**The positive control comes first, and it is why the seven arms mean
anything.** A validator that refuses everything passes all seven. So the
first check is that a complete record validates, and eleven further
checks require specific well-formed variants to validate — `UNQUANTIFIED`
with a reason, `UNTESTED` outside_this, a point from a named statistic, a
resolvable parent.

39 checks, both directions on every rule that has two.

---

## 2b. THE CONSTRAINT ON OUTPUT

The tool reports structure and never labels a record as wrong. `VALID`
and `INVALID` are about **conformance to the record schema** — never
about whether a claim is true, how much weight a measurement carries, or
what to do next, and none of those is computed. The report says so above
the table.

Enforced with the same screen the detector uses, **imported** from
`sheet-structure-scan/no_severity.py` rather than copied, and run over
the emitted report on every invocation.

## 3. WHAT THE SCHEMA DOES NOT HOLD

Found by filling it with six real claims from this repository, not by
inspection. See `CLAIM_TABLE.md` for the measurements.

- **No denominator field.** `129 of 825`, `22 of 22`, `1 of 11` — every
  record puts its denominator in the `units` string. A ratio needs both
  operands named and this schema names one.
- **No sibling relation.** Two claims measured in one run either fake a
  parent edge or are given the same parents. Only the second is honest,
  and the first is what got written before it was caught.
- **The clock is about the instrument, not the claim,** wherever the
  claim is arithmetic on a fixed artifact. A byte-identical file does not
  decay; the reader does.

---

## 4. FALSIFIERS

| # | what would refute the design |
|---|---|
| F1 | a well-formed claim the schema refuses |
| F2 | a claim that validates while a reader would say a field is missing in substance — the sentinel accepted where a real value existed |
| F3 | a hedge that survives field 1 and changes what the assertion licenses |
| F4 | a load path that misses a real dependency, because field 6 records what the author remembered rather than what the claim rests on |
| F5 | a corpus where `COLLAPSED` never occurs, making field 7's stated purpose untested — **fired at `CR_006`, closed at `CR_016` by the hotel factor** |
| F6 | a corpus where no record carries a measured `rate_ceiling`, making the adiabatic/sudden distinction untested — **currently firing, see `CR_017`** |
| F7 | a way to get a date out of the schema without three derived sub-fields behind it |
| F8 | a frame added to the registry that requires any existing record to be edited — the acceptance test, and it is run inside both selftests rather than left as a command someone remembers |
| F9 | a unit that resolves without being registered, or a reader that gets a duration without naming a frame |
