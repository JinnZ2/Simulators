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
