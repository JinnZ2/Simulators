# COLLISIONS

Generated from `collisions.json` by `check_concept_map.py --write`. Edit the JSON, not this file.
One block per multi-agent collision. Rows are kept, not resolved away; a resolved row stays.
As of 2026-11-11.

## 2026-11-11  GAP_INSTRUMENT

- agents: two Claude Code sessions
- what collided: one status name, two meanings (an instrument crash; a label the instrument does not recognise)
- how found: as stated by Kavik + Claude chat-side; not re-derived here
- resolution: split into GAP_INSTRUMENT_CRASH / GAP_INSTRUMENT_UNRECOGNIZED_LABEL; both names are on unmerged branches only
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/82; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/85; TAF branches claude/unknown-axis-followup-2 (b85433c), claude/not-determinable-reason (92cd578)

## 2026-11-10/11  playground

- agents: Perplexity (study-aperture) / Claude Code (Simulators)
- what collided: two builds of one equation-substitution laboratory from related specs, different organisation
- how found: concept map survey, 2026-11-11
- resolution: OPEN: cross-run pending
- evidence: https://github.com/JinnZ2/Simulators/pull/257; study-aperture@origin/main:experimental/playground/; CONCEPT_MAP.md row 'playground'

## 2026-11-11  pipeline aggregation

- agents: three sessions, as stated; builders not checked here
- what collided: three versions of one function across TAF PRs 81, 82, 84
- how found: as stated by Kavik + Claude chat-side
- resolution: OPEN: pick pending
- note: PR titles: 82 and 84 both name 'pipeline NOT_MEASURED'; 81 (closed, unmerged) does not name the pipeline in its title. The diffs were not compared in this session.
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/81; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/82; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/84

## 2026-11-11  expiry register

- agents: two sessions, as stated
- what collided: two registers of the same slots under different counting rules: PR 77 value rule, PR 78 token rule
- how found: PR 79 reconciles them
- resolution: both kept, split coded (PR 79 merged; 78 merged; 77 closed unmerged)
- evidence: https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/77; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/78; https://github.com/JinnZ2/thermodynamic-accountability-framework/pull/79

## 2026-11-10/11  provenance credit

- agents: Kimi / Kavik / DeepSeek
- what collided: Kimi's provenance table credits a physics point made by Kavik to DeepSeek
- how found: as stated by Kavik + Claude chat-side
- resolution: recorded; uncorrected in source
- note: The table was not located in any repo checked on 2026-11-11 (Simulators, study-aperture, method-layer, TAF). Which point and which table are not on record here.
- evidence: NOT LOCATED
