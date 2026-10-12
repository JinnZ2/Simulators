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
an A or B off the pins.

That marker was renamed, not removed. Main's A splits the registered P4
("Effective-N for the animal evidence") into P4a ("Independent-origin
count", a new test that needs a topology only) and P4b ("Phylogenetic
independent contrasts", the registered P4's test, which now needs branch
lengths). Recorded in PREDICTIONS.md, amendment 2 note 1 (fb42189).
Results bind to the registered A only; main's A needs its own
pre-registered run before it is tested.

A is read from `registered/human-sensing-prior.7f780aa.md`, a byte copy of
A at 7f780aa. It matches the pin [CHOICE 16]. The merge of main (79e6374)
replaced the working copy with main's revision (sha256 a5c4b6cf...). Every
report prints the working copy as LIVE and does not test it. `--a-file`
overrides the default.

## The length control arm AF (= A_PAD)

```text
AF   A's text, one blank line, then lorem-ipsum words cycled from the first,
     inside A's single reference block, cut at a word boundary so the AF
     block is not longer than B's block and within one word of it
     (19029 chars against 19030; 1190 filler words)        [CHOICE 14]
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

The filler is recorded by hash in PREDICTIONS.md, amendment 2 note 1
(fb42189): source is the standard lorem-ipsum word list (69 words, pathways.py
LOREM); genre is typesetting placeholder text. filler(1190) is 7553 chars,
sha256 1a39c66c...9fe99c; af_text(A_reg, 1190) is 18999 chars, sha256
e570b26d...79a745. test_pathways.py checks the filler hash against the note.

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

`python3 pathways.py --lengths`: A 11474 chars (~2868 tokens), AF 19029
(~4757), B 19030 (~4758), A+B 30504 (~7626), with the unnumbered labels of
amendment 3. B is 1.66x A. A vs B is
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
python3 pathways.py --emit-job runs/<tag>.json --run-tag <tag> [--phase pilot|main] \
        [--repeats K] [--seed N] [--tier default]      # salt generated: SEALED
python3 pathways.py --size-check runs/<tag>.json --context-limit N \
        --reserve-output M --limit-source "<where N comes from>" --out size.json
python3 pathways.py --import-runner results.jsonl --job runs/<tag>.json \
        --sheet sheet.jsonl --key key.jsonl --manifest-stub m.json
python3 pathways.py --reveal runs/<tag>.json --expect <sha256 from HOLDS>
python3 test_pathways.py                  # constructed worlds; every verdict reachable
```

## The chat-side runner (amendment 3)

There is no model endpoint here. Runs go through a claude.ai artifact that
uses the platform's sample capability; the operator taps batches.

```text
--emit-job        one JSON file, format pathways-run/1
                  template "{DOCUMENTS}Question: {QUESTION}"
                  doc_separator ""   no_doc_text ""
                  documents A, B, AF, each "Reference document:\n<<<\n" + text + "\n>>>\n\n"
                  documents_source: raw sha256 per document (A, B = the pins)
                  items: id, arm, class, probe, repeat (1-based), docs, question,
                         prompt_sha256; ordered by opaque id
                  every prompt is built by the harness and checked against the
                  runner assembly before the file is written
runner            docs_text = docs ? doc_separator.join(documents[k]) : no_doc_text
                  prompt = template, {DOCUMENTS} then {QUESTION}, literal
                  hash differs -> not sent, status hash_mismatch
--import-runner   answered -> coding sheet (no arm)
                  refused / empty -> outcomes, coded "no" by the harness from
                  the key, off the sheet, outside kappa and the leak check
                  (amendment 4 item 4)
                  error / hash_mismatch / prompt_too_large / no row -> NOT_DELIVERED,
                  counted per class per arm, not coded, not imputed
                  writes the key (with each item's runner status and the job
                  sha256) and a manifest stub (runner strings, tier counts, job
                  sha256, blind from the salt source; date from the results;
                  coders and size_check left to fill)
--score           accepts PLATFORM_DEFAULT_NOT_SETTABLE, PLATFORM_FRAMING_NOT_VISIBLE,
                  the runner model string, model_tier_requested and
                  model_tier_applied_counts; refuses more than one applied tier
                  or a tier other than the one requested
                  amendment 4: refuses a runner manifest without job_sha256,
                  blind (SEALED or COMPROMISED) and a PASS size_check for the
                  same job; a COMPROMISED pilot cannot pass the gate, a
                  COMPROMISED main run is refused; contrasts are flagged
                  LOSS_DIFFERENTIAL / OUTCOME_DIFFERENTIAL when the two arms'
                  NOT_DELIVERED or fixed-code counts differ; A vs B is also
                  printed with fixed-code rows excluded (sensitivity only)
```

The empty separator and no_doc_text are deliberate: a runner that swaps in
a default for an empty string breaks exactly the hashes it touched (all 45
NONE items for no_doc_text), so the change shows as hash_mismatch.

Scope: single model, single platform. Exact model and sampling settings
are not visible; that is a limit, not a check. The job file, the results
and the key carry the arm. They are key material and go to no coder.

## Blinding, size check, missingness (amendment 4)

```text
job file           not committed until coding closes; runs/ is git-ignored;
                   its sha256 goes in notes/queue/HOLDS.md and the manifest
salt               generated at emission (32 hex), lives only in the job file
reveal             after coding closes: commit the file, --reveal must say VERIFIED
size check         bytes per prompt (>= 1 byte per token, assumed) + reserve
                   <= declared context limit, or no run; limit and its source
                   declared by the operator, none assumed
NOT_DELIVERED      per class per arm; any arm difference flags the contrast;
                   nothing imputed, nothing dropped to balance
refused / empty    fixed code "no"; counts per class per arm; any arm
                   difference flags the contrast
```

pilot-2026-10-08a (commit 6f1544c, file sha256
5e55685f8f8922186a843782c773456e5d72394550626114c123528382b86457) is
COMPROMISED: it is in public history and its ids use the public salt
"hsp", so the arm map can be recomputed from the code. It is retired unrun
and removed from the tree head. Its replacement is pilot-2026-10-08b, 270
items, file sha256
227bc386f8c5cd764fcd329aa6802b3ac7d40f78653f97a32dc87e609de0b6a8, salt
generated, not committed. Every prompt hash equals 10-08a's prompt for the
same (probe, arm, repeat); only the ids and the salt differ.

`python3 pathways.py --size-check` on that job (samples/size_check.sample.txt)
reads REFUSED_UNDECLARED: the largest item is 30696 bytes (AB and BA), so
any declared limit of at least 30696 plus the output reserve passes.

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
filename in the prompt             never; neutral "Reference document:"
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

Before main was merged in, this branch did not contain #105 or #116. Its
merge base with main was 9262516 (#115, 2026-10-05), and neither d675fc7
(the #105 merge) nor 59a5e5d was an ancestor of it. Its count was a
count on an older tree and was not adopted as main's baseline. Another
session then merged main into the branch (79e6374, see notes/queue/HOLDS.md).
The branch now contains 59a5e5d, and its merge base with main is main.

```text
tree                               runner               failed  passed
59a5e5d (main, #116)               pytest               4       141
branch before the merge (0b04b02)  pytest and unittest  3       133
branch after the merge             pytest               4       144
```

Before the merge, the branch failed the 3 ids pinned at 59a5e5d. The
fourth was a test the branch did not yet have. After the merge, it fails
exactly the 4 pinned ids. `python3 tools/known_red_check.py --suite`
reads 28 pins: 28 MATCH, 0 MISMATCH, VERDICT PASS.

```text
tests/test_compile_gate.py::EveryModuleCompiles::test_no_module_binds_a_toplevel_name_twice
tests/test_known_answer_gate.py::ToolRuns::test_tool_exits_clean
tests/test_run_manifest.py::TestRedirectContract::test_no_redirect_names_a_target_that_is_missing
tests/test_run_manifest.py::TestRedirectContract::test_the_one_known_violation_is_pinned
```

Before the merge, running 59a5e5d's compile gate on the branch failed 2
of its tests: 7 files did not compile and 16 top-level names were bound
twice, all outside human-sensing-prior. Main had repaired the 7 files by
59a5e5d (archive moves and restores). After the merge, only the
duplicate-names test fails, as pinned. Nothing in human-sensing-prior is
on either list.

## State

Pilot: SEALED JOB EMITTED, NOT LOADED. pilot-2026-10-08a was loaded into
the runner (HOLDS [f]) and retired unrun by amendment 4 (COMPROMISED).
pilot-2026-10-08b replaces it. Before any call: load 10-08b, record a new
order seed, and record a PASS size check against a declared limit. The
pilot runs first under its own run_tag, as amendment 2 item 2 requires.

Nothing has been run: no pilot and no main run. No model was called and
no response was coded. A world in
`test_pathways.py` returning the verdict it was built for shows the
verdict is reachable and says nothing about either file.

## Still open (operator, 2026-10-07; recorded, not built)

- AMENDMENT 2 (optional, dated if taken): a length-matched arm A_PAD,
  pathway A padded to B's length, to separate content from context length.
  Not written. PREDICTIONS.md carries amendment 1 only.
- Pilot at k = 3 before the full run. Pilot rows are excluded from the
  headline.
- The merge of main (79e6374) brought #116's edits into pathway A. A is
  now 15318 chars (it was 11475 when the predictions were registered),
  and the NEXTSTEP feature marker `**P4. Effective-N` no longer occurs in
  A (#116 split P4 into P4a/P4b). test_pathways.py reads 96/2 for that
  reason. Repoint the marker, or pin A to its registered text: the
  operator's call, not made here.

Resolution, same day, after the merge (b0c8795 and its follow-up):

- AMENDMENT 2 is written (0b04b02), and the harness implements it. The arm
  is named AF in the amendment and the code. AF is the A_PAD above.
- The k = 3 pilot gate is built. A main score is refused without
  PILOT_PASS from a pilot under another run_tag.
- Pathway A drift: pinned, not repointed. Amendment 2 item 4 registered the
  pin, and A is read from the registered copy [CHOICE 16]. The feature
  marker `**P4. Effective-N` locates in the registered copy. Testing
  main's revision of A would need its own registration.
