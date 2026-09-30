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
