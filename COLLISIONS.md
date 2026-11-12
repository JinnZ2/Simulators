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
  - commits: a2c5d99 rename, f12fc01 origin
  - a2c5d99 role rename: subject: Rename GAP_INSTRUMENT -> GAP_INSTRUMENT_CRASH
  - f12fc01 role origin: adds GAP_INSTRUMENT (crash sense): 22 added lines name it, 0 removed; subject 'crash is GAP_INSTRUMENT'
- side TAF PR 84 (thermodynamic-accountability-framework, 2 commits, 2026-11-11T14:04:17+00:00 .. 2026-11-11T14:15:24+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWFx2jFzaiK4egn9iaJ
  - commits: 92cd578 rename, f603b43 origin
  - 92cd578 role rename: subject: Split GAP_INSTRUMENT: UNRECOGNIZED_LABEL vs CRASH
  - f603b43 role origin: adds GAP_INSTRUMENT (unrecognised-label sense): 11 added lines name it, 0 removed

## 2026-11-10/11  playground

- agents: Perplexity (study-aperture) / Claude Code (Simulators)
- what collided: two builds of one equation-substitution laboratory from related specs, different organisation
- how found: concept map survey, 2026-11-11
- resolution: OPEN: cross-run pending
- evidence: https://github.com/JinnZ2/Simulators/pull/257; `study-aperture:experimental/playground@origin/main`; `Simulators:CONCEPT_MAP.md`
- side study-aperture experimental/playground (study-aperture, 18 commits, 2026-11-11T03:33:20+00:00 .. 2026-11-11T12:06:41+00:00): model Perplexity (trailer names no model version); session VOID
  - commits: 1fc37a8 VOID, 12beac8 VOID, c0873df VOID, e4a9bc9 VOID, bbd7c76 VOID, 8f8ae94 VOID, a441494 VOID, e433071 VOID, 28efc3e VOID, e5541f9 VOID, c780f5c VOID, 05b2f1a VOID, 474db2a VOID, 18b8722 VOID, c86d6b9 VOID, ea34f5c VOID, 9587178 VOID, 79f402c VOID
  - role VOID: not coded: only GAP_INSTRUMENT was filled from git (2026-11-12 instruction)
  - session VOID: no Claude-Session line; channel: non-merge commit, committer is the owner's GitHub account (users.noreply), not web-flow; trailer names Perplexity only
- side Simulators PR 257 relational-playground/ (Simulators, 16 commits, 2026-11-11T08:43:46+00:00 .. 2026-11-11T20:14:00+00:00): model Claude Fable 5.2; session https://claude.ai/code/session_01BSBFWG4whgMfkPUeexTM9s
  - commits: 02bc605 VOID, a1c04ae VOID, 512f320 VOID, c395a41 VOID, beac98b VOID, f9a1aac VOID, 2cdfd53 VOID, 02dd4c7 VOID, d31383b VOID, 70e546f VOID, 9b8c5e2 VOID, 92a8ca9 VOID, decb1a7 VOID, 7b06c26 VOID, 861b7c5 VOID, 62e8fb7 VOID
  - role VOID: not coded: only GAP_INSTRUMENT was filled from git (2026-11-12 instruction)

## 2026-11-11  pipeline aggregation

- agents: three Claude Code sessions (three TAF PR branches)
- what collided: calibration/pipeline.py score aggregation changed three ways: PR 81 sets a no-score result to (None, Band.UNKNOWN) inline; PR 82 adds _aggregate returning 2 values, (None, NOT_MEASURED) with no module report; PR 84 adds _aggregate returning 3 values, the third a not_measured_reason
- how found: chat-side, TAF cleanup phase 1 inventory, trial merge of stack tips (TAF_CLEANUP_PHASE1_INVENTORY.md, not in the TAF checkout read here); the three diffs of calibration/pipeline.py were then read in this session on 2026-11-11 and match
- resolution: picked 2026-11-11 (Kavik): three-value (score, band, reason) from PR 84 plus the no-score -> UNKNOWN rule from PR 81, folded on the PR 85 branch (65bb724); 80/82/84 closed, branches kept under archive/
- note: Diffs read at PR tips ed275ef (81), a2c5d99 (82), 92cd578 (84). PR 81's title does not name the pipeline; the change is in its diff.
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/81; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/82; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/84; `thermodynamic-accountability-framework:calibration/pipeline.py@origin/archive/silent-fill-register`; `thermodynamic-accountability-framework:calibration/pipeline.py@origin/archive/unknown-axis-followup`; `thermodynamic-accountability-framework:calibration/pipeline.py@origin/archive/not-determinable-reason`; TAF_CLEANUP_PHASE1_INVENTORY.md: NOT COMMITTED as of 2026-11-11 (written to a cleanup-session scratchpad); to be linked at TAF docs/cleanup/ when it lands
- side TAF PR 81 (thermodynamic-accountability-framework, 1 commit, 2026-11-11T08:54:31+00:00 .. 2026-11-11T08:54:31+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWFx2jFzaiK4egn9iaJ
  - commits: ed275ef VOID
  - role VOID: not coded: only GAP_INSTRUMENT was filled from git (2026-11-12 instruction)
- side TAF PR 82 (thermodynamic-accountability-framework, 1 commit, 2026-11-11T09:03:08+00:00 .. 2026-11-11T09:03:08+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWLfMGR7yRZZCUHBs9g
  - commits: f12fc01 VOID
  - role VOID: not coded: only GAP_INSTRUMENT was filled from git (2026-11-12 instruction)
- side TAF PR 84 (thermodynamic-accountability-framework, 1 commit, 2026-11-11T14:04:17+00:00 .. 2026-11-11T14:04:17+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWFx2jFzaiK4egn9iaJ
  - commits: f603b43 VOID
  - role VOID: not coded: only GAP_INSTRUMENT was filled from git (2026-11-12 instruction)

## 2026-11-11  expiry register

- agents: two sessions, as stated
- what collided: two registers of the same slots under different counting rules: PR 77 value rule, PR 78 token rule
- how found: PR 79 reconciles them
- resolution: both kept, split coded (PR 79 merged; 78 merged; 77 closed unmerged)
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/77; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/78; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/79
- side TAF PR 77 (thermodynamic-accountability-framework, 1 commit, 2026-11-11T01:17:29+00:00 .. 2026-11-11T01:17:29+00:00): model Claude Fable 5.2; session https://claude.ai/code/session_01BSBFWG4whgMfkPUeexTM9s
  - commits: 614b795 VOID
  - role VOID: not coded: only GAP_INSTRUMENT was filled from git (2026-11-12 instruction)
- side TAF PR 78 (thermodynamic-accountability-framework, 3 commits, 2026-11-11T00:41:06+00:00 .. 2026-11-11T00:42:59+00:00): model Claude Opus 5.5; session https://claude.ai/code/session_01BSBFWLfMGR7yRZZCUHBs9g
  - commits: e177780 VOID, bbe4da9 VOID, c777c6e VOID
  - role VOID: not coded: only GAP_INSTRUMENT was filled from git (2026-11-12 instruction)

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

Per repo, four forms, none picked. Before a form's first commit: that field VOID (not inferred from date or style).

- Simulators, a. first model trailer: `11033ad` 2026-07-04T11:01:15+00:00; agent Claude; model Opus 4.7 (1M context)
- Simulators, b. first Claude-Session keyed trailer: `11033ad` 2026-07-04T11:01:15+00:00
- Simulators, c. first bare session URL: VOID (no commit on main carries a claude.ai/code/session URL outside a 'Claude-Session:' key (main tip 34eb3cf))
- Simulators, d. first non-Claude model trailer: VOID (no Co-Authored-By trailer on main names a non-Claude model agent (main tip 34eb3cf); the only non-Claude Co-Authored-By value is JinnZ2 (4 commits, users.noreply address), a person, not a model)
  - 154 commits on main before line a
- thermodynamic-accountability-framework, a. first model trailer: `3410a18` 2026-09-23T03:55:11+00:00; agent Claude; model Opus 5
- thermodynamic-accountability-framework, b. first Claude-Session keyed trailer: `3410a18` 2026-09-23T03:55:11+00:00
- thermodynamic-accountability-framework, c. first bare session URL: `56a2ebe` 2026-03-24T13:26:16+00:00; author Claude
- thermodynamic-accountability-framework, d. first non-Claude model trailer: VOID (no Co-Authored-By trailer on main names a non-Claude model agent (main tip 953f1a8))
  - 442 commits on main before line a
  - note: 97 commits on main carry a claude.ai/code URL in any form; 44 in the bare form; 11 carry 'Co-Authored-By: Claude' with no model
- study-aperture, a. first model trailer: `62858b4` 2026-10-28T06:29:46-05:00; agent Claude; model Opus 5.5
- study-aperture, b. first Claude-Session keyed trailer: `62858b4` 2026-10-28T06:29:46-05:00
- study-aperture, c. first bare session URL: VOID (no commit on main carries a claude.ai/code/session URL outside a 'Claude-Session:' key (main tip c26fbd2))
- study-aperture, d. first non-Claude model trailer: `79f402c` 2026-11-11T03:33:20+00:00; agent Perplexity
  - 13 commits on main before line a
  - note: 0384df3 (Perplexity) is dated 2026-11-10T22:10:30-06:00 = 2026-11-11T04:10:30Z, after 79f402c; first Manus trailer dd220df 2026-11-11T19:30:23Z

Untrailered commits (no Co-Authored-By trailer) after line a:

| repo | main tip | merge | non-merge web-UI | non-merge other | total |
|---|---|---|---|---|---|
| Simulators | `34eb3cf` | 267 | 142 | 37 | 446 |
| thermodynamic-accountability-framework | `953f1a8` | 14 | 1 | 0 | 15 |
| study-aperture | `c26fbd2` | 27 | 0 | 0 | 27 |

- note: Read from git on origin/main; 'first' = earliest committer date (UTC), not topological order. a = first Co-Authored-By naming a Claude model; b = first 'Claude-Session:' keyed trailer; c = first bare claude.ai/code/session URL line; d = first Co-Authored-By naming a non-Claude model agent. None is picked. Untrailered = no Co-Authored-By trailer, counted from line a to the main tip named. merge = more than one parent; web-UI = non-merge with committer GitHub <noreply@github.com> (web-flow); other = the rest. Simulators 'other' splits by committer name: Claude 32, JinnZ2 5.

## CONDITIONS (as of 2026-11-11)

These affect how to read the record.

- Model marking began PLACEHOLDER (chat-side estimate from 'recently'; unsourced) (per-repo first-form commits listed under MARKING START); earlier collisions can't be split by model.
- GitHub mobile UI change (PLACEHOLDER (owner report, date not established)): owner can no longer delete branches from phone; branch clutter accumulated partly from this; deletions now routed via Manus + auto-delete on.
- Owner works phone-only (no keyboard, no local compute).
- Sessions vary in model (Opus/Sonnet/Haiku/Fable) and model updates.
- Committer/author field = the pusher, not the model (basis: the 18 Perplexity commits in the playground row are committed under the user's GitHub noreply account).

## SUMMARY

- rows counted (every side carries a trailer): 4 of 5; not counted: provenance credit
- models differ: 2 (playground, expiry register)
- same model, different session: 2 (GAP_INSTRUMENT, pipeline aggregation)
- same model, same session: 0 (none)
- by side pair over counted rows: models differ 2, same model different session 3, same model same session 1
- no interpretation until n is larger.
