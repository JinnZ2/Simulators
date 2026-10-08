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

## AMENDMENT 2 -- 2026-10-07, before any run

Appended, not rewritten. The original (first 6475 bytes) and amendment 1
are unchanged. No model has been called and no response coded as of this
amendment. No registered prediction changes. The rules below add one
control arm, a pilot phase and a pin on the documents under test, and
promote one harness choice to a rule.

### 1. Length-matched control arm AF

B's assembled block is 1.66x A's in characters. A-vs-B therefore compares
structure and volume together. Arm AF is A's text followed, inside the
same reference block, by neutral filler up to B's block length:

```text
filler     lorem-ipsum words from the standard placeholder list, generated
           deterministically, after one blank line, cut at a word boundary
           so AF's block is within one word of B's block, never longer
position   inside A's block, so AF, A and B each present as one document
arms       NONE / A / AF / B / AB / BA       (k = 30: 2700 responses)
```

No filler is perfectly neutral. A model can remark on placeholder text,
which a coder could read as an arm cue. The guess check below covers AF.
`--strip` also removes 8-word runs of the filler.

Two comparisons are added per class. Both are REPORTED, and neither is
predicted:

```text
A vs AF     volume at fixed content
AF vs B     structure at matched length
```

Each class's A-vs-B verdict gets an attribution read from AF vs B (AF
standing for A):

```text
A-vs-B          AF-vs-B                    attribution
win for X       win for the same side      STRUCTURE_SURVIVES
win for X       TIE or the other side      NOT_SEPARABLE_FROM_VOLUME
TIE             TIE                        TIE_SURVIVES
TIE             a win                      TIE_NOT_SURVIVING
otherwise (UNRESOLVED / NOT_EVALUABLE / NOT_READABLE on either)   UNRESOLVED
```

The registered predictions are still scored on A vs B, as registered.
The attribution is printed beside each one. A HELD prediction whose
attribution is NOT_SEPARABLE_FROM_VOLUME is reported as held for A as
written, but not as evidence that structure carried it.

Leakage: AF is a sixth exact-arm category (chance 1/6). At the
document-set grain AF counts as A, so the categories are NONE / A / B /
both, and chance is the largest true share.

### 2. Pilot phase

```text
pilot      k = 3, its own run_tag, manifest phase "pilot"
gate       PILOT_PASS iff, in every class, min pairwise kappa >= 0.60
           over all arms' rows (about 54 rows per class at k = 3), AND no
           coder reads LEAK_DETECTED at either grain; else PILOT_FAIL with
           the reasons named
headline   a pilot score prints the gate, kappa, agreement and leakage
           only; no A-vs-B verdict, prediction status or pattern
main       manifest phase "main" must name pilot_run_tag (different from
           run_tag) and pilot_result PILOT_PASS, or --score refuses.
           Pilot rows never enter a main score: a row with another
           run_tag is refused (amendment 1 item 3)
after FAIL the probes and predictions do not change. Coding instructions
           or strip parameters may change, but only by a further dated
           amendment, followed by a new pilot under a new run_tag
```

The pilot kappa is a point estimate on about 54 rows per class. Its
standard error is roughly 0.1, so a pass near the floor is weak. The
main run recomputes kappa on all of its own rows and gates on that.

### 3. CHOICE 8 becomes a rule

If the difference interval lies inside [-0.15, +0.15], the class reads
TIE, even when the interval also excludes 0. This is equivalence-testing
logic: a difference that is real but smaller than the declared tolerance
counts as equivalence.

### 4. The documents under test are pinned by hash

The predictions were registered (7f780aa) against these bytes:

```text
A  human-sensing-prior.md  sha256 1a42dc8cf9807aa832feb3308f3d847dfdd9e90a7454c676d6611aaba592cbd7
B  PATHWAY_B.md            sha256 52a930468873cc0008e407cd59c9c1e5e34ae1dc6624f627ffbe842e8d0e5f8e
```

`main` carries a later revision of A, made by another session on another
branch (e82e0cc, c3578c8; sha256
a5c4b6cf6e0cb08989aa775b589e5cc98ade94c578df3c3a459bea18161db329). It
splits P4 into P4a/P4b and narrows the Goris scope. On that revision the
NEXTSTEP feature marker `**P4. Effective-N` no longer locates. That file
is a different object, and these predictions were not registered against
it. `--emit` refuses an A or B whose sha256 differs from the pins above.
After a merge, the registered A can be supplied with
`--a-file`, e.g. `git show 7f780aa:human-sensing-prior/human-sensing-prior.md`.
Testing main's A would need its own registration.

## Amendment 2, note 1 (2026-10-07): the AF filler, recorded

A dated note. It changes no prediction, rule, threshold or arm. It records
what the AF filler in amendment 2 item 1 is, so the filler can be checked
by hash.

```text
source     the standard lorem-ipsum placeholder word list (pseudo-Latin,
           derived from Cicero, De finibus bonorum et malorum 1.32-33),
           69 words, held in pathways.py as LOREM
genre      typesetting placeholder text; it carries no claim, no sensing
           vocabulary and no instruction
build      words cycled from the first word, joined by single spaces,
           cut to n = 1190 words; AF = A + "\n\n" + filler
LOREM      " ".join(LOREM)       69 words     sha256 bfe69795f172797361fa75e5e335920249118ced773e2d8b308088882883e315
filler     filler(1190)          7553 chars   sha256 1a39c66c65c72f1ab07b6f5cdd052abf19dc64e0927ea496df5102f4659fe99c
AF text    af_text(A_reg, 1190)  18999 chars  sha256 e570b26d5659dba21c6feb791fc310c53f9d8a699035e7120485167a1179a745
```

A_reg is the registered A (sha256 1a42dc8c...cbd7). The AF arm block,
with its arm framing, is 19030 chars against B's 19031.

The P4 marker, checked against main's revision of A: P4 was split, not
removed. The registered P4 ("Effective-N for the animal evidence",
phylogenetic independent contrasts) now appears as P4b ("Phylogenetic
independent contrasts", which now needs branch lengths), beside a new
P4a ("Independent-origin count", topology only). These predictions and
any results bind to the registered A only. Main's A is a different
object; testing it needs its own registration before any run.

## Amendment 3 (2026-10-08): runner substitution

Appended before any run. It changes no prediction, decision rule,
threshold, arm, probe, repeat count or pilot gate. It records how the
runs are executed, because the execution differs from what amendment 1
item 3 assumed.

### 1. The runner

There is no model endpoint in the Claude Code environment. The pilot
(and the main run, if it is run the same way) is executed by a chat-side
runner: a claude.ai artifact that uses the platform's sample capability.
The operator taps batches; the chat side loads a job file and reads the
results back.

The runner cannot see or set the exact model or the sampling settings.
The manifest records this with fixed strings, which `--score` accepts:

```text
model                        "claude.ai sample capability; exact model not exposed"
temperature, top_p,
max_tokens                   "PLATFORM_DEFAULT_NOT_SETTABLE"
system_prompt                "PLATFORM_FRAMING_NOT_VISIBLE"
model_tier_requested         the tier named in the job (e.g. "default")
model_tier_applied_counts    {tier: count} over delivered items, from the results
```

Amendment 1 item 3 asks for one fixed model and fixed settings. Under
the runner that is read as: one tier requested, and every delivered item
reports that same tier applied. `--score` refuses a runner manifest whose
applied counts name more than one tier, or a tier other than the one
requested. Whether the platform holds the model and settings fixed
within a tier is not observable from here. That is a stated limit, not
a check.

### 2. Scope

Single model, single platform. A result describes how the model behind
the sample capability, under the platform's own framing, responds to
these prompts. It says nothing about other models, or about the same
model with other settings or without that framing. A coder of the same
model class is still declared as such (amendment 1 item 7).

### 3. The job file and its assembly

`--emit-job` writes one JSON file, format "pathways-run/1": run_tag,
phase, model_tier, an optional seed, a template, a doc_separator, a
no_doc_text, the documents, and one item per prompt with its
prompt_sha256. The runner assembles each prompt as:

```text
docs_text = docs ? doc_separator.join(documents[k] for k in docs) : no_doc_text
prompt    = template, {DOCUMENTS} -> docs_text, then {QUESTION} -> question
            (literal replacement, all occurrences)
```

An item whose assembled prompt does not match its prompt_sha256 is not
sent; its status is hash_mismatch. The harness assembles prompts the
same way, and the tests check that both give the same bytes for every
item.

This assembly joins fixed per-document strings, so it cannot number
documents by position. Amendment 1 item 6 labelled them "Reference
document 1/2". That labelling is replaced by an unnumbered one:

```text
template        "{DOCUMENTS}Question: {QUESTION}"
doc_separator   ""
no_doc_text     ""
document k      "Reference document:\n<<<\n" + text + "\n>>>\n\n"
```

No filename appears, as before. AB and BA still differ only in order.
The NONE prompt is "Question: " + the probe, as before. The two empty
strings are deliberate: a runner that substitutes a default for an empty
string produces a hash_mismatch, not a silently different prompt. The
job also records, for each document, its raw sha256, so the wrapped
text can be checked against the pins.

With the unnumbered label, the blocks are AF 19029 chars and B 19030.
That replaces the 19030 / 19031 in amendment 2 note 1, which measured
the numbered label. The filler (1190 words) and its sha256 are unchanged.

### 4. Result statuses

The runner returns one row per item with a status:

```text
answered, refused, empty         OUTCOMES. Coded like any response. A refusal
                                 or an empty reply is what the model did.
error, hash_mismatch,
prompt_too_large, no row         NOT_DELIVERED. Not coded, not imputed.
                                 Counted per arm and printed.
```

prompt_too_large falls on the long arms (AB, BA) if it falls anywhere, so
not-delivered counts are printed per arm and are not assumed to be
missing at random.

### 5. Order

Job items, and the coding sheet built from results, are ordered by
opaque id. Neither the send order nor a row's position on the sheet
follows the arm. Before this amendment `--sheet` kept the battery order,
which groups rows by arm within each probe. Nothing was ever coded under
that order.

### 6. Key material

The job file and the results carry each item's arm. They are key
material and are not given to coders. The job file is committed to the
repository (`runs/`), so a coder with repository access could read it.
Coders are asked not to open `runs/`, and the leak check (amendment 1
item 5) measures what reached them either way.
