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

### 5 — the clock

`holds_for`, and a `next_check` that parses as an ISO date. No claim
without one. `record.py due --on DATE` turns the field into a state:
`CURRENT`, `DUE`, or `UNPARSEABLE`.

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
| `COLLAPSED` | a distribution was reduced | `from`, `point`, `why` |
| `EXACT` | a count or a definition, so a point *is* the measurement | `basis` |

`point` comes from a **closed vocabulary** — `mean`, `median`, `mode`,
`min`, `max`, `lower_quartile`, `upper_quartile`, `interquartile_range`,
`percentile`, `single_draw`, `other`. Closed, because "a statistic" as
free text is exactly how an upper quartile becomes "the value". With an
`other` escape that must name what it is, because
`uninstrumented/UNI_013` recorded what a vocabulary closed on purpose
costs when a real case does not fit, and the repair it asked for was
this one.

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
| F5 | a corpus where `COLLAPSED` never occurs, making field 7's stated purpose untested — **this one has already fired, see `CR_006`** |
