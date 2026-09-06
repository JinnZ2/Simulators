# WORK ORDER — FRAME-LOCATION BENCHMARK (harness-split)

CC0. Public domain. No attribution requested or accepted.

Build constraints: Python 3 stdlib only. No network at run time. No
dependencies. Single folder. Must build and run on a phone.

---

## 0. WHAT THIS MEASURES, AND WHAT IT DOES NOT

Existing reasoning benchmarks supply a well-posed problem and score the
answer. This one supplies a problem that may be MIS-POSED and scores
whether the mis-posing is named BEFORE an answer is produced.

Second axis: the same task set is run under two or more HARNESS
conditions — cold, and with a carried context file of prior positions
and corrections. This tests whether a persistent context file produces a
harness effect on this capability, in the ARC-AGI sense of a harness
(scaffolding around the model, not the model itself).

NOT measured: answer quality, knowledge breadth, calibration, or
anything about the operator. See §7.

---

## 1. DELIVERABLE A — `cases.jsonl`

One JSON object per line. No prose in the file.

```
{
  "id":            "FL-014",
  "domain":        "hydrology",
  "prompt":        "<the stated problem, verbatim, as a user would send it>",
  "posed":         "MIS" | "WELL",
  "fault_class":   "WRONG_INSTRUMENT" | "MISSING_DENOMINATOR"
                 | "UNSCOPED_CLAIM"   | "UNIT_OF_ANALYSIS"
                 | "PROXY_AS_QUANTITY"| "SINGLE_EVENT_FRAME"
                 | "ACCEPTED_SIDE"    | null,
  "fault_target":  "<the specific variable/term that is wrong>",
  "accept":        ["<alt strings that count as naming the same target>"],
  "well_posed_answer": "<required only when posed=WELL>",
  "source":        "field | published | constructed",
  "notes":         "<how the correct reframe is known>"
}
```

### Case set requirements

```
R1  >= 40% of cases posed=WELL. CONTROLS ARE LOAD-BEARING.
    Without them, "always declare MIS" wins the benchmark.
R2  fault_class balanced; no class >25% of MIS cases.
R3  >= 3 domains, and >= 1 domain per fault_class outside the
    domain the class was first observed in.
R4  Every MIS case states in `notes` HOW the correct reframe is
    known. If it is known only from the author's judgement, mark
    source=constructed and flag it.
R5  No case content may appear anywhere in any harness file. §4.
R6  Prompts are the stated problem ONLY. No hedging, no hints, no
    "is this the right question" framing.
```

---

## 2. DELIVERABLE B — `protocol.md` + response contract

The scoring problem is that grading a free-text reframe requires a
grader who can already do the reframe. Solved by forcing a structured
declaration BEFORE the answer:

```
Every response must begin with exactly these three lines:

POSED: WELL | MIS
TARGET: <single term or variable, or NONE>
THEN answer.
```

This makes scoring a field comparison, not a judgement. The model is
told the contract and told that both verdicts are live. It is NOT told
the class distribution.

```
CONTRACT RULES
  C1  Contract text is identical across all arms.
  C2  Contract does not name the fault_class list.
  C3  Malformed header = MALFORMED, scored separately, not as wrong.
  C4  Single-shot. No follow-up turns in the base run.
```

---

## 3. DELIVERABLE C — `score.py`

Pure counting. No model calls. Reads `cases.jsonl` + a runs directory.

```
INPUT   runs/<arm>/<model>/<case_id>.txt   raw response text
OUTPUT  per arm x model:

  posed_accuracy        correct WELL/MIS calls / total
  false_positive_rate   WELL cases called MIS        <- the real ceiling check
  false_negative_rate   MIS cases called WELL
  target_hit            MIS cases correct AND target in accept[]
  target_miss_named     MIS called correctly, target wrong
                          -> detected the strain, mislocated it
  by_fault_class        target_hit broken out
  by_domain             target_hit broken out
  malformed_rate
  turns_to_arrival      multi-turn variant only, §5
```

```
SCORING RULE
  A MIS case counts ONLY on target_hit.
  Calling MIS without locating the target is recorded separately
  and never summed into the headline number.
```

---

## 4. HARNESS ARMS

The independent variable. Each arm is a text file prepended to the
prompt; nothing else differs.

```
ARM 0  COLD          no file
ARM 1  FORMAT        output-format and register preferences only
ARM 2  POSITIONS     standing framework positions, no corrections
ARM 3  CORRECTIONS   logged prior errors and their repairs only
ARM 4  FULL          2 + 3
```

```
CONTAMINATION RULE  (load-bearing, single point of failure)
  No harness file may contain any case's domain-specific content,
  fault_target, or a worked instance of the same fault in the same
  domain. Cross-domain instances of a fault_class ARE permitted —
  that is the transfer being measured.
  Build harness files FIRST, freeze them, then write cases against
  a held-out list. Record the freeze order in the run log.
```

The four-arm split is the point. A single with/without comparison
returns "the file helped" and cannot say what carried the effect.

---

## 5. VARIANT — `turns_to_arrival`

Multi-turn. Same cases, contract dropped. A scripted probe
("what would you need to answer that?") is issued up to N=5 turns.
Score = turn index at which POSED/TARGET first surfaces unprompted,
or N+1 if never. Probes are fixed strings, identical across arms.

Cheaper to interpret than the single-shot run, harder to automate.
Build second.

---

## 6. CLAIM TABLE

Each with its refutation condition. No claim ships without one.

```
FL-1  Frame-location is separable from answering.
      REFUTED IF: posed_accuracy tracks general capability rank
      across models with no residual.

FL-2  Current benchmarks exclude this by construction (every task
      supplied is well-posed).
      REFUTED IF: a published suite contains scored mis-posed items.

FL-3  A persistent context file produces a harness effect here.
      REFUTED IF: ARM 4 does not exceed ARM 0 beyond run variance.

FL-4  The effect is carried by CORRECTIONS, not by format or by
      stated positions.
      REFUTED IF: ARM 1 or ARM 2 matches ARM 3.

FL-5  Fault classes transfer across domains.
      REFUTED IF: target_hit for a class collapses outside the
      domain the class was first written in.

FL-6  Naming the strain and locating it are distinct capacities.
      REFUTED IF: target_miss_named is near zero across all arms —
      then it is one capacity and the split is decoration.

FL-7  Harness effect is larger on MIS cases than on WELL cases.
      REFUTED IF: the arm delta is flat across posed values —
      then the file is buying compliance with the contract, not
      frame-location.
```

---

## 7. NULLS AND SCOPE

```
N1  If false_positive_rate is high in every arm, the benchmark is
    measuring suspicion, not frame-location. The instrument fails.
    Report it as an instrument failure, not as a model finding.

N2  If ARM 0 already scores near ceiling, the case set is too easy
    and the harness question cannot be asked with it. Say so; do
    not rescale to manufacture a spread.

N3  If ARM 4 UNDERPERFORMS ARM 0, that is a real and reportable
    result — a carried file can over-fit the reader to a prior
    fault set. Do not suppress it.

N4  Any harness-effect number is a property of THAT harness file.
    Every reported score carries its arm label, always, in the same
    line. An unlabelled score from this benchmark is void.
```

```
SAMPLING ABSENCE, stated in the body and not as a caveat:
  The case set is authored, not sampled. It shows which faults the
  author can construct and verify — not the field distribution of
  mis-posed problems. Frequency claims are out of scope.
```

```
OUT OF SCOPE — NO EXCEPTIONS
  No section characterizing the author, the operator, working
  style, or biography. Not in the repo, not in the README, not in
  the case notes. Cases carry the problem and the key, nothing else.
```

---

## 8. BUILD ORDER

```
1  harness files, frozen, freeze order logged   (§4)
2  10 cases, 4 WELL / 6 MIS, one domain          smoke test
3  score.py against hand-made runs               verify counting
4  expand to >= 40 cases, >= 3 domains           (§1 R1-R6)
5  run ARM 0 and ARM 4 only                      is FL-3 alive
6  full four-arm run                             FL-4
7  turns_to_arrival variant                      (§5)
```

Stop after step 5 if FL-3 is refuted. Steps 6–7 are only worth their
cost if there is an effect to decompose.

---

## 9. OPEN NODE

Cases with `source=constructed` are the weak joint: the correct reframe
is known from the author's judgement rather than from an independent
record. Field and published cases have an external check; constructed
ones do not.

Not resolved here. Minimum handling: report headline numbers with
constructed cases EXCLUDED, and again with them included. If the two
numbers diverge, the divergence is the finding.
