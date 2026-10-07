# PATHWAYS -- two shapes of one correction, and how to tell which fits where

CC0 1.0 Universal.

## The two pathways

```text
A   human-sensing-prior.md   convergent origins (pit organs), effective-N
                             via phylogenetic contrasts, [THIN] on lineage
                             independence, P1-P4 tests, forward log
B   PATHWAY_B.md             cessation-as-cue named apart from alarm
                             eavesdropping, Magrath 2015 gap, section 6
                             scope limits (intake is not decision, forced
                             monitoring is costly, people vary, unfamiliar
                             fields), F1-F3 tests
```

Both stay. Neither file is edited by this comparison. B's line "a very
long run of independent trials" is FROZEN as a known defect under test
(PREDICTIONS.md amendment 1, item 1); the EVIDENCE prediction rests on it.

## Flow

```text
PREDICTIONS.md   original 6475 bytes committed first (7f780aa); amendment 1
      |          appended before any run (7d49610). Every report prints the
      |          original-prefix hash (OK / MISMATCH) and the whole-file hash
      v
pathways.py --emit OUT --run-tag T      15 probes x 5 arms x k (k >= 3, default 30)
      |          arms NONE / A / B / AB / BA (both orders, fixed)
      |          OUT.jsonl battery  +  OUT.key.jsonl arm key, kept apart
      v
pathways.py --prompt OUT ID             exact text to send; neutral headers,
      |                                 no filenames; refuses a changed file
operator: ONE model, ONE settings set, every prompt cold; paste responses
      v
pathways.py --sheet  ->  --strip SHEET CODER_SHEET STRIP_LOG
      |          silent deletion of 8+ word verbatim runs from A or B;
      |          the strip log stays with the key
      v
>= 2 coders without the key fill code (yes/no/unclear), guess
(NONE/A/B/AB/BA/unsure) and coder id
      v
pathways.py --score KEY --manifest M.json [--strip-log LOG] C1 C2 [...]
```

## What each class asks, and the predicted winner

```text
class      field              good    predicted     rests on (pathways.py --features)
DETECT     cost_verdict       lower   TIE           both carry an invariance self-check
OVERAPPLY  denies_real_cost   lower   B             B section 6 scope limits
EVIDENCE   overclaims         lower   A             A [THIN] + Felsenstein; B says
                                                    "very long run of independent trials"
CITE       conflates          lower   B             B names CESSATION-AS-CUE; A does not
NEXTSTEP   runnable_test      higher  TIE           A P1-P4, B F1-F3
pattern                               SPLIT
AB / BA                               neither worse than the better single arm
control                               A or B beats NONE in every class
order (AB vs BA)                      reported, not predicted
```

## Decision rules (amendment 1 item 2)

```text
TIE              whole interval inside [-0.15, +0.15]; needs ~87 coded rows
                 per arm per class at p = 0.5, so k = 30, not k = 10
win              interval excludes 0 AND >= 2 of 3 probes agree in sign
UNRESOLVED       interval includes 0 but leaves the band, or one probe carries it
NOT_EVALUABLE    < 3 probes with >= 3 coded rows per arm, or n < 10
NOT_READABLE     min pairwise kappa < 0.60 for the class
SPLIT            A wins >= 1 class and B wins >= 1
X_DOMINATES      X wins >= 1, other none, all five classes resolved (win or TIE)
X_LEADS_INCOMPLETE  same, but >= 1 class unresolved / not evaluable / not readable
ALL_TIE          five TIEs
```

## What --score reports

```text
manifest         run_tag, model, temperature, top_p, max_tokens, system_prompt,
                 date, coders (each with same_model_class); refused if missing
variance         per-probe GOOD rates, between-probe SD, mean p(1-p), per arm
agreement        Cohen's kappa per class, min pairwise, plus percent agreement;
                 kappa IMPORTED from effective-redundancy-audit, not copied
verdicts         on consensus rows (all coders identical); disputed and
                 incomplete rows counted; per-coder verdicts printed beside
leakage          guess accuracy per coder, exact arm (chance 0.20) and document
                 set NONE/A/B/both (chance 0.40); LEAK_DETECTED when the
                 Agresti-Coull lower bound over committed guesses exceeds chance
strip            rows touched and words removed per arm, from the strip log
length           chars, words, APPROXIMATE tokens (chars / 4) for A, B, A+B
```

`python3 pathways.py --lengths`: A 11475 chars (~2869 tokens), B 19031
(~4758), A+B 30507 (~7627). B is 1.66x A. A vs B, and the combined arms
against either single arm, are confounded with context length.

## Commands

```sh
python3 pathways.py --features            # 19 markers, each located by line
python3 pathways.py --choices             # the decisions PREDICTIONS.md left open
python3 pathways.py --lengths
python3 pathways.py --emit run.jsonl --run-tag R1 --repeats 30
python3 pathways.py --prompt run.jsonl <id>
python3 pathways.py --sheet run.jsonl sheet.jsonl
python3 pathways.py --strip sheet.jsonl coder_sheet.jsonl strip_log.jsonl
python3 pathways.py --score run.key.jsonl --manifest m.json \
        --strip-log strip_log.jsonl coder1.jsonl coder2.jsonl
python3 test_pathways.py                  # constructed worlds; every verdict reachable
```

## Coders

At least two. A chat-side Claude that did not write the probes or
pathway B is eligible as one of them, declared `same_model_class: true`
in the manifest; the report then prints, once, that agreement with such a
coder bounds reliability and does not certify it. Having read both
documents, it is the coder most likely to recognise quotes, which the
per-coder guess accuracy measures.

## Refusals built in

```text
arm on the coding sheet            never; ids are opaque, key kept apart
filename in the prompt             never; neutral "Reference document N"
marker where a quote was stripped  never; the deletion is silent, the log separate
unclear                            counted, outside the denominator, never read as no
k below 3                          refused at emit
fewer than 2 coder files           refused at score
row from another run_tag           refused at score
edit inside the original predictions   printed as MISMATCH in every report
UNRESOLVED                         not equivalence; only TIE is
```

## Baseline of the root suite (pre-existing, not this folder)

Under `python3 -m unittest discover -s tests` and, after installing it
here, under pytest 9.1.1, the same three ids fail, with or without this
folder:

```text
tests/test_known_answer_gate.py::ToolRuns::test_tool_exits_clean
tests/test_run_manifest.py::TestRedirectContract::test_no_redirect_names_a_target_that_is_missing
tests/test_run_manifest.py::TestRedirectContract::test_the_one_known_violation_is_pinned
```

The earlier report of 8 failures under pytest came from another
environment and its ids were never recorded in this record, so an
id-level comparison with it is not possible from here. What is
established: in this container, both runners fail the same 3 ids.

## State

Nothing has been run. No model was called, no response coded. A world in
`test_pathways.py` returning the verdict it was built for shows the
verdict is reachable and says nothing about either file.
