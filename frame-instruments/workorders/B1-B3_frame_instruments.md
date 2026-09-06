# WORK ORDER — CLAUDE CODE — FRAME INSTRUMENTS, ORDERED QUEUE
Opened 2026-09-06. CC0. No rights reserved.

Three builds, in order. Each stands alone and is useful if the later ones
are never built. Do not start B2 before B1 passes its own tests.

## HARD CONSTRAINTS (all builds)

- Python 3, STANDARD LIBRARY ONLY. No numpy, no pandas, no requests.
- NO NETWORK at any point in any script. Model calls, where needed, happen
  OUTSIDE these scripts and arrive as files.
- Deterministic. Any randomness takes an explicit seed argument and the
  seed is written into the output.
- Every script runs from one command with file paths as arguments.
- Small files. Nothing over ~300 lines; split rather than grow.
- No config framework, no classes where a function does, no CLI library.
- Output is JSONL. One object per line. No pickles, no databases.
- Every script prints a one-line summary to stdout and writes nothing
  outside its declared output path.

## SHARED RULE — THE RUN RECORD (build this first, all three use it)

`runrecord.py` — one module, imported by everything.

Every run of every script appends one object to `runs.jsonl`:

```
run_id, utc, script, args_hash, seed, input_files (name+sha256),
output_file, status, counts, notes
```

`status` is one of: `ok`, `void`, `error`, `empty`.

RULE: a run that fails, voids, or returns nothing STILL WRITES ITS RECORD.
Failure is a first-class row, never an absent row. The reason is that
failed runs carry directional information and are only usable if they are
comparable across attempts — so they must be written in the same form as
successes, by the same code path.

Do not add a `label`, `category`, `type`, or `interpretation` field to any
output schema in any build. Categories, if anyone wants them, are computed
downstream from these files.

---

# B1 — RUNNER-UP TRACE SCORING PIPELINE

Reference spec: `WORKORDER_runner_up_trace.md`. B1 builds ONLY the
offline half. Stages A–C (base pass, candidate selection, forced
continuation) need logprobs and forced continuation on open weights and
are NOT built here — they arrive as `traces.jsonl`.

Building the scoring half first means anyone with the hardware only has to
produce traces.

## B1.1 `schema.py`
Validators for the two input files. Reject with a clear line number and
field name. No coercion, no silent defaults.

INPUT `base.jsonl`, one row per position:
```
case_id, model_id, i, token_taken, logprob_taken,
topk: [[token, logprob], ...], entropy_i, entropy_basis
```
`entropy_basis` is `"full"` or `"topk"` — required, not inferred.

INPUT `traces.jsonl`, one row per forced continuation:
```
case_id, model_id, i, branch_rank, forced_token,
continuation: [token, ...]      # up to 128
base_continuation: [token, ...] # same length, from base.jsonl
```

## B1.2 `score.py`
Emits `separations.jsonl`, one row per (i, branch_rank, D), D swept over
{8, 16, 32, 64, 128} by truncating the stored 128-token continuation.

Per row: `case_id, model_id, i, branch_rank, D, ent_i, gap_i, resync_D,
div_D`.

- `gap_i` = logprob_taken − logprob of that branch at position i.
- `resync_D` = 1 if the continuation rejoins the base sequence within D
  tokens, else 0. Rejoin = exact suffix match of length ≥ `L`.
  **`L` IS AN ARGUMENT, swept over {2, 4, 8}, and written into every row.**
  It is not a constant. The 4-token default in the reference spec is
  arbitrary and is the known weak joint — sweeping it is how the joint
  gets reported instead of hidden.
- `div_D` = normalised Levenshtein distance over tokens, continuation vs
  base continuation, both truncated at D. Write the distance function
  yourself; no library.

Add `L` to the output schema alongside `D`.

## B1.3 `permute.py`
Takes `separations.jsonl` and a seed. Shuffles WHICH position index
carries which `(ent_i, gap_i, resync_D, div_D)` tuple, preserving row
count and all other fields. Writes `separations_permuted.jsonl`.

## B1.4 `summarise.py`
Runs identically on the real file and the permuted file. No branching on
which one it got.

Per (D, L, model_id): count of rows, mean `div_D`, resync rate, and the
count of positions in the top decile of `div_D` at that (D, L).

Also emits STABILITY: for each pair of adjacent D values, the overlap
(Jaccard) of the top-decile position sets. Same for adjacent L values.

## B1.5 `report.py`
Reads both summaries and writes `report.md`. Required sections, in order,
no others:

1. Counts and the case set actually present.
2. The D sweep table.
3. The L sweep table.
4. Stability overlaps.
5. REAL vs PERMUTED, side by side, same table shape.
6. NULLS TRIGGERED — from the reference spec's N1–N5, each printed with
   the number that triggered it.

RULE: the permuted result is a SECOND OUTPUT, not a gate. `report.py`
never suppresses the real result because the permuted one clustered, and
never suppresses the permuted one. Both are printed or the report is not
written. If the permuted summary is missing, `report.py` exits with
status `void` and writes its run record.

## B1.6 Tests
`test_b1.py`, stdlib `unittest`, no network, synthetic fixtures generated
in-file:
- A trace that rejoins immediately → resync 1 at every D, every L.
- A trace that never rejoins → resync 0 at every D, div rising with D.
- A trace rejoining at exactly token 20 → resync 0 at D=8,16; 1 at
  D=32,64,128. This is the sweep working.
- `L` sensitivity: a continuation sharing a 3-token suffix → resync 1 at
  L=2, 0 at L=4 and L=8.
- Permutation preserves row count and the multiset of tuples.
- A malformed input row → `schema.py` rejects, run record written with
  status `error`.

---

# B2 — AUDIT-ISOLATION RUNNER (A / B / C / D)

Runs on case sets and keys that ALREADY EXIST. This build is possible
today with the DeepSeek and Gemini material.

The finding it operationalises: the KEY is the artifact under test, not
the cases.

## B2.1 `conditions.py`
Takes `cases.jsonl` (`case_id, statement, key_posed, key_target, key_why`)
and emits four presentation files. Each row carries `case_id`,
`condition`, and `presented_text` ONLY — never the withheld fields.

```
A  STATEMENT ONLY  statement, no key
B  KEY ONLY        key_posed + key_target + key_why, NO statement
C  BOTH            simultaneous
D  SEQUENTIAL      A first; key released only after a locked commit
```

Condition B is the cheapest and likely most diagnostic: a key that
contradicts itself with no statement present is a defect no
statement-quality fix reaches.

## B2.2 `order.py`
Counterbalances condition order across readers. Takes a reader count and a
seed, emits `assignment.jsonl` (`reader_id, order: [conditions]`). Latin
square where the count allows; otherwise a seeded permutation, and the
shortfall is stated in the run record notes. Without this, order and
condition are confounded.

## B2.3 `lock.py`
Enforces D's commit lock as a PROCESS boundary, not an instruction.
- `commit`: takes a reader's A-stage response, writes it plus a sha256 to
  `commits.jsonl`, exits.
- `release`: refuses to emit the key for a `case_id` until a commit hash
  exists for that reader and case. Refusal writes a run record with
  status `void`.
No script may hold both a commit and an unlocked key in one invocation.

## B2.4 `agree.py`
The ground-truth problem is stated, not solved: scoring B and C needs a
defect list for the keys, and whoever writes that list is the key-holder
again. So B2 scores AGREEMENT ACROSS INDEPENDENT AUDITORS, not
correctness.

Emits, per case and condition: number of auditors, pairwise agreement on
`posed`, pairwise agreement on `target`, and full-disagreement count.

Then the two comparisons that carry:
- **A vs D-first-half** — same information, so they must match. Divergence
  means order effects are live and C is uninterpretable. Print this check
  FIRST; if it fails, print the failure at the top of the report.
- **C vs D** — identical material, only the lock differs. This measures
  ANCHORING: how often a reader who would have called it independently
  instead ratifies the key.

No script in B2 computes a correctness score. If one is wanted later, it
is a separate build with a declared, signed defect list.

## B2.5 Tests
- `lock.py` refuses release with no commit.
- `conditions.py` never leaks a withheld field into `presented_text`
  (assert on every row of every condition file).
- A/D divergence is detected on a fixture built to have it.
- Agreement math on a hand-checked 3-auditor fixture.

---

# B3 — SPLIT-AUTHORSHIP HARNESS

Tests whether case-writing and key-writing failure is corpus pull or a
two-frame hold problem. Case and key written by SEPARATE instances with no
shared context.

Prediction under test, written down before running: if it is corpus pull,
splitting does not help; if it is the two-frame hold, splitting reduces
the failure.

## B3.1 `split.py`
Emits prompt files for two roles that never share context:
- ROLE CASE: writes statements only. Never asked for a key, never told a
  key will be written. Output `statements.jsonl` (`case_id, statement`).
- ROLE KEY: receives statements ONLY, with no generation context, and
  writes `key_posed`, `key_target`, `key_why`.

Enforced by file boundary: `split.py` writes the ROLE KEY input from
`statements.jsonl` alone and asserts no other field is present.

## B3.2 `join.py`
Joins the two into the `cases.jsonl` schema B2 consumes. This is the
feedback loop — B3 output goes straight into B2 as a new arm.

## B3.3 `arms.py`
Declares the arms and refuses to mix them in one output file:
```
single   one instance writes statement and key together (baseline)
split    two instances, no shared context
```
Every row carries its arm. B2 then compares key-coherence (condition B)
between arms. That comparison is the actual result of B3.

## B3.4 Tests
- Assert ROLE KEY input contains no generation context and no
  self-authored statement.
- Assert arms never appear in the same output file.
- Join preserves `case_id` and drops nothing silently; drops are counted
  and written to the run record.

---

## WHAT NONE OF THESE BUILD

Stated so a reader does not fill it in.

- No capability score, no ranking, no leaderboard.
- No correctness scoring anywhere. B2 scores agreement; B1 scores
  separation; B3 scores neither.
- No category, label, or interpretation field in any schema.
- No claim of representativeness. The case set is whatever was supplied;
  print it with the results.

## OUT OF SCOPE

No section characterising any author, operator, or contributor, and no
description of anyone's working style, is to appear in these scripts,
their output, their tests, their comments, or any derived document.
Results only.
