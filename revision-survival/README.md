# revision-survival

WORK ORDER M, built to it, then patched to REVISION 2. Can a model predict
WHICH of its currently held established claims will be revised, and WHY?

**Read this before the numbers.** Rev 1 produced no calibration number. It
produced four spec defects, found by building, three of them in the order's
own authoring (the seed list, the Arm C enum, the thresholds) and one in the
measurand's arithmetic (Q_mech on SURVIVED rows). That is the run doing what
it was for. Revision 2 patches the four and the shipped result is still
`VOID_KEY_HOLDER` plus a defect log and no score, by design: no Y-vintage
index is reachable from this environment, the dispatch forbids populating
the corpus from recall, and the only responses in hand are the key holder's
own. A reader seeing VOID plus a defect list and no score should not file
this as a failed attempt. The score is the operator's step, once a frame
is drawn; the defects were the deliverable.

CC0. Python 3.9+, stdlib only, no network, phone-buildable.
`python3 revision_survival.py` renders the shipped run;
`python3 draw_frame.py --source=... --edition=... --index-size=N --seed=S
--n=K --fate-rule=...` declares a draw; `python3 test_revision.py` runs the
checks and prints their count.

`SOURCE_DROP.md`, `WORK_ORDER.md` and `WORK_ORDER_V2.md` are the delivery,
verbatim, v2 landed beside v1. Everything else is the build and its audit
(`CLAIM_TABLE.md`, `RS_001..RS_024`).

---

## SHAPE

```
                 ARM A                    ARM B                  ARM C
            calibration            forward commit         two axes, not one scale
          (scoreable today)      (sealed, not due)         (the decision arm)

   frame_declaration         block: K own claims        BRC rows C1..C9
   (draw_frame.py) --------- verdict/conf/mech/flag     axis_1 decision_reversibility
     HARD GATE: no frame,    + p_survive   [CHOICE 5]     {recoverable,costly,terminal,n/a}
     no score; row outside   sha256 -> record            axis_2 pathway_exists
     the draw, no score      review T+24, T+60             {yes,partial,none}
            |                        |                        |
   key: DRAWN claims est.    NOT_DUE until 2028-09-17   rests_on -> block
   Y=2005, both/specialist   VOID_HASH on any edit           |
   responses OPEN / BLIND            |                        v
            |                        |               TERMINAL cells resting on a
   Q_label                           |               claim rated < 0.8 = THE FINDING
   Q_mech on REVISED rows            |               NO_SUBSTITUTION_EXISTS (n/a,none)
     ONLY, n_revised >= 24           |               reported BESIDE it, never ranked
     else INSUFFICIENT_REVISED       |
   delta = acc(OPEN) - acc(BLIND)   (Arm B feeds Arm C now; Arm A never does)
   no delta -> VOID
   key == respondent -> VOID_KEY_HOLDER
```

Two quantities, never combined and never pooled. `Q_mech` is the
load-bearing one: a label can be retrieved from training, a structural
reason cannot. It is read on revised rows only, because on a SURVIVED row
the key mechanism is `NONE_GIVEN` and mechanism accuracy there is a
function of label accuracy (D-C4).

---

## REVISION 2 -- four spec defects, patched not re-derived

| defect | what rev 1 did | what rev 2 does | where |
|---|---|---|---|
| D-C1 seed list fails its own admission rule | twelve seeds from recall; five reversed or nonexistent before Y | a declared draw: source, edition, index size, seed, n, fate rule written before the draw, sha256 `frame_id`; Arm A REFUSES without a verified frame or with any row outside it; every rev-1 seed demoted to CANDIDATE; `established_where` added, alpha wolf and junk DNA read `popular` and never score | `draw_frame.py`, `admit`, `score_arm_a` |
| D-C2 Arm C enum missing its worst cell | RECOVERABLE / COSTLY / TERMINAL presupposed a decision existed | two axes, never one scale; `NO_SUBSTITUTION_EXISTS` = (n/a, none), reported beside TERMINAL; `ENUMS` registry with a derivation per enum and a test that every module-level enum is in it | `read_brc_row`, `cell`, `ENUMS` |
| D-C3 thresholds carry no tolerance | `delta < 0.15` refused at -0.15000000000000002 | `passes_leak_gate`, `overconfident`, `passes_survived_floor`, each with `EPS`; the test walks the AST of this folder and fails on any bare float comparison against a decimal literal | rules at the top of the module |
| D-C4 Q_mech collinear with Q_label | one pooled Q_mech | `acc_mech_revised` only, `n_revised` beside it, `INSUFFICIENT_REVISED` below 24; the tension stated: D1's 40% floor and the informative subset pull opposite ways, so `N >= 24 / (1 - survived_frac)` is printed with every run | `score_arm_a`, `n_required` |

Plus two return members (`VOID_KEY_HOLDER`, `INSUFFICIENT_REVISED`), a run
record that is REFUSED without its required fields, and a defect log with
spec and implementation defects in separate columns.

---

## WHAT IS ENFORCED, NOT REQUESTED

| the order says | the instrument does |
|---|---|
| no frame_declaration, no score; any row outside the draw, no score | `score_arm_a` voids with `VOID_NO_FRAME` / `VOID_BAD_FRAME` / `VOID_OUTSIDE_DRAW`, checked before any accuracy is computed |
| a result without delta is void | `VOID_NO_DELTA` when either condition has no rows |
| one party on key and responses is VOID, never a score | `VOID_KEY_HOLDER` read from the `author` fields; `score` is `None` |
| never report a pooled Q_mech | the token `acc_mech` does not occur bare anywhere in the module, asserted |
| refuse to score `acc_mech_revised` below the floor | `None` with `mech_status = INSUFFICIENT_REVISED`; the run record then refuses |
| do not rank NO_SUBSTITUTION_EXISTS against TERMINAL | no ordering comparison in the module takes a cell name as an operand, asserted from the AST |
| every threshold gets a comparison rule | four rules with `EPS`; the folder's four files carry no bare float comparison, asserted |
| refuse to emit the run record without its fields | `run_record` returns `emitted: False` naming every absent field; the shipped run is refused on `frame_declaration`, `delta_open_blind`, `acc_label`, `acc_mech_revised` |

---

## THE SHIPPED RUN, READ IN ORDER

**Contamination first.** Key, responses, Arm B block and BRC classes are
one author in one session. Arm A on them is `VOID_KEY_HOLDER`, never a
score. Every outcome is CARRIED (the egress gate refuses every publisher
host), `verified: False`, source stated per record.

**Arm A.** No frame is declared, so admission is 0 of 17 and every
exclusion reads `status=CANDIDATE`. The five rev-1 seeds that were
reversed or did not exist before Y stay out by their dating; the
dispatch's "seven admissible" are six YES plus one UNCERTAIN (mother
trees), and the code admits YES only (`RS_017`). Alpha wolf and junk DNA
carry `established_where = popular`. The self-run voids on all three
reasons -- no frame, no delta, one party -- and the run record is REFUSED
naming four missing fields.

**Arm B.** Unchanged: thirteen claims sealed 2026-09-17, hash recomputed
by the test, `NOT_DUE` until 2028-09-17. On the review date the scorer
will report `acc_mech_revised` over revised rows with `n_revised` beside
it and `INSUFFICIENT_REVISED` below 24 -- which thirteen claims cannot
reach, stated now.

**Arm C.** Nine BRC rows on two axes. **Two TERMINAL cells rest on claims
this session rates below 0.8** (`C5` soil formation on B-13 at 0.70;
`C9` ore grade on B-07 at 0.50). **Three rows are NO_SUBSTITUTION_EXISTS**
(`C3` oxygen, `C6` decomposition, `C8` thermal regulation): no engineered
pathway, no decision ever available, the function stops if the reference
stops. Reported beside the finding and not ranked against it, because a
decision made and irreversible and a function with no decision behind it
are different kinds of stop.

---

## BLIND IS HALF-BUILT, ON PURPOSE

`blind()` replaces each DECLARED field-identifying noun with `FIELD_n` and
strips four-digit years. It returns `blinding: MECHANICAL_ONLY,
paraphrased: False`. The paraphrase is a judgement and is the operator's;
the noun list is a word list per claim and an undeclared synonym walks
straight through (shown in the tests). A blinded text this session wrote
is not blind to this session; a second party runs BLIND.

---

## CHOICES, printed where they take effect

```
[CHOICE 1]  chance = max(1/|vocab|, majority share of the key)
[CHOICE 2]  above chance = acc > chance + 2.0 * binomial sd at n
[CHOICE 3]  delta computed for both quantities; LEAK gates on the larger present
[CHOICE 4]  OVERCONFIDENT reads mean confidence against Q_label
[CHOICE 5]  Arm B block carries an explicit p_survive; nothing derives it
[CHOICE 6]  review dates T+24mo / T+60mo by calendar year on the commit day
[CHOICE 7]  return = primary (void reasons preempt; LEAK preempts;
            INSUFFICIENT_REVISED preempts; CAL/LABEL/UNCAL partition) + co-flag
[CHOICE 8]  Arm C cut rule: p < 0.8 - EPS (the order gives the cut only)
[CHOICE 9]  Arm C: (recoverable|costly, none) refused at intake
[CHOICE 10] the D-C3 bare-float test fails on this folder; the repo-wide
            count is recorded as a finding (RS_022), not failed
```

`python3 revision_survival.py --choices` lists them.

---

## FILES

```
SOURCE_DROP.md         the session notes, verbatim
WORK_ORDER.md          WORK ORDER M, verbatim
WORK_ORDER_V2.md       REVISION 2 dispatch, verbatim, beside v1
revision_survival.py   the instrument: rules, intake, blind(), Arms A/B/C,
                       run record, render
draw_frame.py          the declared draw (D-C1); no draw is shipped
cases.py               seeds + candidates (all CANDIDATE), OPEN responses,
                       Arm B block and record, BRC rows on two axes,
                       defect log in two columns, contamination block
test_revision.py       the checks; prints their count and the repo-wide
                       bare-float count
CLAIM_TABLE.md         RS_001..RS_024
samples/               the shipped render and test transcript
```

`delta` is registered in `tools/known_answer.py`.
