# measurand-partition

Five work orders delivered as one message (`WORK_ORDER.md`, verbatim) and
built to. Each runs standalone; none requires the others; each states what
it does not know. What they share is one instrument fault, and `common.py`
carries it as a record shape:

```
  an observation made in ONE setting
        |
        v
  scored against an OUTCOME produced by MANY unmeasured variables
        |
        v
  the whole residual assigned to the thing observed

  WO-1  the child             WO-4  the building method
  WO-3  the observer's eye    WO-5  the released athlete
```

CC0. Python 3.9+, stdlib only, no network, phone-buildable. Every module
renders on bare invocation and refuses `--selftest` (exit 2);
`python3 test_partition.py` runs the checks and prints their count.
**Everything constructed is marked PROPOSED**, the delivery's own tag for a
design that is not a finding. Nothing here is a statement about any
person, program, structure or piece of wood, and every literature figure
the orders carry (the London taxi hippocampus, the 2025 five-modality
questionnaire, ~6.3 h adolescent sleep, the coach's-eye longitudinal
work, 250-year barns) is carried unverified: the egress gate refuses
every publisher host (`MPS_017`).

---

## WHAT EACH MODULE DOES, AND REFUSES

| order | module | computes | refuses |
|---|---|---|---|
| WO-1 | `wo1_partition.py` | the residual GATE (a score is a residual candidate only when A1-A4 are each MEASURED with a named instrument and the interaction is entered); the TWO-SETTING floor (share of individuals whose label moved between settings) | to subtract anything -- the order supplies no axis-to-performance model; to score a single-setting individual (UNBOUNDED); to read an unrun arm as floor 0 (NOT_RUN) |
| WO-2 | `wo2_band_sweep.py` | a CURVE per subject: floor, ceiling, width, and where the standard test point sits | to estimate a band from fewer than three levels; to interpolate a level nobody swept; to read a curve that never turns down as having no ceiling (CEILING_NOT_REACHED) |
| WO-3 | `wo3_control_manifest.py` | 3a the manifest (HELD / ADVISED_ON / NOT_TOUCHED / UNDECLARED); 3b the gradient and the trend of accuracy against it; 3c the ceiling from declared variance shares | to count ADVISED_ON as a fraction of HELD; to grade a program with an UNDECLARED variable; to state a ceiling with a not-controllable share undeclared |
| WO-4a | `wo4_lumber.py` | stiffness and strength ratios for the standard nominal-to-actual pairs; the quantity mismatch between the order's arithmetic and its test | to hold a material term; to return 0 or 1 on a malformed section |
| WO-4b | `wo4_survival.py` | Kaplan-Meier per population per maintenance arm over matched strata; the scope of a durability claim | to pool MAINTAINED_IN_USE with SURVIVING_NEGLECTED (`pooled()` exists to refuse); to read REMOVED as failure; to age a structure with no construction year |
| WO-5 | `wo5_deselection.py` | one cohort scored under PODIUM and under LEARNED; the size of the failure category that exists under one and not the other; the import line | to run LEARNED without untrained peers; to default an imported frame's measurand to PODIUM |

---

## WHAT CAME OUT, MODULE BY MODULE

**WO-1.** Nothing here can compute a residual's size, and that is the
finding about the design: STEP 3 ("report the residual after A1-A4 are
entered") is a gate, not a subtraction, until someone supplies the model
the order does not. The two-setting arm needs no model and runs: on the
constructed set one of two twice-labelled individuals moved, floor 0.50,
three single-setting individuals UNBOUNDED (`MPS_002`, `MPS_003`).

**WO-2.** The measurement fault reproduces exactly: a band shifted low, a
band shifted high and a flat curve return the same point read at the
standard level (0.10) and separate under the sweep into BAND_LOCATED on
opposite sides and NOT_REGISTERED (`MPS_004`). Absences are three states,
not one: NOT_REGISTERED, NOT_ESTIMABLE, CEILING_NOT_REACHED (`MPS_005`).

**WO-3.** The academy as the order describes it grades 0.40 with two
ADVISED_ON variables counted apart, because education on intake is not
control of intake (`MPS_006`). WO-3b returns NOT_EVALUABLE with no
program carrying a measured accuracy, and WO-3c returns UNDECLARED until
the not-controllable variance shares are declared -- which is the state
the literature reads its reliability results in, an implicit ceiling of
100% (`MPS_007`). The general form the order calls transferable is
`common.attribution()`.

**WO-4a.** The order's number holds and its mechanism sentence does not.
`I = b h^3 / 12` is cubic in depth and linear in width; a 4x4 shrinks in
both, so the fourth power is the product and 41.4% of stiffness goes.
Depth alone gives 33% (`MPS_008`). And the arithmetic quotes STIFFNESS
while the test ("load capacity to failure") measures STRENGTH, whose 4x4
ratio is 0.670 not 0.586 -- the test as written returns one number to be
read against a claim about the other (`MPS_009`). The square case also
understates the general one: a 2x4 keeps half (`MPS_010`).

**WO-4b.** The critical split is enforced before any record exists:
`pooled()` refuses by name, REMOVED censors, UNKNOWN maintenance is
excluded and counted, an unmatched stratum enters no comparison
(`MPS_011`). "150 years with proper maintenance" reads against the
maintained arm only, from a declared boolean and never from the wording
(`MPS_012`).

**WO-5.** Under PODIUM three athletes are failures; under LEARNED the
same three are AHEAD of untrained peers on four of five capacities and
TIE on the one they were released for. The category of three exists
under one measurand and not the other (`MPS_013`). The cohort is
CONSTRUCTED to the prediction's shape, so this is a known-answer run on
the scorer and no evidence about athletes; LEARNED is NOT_COMPUTABLE
without the untrained group nobody recruits (`MPS_014`), and an imported
frame must declare its measurand apart from its fields (`MPS_015`).

**The nulls.** Four of the five orders rest a step on an absence -- "not
searched", "nothing found", "no comparison exists" -- and only WO-4b
states its corpus (ten results, all builders). The others carry no corpus
and no terms, so they are the author's nulls and not bounded ones
(`MPS_016`).

---

## FILES

```
WORK_ORDER.md            the five orders, verbatim
common.py                the shared record shape; four populations
wo1_partition.py         residual gate + two-setting floor
wo2_band_sweep.py        curve, floor, ceiling, standard-point position
wo3_control_manifest.py  manifest, gradient, trend, accuracy ceiling
wo4_lumber.py            second moment, section modulus, the mismatch
wo4_survival.py          matched Kaplan-Meier, two arms, pooled() refuses
wo5_deselection.py       PODIUM vs LEARNED, the manufactured category
test_partition.py        the checks; prints their count
CLAIM_TABLE.md           MPS_001..MPS_017
samples/                 the renders and the test transcript
```

`wo4_lumber.py::stiffness_ratio` is registered in `tools/known_answer.py`.
