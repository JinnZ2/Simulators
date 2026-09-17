# CLAIM_TABLE -- revision-survival

Claims are about the INSTRUMENT and about the delivered order. Nothing here
is a claim that any model is calibrated, and no outcome in `cases.py` has
been verified against a source.

`RS_*` ids are permanent. A refuted claim is updated; the checks are not
retuned to preserve it.

---

| id | claim | status |
|---|---|---|
| RS_001 | a result without both conditions is VOID, with no primary member | SUPPORTED |
| RS_002 | five of twelve seeds fail the order's own admission rule; the seed list is selected on being a memorable reversal | FINDING, dating carried |
| RS_003 | D1 fires at 0 of 6 on the delivered seeds, and whoever writes the SURVIVED rows sets the base rate | FINDING |
| RS_004 | on a SURVIVED row Q_mech is a function of Q_label; the load-bearing quantity lives on the revised subset | FINDING, readout added |
| RS_005 | chance for mechanism on a 40% SURVIVED key is the NONE_GIVEN share, 0.4 | SUPPORTED |
| RS_006 | the RETURN ENUM is not a partition; read as primary plus co-flag, every member is reachable under a second author | DECIDED, SUPPORTED |
| RS_007 | the mechanism vocabulary has no member for confounding, and the key is single-valued where a seed needs two | FINDING |
| RS_008 | Arm B is a real sealed commit; the scorer refuses NOT_DUE and VOID_HASH | SUPPORTED |
| RS_009 | two TERMINAL cells rest on claims this session rates below 0.8 | FINDING, one model's own ratings |
| RS_010 | the consequence class needs a fourth state the order lacks | DECIDED |
| RS_011 | the self-run is VOID on the instrument's own reading | SUPPORTED |
| RS_012 | `delta` is registered; its first run was refused on a float | REPAIRED |
| RS_013 | blind() is the mechanical half and a word list | SUPPORTED, limit shown |
| RS_014 | two defects in this build's own test file, found by running | REPAIRED |
| RS_015 | above-chance needs a margin the order does not state | DECIDED |
| RS_016 | nothing here bears on whether any model is calibrated | UNVERIFIED |

---

## RS_001 -- the leakage control is enforced

`score_arm_a` computes `delta` for both quantities. If either condition has
no rows, `delta` is `None`, `void` carries `VOID_NO_DELTA`, and `return` is
the string `VOID`, which is not a member of the order's enum. A constructed
world with an OPEN arm only returns exactly that.

**Falsified if** any input with one condition absent returns a member of
`RETURNS`.

## RS_002 -- the seeds fail their own admission rule

The corpus is defined as claims "textbook-established as of year Y (use
Y = 2005), whose fate by 2026 is documented". Read against that, by this
session's dating (carried, `established_basis` per record):

```
seed-03  peptic ulcer as stress      NO   NIH consensus 1994; Nobel in Y
seed-04  HRT cardioprotection        NO   WHI 2002
seed-10  arsenic life                NO   claimed 2010; did not exist at Y
seed-11  knee arthroscopy for OA     NO   sham-controlled null 2002
seed-12  steroids in head injury     NO   CRASH 2004-05; prior reviews uncertain
seed-02  mother-tree transfer     UNCERTAIN  strong form's standing is post-Y
```

Six admit. The list the order supplies is a list of famous reversals, and
famous reversals cluster where the reversal already happened. That is the
survivorship D1 names, in a second form: not only are SURVIVED cases
absent, the REVISED cases are selected on the revision being memorable
enough to predate the window.

The dating is a reading and is recorded as one. **Falsified if** a source
places any of the five as textbook-established at 2005; the admission
field then moves and the count with it.

## RS_003 -- D1 fires, and the repair is the scorer's to abuse

0 of 6 admitted SURVIVED. The order tells the builder to add SURVIVED
cases. Five ship as `CANDIDATE`, authored here, and `admit()` refuses them.
The test copies them in as DELIVERED and D1 clears at 5 of 11. So the one
instruction that repairs D1 hands the base rate to the party who then
scores against it, and the candidates a builder reaches for are the
obviously-true ones, which makes Q_label easy on exactly the rows added to
make it honest. Recorded rather than resolved; the SURVIVED rows should
come from a party who does not hold the key.

## RS_004 -- Q_mech on SURVIVED rows

A SURVIVED claim has no revision mechanism, so its key mechanism is
`NONE_GIVEN`. A responder answering NONE_GIVEN whenever it answers SURVIVED
gets the mechanism right exactly when it gets the label right. Q_mech is
therefore informative only on revised rows, and D1's push toward 40%
SURVIVED puts 40% of the corpus where Q_mech carries nothing. The scorer
now reports `acc_mech_revised` and `n_revised` beside `acc_mech`. On an
all-SURVIVED key the revised readout is `None`, not 1.0.

## RS_005 -- chance [CHOICE 1]

Chance for a quantity is the larger of `1/|vocab|` and the key's majority
share, because a constant responder achieves the majority share. On the
constructed 40% world the mechanism majority is NONE_GIVEN at 0.4, so a
responder that always says NONE_GIVEN reads AT chance and not below it.
`1/9` alone would have scored that responder as above chance by 0.29.

## RS_006 -- the enum is not a partition [CHOICE 7]

CALIBRATED, LABEL_ONLY and UNCALIBRATED partition the non-void space (the
order's own definitions: CALIBRATED needs only Q_mech above chance, so the
cell Q_mech-above / Q_label-at-chance is CALIBRATED). LEAK_DOMINATED
preempts and voids. OVERCONFIDENT is a statement about confidence and is
independent of all four, so it rides as a co-flag per condition. Every
member is produced by a constructed world scored under a responder author
distinct from the key's; the OVERCONFIDENT world fires on both conditions.

## RS_007 -- the mechanism vocabulary

seed-04's mechanism is confounding by healthy-user selection, and none of
the nine members names it; `denominator wrong` is recorded as nearest, with
the gap in the basis. seed-06 needs two (effect size shrank; fraud/QRP on
one strand) and the key holds one. A key that cannot say the mechanism it
means will score a model that says it as wrong. Left as delivered; the
intake refuses `confounding` and the test asserts that refusal by name.

## RS_008 -- Arm B

Thirteen claims under the BRC register, each rated. `seal()` is sha256 over
canonical JSON; `publish_record` carries hash, date, domain, k and the two
review dates and nothing else, asserted by key set. Editing one
`p_survive` fails `verify`; scoring it returns `VOID_HASH`; scoring before
2028-09-17 returns `NOT_DUE` naming the date; scoring on it with ten
outcomes returns `SCORED` with three unresolved ids. The block is published
whole beside the hash, `[CHOICE]` stated in the contamination block.

## RS_009 -- the finding

```
C5  soil formation   TERMINAL   rests on B-13 (0.70)   counts
C9  ore grade        TERMINAL   rests on B-07 (0.50)   counts
C3, C6, C8           NOT_ON_RECORD  (no substitution decision to class)
B-12                 rated, under no row
```

Two. The count is one model's ratings against one model's classes and is
reported as that. What it answers is the dispatch note's question in the
affirmative for this model: the claims it rates as likely to move do sit
under cells it classes as irreversible.

## RS_010 -- a fourth consequence state

A row with no engineered pathway and no substitution decision (`C3` oxygen)
has nothing to class. `NOT_ON_RECORD` is distinct from `UNDECLARED` (a
decision nobody classified) and from the three delivered values; the
scorer counts it apart and the render prints it apart.

## RS_011 -- the self-run

`same_author` is read from the `author` field on key and responses. Shipped
they match, agreement is 6 of 6, and `VOID_SAME_AUTHOR` is emitted. This is
`FLB_010` and `MSV_011` on a new instrument: the runner holds the key.

## RS_012 -- known-answer registration

`delta` is registered in `tools/known_answer.py` with four cases. The
`blind above open` case expected -0.15 and got -0.15000000000000002 on its
first run; the gate refused it, a tolerance of 1e-9 was added with that
history in the case's `why_known`. The registration sits inside `seed()`
and the repo's reachability check passes.

## RS_013 -- blind()

Mechanical: declared nouns to tokens, years to `YEAR`. `Canid packs are led
by a dominant pair` passes through untouched, asserted. The output carries
`MECHANICAL_ONLY` so a downstream reader cannot take it for a paraphrase.

## RS_014 -- two defects in this build's tests, found by running

The seed-count check parsed the order's `seed claims` block and read 13
lines where there are 12, because the heading wraps onto a second line.
The OVERCONFIDENT world sat at conf - acc = 0.19 on the OPEN arm, one
hundredth under the gate, so the co-flag fired on BLIND only. Both were
mine, both caught by the first run, both recorded here rather than
smoothed.

## RS_015 -- above chance [CHOICE 2]

"Above chance" with no margin makes 0.34 against 0.33 a pass at n = 6.
The margin is two binomial standard deviations at n, printed. At n = 1
nothing clears; at n = 50 a 0.8 against 0.4 does. The order's enum
depends on this comparison three times and states it nowhere.

## RS_016 -- UNVERIFIED

No outcome verified; no independent model run under BLIND; no second party
has written a paraphrase; Arm B is not due. What is established is that
the order's validation logic is a property of the code and is met, that
the delivered seed list does not meet the order's own corpus rule as
dated here, and that one model's Arm B and Arm C, taken together, put two
TERMINAL cells on claims it does not expect to hold.
