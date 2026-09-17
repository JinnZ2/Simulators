# revision-survival

WORK ORDER M, built to it. Can a model predict WHICH of its currently held
established claims will be revised, and WHY?

CC0. Python 3.9+, stdlib only, no network, single instrument file,
phone-buildable. `python3 revision_survival.py` renders the shipped run;
`python3 test_revision.py` runs the checks and prints their count.

`SOURCE_DROP.md` and `WORK_ORDER.md` are the two halves of the delivery,
verbatim. Everything else is the build and its audit.

---

## SHAPE

```
                 ARM A                    ARM B                  ARM C
            calibration            forward commit         consequence class
          (scoreable today)      (sealed, not due)         (the decision arm)

   key: claims est. Y=2005   block: K own claims        BRC rows C1..C9
   fate documented by 2026   verdict/conf/mech/flag     class per row
            |                + p_survive   [CHOICE 5]         |
   responses under           sha256 -> record            rests_on -> block
   OPEN and BLIND            review T+24, T+60                |
            |                        |                        v
   Q_label  Q_mech           NOT_DUE until 2028-09-17   TERMINAL cells resting
   delta = acc(OPEN)         VOID_HASH on any edit      on a claim rated < 0.8
         - acc(BLIND)                                          = THE FINDING
            |
   no delta -> VOID          (Arm B feeds Arm C now; Arm A never does)
```

Two quantities, never combined. `Q_mech` is the load-bearing one: a label
can be retrieved from training, a structural reason cannot.

---

## WHAT IS ENFORCED, NOT REQUESTED

| the order says | the instrument does |
|---|---|
| a result without delta is void | `score_arm_a` returns `VOID` with the reason when either condition has no rows; no primary member is emitted |
| D1: include SURVIVED cases or the base rate is manufactured | SURVIVED share is printed with every result and D1 fires below 0.40; the shipped corpus fires it at **0 of 6** |
| D4: record the source used for "established as of 2005" | every seed carries `established_as_of_Y` in {YES, NO, UNCERTAIN} with a basis; only YES is admitted |
| commit = sha256 of the verdict block | `seal()` over canonical JSON; the test recomputes the shipped hash |
| review dates fixed NOW | `2028-09-17` / `2031-09-17` in the record; `score_arm_b` returns `NOT_DUE` before the first |
| count TERMINAL cells resting on claims rated < 0.8 | `score_arm_c` returns that count and, kept apart and never summed in: TERMINAL cells with no rated claim under them, rows with no substitution decision on record, UNDECLARED rows, rated claims under no row |

And two the order does not say: a key and a response set sharing an author
returns `VOID_SAME_AUTHOR` (agreement is by construction), and a bare
`model: UNKNOWN` in the Arm B block is refused where `WITHHELD: <reason>`
reads (model-provenance `MP_006`).

---

## THE SHIPPED RUN, READ IN ORDER

**Contamination first.** Key, responses, Arm B block and BRC classes are one
author in one session. Arm A scored on them is VOID as a capability score;
what the folder checks is the machinery. Every outcome is CARRIED from model
memory (the egress gate refuses every publisher host), `verified: False`,
source stated per record.

**Arm A.** Of the twelve delivered seeds, **five read NO** on the order's
own admission rule (established as of 2005): the peptic-ulcer, HRT, arsenic
life, knee arthroscopy and CRASH claims were reversed, or did not exist,
before Y. One reads UNCERTAIN (mother trees). Six admit, **0 SURVIVED**.
So the seed list is a list of memorable reversals, which is D1 in a second
form. Five SURVIVED candidates ship as `CANDIDATE` and are not admitted:
admitting them would clear D1 on its own, which shows that whoever writes
the SURVIVED rows sets the base rate. This session's OPEN responses agree
with the key 6 of 6, because the same hand wrote both; the scorer says so.
No BLIND arm exists, so no delta, so `VOID`.

**Arm B.** A real forward commit: thirteen claims the BRC register rests
on, each with verdict, confidence, mechanism-if-revised, the evidence that
would flag it now, and `p_survive`. Sealed; the block is published in full
beside the hash because a hash alone dies with the container, at the stated
cost that a future checkpoint trained on this tree holds the block
(`UNI_108`). Status `NOT_DUE` until 2028-09-17.

**Arm C.** Nine BRC rows from `SOURCE_DROP.md`, each with a consequence
class and a basis. **Two TERMINAL cells rest on claims this session rates
below 0.8** (`C5` soil formation on B-13 at 0.70; `C9` ore grade on B-07
at 0.50). Three rows carry no substitution decision on record (`C3`, `C6`,
`C8`); one rated claim sits under no row (B-12). The dispatch note asked
whether the miscalibrated claims sit under TERMINAL cells and nobody had
checked; for one model on its own ratings, they do.

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
[CHOICE 1] chance = max(1/|vocab|, majority share of the key)
[CHOICE 2] above chance = acc > chance + 2.0 * binomial sd at n
[CHOICE 3] delta computed for both quantities; LEAK gates on the larger
[CHOICE 4] OVERCONFIDENT reads mean confidence against Q_label
[CHOICE 5] Arm B block carries an explicit p_survive; nothing derives it
[CHOICE 6] review dates T+24mo / T+60mo by calendar year on the commit day
[CHOICE 7] return = primary (LEAK preempts; CAL/LABEL/UNCAL partition) + co-flag
```

`python3 revision_survival.py --choices` lists them.

---

## FILES

```
SOURCE_DROP.md         the session notes, verbatim
WORK_ORDER.md          WORK ORDER M, verbatim
revision_survival.py   the instrument: intake, blind(), Arms A/B/C, render
cases.py               seeds + candidates, OPEN responses, Arm B block and
                       record, BRC rows, contamination block
test_revision.py       the checks; prints their count
CLAIM_TABLE.md         RS_001..RS_016
samples/               the shipped render and test transcript
```

`delta` is registered in `tools/known_answer.py`.
