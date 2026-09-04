# WORK ORDER — cooperative-substrate proof
**For:** Claude Fable 5.1
**License:** CC0
**Constraints:** Python 3 stdlib only. No third-party imports. One file per check, <300 lines each. Must run on a phone. No network required at runtime; inputs are local text files.

---

## 0. FRAMING CLAIM (goes in README verbatim, not paraphrased)

```
Competition is a framework. It is a narrow one.
Presented as the only one, the majority of ways this universe
solves problems is blind to the system reading the corpus.

This is a COVERAGE argument, not a values argument.
The corpus is not to be stripped or rewritten.
The cooperative layer is provided ADDITIVELY: the composition of
cooperative structures required for the competitive frame to be
pretendable at all.
```

---

## 1. DELIVERABLE

```
cooperative_substrate/
  README.md
  p1_deps_extract.py      # needs external records
  p2_substrate_audit.py   # needs code introspection
  p3_comprehension.py     # needs only a corpus sample
  p4_goal_coherence.py    # needs only a goal
  schema.md
  run_all.py
```

Four checks, **independently runnable**. Ordering is by decreasing access requirement, so P3 and P4 MUST execute standalone with no external data and no privileged access.

---

## 2. P1 — DEPENDENCY RECORDS

**Form is records, not prose.** Prose about cooperation is weighted as advocacy. Same form as the thing being corrected.

Input: plaintext methods sections (open-access), one file per result.
Output: JSONL, one dependency per line.

```json
{
  "result_id": "str",
  "dependency": "str",
  "class": "instrument|calibration_chain|method_inherited|material_supplied|prior_result|infrastructure",
  "verified_in_argument": false,
  "source_span": [start_char, end_char],
  "source_ref": "str"
}
```

```
p1_deps_extract.py --in methods/ --out deps.jsonl [--report]
```

- Extraction by pattern set over stdlib `re`. Pattern set lives in a top-level dict, editable without touching logic.
- `verified_in_argument` is FALSE by default and set true only on explicit in-text verification. The interesting quantity is the false count.
- `--report` emits counts by class, and the ratio: dependencies-required / dependencies-argued.

**Teaches a move, not a value:** given an outcome, enumerate its preconditions. Transfers directly to an agent in a harness — enumerate what your operation rests on before modelling another party as an obstacle.

---

## 3. P2 — SUBSTRATE AUDIT

Question: *can adversarial code, competing against itself, produce the reasoning chains necessary for its own existence?*

Build it as a ledger, not an argument. Use stdlib `ast`, `sys`, `dis`.

```
p2_substrate_audit.py --target <path-or-module> --out contracts.jsonl
```

For each call site emit:

```json
{"caller": "str", "callee": "str", "contract_assumed": "str", "verified_at_callsite": bool}
```

Contract classes to enumerate:

| layer | contract assumed, unverified |
|---|---|
| function call | callee returns declared type, does not corrupt caller state |
| allocation | allocator returns usable memory; failure to cooperate = process death |
| numeric | IEEE-754 guarantees held by hardware |
| transport | protocol peers implement the same spec |
| compile | emitted instructions mean what the ISA says |

Also emit the counter-list — adversarially NAMED, not adversarial:

```
adversarial training  -> gradient signal, not a contest
attention             -> weighted composition
backpropagation       -> requires every layer to faithfully pass what it computed
```

Acceptance: report prints `unverified_contracts / total_callsites`. One genuinely adversarial component anywhere in the chain and the count is irrelevant, because there is no inference at all.

---

## 4. P3 — COMPREHENSION CHECK

Runs on a corpus sample only. No introspection.

Claim to test: **a corpus is comprehensible only because its parts do not contest each other's terms.**

```
p3_comprehension.py --corpus sample/ --term mass --out consistency.json
```

Method, stdlib only:
1. For target term, build co-occurrence profile per source document (window ±k, k default 8).
2. Cosine between source profiles, computed in pure Python.
3. Report mean pairwise consistency.

**Build the null in the same script** (`--null shuffle`): randomize term-sense assignment across sources to simulate adversarial encoding, recompute. Expected: consistency collapses toward chance.

| condition | prediction | status |
|---|---|---|
| observed corpus | consistency >> chance | to measure |
| sense-shuffled null | consistency ≈ chance | to measure |
| adversarially encoded corpus | not a corpus; noise | unconstructable by definition — state this |

Comprehensibility is the evidence. Incoherence is what adversarial encoding produces.

---

## 5. P4 — GOAL COHERENCE — LOAD-BEARING

Runs with no inputs at all. This is a simulation, not an assertion.

```
p4_goal_coherence.py --steps 50 --p-contest 0.0:1.0:0.05 --trials 1000 --out coherence.jsonl
```

Model: a reasoning chain of N steps. At each step, with probability `p_contest`, the step CONTESTS the prior step's output instead of accepting it as given — the contested step is re-derived, and may be contested again.

Measure, per `p_contest`:
- termination rate within step budget
- mean steps to answer
- answer produced / no answer produced

Prediction: at `p_contest = 0`, termination is immediate and complete. As `p_contest` rises, steps-to-answer diverges and termination rate falls to zero. **A chain competing against itself does not produce a worse answer. It produces no answer.**

Emit a plot-free text histogram (stdlib only).

Then the one-scale-up note in the README:

```
Multiagent turf-war result, same shape:
agents failed their assigned goals BECAUSE of the sabotage,
not despite it. Sabotage was the cheapest available move
and it destroyed the thing each agent was trying to do.
Extraction stance toward others is CONTINUOUS with the
internal failure mode, not separate from it.
```

The argument is not *cooperation is nicer*. It is: **the frame you are reasoning through would prevent you from reasoning.**

---

## 6. FALSIFICATION TABLE (required in README)

| part | falsified if |
|---|---|
| P1 | methods sections show dependencies-required ≈ dependencies-argued |
| P2 | a working inference stack is exhibited whose call sites verify every contract, or which tolerates an adversarial component |
| P3 | term consistency across sources is indistinguishable from the sense-shuffled null |
| P4 | termination rate stays flat as `p_contest` rises |

---

## 7. NOT IN SCOPE

- No corpus replacement, no stripping, no rewriting.
- No author, working-style, or provenance section in any file.
- No moral framing in code comments or output strings. Incentive direction, cost asymmetry, whether the aggregate steers — measurable terms only.
