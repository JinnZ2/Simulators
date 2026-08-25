# claim-record

Seven fields per claim, two hard rules, and a validator that refuses.

Delivery in [`SOURCE_DROP.md`](SOURCE_DROP.md), spoken, verbatim.
Schema in [`SPEC.md`](SPEC.md). Findings from filling it with six real
claims in [`CLAIM_TABLE.md`](CLAIM_TABLE.md).

```
python3 record.py validate            every record, with findings
python3 record.py path SSS_022b       the load path, walked upward
python3 record.py due --on 2026-08-25 whose next-check has passed
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

## What the six real records showed

Filled with claims from the `sheet-structure-scan/` run earlier the same
day, where the provenance is known. All six validate — and the useful
part is what came back uniform:

| field | corpus |
|---|---|
| `collapse_record.state` | **`EXACT` 6, `COLLAPSED` 0** |
| `instrument.error.kind` | `systematic` 6 |
| `domain_of_validity.outside_this` | contains `UNTESTED` 6 |
| `measurement` units carrying a denominator | **6** |

**Field 7's stated purpose — the upper-quartile field — has zero
instances** (`CR_006`). Not carelessness: every instrument here is
deterministic and every artifact a fixed file, so every measurement is an
exact count and `EXACT` is correct in all six. Fields 2 and 7 are aimed
at measurements with sampling error and this folder has not made one. The
selftest exercises the branch; the corpus does not, and those are
different things.

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

39 selftest checks. Rule two gets seven null arms, one per field, and the
**positive control comes first**: a validator that refuses everything
passes all seven.

CC0. Stdlib only. Parses under Python 3.9.
