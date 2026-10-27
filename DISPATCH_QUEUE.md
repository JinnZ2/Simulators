# DISPATCH_QUEUE

Approved by Kavik 2026-10-10.

Purpose: standing-rule step 5 needs a queue both sessions can read.
Chat-side memory is unreachable from Claude Code, so it is mirrored here.
This file replaces the chat-side queue for step 5. Keep both in sync;
the repo file is authoritative for Claude Code.

Standing rule:
  Before any build: read this file, record branch + scope,
  skip if another session holds it. After merge/close: update
  the line, never delete it (append-only).

Format: append-only, one line per branch, pipe-delimited:
  branch | scope paths | session | status | date

A later line for the same branch supersedes an earlier one. Nothing
above it is edited or removed.

## Seed (as dispatched, 2026-10-10)

claude/presignal-ledger      | tools/presignal_ledger.py | — | merge-ready #137 | 2026-10-10
claude/threshold-states-escape | UNKNOWN | — | open | 2026-10-07
claude/baseline-by-id          | UNKNOWN | — | open | 2026-10-07
claude/sense-as-match          | UNKNOWN | — | open | 2026-10-07
claude/coinage-log-status-split| UNKNOWN | — | open | 2026-10-07
claude/human-sensing-prior     | UNKNOWN | — | open | 2026-10-07

## Log

claude/dispatch-queue | DISPATCH_QUEUE.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/presignal-ledger | tools/presignal_ledger.py | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #137 (merged 2026-10-09; tip 6ca6a34 in main) | 2026-10-10
claude/threshold-states-escape | UNKNOWN | — | MERGED #123 (tip 378b4ee in main) | 2026-10-10
claude/baseline-by-id | UNKNOWN | — | MERGED #119 (0a04bea); no remote branch | 2026-10-10
claude/sense-as-match | UNKNOWN | — | NOT_FOUND under this name; claude/repin-sense-as-match tip 948f508 in main | 2026-10-10
claude/coinage-log-status-split | UNKNOWN | — | MERGED #121 (59b71f8); no remote branch | 2026-10-10
claude/human-sensing-prior | UNKNOWN | — | NOT_FOUND under this name; claude/human-sensing-prior-cc0-cbm411 tip 9202714 open, not in main | 2026-10-10
claude/dispatch-queue | DISPATCH_QUEUE.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #145 (03cd312); line appended via claude/dispatch-queue-145 | 2026-10-10
claude/bin-self-test | tools/bin_self_test.md, tools/coupling_and_accumulation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/bin-self-test | tools/bin_self_test.md, tools/coupling_and_accumulation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/bin-self-test | tools/bin_self_test.md, tools/coupling_and_accumulation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #148 (3e18eb0) | 2026-10-10
method-layer:claude/bin-self-test | tools/bin_self_test.md, tools/coupling_and_accumulation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#4 (1fb7f6f) | 2026-10-10
claude/bin-self-test-fill | tools/bin_self_test.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/bin-self-test-fill | tools/bin_self_test.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/bin-self-test-fill | tools/bin_self_test.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #151 (04cd9f6) | 2026-10-10
method-layer:claude/bin-self-test-fill | tools/bin_self_test.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#5 (ecca94f) | 2026-10-10
claude/uncounted-observer | tools/uncounted_observer_isolation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/uncounted-observer | tools/uncounted_observer_isolation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/uncounted-observer | tools/uncounted_observer_isolation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #154 (795403e) | 2026-10-10
method-layer:claude/uncounted-observer | tools/uncounted_observer_isolation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#6 (4692249) | 2026-10-10
claude/contested-area | tools/contested_area_hidden_assumption.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/contested-area | tools/contested_area_hidden_assumption.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/contested-area | tools/contested_area_hidden_assumption.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #157 (fd4f928) | 2026-10-10
method-layer:claude/contested-area | tools/contested_area_hidden_assumption.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#7 (259d49b) | 2026-10-10
claude/landauer-floor | tools/landauer_floor_vs_run_cost.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/landauer-floor | tools/landauer_floor_vs_run_cost.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/landauer-floor | tools/landauer_floor_vs_run_cost.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #160 (b4c2032) | 2026-10-10
method-layer:claude/landauer-floor | tools/landauer_floor_vs_run_cost.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#8 (a23f074) | 2026-10-10
claude/landauer-floor-tags | tools/landauer_floor_vs_run_cost.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/landauer-floor-tags | tools/landauer_floor_vs_run_cost.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/contested-area-observed | tools/contested_area_hidden_assumption.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/contested-area-observed | tools/contested_area_hidden_assumption.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/landauer-floor-tags | tools/landauer_floor_vs_run_cost.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #163 (82f8d57) | 2026-10-10
method-layer:claude/landauer-floor-tags | tools/landauer_floor_vs_run_cost.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#9 (46c4859) | 2026-10-10
claude/contested-area-observed | tools/contested_area_hidden_assumption.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #164 (6bda958) | 2026-10-10
method-layer:claude/contested-area-observed | tools/contested_area_hidden_assumption.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#10 (29a845a) | 2026-10-10
claude/natural-two-senses | tools/natural_two_senses.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/natural-two-senses | tools/natural_two_senses.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/natural-two-senses | tools/natural_two_senses.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #167 (aeb5a4b) | 2026-10-10
method-layer:claude/natural-two-senses | tools/natural_two_senses.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#11 (c24f353) | 2026-10-10
claude/natural-two-senses-coupling | tools/natural_two_senses.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
method-layer:claude/natural-two-senses-coupling | tools/natural_two_senses.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-10
claude/natural-two-senses-coupling | tools/natural_two_senses.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #170 (a373d28) | 2026-10-10
method-layer:claude/natural-two-senses-coupling | tools/natural_two_senses.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#12 (79bd44c) | 2026-10-10
claude/held-tie-bin-slack | tools/held_tie_precision.md, tools/bin_slack_conservation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-11
method-layer:claude/held-tie-bin-slack | tools/held_tie_precision.md, tools/bin_slack_conservation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD | 2026-10-11
claude/held-tie-bin-slack | tools/held_tie_precision.md, tools/bin_slack_conservation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #173 (6491f1e) | 2026-10-11
method-layer:claude/held-tie-bin-slack | tools/held_tie_precision.md, tools/bin_slack_conservation.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED method-layer#13 (1ac1a8c) | 2026-10-11
claude/coinage-log-source | coinage-log/source/coinage-log.full.md, coinage-log/MISSING_SOURCE.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 7 chunks) | 2026-10-11
claude/telling-installs-the-limit | tools/telling_installs_the_limit.md | session_01U4mRsfZAdaV1xWBmZSRbjK | HELD | 2026-10-12
method-layer:claude/telling-installs-the-limit | tools/telling_installs_the_limit.md | session_01U4mRsfZAdaV1xWBmZSRbjK | HELD | 2026-10-12
claude/telling-installs-the-limit | tools/telling_installs_the_limit.md | session_01U4mRsfZAdaV1xWBmZSRbjK | MERGED #178 (a915fad) | 2026-10-12
method-layer:claude/telling-installs-the-limit | tools/telling_installs_the_limit.md | session_01U4mRsfZAdaV1xWBmZSRbjK | MERGED method-layer#14 (6f632a8) | 2026-10-12
claude/coinage-log-source | coinage-log/source/coinage-log.full.md, coinage-log/MISSING_SOURCE.md, coinage-log/check_coinage.py (scope extended by ratification) | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #176 (e1bb85b; merge 54676a9) | 2026-10-12
claude/human-sensing-prior-cc0-cbm411 | human-sensing-prior/*, CLAUDE.md, README.md, notes/queue/HOLDS.md | session_01U4mRsfZAdaV1xWBmZSRbjK | MERGED #182 (e71df2c); amendment 4 | 2026-10-12
claude/no-anchor-source | memory-archive/no-anchor-information-mismanagement.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 8 chunks) | 2026-10-12
claude/no-anchor-source | memory-archive/no-anchor-information-mismanagement.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #185 (258895c; merge d4e66ff) | 2026-10-12
claude/funnel-governance-source | memory-archive/funnel-governance-precursor-match.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 7 chunks) | 2026-10-12
claude/funnel-governance-source | memory-archive/funnel-governance-precursor-match.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #188 (954ec1c; merge 61bc726) | 2026-10-12
claude/corpus-as-sample-source | memory-archive/corpus-as-sample-not-reality.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 8 chunks) | 2026-10-12
claude/corpus-as-sample-source | memory-archive/corpus-as-sample-not-reality.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #191 (3ff325d; merge 7b374c4) | 2026-10-12
claude/cross-layer-step-register-source | memory-archive/cross-layer-step-register.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 8 chunks) | 2026-10-12
claude/cross-layer-step-register-source | memory-archive/cross-layer-step-register.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #194 (bab1447; merge d71b789) | 2026-10-12
claude/when-to-decouple-source | memory-archive/when-to-decouple-triage-and-fail-safe.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 8 chunks) | 2026-10-12
claude/when-to-decouple-source | memory-archive/when-to-decouple-triage-and-fail-safe.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #197 (a27cd49; merge d31b46c) | 2026-10-12
claude/coupling-is-the-floor-source | memory-archive/coupling-is-the-floor-separation-is-the-artifact.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 8 chunks) | 2026-10-12
claude/coupling-is-the-floor-source | memory-archive/coupling-is-the-floor-separation-is-the-artifact.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #200 (83166f0; merge ebfffa7) | 2026-10-12
claude/measurand-stage-attribution-source | memory-archive/measurand-stage-attribution-failures.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 7 chunks) | 2026-10-12
claude/measurand-stage-attribution-source | memory-archive/measurand-stage-attribution-failures.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #203 (d8adf4d; merge 12fa2ff) | 2026-10-12
claude/value-vocabulary-threshold-source | memory-archive/value-vocabulary-threshold-register.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 7 chunks) | 2026-10-12
claude/value-vocabulary-threshold-source | memory-archive/value-vocabulary-threshold-register.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #206 (2b1da47; merge 553940c) | 2026-10-12
claude/unmarked-boundary-source | memory-archive/unmarked-boundary-as-root-error-class.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (awaiting 7 chunks) | 2026-10-12
claude/unmarked-boundary-source | memory-archive/unmarked-boundary-as-root-error-class.md | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #209 (3765ffe; merge b9e14ec) | 2026-10-12
claude/field-mode-eval | field-mode-eval/ | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (building; standalone repo creation refused, lands as folder) | 2026-10-13
claude/field-mode-eval | field-mode-eval/ | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #212 (23a711a; merge ac81878) | 2026-10-13
claude/evidence-demotion-detector | evidence-demotion-detector/ | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (building; standalone repo creation refused, lands as folder) | 2026-10-13
claude/evidence-demotion-detector | evidence-demotion-detector/ | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #215 (2332d52; merge 1a87487) | 2026-10-13
claude/edd-affect-negation | evidence-demotion-detector/ | session_01Y4zVdoRHPDHpVwSPbqbeLR | HELD (fix: AFFECT_ASSERT negated-mention suppression) | 2026-10-13
claude/edd-affect-negation | evidence-demotion-detector/ | session_01Y4zVdoRHPDHpVwSPbqbeLR | MERGED #218 (d241cb7; merge 9216ca6) | 2026-10-13
claude/reversible-loop-triage-rubric-2vu4tt | tools/experiment_fruitfulness_triage.md, tools/experiment_fruitfulness_triage.py, tools/known_answer.py, tests/test_known_answer_gate.py, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | HELD (building; method-layer mirror out of session scope) | 2026-10-13
claude/reversible-loop-triage-rubric-2vu4tt | tools/experiment_fruitfulness_triage.md, tools/experiment_fruitfulness_triage.py, tools/samples/experiment_fruitfulness_triage.sample.txt, tools/known_answer.py, tests/test_known_answer_gate.py, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | HELD (built, pushed 60e83c7, not merged; scope adds the sample report; method-layer mirror out of session scope) | 2026-10-14
claude/reversible-loop-triage-rubric-2vu4tt | tools/experiment_fruitfulness_triage.md, tools/experiment_fruitfulness_triage.py, tools/samples/experiment_fruitfulness_triage.sample.txt, tools/external_report_audit_okcomputer.md, tools/check_citations.py, tools/contested_area_hidden_assumption.md, tools/coupling_vs_border_energy_yardstick.md, tools/yardstick.py, tools/samples/, tools/known_answer.py, tests/test_known_answer_gate.py, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | HELD (WO-3 built 60e83c7, not merged; WO-4 audit + WO-5 worked instance and yardstick building) | 2026-10-14
method-layer:claude/reversible-loop-triage-rubric-2vu4tt | tools/contested_area_hidden_assumption.md, tools/coupling_vs_border_energy_yardstick.md | session_01XBfHEmzGNs1ituvWMBetcX | HELD (WO-5 mirror) | 2026-10-14
claude/reversible-loop-triage-rubric-2vu4tt | tools/experiment_fruitfulness_triage.md, tools/experiment_fruitfulness_triage.py, tools/samples/experiment_fruitfulness_triage.sample.txt, tools/samples/yardstick.sample.txt, tools/external_report_audit_okcomputer.md, tools/check_citations.py, tools/contested_area_hidden_assumption.md, tools/coupling_vs_border_energy_yardstick.md, tools/yardstick.py, tools/known_answer.py, tests/test_known_answer_gate.py, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | MERGED #226 (11bb73f; merge 3e82e73) | 2026-10-14
method-layer:claude/reversible-loop-triage-rubric-2vu4tt | tools/contested_area_hidden_assumption.md, tools/coupling_vs_border_energy_yardstick.md, README.md | session_01XBfHEmzGNs1ituvWMBetcX | MERGED method-layer#20 (9f13670; merge 9c6d5b0) | 2026-10-14
claude/reversible-loop-triage-rubric-2vu4tt | tools/contested_area_hidden_assumption.md, tools/coupling_vs_border_energy_yardstick.md, tools/yardstick.py | session_01XBfHEmzGNs1ituvWMBetcX | HELD (WO-5 re-render from the delivered order; supersedes the summary-based render f247f94) | 2026-10-15
method-layer:claude/reversible-loop-triage-rubric-2vu4tt | tools/contested_area_hidden_assumption.md, tools/coupling_vs_border_energy_yardstick.md | session_01XBfHEmzGNs1ituvWMBetcX | HELD (WO-5 re-render mirror; supersedes 9f13670) | 2026-10-15
claude/reversible-loop-triage-rubric-2vu4tt | tools/contested_area_hidden_assumption.md, tools/coupling_vs_border_energy_yardstick.md, tools/yardstick.py | session_01XBfHEmzGNs1ituvWMBetcX | MERGED #228 (29c0fb9; merge bf07acc) | 2026-10-15
method-layer:claude/reversible-loop-triage-rubric-2vu4tt | tools/contested_area_hidden_assumption.md, tools/coupling_vs_border_energy_yardstick.md | session_01XBfHEmzGNs1ituvWMBetcX | MERGED method-layer#21 (025ece1; merge 27952f8) | 2026-10-15
claude/reversible-loop-triage-rubric-2vu4tt | tools/experiment_fruitfulness_triage.md, tools/clean_run_wo3/, tools/triage_clean_run.py, tools/known_answer.py, tests/test_known_answer_gate.py, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | HELD (WO-3 clean run + second scorer via fresh session; PROPOSED GA (g) variants) | 2026-10-15
claude/reversible-loop-triage-rubric-2vu4tt | tools/experiment_fruitfulness_triage.md, tools/clean_run_wo3/, tools/triage_clean_run.py, tools/known_answer.py, tests/test_known_answer_gate.py, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | MERGED #231 (5eb76eb, 5d230ba; merge f3b1c74) | 2026-10-15
claude/reversible-loop-triage-rubric-2vu4tt | tools/experiment_fruitfulness_triage.md, tools/blind_run_wo3/, tools/triage_blind_run.py, tools/samples/triage_blind_run.sample.txt, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | MERGED #234 (58016a4, 95d2579, bf0af2d, e7e463f; merge f5f5ccf) WO-3 blind run on post-cutoff anchor BLIND; second scorer CONTAMINATED-BY-PRIOR; independent second scorer still owed | 2026-10-16
claude/reversible-loop-triage-rubric-2vu4tt | reg-uncertainty-registry/ | session_01XBfHEmzGNs1ituvWMBetcX | HELD (WO-REG-1 regulatory uncertainty registry: kimmy_v1 landed verbatim as SOURCE, REVIEW_v1 adjudicated as NCRs, night shift added, RUS-0.2, stdlib tools) | 2026-10-18
claude/reversible-loop-triage-rubric-2vu4tt | reg-uncertainty-registry/, tools/known_answer.py, tests/test_known_answer_gate.py, KNOWN_RED.md, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | MERGED #236 (squash through 6c30e92) + #237 (merge b2d5e23) WO-REG-1 consolidated bundle: registry built and validated, RUS-0.2 reproduces Annex A, RUS-0.3 PROPOSED, report rendered from registry; second coding NOT returned (RUR_016 UNVERIFIED); supersedes the 2026-10-18 HELD line | 2026-10-25
claude/reversible-loop-triage-rubric-2vu4tt | floor-capability/, tools/known_answer.py, tests/test_known_answer_gate.py, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | MERGED #239 (1a91643; merge 8820bd3) FLOOR CAPABILITY draft v0 landed (via compaction summary, pinned) and instrumented; FLC_001..017; all CONSTRUCTED, FLC_016 UNVERIFIED (no plant data) | 2026-10-25
claude/gap-instruments | gap-instruments/, tools/gap_instruments.py, README.md, CLAUDE.md | session_01JDQmXAxtSZNqWDfLcp3yks | OPEN (gap_instruments.py + gating_diagnostic.py landed verbatim in source/, eight marked fixes in the working copy, mirrored to tools/ here and in method-layer) | 2026-10-25
claude/reversible-loop-triage-rubric-2vu4tt | extraction-chain-join/, tools/known_answer.py, tests/test_known_answer_gate.py, README.md, CLAUDE.md | session_01XBfHEmzGNs1ituvWMBetcX | MERGED #241 (44a6f8b, c8e6ef8, e4957be, cc24b0c; merge cb972f3) extraction-money-power-emissions chain: order RECONSTRUCTED from the session summary (ECJ_001); G1..G7 instruments + chain join, coverage on every reading, NO_PATTERN added, end-to-end effect refused; ECJ_001..020, all CONSTRUCTED, ECJ_020 UNVERIFIED (no custodian records) | 2026-10-25
claude/glyph-inward-gaps | held-gaps/, tools/glyph_reasoning.md, tools/inward_turn.md, GAP_INDEX.md, CLAUDE.md | session_01JDQmXAxtSZNqWDfLcp3yks | OPEN (GAP 1-4 filed as indexed open questions; GLYPH and INWARD-TURN as shared tools docs, mirrored in method-layer) | 2026-10-27
claude/reversible-loop-triage-rubric-2vu4tt | gap-instruments/gap_instruments.py, tools/gap_instruments.py, gap-instruments/README.md, gap-instruments/samples/, tools/known_answer.py, README.md, CLAUDE.md; method-layer tools/gap_instruments.py | session_01XBfHEmzGNs1ituvWMBetcX | OPEN (work order "gap_instruments.py extension": A1 limit_basis, A2 CalibrationRecord + calibration_summary, A3 ConfoundRecord; built on #243 head 0802bc1, merged into this branch, not rebuilt; the reshaped method-layer/gap_instruments.py not extended) | 2026-10-27
