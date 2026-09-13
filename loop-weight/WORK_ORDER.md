# WORK ORDER — `loop_weight.py`

Source-relevance weighting on feedback-loop structure.
CC0. Python 3, stdlib only. No network. Phone-buildable.

---

## 1. MEASURAND

For a source reporting on a system, measure how much information about
that system the report can carry.

Three quantities. They are **not** combined into a single score.

| # | Symbol | Name | What it measures | Units |
|---|--------|------|------------------|-------|
| 1 | `L` | loop length | hops between the action/decision and the observation the source made | integer ≥ 0 |
| 2 | `R` | per-hop retention | fraction of signal surviving each hop, per hop | float 0.0–1.0, or `None` |
| 3 | `C` | calibration | whether the source's reading maps to the thing | float 0.0–1.0, or `None` |

`L` is topology. `R` is channel. `C` is whether the instrument is
pointed at the right thing.

They can disagree. A short loop through a lossy channel may carry less
than a longer clean one. A one-hop instrument that is always wrong
reports no noise **within its own frame** and must not score high.

---

## 2. HARD CONSTRAINTS

```
- stdlib only. no numpy, no pandas, no requests.
- single module + single test file. both runnable on a phone.
- no network calls anywhere, including tests.
- CC0 header on both files.
- NO scalar collapse. any function returning one number that
  stands in for all three is out of spec.
- NO authority terms. the module must contain no field, weight,
  or parameter named or derived from: credential, title, rank,
  seniority, institution, citation count, follower count,
  publication venue, volume, reach.
  these are the quantities being replaced. their presence is a defect.
- C is NEVER self-reported. no code path may set C from a claim
  made by the source about itself.
```

---

## 3. CALIBRATION — the constrained term

`C` has exactly two admissible derivations. Implement both.

```
C-1  DISAGREEMENT
     C derived from divergence against >=1 independent instrument
     observing the same referent.
     independence must be asserted per pair and stored; if the two
     instruments share a hop, the pair is not independent and is
     excluded.

C-2  OUT-OF-FRAME OUTCOME
     C derived from the source's prior predictions scored against
     outcomes the source did not define, select, or time.
     predictions must be timestamped before outcome resolution.
```

If neither is available, `C = None` and the return enum is
`UNCALIBRATED`. Not a default value. Not an imputed mean.

---

## 4. RETURN ENUM

```python
class LoopRead(Enum):
    SHORT_CALIBRATED     # low L, C known and high
    SHORT_UNCALIBRATED   # low L, C is None        <- the confident-wrong case
    SHORT_MISCALIBRATED  # low L, C known and low
    LONG_CALIBRATED      # high L, C known and high
    LONG_UNCALIBRATED    # high L, C is None
    LONG_MISCALIBRATED   # high L, C known and low
    LOSSY                # R below threshold, dominates regardless of L
    INSUFFICIENT         # L itself unknown; no read possible
```

**Every member must be reachable by at least one case in the test set.**
A declared member that no path populates is a defect: a reader cannot
distinguish *no such case was found* from *nobody looked*.

---

## 5. WORKING NULL — hand-built case set

Ship `cases.py` with a minimum of 8 hand-built cases, one per enum
member. Each case is a dict with the raw inputs only — no precomputed
scores. At least these four must be present and must resolve as marked:

```
A. one hop, no independent instrument, no scored predictions
   -> SHORT_UNCALIBRATED
   (the always-wrong instrument. short loop must NOT rescue it.)

B. one hop, scored against out-of-frame outcomes, high agreement
   -> SHORT_CALIBRATED

C. four hops, each hop a documented verbatim relay, C established
   by C-2  -> LONG_CALIBRATED
   (long loop must be able to outscore case A.)

D. two hops, R below threshold at hop 2
   -> LOSSY
   (R dominates. short L must not override.)
```

Cases A and C are the falsifiers. If the implementation cannot produce
C outscoring A, the instrument has rebuilt an authority claim with
"short loop" as the new credential, and fails.

---

## 6. DECLARATION BLOCK

Emit a machine-readable declaration at module level, for the join
registry:

```python
DECLARATION = {
    "measurand": "information carried by a source report about a referent system",
    "axes": ["loop_length", "per_hop_retention", "calibration"],
    "returns": [m.name for m in LoopRead],
    "scalar_collapse": False,
    "self_report_admitted": False,
    "unknown_states": ["UNCALIBRATED", "INSUFFICIENT"],
}
```

---

## 7. DELIVERABLES

```
loop_weight.py   module + DECLARATION
cases.py         >=8 hand-built cases, one per enum member
test_loop.py     asserts every enum member reachable
                 asserts case C outscores case A
                 asserts no authority-named field exists in the module
README.md        measurand, the three quantities, the two C derivations,
                 and the A/C falsifier stated as the pass condition
```

---

## 8. OUT OF SCOPE

```
- do not infer L from source type, occupation, or domain.
  L is counted from the described path, or it is INSUFFICIENT.
- do not build a source database, registry of people, or ranking list.
- do not add a tie-breaker that resolves to volume or agreement-count.
- do not weight by how many sources say the same thing; correlated
  sources sharing a hop are one instrument, not N.
```
