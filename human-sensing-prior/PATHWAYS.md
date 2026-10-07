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

Both are pinned by sha256 (amendment 2 item 4). `main` carries a later
revision of A on which the NEXTSTEP marker `**P4. Effective-N` no longer
locates; the predictions were not registered against it. `--emit` refuses
an A or B off the pins; after a merge supply the registered A with
`--a-file`.

## The length control arm AF (= A_PAD)

```text
AF   A's text, one blank line, then lorem-ipsum words cycled from the first,
     inside A's single reference block, cut at a word boundary so the AF
     block is not longer than B's block and within one word of it
     (19030 chars against 19031; 1190 filler words)        [CHOICE 14]
```

Two comparisons are added per class. Both are reported, and neither is
predicted: A vs AF (volume at fixed content) and AF vs B (structure at
matched length). Each A-vs-B verdict gets an attribution:

```text
A-vs-B     AF-vs-B               attribution
win X      same side wins        STRUCTURE_SURVIVES
win X      TIE or other side     NOT_SEPARABLE_FROM_VOLUME
TIE        TIE                   TIE_SURVIVES
TIE        a win                 TIE_NOT_SURVIVING
otherwise                        UNRESOLVED
```

The predictions are still scored on A vs B, as registered.

## Flow

```text
PREDICTIONS.md   original 6475 bytes committed first (7f780aa); amendments 1
      |          (7d49610) and 2 (0b04b02) appended before any run. Every
      |          report prints each registered layer (OK / MISMATCH) and the
      |          whole-file hash
      v
PILOT    --emit P --run-tag P1 --repeats 3      15 x 6 x 3 = 270 prompts
      |  ... same steps as below, manifest phase "pilot" ...
      |  --score: gate only (kappa >= 0.60 per class over all arms, no
      |  coder LEAK_DETECTED at either grain); no verdict, no pattern
      v  PILOT_PASS required; after PILOT_FAIL probes and predictions stay
pathways.py --emit OUT --run-tag T      15 probes x 6 arms x k (default 30 = 2700)
      |          arms NONE / A / AF / B / AB / BA (both orders, fixed)
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
      main manifest: phase "main", pilot_run_tag (not run_tag),
      pilot_result PILOT_PASS, or refused. Pilot rows carry the pilot
      run_tag and are refused by a main score, so they never reach the
      headline.
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

## Decision rules (amendment 1 item 2, amendment 2 item 3)

```text
TIE              whole interval inside [-0.15, +0.15], even when it excludes
                 0 (amendment 2 item 3: equivalence); needs ~87 coded rows
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
manifest         run_tag, phase, model, temperature, top_p, max_tokens,
                 system_prompt, date, coders (each with same_model_class);
                 main adds pilot_run_tag and pilot_result; refused if missing
variance         per-probe GOOD rates, between-probe SD, mean p(1-p), per arm
agreement        Cohen's kappa per class, min pairwise, plus percent agreement;
                 kappa IMPORTED from effective-redundancy-audit, not copied
verdicts         on consensus rows (all coders identical); disputed and
                 incomplete rows counted; per-coder verdicts printed beside
length control   A vs AF, AF vs B, attribution per class
leakage          guess accuracy per coder, exact arm (6 arms, chance 1/6 when
                 balanced) and document set NONE/A/B/both with AF counted as
                 A (chance 1/3); LEAK_DETECTED when the
                 Agresti-Coull lower bound over committed guesses exceeds chance
strip            rows touched and words removed per arm, from the strip log
length           chars, words, APPROXIMATE tokens (chars / 4) for A, AF, B, A+B
```

`python3 pathways.py --lengths`: A 11475 chars (~2869 tokens), AF 19030
(~4758), B 19031 (~4758), A+B 30507 (~7627). B is 1.66x A. A vs B is
confounded with context length; AF vs B is not. The combined arms are
longer than either single arm and stay confounded.

## Commands

```sh
python3 pathways.py --features            # 19 markers, each located by line
python3 pathways.py --choices             # the decisions PREDICTIONS.md left open
python3 pathways.py --lengths
python3 pathways.py --emit pilot.jsonl --run-tag P1 --repeats 3
python3 pathways.py --emit run.jsonl --run-tag R1 --repeats 30 [--a-file A.md]
python3 pathways.py --prompt run.jsonl <id> [--a-file A.md]
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
A or B off the registered sha      refused at emit
pilot key not k = 3 or missing an arm   refused at score
main score without PILOT_PASS      refused at score
fewer than 2 coder files           refused at score
row from another run_tag           refused at score
edit inside the original predictions   printed as MISMATCH in every report
UNRESOLVED                         not equivalence; only TIE is
```

## Baseline of the root suite (pre-existing, not this folder)

The earlier report of 8 failures under pytest came from another
environment and its ids were never recorded. They are not reconstructed
here. The comparison point is the KNOWN_RED pins at 59a5e5d (the merge
of #116 on main).

This branch does NOT contain #105 or #116. Its merge base with main is
9262516 (#115, 2026-10-05); neither d675fc7 (the #105 merge) nor 59a5e5d
is an ancestor of HEAD. So this branch's count is a count on an older
tree. It is not adopted as main's baseline.

```text
tree                       runner               failed  passed
59a5e5d (main, #116)       pytest               4       141
this branch HEAD           pytest and unittest  3       133
```

The 3 failing here are the 3 pinned at 59a5e5d. The fourth at 59a5e5d is
a test this branch does not have:

```text
tests/test_compile_gate.py::EveryModuleCompiles::test_no_module_binds_a_toplevel_name_twice   59a5e5d only
tests/test_known_answer_gate.py::ToolRuns::test_tool_exits_clean                         both
tests/test_run_manifest.py::TestRedirectContract::test_no_redirect_names_a_target_that_is_missing   both
tests/test_run_manifest.py::TestRedirectContract::test_the_one_known_violation_is_pinned           both
```

Running 59a5e5d's compile gate against this branch's tree fails 2 of its
tests: 7 files do not compile (syntax errors) and 16 top-level names are
bound twice. All of them are in
other folders (assessor-coupling, chain-position,
cooperative-substrate-proof, stability-trigger-envelope); none is in
human-sensing-prior. A merge into main inherits them unless main has
already repaired them.

## State

Nothing has been run: no pilot and no main run. No model was called and
no response was coded. A world in
`test_pathways.py` returning the verdict it was built for shows the
verdict is reachable and says nothing about either file.
