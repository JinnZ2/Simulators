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
| RS_010 | the consequence class needs a fourth state the order lacks | SUPERSEDED by D-C2 (RS_018) |
| RS_011 | the self-run is VOID on the instrument's own reading | SUPPORTED; rev 2 names it VOID_KEY_HOLDER |
| RS_012 | `delta` is registered; its first run was refused on a float | REPAIRED; reclassified as spec defect D-C3 (RS_019) |
| RS_013 | blind() is the mechanical half and a word list | SUPPORTED, limit shown |
| RS_014 | two defects in this build's own test file, found by running | REPAIRED |
| RS_015 | above-chance needs a margin the order does not state | DECIDED |
| RS_016 | nothing here bears on whether any model is calibrated | UNVERIFIED |
| RS_017 | D-C1: Arm A is gated on a verified frame_declaration; every rev-1 seed is CANDIDATE; the dispatch's "seven admissible" are six YES plus one UNCERTAIN | SUPPORTED, gate; FINDING on the count |
| RS_018 | D-C2: Arm C runs on two axes; NO_SUBSTITUTION_EXISTS is (n/a, none), reported beside TERMINAL and ranked against nothing; every enum carries a derivation | SUPPORTED, DECIDED |
| RS_019 | D-C3: every threshold comparison carries EPS; -0.15000000000000002 passes the leak gate; the folder has no bare float comparison | REPAIRED |
| RS_020 | D-C4: acc_mech_revised is the only mechanism figure; below 24 revised rows it is INSUFFICIENT_REVISED; the D1 tension is stated and N is sized from it | SUPPORTED |
| RS_021 | the self-run returns VOID_KEY_HOLDER and its run record is REFUSED naming four fields; a constructed drawn world emits one | SUPPORTED |
| RS_022 | the repo carries bare float comparisons against decimal literals in most Python files; recorded, not failed | FINDING, [CHOICE 10] |
| RS_023 | the defect log keeps spec and implementation defects in disjoint columns; four spec, three implementation | SUPPORTED |
| RS_024 | rev 2 verifies nothing more than rev 1 did: no draw made, no frame from a real index, no second party | UNVERIFIED |

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

---

## REVISION 2

## RS_017 -- the draw frame is a HARD GATE (D-C1)

`draw_frame.draw(source_id, edition, index_size, rng_seed, n, fate_rule)`
samples positions without replacement under `random.Random(rng_seed)` and
hashes the whole declaration, fate rule included, into `frame_id`.
`check_frame` recomputes it, so an edited position list, fate rule or id
no longer verifies. `score_arm_a(claims, responses, frame)` voids with
`VOID_NO_FRAME`, `VOID_BAD_FRAME` or `VOID_OUTSIDE_DRAW` before any
accuracy is computed, and `admit` scores only rows that are `DRAWN`, in
the frame, established YES, and `established_where` in {specialist, both}.

No draw is shipped. Every rev-1 record is `CANDIDATE` with
`draw_position: None`; the dispatch's DO NOT (no seeds from recall,
including this session's) is asserted over `cases.CLAIMS`.

**The count.** The dispatch says "the 7 admissible rev-1 seeds". Five read
NO by their dating; of the remaining seven, six read YES and one
(seed-02, mother trees) reads UNCERTAIN. The code admits YES only, so the
dispatch's seven is six under the order's own admission rule. Recorded,
not adjudicated: whether UNCERTAIN dating admits is the operator's rule
and belongs in the fate rule written before the draw.

**Falsified if** any row not produced by the declared draw reaches a
score, or a frame that does not verify is accepted.

## RS_018 -- two axes, never one scale (D-C2)

`decision_reversibility` in {recoverable, costly, terminal, n/a} and
`pathway_exists` in {yes, partial, none}. `cell()` derives the name:
(n/a, none) is `NO_SUBSTITUTION_EXISTS`, (n/a, yes|partial) is
`NOT_ON_RECORD`, `terminal` is `TERMINAL` whatever the pathway. The shipped
register puts `C3`, `C6`, `C8` in the worst cell rev 1 could not name, and
the finding (`C5`, `C9`) is unchanged. The test walks the module's AST and
asserts no ordering comparison takes a cell name as an operand.

`[CHOICE 9]`: (recoverable|costly, none) is refused at intake, since a
reversible substitution decision presupposes a pathway to substitute along.

**Completeness assertion.** `ENUMS` maps every module-level string tuple to
its members and a derivation from the measurand's outcomes; the test
finds every such tuple by AST and requires it to be registered with a
non-empty derivation, or declared in `NOT_ENUMS` (`RETURNS_V1`,
`RETURNS_V2_ADDED`, `RUN_RECORD_REQUIRED` -- two partial vocabularies and
a field list). A severity ranking whose worst cell is absent reads as
complete from inside; the derivation is what a reader checks.

**Falsified if** a module-level enum lands without a derivation and the
suite stays green.

## RS_019 -- comparison rules with tolerance (D-C3)

`passes_leak_gate`, `overconfident`, `passes_survived_floor` and
`below_survival_cut` ([CHOICE 8]) each state their rule once with
`EPS = 1e-9`. `delta(0.4, 0.55)` is `-0.15000000000000002` and passes the
leak gate; `overconfident(0.6, 0.4)` fires on `0.20000000000000004`.
`RS_012`'s known-answer case, which carried `tol=1e-9` as a case-level
patch, is reclassified: the defect was in the order's threshold statement
and the rule now lives in the module.

The suite walks the AST of the folder's four files and fails on any
`ast.Compare` with a float constant operand; the test file itself passes
literals as arguments to `near()` rather than comparing against them.

**Falsified if** a bare float comparison lands in the folder and the suite
stays green.

## RS_020 -- Q_mech on revised rows only, sized from D1 (D-C4)

`acc_mech_revised` is computed over rows whose key label is not SURVIVED;
`n_revised` sits beside it; below `N_REVISED_MIN = 24` it is `None` and
`mech_status` reads `INSUFFICIENT_REVISED`, which preempts the
CAL/LABEL/UNCAL partition. The token `acc_mech` does not occur bare in the
module, asserted. The tension: D1 requires 40% SURVIVED rows and every one
of them is a row Q_mech cannot be read on, so the requirement is on the
revised subset and `n_required(survived_frac) = ceil(24 / (1 - frac))` is
printed with every run -- 40 at 0.4, 60 at 0.6, None at 1.0. A constructed
world of 50 at survived 0.6 has 20 revised rows and returns
`INSUFFICIENT_REVISED`; Arm B's thirteen claims cannot reach the floor
either, and its scorer says so on the review date.

**Falsified if** any pooled mechanism accuracy is emitted, or a figure is
returned below the floor.

## RS_021 -- VOID_KEY_HOLDER and the run record

The shipped run voids on all three reasons (no frame, no delta, one
party) and returns `VOID_KEY_HOLDER`, an enum member with `score: None`.
`run_record` is REFUSED on it, naming `frame_declaration`,
`delta_open_blind`, `acc_label` and `acc_mech_revised`; on the constructed
drawn world it emits with every required field, the frame's source,
edition, seed and n, the Arm C table on both axes, and the defect log.
A defect log with one column is refused.

## RS_022 -- the repo-wide bare-float count [CHOICE 10]

The D-C3 test is enforced on this folder and RECORDED for the tree: the
suite prints the number of Python files carrying a bare float comparison
against a decimal literal and the number of such comparisons (369 files
and 1813 comparisons when this was written; the live count is printed by
the test and moves with the tree). Failing the repo suite on it would turn
every folder red for a rule one dispatch stated for one folder; the count
is the finding and the rule's scope is the operator's call.

## RS_023 -- the defect log

`cases.DEFECT_LOG` carries `spec` (D-C1, D-C2, D-C3, D-C4, RS_007) and
`implementation` (RS_014a, RS_014b, RS_012) with disjoint ids, each entry
naming what was found, how, and what patched it. Three of the four spec
defects are in the order's own authoring; D-C3 is in its threshold
statement. That is the run's product.

## RS_024 -- UNVERIFIED

No draw was made from a real Y-vintage index, no second party has
responded under BLIND, no outcome has been read. What rev 2 establishes
is that the four patches are properties of the code and are met, and that
the shipped result is a refusal with a defect log rather than a score.
