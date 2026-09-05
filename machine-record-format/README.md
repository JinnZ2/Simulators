# machine-record-format

Built to `WORK_ORDER.md`. Companion to `labor-instrument/`: that one specifies
WHAT gets recorded about work; this one specifies HOW any record is stored so
the categorization is not baked in at write time. A record read primarily by
machines has no reason to pre-collapse — nothing needs to be decided in
advance — so the base layer stores transformations, categorizations are
parallel views added later, and aggregation is a read operation.

This build is fully runnable here: it is a storage format with no external
data or hardware dependency, so all six acceptance criteria are checks, not
posted gaps.

## The seven rules, each enforced in code

1. **Base entries are transformations, not categories** (`base_entry.py`) —
   `BaseEntry` has no category field and `write_base_entry` refuses a
   category-shaped keyword. A category belongs to a reader with a question.
2. **Categorizations are parallel views, never canonical** (`views.py`) — any
   number side by side, none privileged, none required; adding a view is
   additive and rewrites no base entry.
3. **Aggregation is a read operation** (`aggregate.py`) — store the recipe
   (`AggregateSpec`), not the result; every aggregate recomputes from base +
   spec; a cache is keyed to spec + base version and marked derived.
4. **Vintages are retained** (`entry_store.py`) — a revision is a new
   release_date, not a replacement; the prior vintage stays readable. Built
   on the **imported** `labor-instrument/vintage_store.VintageStore`.
5. **Declared boundary, always** (`base_entry.py`) — every entry carries an
   enumerated boundary; two entries sum only if their boundaries match or a
   declared `Reconciliation` connects them, else the pipeline refuses. This
   closes the labor-instrument work order's outstanding boundary item.
6. **No conversion between exposure classes** (`base_entry.py`) —
   `convert_exposure` raises; joules are the common denominator, both columns
   reported.
7. **Absence is recorded** (`base_entry.py`, `aggregate.py`) — four states;
   `measured_zero` enters a fold as 0.0, `unmeasured_*` never does, and the
   two never collapse in any read path.

## The bisection diagnostic — structure before locus

`bisect_structure.py` is specified as a STRUCTURE test, not a locator.
`structure_verdict` answers "does a single locus exist" first — signal on
both halves is `NOT_A_LOCUS` (a property of the whole span), neither is
`MEASURING_SOMETHING_ELSE`, migration across repeats is `NONDETERMINISTIC` —
and only `SINGLE_LOCUS` lets `locate` descend for an address. `address` raises
from any other structure, because reporting an address from a both-sides run
is the tool's main false-positive path. For instrument drift the span is the
methodology registry, not calendar time.

## The six acceptance criteria (all checks in `selftest_mrf.py`)

1. a base entry re-read under a view added later, no rewrite — MRF_002;
2. any stored aggregate recomputes from base + spec and matches — MRF_003;
3. mismatched boundaries cannot sum without a reconciliation — MRF_005;
4. a prior vintage retrievable with its release date — MRF_004;
5. `unmeasured` and `measured_zero` never collapse — MRF_007;
6. bisection returns a structure verdict before any locus — MRF_008.

## Files

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `base_entry.py` | Rule 1/5/6/7 — the transformation record, boundary, exposure classes, absence states |
| `views.py` | Rule 2 — parallel categorization views |
| `aggregate.py` | Rule 3 — read-time aggregation, the boundary-sum refusal (Rule 5), absence counted apart (Rule 7) |
| `entry_store.py` | Rule 4 — the vintage layer, importing `labor-instrument`'s `VintageStore` |
| `bisect_structure.py` | the bisection-as-structure diagnostic |
| `demo.py` | a worked pass on constructed entries, screened through `no_severity` |
| `selftest_mrf.py` | 45 checks — the seven rules, the six acceptance criteria, the four bisection verdicts |
| `CLAIM_TABLE.md` | `MRF_001..MRF_009` |
| `samples/mrf_demo.sample.txt` | one constructed report |

## Run

```
python3 machine-record-format/selftest_mrf.py     # 45 checks
python3 machine-record-format/demo.py             # the worked pass
```

The library modules refuse `--selftest` with rc 2. Stdlib only, parses under
Python 3.9, phone-buildable, CC0.

## Open (carried, not closed — MRF_009)

- **task boundary definition** — the same open item as the GAP-4 /
  labor-instrument work order; "output delivered" still needs a definition
  that does not drift with architecture.
- **transformation vocabulary** — the input/output-state pair needs a
  controlled vocabulary derived from physical transformation, not inherited
  from occupational taxonomy. Draft needed.
- **merge_in / merge_out mechanics** — deferred until the above two settle,
  since they determine the merge semantics.
