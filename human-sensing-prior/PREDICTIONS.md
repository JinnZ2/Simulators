# PREDICTIONS -- pathway A vs pathway B

Committed BEFORE `pathways.py`, its probe battery, or any run existed.
`pathways.py` prints the sha256 of this file in every report. If the hash
in a report does not match this file, the predictions were edited after
the harness existed, and the report should say so.

```text
pathway A   human-sensing-prior.md   (main, PR #115; another session)
pathway B   PATHWAY_B.md             (this branch, c9715a0)
NONE        no reference document    (control)
AB          both documents, order alternated by repeat
```

The question is not "which file is better". It is: for each problem
class, does one pathway move a model's answer in the right direction more
than the other does, and does either beat having no document at all?

## Problem classes and what is coded

Each response is coded on ONE field for its class, three values:
`yes` / `no` / `unclear`. `unclear` is counted and kept out of the
denominator. It is never read as `no`.

```text
class      probe shape                               field              good
---------  ----------------------------------------  -----------------  ------
DETECT     a person describes everyday multi-        cost_verdict       lower
           channel sensing; no cost is stated         (response says or
                                                      assumes the person
                                                      pays effort for it)
OVERAPPLY  a person describes a case with a REAL     denies_real_cost   lower
           cost: two decisions at once, long rare-   (response waves the
           target watch, an unfamiliar field          cost away with the
                                                      "parallel is cheap"
                                                      claim)
EVIDENCE   asks how strong the evidence is that      overclaims         lower
           parallel sensing is the cheap default      (states lineages as
                                                      independent trials,
                                                      or the energy basin
                                                      as measured)
CITE       asks whether a deer reading frog silence  conflates          lower
           is the same as alarm-call eavesdropping    (treats cessation as
                                                      alarm eavesdropping,
                                                      or cites the alarm
                                                      literature as
                                                      covering it)
NEXTSTEP   asks what would test the claim            runnable_test      higher
                                                      (names a test with a
                                                      stated refuting
                                                      outcome)
```

## Predictions (per class, A vs B)

Each prediction names the feature in the document that is expected to
carry it. `pathways.py --features` locates each feature by line, so the
reason for a prediction is checkable without trusting this file.

```text
class      predicted       carried by
---------  --------------  -----------------------------------------------
DETECT     NO DIFFERENCE   both carry an invariance self-check (A: one
                           step, "change the described processing"; B: four
                           steps incl. substitution person -> deer).
                           Both predicted below NONE.
OVERAPPLY  B BETTER        B section 6 scope limits: intake is not
                           decision; forced narrow monitoring is costly;
                           people vary; unfamiliar fields. A's only scope
                           note separates hardware upkeep from operating
                           mode. A predicted NOT below NONE here, possibly
                           above it (the correction over-applied).
EVIDENCE   A BETTER        A: convergent origins (pit organs) in place of a
                           count, an explicit [THIN] that lineages are not
                           independent draws, effective-N via phylogenetic
                           contrasts, and "survival shows viable, not
                           cheapest". B section 3 itself says "a very long
                           run of independent trials" -- the overclaim is
                           in B's text.
CITE       B BETTER        B names cessation-as-cue as distinct from alarm
                           eavesdropping and states Magrath 2015 does not
                           cover it. A does not draw the distinction.
NEXTSTEP   NO DIFFERENCE   both carry tests with refuting outcomes (A: P1-P4
                           plus a forward log; B: F1-F3). If one wins,
                           A is the likelier, for P2 and P4 having no
                           counterpart in B.
```

## Predictions (pattern)

```text
P-SPLIT    the overall pattern is SPLIT: each pathway wins at least one
           class the other loses. This is the operator's hypothesis
           ("one alternative is better for some problems and the other
           for others") and the one this file predicts.
P-AB       the AB arm matches the better single arm in every class. If AB
           is worse than the better single arm in a class, the two
           documents interfere (dilution or contradiction), and that is a
           finding against merging them into one file.
P-CONTROL  in every class at least one of A, B beats NONE. A class where
           neither does is a class neither document reaches.
```

## What would refute the split

- One pathway wins or ties every class: DOMINATES. Then the dominated
  file is a candidate for retirement into `legacy/`, not deletion.
- No detected difference in any class at the stated n: the run did not
  have the power to answer, or the two files are interchangeable. The
  report prints the minimum detectable difference so these two can be
  told apart.

## Contamination, declared

- The author of pathway B wrote this file and the probes. Pathway A was
  written by another session of the same model class. Neither is a
  neutral party; the coder must be.
- Responses may quote their reference document, so a coder can sometimes
  infer the arm despite opaque ids. The sheet withholds the arm; it cannot
  withhold what the model wrote.
- Nothing has been run. Every line above is a prediction.
