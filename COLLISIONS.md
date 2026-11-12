# COLLISIONS

Generated from `collisions.json` by `check_concept_map.py --write`. Edit the JSON, not this file.
One block per multi-agent collision. Rows are kept, not resolved away; a resolved row stays.
As of 2026-11-11.

## 2026-11-11  GAP_INSTRUMENT

- agents: two Claude Code sessions
- what collided: one status name, two meanings (an instrument crash; a label the instrument does not recognise)
- how found: chat-side (Kavik + Claude), comparing the report of TAF PR 82 (GAP_INSTRUMENT = a module raised) with the report of PR 84 (= a label outside the severity table). PR tips dated 2026-11-11T14:15:59Z (82, a2c5d99) and 2026-11-11T14:15:24Z (84, 92cd578); the report texts themselves are not in a repo
- resolution: split into GAP_INSTRUMENT_CRASH / GAP_INSTRUMENT_UNRECOGNIZED_LABEL; both names are on unmerged branches only
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/82; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/85; `thermodynamic-accountability-framework:calibration@origin/claude/unknown-axis-followup-2`; `thermodynamic-accountability-framework:calibration@origin/archive/not-determinable-reason`
- side TAF PR 82 (thermodynamic-accountability-framework, 2 commits, 2026-11-11T09:03:08+00:00 .. 2026-11-11T14:15:59+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWFx2jFzaiK4egn9iaJ | https://claude.ai/code/session_01BSBFWLfMGR7yRZZCUHBs9g
  - commits: a2c5d99, f12fc01
- side TAF PR 84 (thermodynamic-accountability-framework, 2 commits, 2026-11-11T14:04:17+00:00 .. 2026-11-11T14:15:24+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWFx2jFzaiK4egn9iaJ
  - commits: 92cd578, f603b43

## 2026-11-10/11  playground

- agents: Perplexity (study-aperture) / Claude Code (Simulators)
- what collided: two builds of one equation-substitution laboratory from related specs, different organisation
- how found: concept map survey, 2026-11-11
- resolution: OPEN: cross-run pending
- evidence: https://github.com/JinnZ2/Simulators/pull/257; `study-aperture:experimental/playground@origin/main`; `Simulators:CONCEPT_MAP.md`
- side study-aperture experimental/playground (study-aperture, 18 commits, 2026-11-11T03:33:20+00:00 .. 2026-11-11T12:06:41+00:00): model Perplexity (trailer names no model version); session VOID
  - commits: 1fc37a8, 12beac8, c0873df, e4a9bc9, bbd7c76, 8f8ae94, a441494, e433071, 28efc3e, e5541f9, c780f5c, 05b2f1a, 474db2a, 18b8722, c86d6b9, ea34f5c, 9587178, 79f402c
- side Simulators PR 257 relational-playground/ (Simulators, 16 commits, 2026-11-11T08:43:46+00:00 .. 2026-11-11T20:14:00+00:00): model Claude Fable 5.2; session https://claude.ai/code/session_01BSBFWG4whgMfkPUeexTM9s
  - commits: 02bc605, a1c04ae, 512f320, c395a41, beac98b, f9a1aac, 2cdfd53, 02dd4c7, d31383b, 70e546f, 9b8c5e2, 92a8ca9, decb1a7, 7b06c26, 861b7c5, 62e8fb7

## 2026-11-11  pipeline aggregation

- agents: three Claude Code sessions (three TAF PR branches)
- what collided: calibration/pipeline.py score aggregation changed three ways: PR 81 sets a no-score result to (None, Band.UNKNOWN) inline; PR 82 adds _aggregate returning 2 values, (None, NOT_MEASURED) with no module report; PR 84 adds _aggregate returning 3 values, the third a not_measured_reason
- how found: chat-side, TAF cleanup phase 1 inventory, trial merge of stack tips (TAF_CLEANUP_PHASE1_INVENTORY.md, not in the TAF checkout read here); the three diffs of calibration/pipeline.py were then read in this session on 2026-11-11 and match
- resolution: picked 2026-11-11 (Kavik): three-value (score, band, reason) from PR 84 plus the no-score -> UNKNOWN rule from PR 81, folded on the PR 85 branch (65bb724); 80/82/84 closed, branches kept under archive/
- note: Diffs read at PR tips ed275ef (81), a2c5d99 (82), 92cd578 (84). PR 81's title does not name the pipeline; the change is in its diff.
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/81; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/82; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/84; `thermodynamic-accountability-framework:calibration/pipeline.py@origin/archive/silent-fill-register`; `thermodynamic-accountability-framework:calibration/pipeline.py@origin/archive/unknown-axis-followup`; `thermodynamic-accountability-framework:calibration/pipeline.py@origin/archive/not-determinable-reason`; TAF_CLEANUP_PHASE1_INVENTORY.md: NOT COMMITTED as of 2026-11-11 (written to a cleanup-session scratchpad); to be linked at TAF docs/cleanup/ when it lands
- side TAF PR 81 (thermodynamic-accountability-framework, 1 commit, 2026-11-11T08:54:31+00:00 .. 2026-11-11T08:54:31+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWFx2jFzaiK4egn9iaJ
  - commits: ed275ef
- side TAF PR 82 (thermodynamic-accountability-framework, 1 commit, 2026-11-11T09:03:08+00:00 .. 2026-11-11T09:03:08+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWLfMGR7yRZZCUHBs9g
  - commits: f12fc01
- side TAF PR 84 (thermodynamic-accountability-framework, 1 commit, 2026-11-11T14:04:17+00:00 .. 2026-11-11T14:04:17+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWFx2jFzaiK4egn9iaJ
  - commits: f603b43

## 2026-11-11  expiry register

- agents: two sessions, as stated
- what collided: two registers of the same slots under different counting rules: PR 77 value rule, PR 78 token rule
- how found: PR 79 reconciles them
- resolution: both kept, split coded (PR 79 merged; 78 merged; 77 closed unmerged)
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/77; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/78; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/79
- side TAF PR 77 (thermodynamic-accountability-framework, 1 commit, 2026-11-11T01:17:29+00:00 .. 2026-11-11T01:17:29+00:00): model Claude Fable 5.2; session https://claude.ai/code/session_01BSBFWG4whgMfkPUeexTM9s
  - commits: 614b795
- side TAF PR 78 (thermodynamic-accountability-framework, 3 commits, 2026-11-11T00:41:06+00:00 .. 2026-11-11T00:42:59+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWLfMGR7yRZZCUHBs9g
  - commits: e177780, bbe4da9, c777c6e

## 2026-11-10/11  provenance credit

- agents: Kimi / Kavik / DeepSeek
- what collided: Kimi audit section 1.1 'Provenance map of the dialogue' assigns P11 (physics common denominator) to DeepSeek. In the dialogue DeepSeek's reply opens 'You're right, and the correction matters' and says 'Your physics point is the strongest substrate-neutral anchor available', which places the point with the human. The human source has no row in the table; the section's prose names an 'unseen interlocutor'
- how found: chat-side read of the pinned texts, then a first-hand check by the forest-ledger session (FML_035); the quoted lines were re-read in this session on 2026-11-11 (audit table line 43; chat paste lines 425 and 436)
- resolution: recorded; uncorrected in source
- note: Refs point at claude/forest-toolkit-build, which contains the PR 256 tip d402fa8; both text files are byte-identical there and match their MANIFEST sha256. 4cf10ec is an earlier reported tip, unresolved in this checkout. No tag: tag pushes are refused from sessions, so by Kavik's decision (2026-11-11) the branch archive/pr256-tip holds the old PR 256 tip d402fa8; pushed and read back at that sha.
- evidence: https://github.com/JinnZ2/Simulators/pull/256; `Simulators:forest-model-ledger/ledger/toolkit/cases/texts/kimi_substrate_neutral_intelligence_audit.md@origin/claude/forest-toolkit-build`; `Simulators:forest-model-ledger/ledger/toolkit/cases/texts/chat_paste_2026-11-10.txt@origin/claude/forest-toolkit-build`; `Simulators:forest-model-ledger/CLAIM_TABLE.md@origin/claude/forest-toolkit-build`; `Simulators:forest-model-ledger/ledger/toolkit/cases/texts/MANIFEST.yaml@origin/archive/pr256-tip`
- side Kimi: model VOID; session VOID; date VOID (VOID: this side is a document author, not a commit; there is no trailer to read)
- side Kavik: model VOID; session VOID; date VOID (VOID: this side is a document author, not a commit; there is no trailer to read)
- side DeepSeek: model VOID; session VOID; date VOID (VOID: this side is a document author, not a commit; there is no trailer to read)

## MARKING START

First commit carrying a Co-Authored-By trailer, per repo. Before it: model VOID (not inferred from date or style).

- Simulators: `11033ad` 2026-07-04T11:01:15+00:00, Claude Opus 4.7 (1M context); 154 commits on main before it
- thermodynamic-accountability-framework: `3410a18` 2026-09-23T03:55:11+00:00, Claude Opus 5; 442 commits on main before it
- study-aperture: `62858b4` 2026-10-28T06:29:46-05:00, Claude Opus 5.5; 13 commits on main before it; first Perplexity trailer 0384df3, 2026-11-10
- note: Read from git (first commit on any ref whose Co-Authored-By trailer is present). This is earlier than the ~2026-11 stated in CONDITIONS for all three repos; both are kept. Commits on main after the start that still carry no trailer (merge commits included): Simulators 445, TAF 15, study-aperture 27.

## CONDITIONS (as of 2026-11-11)

These affect how to read the record.

- Model marking began ~2026-11 (per-repo start commit listed under MARKING START); earlier collisions can't be split by model.
- GitHub mobile UI change (recent, ~2026-11): owner can no longer delete branches from phone; branch clutter accumulated partly from this; deletions now routed via Manus + auto-delete on.
- Owner works phone-only (no keyboard, no local compute).
- Sessions vary in model (Opus/Sonnet/Haiku/Fable) and model updates.

## SUMMARY

- rows counted (every side carries a trailer): 4 of 5; not counted: provenance credit
- models differ: 2 (playground, expiry register)
- same model, different session: 2 (GAP_INSTRUMENT, pipeline aggregation)
- same model, same session: 0 (none)
- by side pair over counted rows: models differ 2, same model different session 3, same model same session 1
- no interpretation until n is larger.
