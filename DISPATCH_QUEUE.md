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
