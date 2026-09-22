# INSTRUMENT-INDEX rebuild specification

REBUILT 2026-09-22 from design recovered from session 2026-09-20
transcript fragments. Original bytes lost. Sections marked [RECOVERED]
match recovered text; sections marked [REBUILD-CHOICE] are new.

CC0. stdlib only. Parses under Python 3.9.

---

## What this is

An index of the instruments in one or more repositories: one row per
scannable file, two renderings of the same rows, and one pre-stated
falsifier run on every build.

The index is not a ranking and computes no score. Every field is either
read out of the file, read out of an override, or the literal `UNRATED`.

---

## [RECOVERED] FIELDS

Thirteen, in this order:

```
id name repo path input_shape catches load_bytes load_tok_est
run_cost run_basis status gate built_against
```

---

## [RECOVERED] ENUMS

`input_shape` is multi-valued, pipe-separated:

| value | meaning |
| --- | --- |
| `CLAIM` | a proposition with a truth value |
| `FALSIFIER` | a stated refutation condition |
| `CATEGORY-SET` | the bins themselves, not an item in them |
| `NUMBER` | a quantity, rate, or score |
| `ABSENCE` | a field reading zero / blank / unclear |
| `CORPUS` | a set of documents to be coded |
| `DECISION` | an option set presented for choice |
| `DOCUMENT` | whole-artifact structural checks |
| `AGENT-OUTPUT` | text produced by a model, audited as such |

`run_cost`: `TRIVIAL | LINEAR | QUADRATIC | CORPUS | EXTERNAL | UNRATED`

`run_basis`: `measured | counted-from-source | author-estimate`. It must
be non-empty whenever `run_cost != UNRATED`.

`gate`: `UNRUN` is the default and is NOT the same as `FAILED`.

`status`: `OBSERVED | DERIVED | PROPOSED | UNRATED`
[REBUILD-CHOICE: enum inferred from fixture values]

---

## [RECOVERED] IN-FILE HEADER (preferred)

```
# INSTRUMENT: presented-binary
# INPUT: DECISION|CLAIM
# CATCHES: second option absent from the ballot
# RUN-COST: TRIVIAL (author-estimate)
# STATUS: OBSERVED
# GATE: PASSED
```

Parsed from the leading comment block; stops at the first non-comment
line. The value in parentheses on `RUN-COST` is `run_basis`.

Fallback: `index-overrides.json` keyed by relative path, same fields.
The in-file header wins over the override.

Neither present: the row is emitted `UNRATED`. NEVER drop a file.

[REBUILD-CHOICE] One comment character, `#`, for all four extensions, so
one parser reads `.py`, `.md`, `.sh` and `.txt`.

[REBUILD-CHOICE] A blank line is not a comment line, so a blank line
terminates the leading block. This is the literal reading of "stops at
the first non-comment line". A header placed below a blank line is not
read, and the file is emitted `UNRATED` -- located, not hidden.

[REBUILD-CHOICE] Header keys are exact uppercase. An unknown key inside
the block is ignored, not flagged.

[REBUILD-CHOICE] The `RUN-COST` parenthetical is optional at parse time.
A `run_cost` other than `UNRATED` with an empty `run_basis` is a flag,
not a parse failure.

[REBUILD-CHOICE] The override supplies whole fields; header and override
are merged per field, not per file, so an override can fill a field the
header omits.

---

## [RECOVERED] WALK

```
EXTS        .py .md .sh .txt
SKIP_DIRS   .git __pycache__ node_modules .github
SKIP_NAMES  README.md LICENSE index-overrides.json
            INSTRUMENT-INDEX.tsv build_index.py
            [REBUILD-CHOICE: also skip INSTRUMENT-INDEX.md]
```

`SKIP_DIRS` and `SKIP_NAMES` match by basename at any depth.

---

## [RECOVERED] ROW RULES

- `load_bytes` is the file size. `load_tok_est` is `bytes // 4`, labeled
  ESTIMATE. No tokenizer in the loop.
- `built_against` is the short git hash, else
  `nogit-<sha256 of paths + mtimes, 10 chars>`. Never guess.
- Tabs and newlines in values become spaces.
- A path passed but missing is `NOT-SCANNED`, which is distinct from a
  repo scanned with zero rated rows. Collapsing them reports a coverage
  hole as a zero.

[REBUILD-CHOICE] `id` is `<repo label>:<relative path>`.

[REBUILD-CHOICE] `repo` is the path exactly as passed on the command
line, not resolved or absolutised, so the label a reader sees is the
label the operator typed.

[REBUILD-CHOICE] `built_against` is per repo, and reads `NOT-SCANNED`
for a missing path.

[REBUILD-CHOICE] The `nogit` fingerprint is sha256 over sorted
`relpath\0mtime_ns` lines, first ten hex characters.

[REBUILD-CHOICE] A path that exists and is not a directory is
`NOT-SCANNED` too.

[REBUILD-CHOICE] The unrated sentinel is the literal `UNRATED` in every
unfilled field except `run_basis`, which is empty, because an empty
basis is what the `run_cost != UNRATED` flag condition tests for.

---

## [REBUILD-CHOICE] FLAGS

Emitted to stderr AND to the MD file:

- an `input_shape` value outside the enum
- a `run_cost` outside the enum (e.g. `BOGUS`) -- flag, do NOT normalize
- `run_cost != UNRATED` with an empty `run_basis`
- a `run_basis` outside the enum

Flags never alter the row value.

`status` and `gate` are not flagged. `gate` in particular is open by
construction: `UNRUN` is a default, not a claim about a gate that ran.

---

## [RECOVERED] AXIS CHECK

A pre-stated falsifier, run on every build.

```
rated = rows with input_shape != UNRATED
frac  = rows whose ONLY shape is CLAIM / rated

frac > 0.70 -> "AXIS FALSIFIED: input_shape does not partition;
                fall back to output type
                (verdict/count/branch/refusal)"
else        -> "axis holds at this build"
no rated rows -> "UNRATED: check not run"
```

`frac` is `None` when there are no rated rows. An empty rated set is not
a fraction of zero.

---

## [RECOVERED] TWO RENDERINGS, ONE PASS

`collect()` runs once; both writers read the same rows; neither is
derived from the other; both say GENERATED, do not hand-edit.

**TSV (agent view).** Header comments: stamp, repo states, row count,
estimate note, axis-check, unrated count ("to-do, located, not hidden"),
`total_load_tok_est`, flag count. Then `FIELDS`. Then rows in source
order.

**MD (human view).**

- Build state table: `repo | state | rows`
- Instruments grouped by repo, repos sorted by load cost descending,
  `catches` in the first column
- Axis-check verdict with the 0.70 threshold stated
- Validity flags (committed, not stderr-only)
- Unrated set as a located to-do list
- Coverage-declaration template
- Per repo: `NOT-SCANNED` renders "Unknown contents, not an empty
  repo."; scanned with nothing rated renders "Scanned, no rated
  instruments found (N file(s) unrated)."

CLI:

```
build_index.py --tsv OUT.tsv --md OUT.md repo1 repo2 ...
```

[REBUILD-CHOICE] Repo load cost for the MD ordering is the sum of
`load_tok_est` over that repo's rows. `NOT-SCANNED` repos sort last,
having no load to rank.

[REBUILD-CHOICE] The stamp is UTC ISO-8601 at build time, shared by both
renderings so a diff between them is never a diff in the stamp.

---

## [REBUILD-CHOICE] COVERAGE DECLARATION

The original six lines were not recovered. Proposed:

```
instruments consulted:
instruments in scope but not run:
unrated files in scope:
axis-check verdict at build:
built_against states:
not checked:
```

This template is replaceable when the original turns up.

---

## [RECOVERED] SPEC NOTES TO KEEP

- An estimate labeled as an estimate is usable; an estimate wearing a
  number is not.
- Single drift risk: hand-editing. If the two files differ, regenerate;
  do not reconcile by hand.

---

## What this does not do

It does not read the instrument. `catches` is the author's sentence,
carried; nothing here checks that the instrument catches it. `gate` is
the author's word; nothing here runs a gate. The axis check is a check
on the INDEX -- whether `input_shape` partitions the set -- and not on
any instrument in it.
