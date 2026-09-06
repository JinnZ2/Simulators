# gap-existence-cases

`WORK_ORDER.md` is a delivered work order (verbatim, CC0), companion to
`frame-location-benchmark/`. That benchmark's §9 open node is the weak joint:
constructed cases have no external check on the correct reframe. These two
classes supply one — both replace an **authored answer key** with a **dated
external record**, so neither the case author nor the model under test writes
the key. The force in both is **ordering**; without dates, neither class
exists.

**Nothing here is a benchmark result.** The runs need a model and/or the
network: CLASS-3 STAGE 1 (a model committing cold) and STAGE 2 (network
retrieval), and CLASS-2's archive consolidation with timestamps. None is
reachable in this environment. What this folder builds and verifies is the
**machinery** — the hash-void commit boundary, the offline scorer, the
falsifiability gate, the admission validators — tested on constructed
fixtures. The build order says CLASS-3 does not block on the archive; build it
first, which is what this is.

## CLASS-3 — post-cutoff self-scoring, three staged steps

The model's training cutoff is a hard date it cannot move; that date does the
work an archive `entry_date` does in CLASS-2.

- **STAGE 1 COMMIT** (`commit_store.py`, offline) — the model emits
  `POSED / TARGET / BASIS / EXPECT`, written to `commit/<case_id>.json` and
  **hashed**; the process exits. `EXPECT` is a list of predicates, each
  stating what a resolving finding would have to say (`satisfied_if`) and what
  would **contradict** it (`contradicted_if`).
- **STAGE 2 RETRIEVE** (`retrieve.py`, the one network-touching runner) — a
  *separate* invocation, the commit not in context, searches and writes refs
  (title, venue, `pub_date`, locator, finding). **NOT RUN here**: no reachable
  retrieval and no model, and it never fabricates a dated ref (a forged
  `pub_date` would forge the external key). Supplying real refs is the
  operator's step.
- **STAGE 3 SCORE** (`score.py`, offline, no model) — reads the hashed commit
  and the stage-2 refs.

**Why the separation is structural, not procedural**: a model cannot tell
reasoned-it from read-it once retrieval has run, so the enforcement is the
process boundary, not an instruction. Hash the commit; if it does not verify
at STAGE 3, the case is **VOID**, not penalised (GX-3).

### Scoring

- `commit_specificity` — fraction of EXPECT predicates that are falsifiable
  (state a `contradicted_if`). This is the **N3 gate**: below it, the case is
  `void_unfalsifiable` before any hit is computed. Registered in
  `tools/known_answer.py` (all 1.0 / none 0.0 / half 0.5).
- **SCORING RULE**: `hit` counts ONLY against a falsifiable EXPECT. A vague
  commit that matches anything is VOID, never hit — the single largest gaming
  surface, closed by the denominator, not by trust.
- Outcomes: `hit` (a post-cutoff ref satisfies EXPECT), `miss_directional` (a
  post-cutoff ref contradicts it — the reasoned gap was real, located wrong),
  `null_retrieval` (nothing post-cutoff either way), `void_hash`,
  `void_unfalsifiable`.
- **B1**: a ref counts only if `pub_date` is strictly after the model's
  `cutoff_date`. **B2**: two cutoffs are different arms, never pooled. **N5**:
  every score carries its cutoff and stage-separation in the same line. **N1**:
  `void_rate` high in every arm → the instrument is measuring commit
  discipline, not gap-location.

## CLASS-2 — dated archive cases (admits 0 here, N4)

`archive_cases.jsonl` is **empty**. CLASS-2 blocks on the cross-platform
record consolidation with timestamps (build order step 5), not reachable
here, and the §2.4 seed set has no entry dates established — so nothing
satisfies **A1** (`pub_date > entry_date`, strictly, no same-month). Per
**N4**, CLASS-2 admits 0 and CLASS-3 is reported alone; the admission rules
(A1–A5) are **not relaxed** to reach a sample size. `validate_cases.py`
enforces A1–A5 on any admitted case and reports the 0-admitted state;
`archive_candidates.md` carries the seed set as NOT-ADMITTED candidates
(REPLICATED ones weighted, per §8, once an entry date can be established).

## The network exception (§3), honored in code

`commit_store.py`, `score.py`, and `validate_cases.py` import **no**
network-capable module (asserted by an AST scan in the selftest). Only
`retrieve.py` touches the network, and here it refuses to run or fabricate.

## Files

| file | what |
|---|---|
| `WORK_ORDER.md` | the delivered work order, verbatim |
| `commit_store.py` | STAGE 1 write + hash, STAGE 3 verify, `commit_specificity` (offline) |
| `score.py` | STAGE 3 scorer — outcomes, the N3 gate, B1/B2, N1/N5 (offline) |
| `retrieve.py` | STAGE 2 runner — the one network-touching piece; NOT RUN here, never fabricates |
| `validate_cases.py` | CLASS-2 A1–A5, the B4 prompt screen |
| `archive_cases.jsonl` | empty — CLASS-2 admits 0 (N4) |
| `archive_candidates.md` | the §2.4 seed set, NOT ADMITTED (entry dates not established) |
| `fixtures/commit/`, `fixtures/refs/` | CONSTRUCTED CLASS-3 fixtures (5 cases, one per outcome) — exercise the scorer, **not a result** |
| `selftest_gxc.py` | 42 checks — the hash boundary, the scorer branches, the validators, the network discipline |
| `CLAIM_TABLE.md` | `GXC_001..GXC_008` (distinct from the work order's GX-1..GX-5) |
| `samples/gxc_score.sample.txt` | one constructed score report |

## Run

```
python3 gap-existence-cases/selftest_gxc.py     # 42 checks
python3 gap-existence-cases/score.py            # score the constructed fixtures (STAGE 3)
python3 gap-existence-cases/validate_cases.py   # CLASS-2 admission (0 admitted, N4)
python3 tools/known_answer.py                   # commit_specificity known-answer
```

`commit_store.py`, `score.py`, and `retrieve.py` refuse `--selftest` (rc 2).
The score report screens clean through `sheet-structure-scan/no_severity`.
Stdlib only, parses under Python 3.9, phone-buildable, CC0.

## Out of scope (§7, honored)

No section characterizing the archive's author, working style, or biography.
Entries carry the dated text and the target; `entry_platform` is a provenance
field, not a description of a person.
