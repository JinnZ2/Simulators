# COLLISIONS

Generated from `collisions.json` by `check_concept_map.py --write`. Edit the JSON, not this file.
One block per multi-agent collision. Rows are kept, not resolved away; a resolved row stays.
As of 2026-11-11.

## 2026-11-11  GAP_INSTRUMENT

- agents: two Claude Code sessions
- what collided: one status name, two meanings (an instrument crash; a label the instrument does not recognise)
- how found: chat-side (Kavik + Claude), comparing the report of TAF PR 82 (GAP_INSTRUMENT = a module raised) with the report of PR 84 (= a label outside the severity table). PR tips dated 2026-11-11T14:15:59Z (82, a2c5d99) and 2026-11-11T14:15:24Z (84, 92cd578); the report texts themselves are not in a repo
- resolution: split into GAP_INSTRUMENT_CRASH / GAP_INSTRUMENT_UNRECOGNIZED_LABEL; both names are on unmerged branches only
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/82; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/85; TAF branches claude/unknown-axis-followup-2 (b85433c), claude/not-determinable-reason (92cd578)

## 2026-11-10/11  playground

- agents: Perplexity (study-aperture) / Claude Code (Simulators)
- what collided: two builds of one equation-substitution laboratory from related specs, different organisation
- how found: concept map survey, 2026-11-11
- resolution: OPEN: cross-run pending
- evidence: https://github.com/JinnZ2/Simulators/pull/257; study-aperture@origin/main:experimental/playground/; CONCEPT_MAP.md row 'playground'

## 2026-11-11  pipeline aggregation

- agents: three Claude Code sessions (three TAF PR branches)
- what collided: calibration/pipeline.py score aggregation changed three ways: PR 81 sets a no-score result to (None, Band.UNKNOWN) inline; PR 82 adds _aggregate returning 2 values, (None, NOT_MEASURED) with no module report; PR 84 adds _aggregate returning 3 values, the third a not_measured_reason
- how found: chat-side, TAF cleanup phase 1 inventory, trial merge of stack tips (TAF_CLEANUP_PHASE1_INVENTORY.md, not in the TAF checkout read here); the three diffs of calibration/pipeline.py were then read in this session on 2026-11-11 and match
- resolution: OPEN: pick pending
- note: Diffs read at PR tips ed275ef (81), a2c5d99 (82), 92cd578 (84). PR 81's title does not name the pipeline; the change is in its diff.
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/81; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/82; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/84

## 2026-11-11  expiry register

- agents: two sessions, as stated
- what collided: two registers of the same slots under different counting rules: PR 77 value rule, PR 78 token rule
- how found: PR 79 reconciles them
- resolution: both kept, split coded (PR 79 merged; 78 merged; 77 closed unmerged)
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/77; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/78; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/79

## 2026-11-10/11  provenance credit

- agents: Kimi / Kavik / DeepSeek
- what collided: Kimi audit section 1.1 'Provenance map of the dialogue' assigns P11 (physics common denominator) to DeepSeek. In the dialogue DeepSeek's reply opens 'You're right, and the correction matters' and says 'Your physics point is the strongest substrate-neutral anchor available', which places the point with the human. The human source has no row in the table; the section's prose names an 'unseen interlocutor'
- how found: chat-side read of the pinned texts, then a first-hand check by the forest-ledger session (FML_035); the quoted lines were re-read in this session on 2026-11-11 (audit table line 43; chat paste lines 425 and 436)
- resolution: recorded; uncorrected in source
- note: The texts are on the PR 256 branch, not in this tree. The delivered commit id 4cf10ec does not resolve in this checkout; the PR tip read here is d402fa8.
- evidence: https://github.com/JinnZ2/Simulators/pull/256; forest-model-ledger/ledger/toolkit/cases/texts/kimi_substrate_neutral_intelligence_audit.md (section 1.1); forest-model-ledger/ledger/toolkit/cases/texts/chat_paste_2026-11-10.txt; forest-model-ledger/CLAIM_TABLE.md FML_035 (same branch)
