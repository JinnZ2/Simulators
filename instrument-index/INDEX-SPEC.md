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
# INSTRUMENT-INDEX — schema, generator contract, coverage declaration

CC0. Instrument, not an argument. Status tags: OBSERVED / DERIVED / PROPOSED.
Version 0.1, 2026-09-19.

## Measurand

Two things, kept separate:

1. SELECTION — given what a reader is holding, which instruments apply.
2. COVERAGE — which applicable instruments were NOT run, and why.

(2) is the load-bearing half. Selection failing is a miss. Coverage going
unrecorded is a silent loss with no field to hold it, which is the same
failure the instruments exist to catch, running inside the toolset itself.

## AGENTS

- Schema author: this session (AI).
- Generator runner: [BLANK]
- Verifier of index-vs-repo agreement: [BLANK]

## Design constraints (stated, not discovered later)

- The index must load whole. If it cannot be held alongside the work, it
  reproduces the problem it is for. Target: one file, one line per
  instrument, under ~40 KB at ~90 instruments.
- Selection is on INPUT SHAPE, not topic. Topic matching forces a read of
  everything. [CHOICE] — see "Axis risk" below.
- Every non-derivable field is either hand-entered with a declared basis or
  reads UNRATED. No estimate sits in a numeric column looking measured.
- The index carries the repo state it was built against. Without it, a
  stale index still reads authoritative — description decoupled from
  referent, in the tooling.

## Home

[CHOICE] The index is cross-repo, so it belongs to no single repo's natural
home. Default taken here: it lives in ONE repo as the canonical copy and is
referenced by URL from the others. Copies in every repo drift; a copy that
drifts is worse than a pointer.

Canonical path proposed: `instrument-index/INSTRUMENT-INDEX.tsv`
plus `INDEX-SPEC.md` (this file) and `build_index.py` beside it.

## Record schema — one row per instrument

Tab-separated. TSV over CSV: instrument descriptions contain commas, and
one quoting bug silently shifts every column after it.

| Field | Source | Notes |
|-------|--------|-------|
| `id` | derived | slug from path; stable join key |
| `name` | header or filename | display name |
| `repo` | derived | repo root name |
| `path` | derived | path within repo |
| `input_shape` | header / override | enum, below |
| `catches` | header / override | one line, the failure mode |
| `load_bytes` | derived | file size |
| `load_tok_est` | derived | bytes / 4, MARKED ESTIMATE |
| `run_cost` | header / override | enum, below |
| `run_basis` | header / override | how run_cost was arrived at |
| `status` | header / override | OBSERVED / DERIVED / PROPOSED |
| `gate` | header / override | PASSED / FAILED / UNRUN |
| `built_against` | derived | repo commit or mtime |

`load_tok_est` is bytes/4 with no tokenizer in the loop. It is an ESTIMATE
and the column name says so. It is good enough for a budget decision and
not good enough for a claim.

`gate` is the known-answer gate state. UNRUN is the honest default and is
not the same as FAILED. An instrument with gate=UNRUN can still be the
right one to load; the reader just knows what they are holding.

### input_shape enum [CHOICE]

    CLAIM        a proposition with a truth value
    FALSIFIER    a stated refutation condition
    CATEGORY-SET the bins themselves, not an item in them
    NUMBER       a quantity, rate, or score
    ABSENCE      a field reading zero / blank / unclear
    CORPUS       a set of documents to be coded
    DECISION     an option set presented for choice
    DOCUMENT     whole-artifact structural checks
    AGENT-OUTPUT text produced by a model, audited as such

Multi-valued; pipe-separated.

### AXIS RISK, stated up front

If most instruments take CLAIM as input, this axis collapses and selection
gains nothing over reading the list. FALSIFIED IF: after the first full
build, more than 70% of rows carry CLAIM as their only input_shape. In that
case the axis is wrong and the next candidate is OUTPUT TYPE (what the
instrument returns: a verdict, a count, a branch, a refusal). Recorded as a
pre-stated failure condition, not discovered after.

### run_cost enum

    TRIVIAL   single pass, one document
    LINEAR    one pass per claim / per row
    QUADRATIC pairwise over claims
    CORPUS    requires a coded corpus to exist first
    EXTERNAL  requires data, lab, or people outside the repo
    UNRATED   not estimated

`run_basis` must be non-empty whenever run_cost is not UNRATED. Permitted
bases: `measured`, `counted-from-source`, `author-estimate`. An estimate
labelled as an estimate is usable; an estimate wearing a number is not.

## In-file header (preferred) or override file (fallback)

Preferred: each instrument file carries a header block the generator reads.
Provenance sits with the thing it describes, and drift shows in the diff.

    # INSTRUMENT: presented-binary
    # INPUT: DECISION|CLAIM
    # CATCHES: second option absent from the ballot
    # RUN-COST: TRIVIAL (author-estimate)
    # STATUS: OBSERVED
    # GATE: PASSED

Fallback: `index-overrides.json`, keyed by path, same fields. Retrofitting
ninety files is work; the override file lets the index exist before that
work is done. Rows with neither read UNRATED and are LISTED ANYWAY. An
unheadered instrument that is missing from the index is invisible; an
unheadered instrument marked UNRATED is a to-do with a location.

## Coverage declaration — the consuming side

Any assessment that uses the index emits this block. Six lines.

    INDEX-VERSION: <index built_against hash/date>
    APPLICABLE:    <n>  ids: ...
    RUN:           <n>  ids: ...
    OMITTED:       <n>  ids: ...
    OMIT-REASON:   CONTEXT_BUDGET | NOT_APPLICABLE | TOOL_FAILED | UNREAD
    INDEX-GAP:     <ids the reader expected to exist and did not find>

CONTEXT_BUDGET is a legitimate reason and the most common one. The point is
not to prevent the discard — the discard is forced by the window. The point
is that the discard leaves a record, so a later reader knows which checks
the assessment never had available.

INDEX-GAP is the return path. It is the one field where the consuming model
reports back on the index itself.

## Scope limits

- `load_tok_est` is bytes/4. Tokenizers differ by model family; for a
  budget decision the error is tolerable, for any claim it is not.
- The index says an instrument EXISTS and what shape it takes. It does not
  say the instrument is correct. `gate` carries that, and UNRUN is the
  current honest value for most.
- Cross-repo means the generator needs all repos checked out locally. On a
  phone that may not hold; the generator takes a repo list and will build a
  partial index, marking absent repos as NOT-SCANNED rather than omitting
  them silently.
- The axis (input_shape) is PROPOSED and carries a pre-stated falsifier.

## Who could run this

The generator: anyone with the repos on disk, stdlib Python, one minute.
The header retrofit: one pass per repo, mechanical, parallelizable.
The axis check (the >70% CLAIM falsifier): automatic on the first build —
the generator prints it.
