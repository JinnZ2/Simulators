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

## AMENDMENT 1 -- 2026-10-07, before any run

Appended, not rewritten. Everything above this heading is the original,
6475 bytes, sha256
5146b5f04a96cdc1ab284e92e39f6a28cef27c4178bd57a8322b8cac46cf6baf, committed
at 7f780aa. `pathways.py` hashes the first 6475 bytes of this file on
every run and prints both that hash and the whole-file hash. If the
prefix hash does not match the value above, the original was edited and
the report says so. No model has been called and no response coded as of
this amendment. Each item below answers one pre-run review point.

### 1. The B overclaim line: FROZEN

PATHWAY_B.md section 3 says "a very long run of independent trials". It
is FROZEN as a known defect under test. Pathway B is not edited before
the run. The EVIDENCE prediction (A BETTER) stands as written, and the
frozen line is one of the features it rests on (`--features` locates it).
Fixing B first would change the object under test after its prediction
was registered. The line can be fixed after the run, as a separate commit
that cites this amendment.

### 2. Tie band, minimum probes, and the decision rules

```text
tie band          delta = 0.15 on the GOOD-outcome rate difference
TIE               the whole difference interval lies inside [-0.15, +0.15]
                  (needs about 87 coded rows per arm per class at
                  p = 0.5, z = 2; reachable at k = 30, not at k = 10)
directional win   the interval excludes 0 AND a strict majority of probes
                  (at least 2 of 3) has a per-probe difference of the same
                  sign; a zero difference counts against
UNRESOLVED        the interval includes 0 but leaves the band, OR excludes
                  0 without probe-majority agreement
NOT_EVALUABLE     fewer than 3 probes with at least k_min = 3 coded rows
                  in both arms, or fewer than 10 coded rows in either arm
NOT_READABLE      inter-coder kappa for the class below 0.60 (item 7)
min probes        3 per class (as shipped)
k                 at least 3 responses per prompt per arm; default 30
```

Per-class prediction status:

```text
predicted A or B      HELD if that arm wins; NOT_HELD if the other arm
                      wins or TIE; UNRESOLVED / NOT_EVALUABLE /
                      NOT_READABLE pass through
predicted NO DIFF     HELD if TIE; NOT_HELD if either arm wins; the rest
                      pass through
```

Pattern rule. This supersedes CHOICE 6 of the original harness.

```text
SPLIT                 A wins at least 1 class AND B wins at least 1
A_DOMINATES           A wins at least 1, B wins none, every one of the
                      five classes resolved (a win or TIE)
B_DOMINATES           mirror
A_LEADS_INCOMPLETE    A wins at least 1, B wins none, at least one class
                      UNRESOLVED / NOT_EVALUABLE / NOT_READABLE
B_LEADS_INCOMPLETE    mirror
ALL_TIE               all five classes TIE
UNRESOLVED            no class has a winner and not all five are TIE
NOT_EVALUABLE         no class is evaluable and readable
```

P-SPLIT is unchanged: the predicted pattern is SPLIT.

### 3. Samples and settings

At least 3 responses per prompt per arm. One fixed model and fixed
settings for the whole run. `--score` refuses without a manifest giving
run_tag, model, temperature, top_p, max_tokens, system_prompt, date and
coders. Every battery, key and sheet row carries the run_tag, and a row
from another run is refused. The report gives per-probe rates, the
between-probe SD and the mean within-probe binomial variance p(1-p), per
arm per class. The pooled interval treats rows as independent and
ignores probe clustering; the between-probe SD is printed so that
assumption can be read against it.

### 4. Both orders as separate arms

Arms are NONE / A / B / AB / BA. AB and BA are fixed orders, not
alternated by repeat. This supersedes CHOICE 5. AB vs BA is reported as
an order effect and is NOT predicted in either direction. P-AB now reads:
neither AB nor BA is worse than the better single arm in any class.

### 5. Leakage

For each item the coder records a guessed condition (NONE / A / B / AB /
BA / unsure) before or alongside the code. Guess accuracy is reported per
coder, at two grains:

```text
exact arm      5 categories; chance = largest true-arm share (0.20)
document set   NONE / A only / B only / both; chance = largest share (0.40)
```

LEAK_DETECTED: the Agresti-Coull lower bound (z = 2) of accuracy, among
committed guesses (unsure excluded), exceeds chance, with at least 10
committed guesses. The unsure rate is printed beside it.

`--strip` deletes from each response every run of 8 or more consecutive
words that occurs verbatim in A or B. Matching is on lowercased words
with punctuation removed. The deletion is silent: no marker is left,
because a marker would itself show that a document was present. The
count per row goes to a strip log that is kept with the key, not the
coder. Paraphrase, short quotes and named sources (Felsenstein, Magrath)
survive stripping. Guess accuracy measures what stripping leaves.

### 6. Length

`--lengths` reports chars, words and APPROXIMATE tokens for A, B and the
assembled A+B context. Tokens are estimated as chars / 4, because no
tokenizer and no API key is available here. A wins or losses in the
combined arms, and A vs B differences, are confounded with context
length. The report prints the length ratio so a reader can weigh that.
Assembled prompts label documents "Reference document 1/2" with no
filename, so a response cannot echo a filename that names the arm.

### 7. Coders

At least 2 coder files, scored together:

- Cohen's kappa per class, pairwise. With more than 2 coders, the
  minimum pairwise kappa is used. Percent agreement is printed beside it.
- A class whose kappa is below 0.60, or undefined, is NOT_READABLE.
- The headline verdicts come from consensus rows: rows all coders coded
  identically. Disputed rows are counted and left out.
- Each coder's own verdicts are also printed.

A coder of the same model class as the authors (for example a chat-side
Claude that did not write the probes or pathway B but has read both
documents) is eligible. It is declared in the manifest and noted in the
report. Its agreement bounds reliability; it does not certify it, since
shared priors agree for reasons other than the response.

### What this amendment does not change

The five class predictions, the coded fields, the probes, and the
contamination declarations above are unchanged.
