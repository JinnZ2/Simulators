# FREEZE CLEANUP MEASURAND

Status: PROPOSED (drafted 2026-11-19, records only, under the freeze). Not adopted until the owner
marks it. The freeze itself is the CONDITIONS item in `collisions.json` (source: the owner's chat
statement of 2026-11-11 in chat Claude, "Freeze new features until map + cleanup done").

The freeze lifts on two conditions. Each gets a measurand line here: what "done" is measured as,
and a done-test per item that a reader can run. A test that cannot be run from a repo is marked
NOT_CHECKABLE_HERE with what would check it. Nothing below picks a reading for the owner.

## 1. "map" (measurand line)

- measurand: multi-home concepts mapped / multi-home concepts that exist, across Simulators,
  study-aperture and thermodynamic-accountability-framework (scope from the root CLAUDE.md line
  for CONCEPT_MAP.md).
- denominator: `MULTI_HOME_REGISTER.json` (DRAFT, built by `build_multi_home_register.py`). It is a
  lower bound from four named sources, not an enumeration.
- reading at draft: 28 rows; in_map YES 11, PARTIAL 3, NO 14 (in_map is an L0 reading).
- done-test: every register row reads in_map YES, the register has had a REVIEW-2 at L2+, and
  `check_concept_map.py --strict` exits 0 with every sibling present (`sibling_state` line shows
  no ABSENT).

## 2. "cleanup" (items as filed on 2026-11-11)

Source located: thermodynamic-accountability-framework `docs/cleanup/TAF_CLEANUP_PHASE1_INVENTORY.md`
(written 2026-11-11, last changed at 3887eb4, 2026-11-18). Its own header says the phase 1 table
"lived in a cleanup-session scratchpad and was never committed". The file carries items
1, 16, 17, 18, 19, 22, 32, 33. The numbering gaps (2-15, 20-21, 23-31) are items filed on
2026-11-11 that are not in any file read here.

NOT LOCATED: the study-aperture branch deletions (items 24-30, as the owner names them). Searched:
study-aperture origin/main and all 39 remote branches (no cleanup or phase 1 record, no archive/*
branch, no commit 2026-11-10..13 naming a delete); Simulators tree; TAF docs/cleanup. The list
needs the chat-side record; until then each of 2-15, 20-21, 23-31 reads NOT LOCATED, never done.

| # | item (as filed) | done-test | reading 2026-11-19 |
|---|---|---|---|
| 1 | TAF #76 merge | PR merged (API) | NOT_CHECKABLE_HERE (api.github.com 403); file says merged |
| 16 | TAF #80+#82+#84+#85 collapse onto #85, folded at 65bb724 | 65bb724 reachable from TAF origin/main | FAILS as written: 65bb724 is not a valid object in a full TAF clone; `origin/claude/unknown-axis-followup-2` (#85 head) still exists |
| 17 | close #73 | `archive/undeclared-intent-switch` exists | holds (branch present) |
| 18 | #78 into #79 | #78 content reachable from main | NOT_CHECKABLE_HERE (needs the #78 head sha) |
| 19 | #77+#81+#83 one PR | `archive/expiry-condition-stage1` and `archive/silent-fill-register` exist | holds (both present) |
| 22 | #79 merge first | 953f1a8 reachable from TAF origin/main | holds |
| 32 | close + archive #52 | `archive/manus-wo6-read-me-this-way` exists | holds (branch present) |
| 33 | drop-electrification-corrosion open PR | PR exists (API) | NOT_CHECKABLE_HERE |
| rename | docs/EXPIRY_REGISTER.md -> EXPIRY_REGISTER_78.md | both files present, old name absent | holds |
| TAF deletes | 18 named branches + stray `archive/expiry-condition-stage1-test` | none present in `git branch -r` after `git fetch --prune` | holds (0 of 18 present; stray absent); the file says "all 19" |
| 2-15, 20-21, 23-31 | not in any file read | NOT LOCATED | NOT LOCATED |
| 24-30 | study-aperture branch deletions | named branches absent from study-aperture remote | NOT LOCATED: no list of names |
| Simulators | COLLISIONS evidence pins | `check_concept_map.py --strict` exit 0 with siblings | holds at the repin of 2026-11-19 |

Count note: the TAF file lists 18 branch names plus one stray archive branch and says "all 19";
18 + 1 = 19 is the reading taken here. That is a reading, not a statement in the file.

done-test for "cleanup" as a whole (PROPOSED): every filed item has a row, every row's done-test
holds, and no row reads NOT LOCATED. At draft: not met (items NOT LOCATED, item 16 fails as
written, three rows NOT_CHECKABLE_HERE).

Checked with full clones of TAF (origin/main 16285cccdd48) and study-aperture (origin/main
03bd2014cd20) on 2026-11-19. Observer slots: null.

## 3. Items 24-30 located (dated 2026-11-19, second pass)

This section supersedes the NOT LOCATED reading for items 24-30 above; the earlier text stays as
written. Source: the owner's chat of 2026-11-11 (chat Claude), work order "Branch deletions
(Kavik -> Manus)", as relayed in the owner's IMPLEMENT request of 2026-11-19. The work order text
itself is not in this repository. The Manus report docs are pending re-attachment.

As relayed:
- 24: TAF, 5 branches. 25: TAF, 13 branches. 26: Simulators, 9. 27: method-layer, 8.
- 28: `manus/wo11-current-main` in 8 repos, plus 2.
- 29: `tool-finder-pointer` in 6 repos.
- 30: `healing-folder-additions-u5aojl` in 3 repos, `clone-refspec-note` in 2, plus 4 named.
- the stray TAF `archive/expiry-condition-stage1-test`.
- safety rules a, b, c, and round 2's a2 (PR merged AND refs/pull/N/head == tip).
- reported outcome, round 1: 41 deleted, 20 skipped, auto-delete on in 15 repos (Manus report,
  not read here).

Reading of 24 + 25: 5 + 13 = 18, the count of TAF names in
`docs/cleanup/TAF_CLEANUP_PHASE1_INVENTORY.md` "Branches still to delete". The split between
24 and 25 is not in that file. Taking those 18 as items 24 + 25 is a reading, not a statement in
either source.

### done-test run: does each named branch still exist?

Method: `git ls-remote --heads https://github.com/JinnZ2/<repo>.git` over 82 repos (the 78
reachable repos named in `tools/tool_inventory.json` meta.repo_heads plus Simulators, method-layer,
study-aperture, TAF), run 2026-11-19T22:57:21Z. Every call exited 0. A branch is matched by exact name,
with or without a `claude/` prefix.

| item | branch | target repos named? | reading |
|---|---|---|---|
| 24 + 25 | the 18 TAF names | yes (TAF) | GONE, 18 of 18 (TAF has 25 heads; none matches) |
| stray | `archive/expiry-condition-stage1-test` | yes (TAF) | GONE (absent in all 82) |
| 26 | 9 Simulators branches | names not relayed | not run (no names); Simulators has 30 heads now |
| 27 | 8 method-layer branches | names not relayed | not run (no names); method-layer has 3 heads now (`main`, `claude/design-basis-headers`, `claude/reversible-loop-triage-rubric-2vu4tt`) |
| 28 | `manus/wo11-current-main` | repo list not relayed (8 + 2) | EXISTS in 22 repos: AI-Human-Audit-Protocol AI-arena Academic-Translator Adaptive-Intelligence-Framework- Antarctic-basin-dynamics BE2-communication Bio-Grid-American-Manufacturing- BioGrid2.0 Combine-Cognitive-Architecture- Coop-framework Cyclic-programming DIY-CNC Fractal_Compass_Core Fulgerite-Antenna-Prototype- GlyphAI HAAS Hardware-Store Inversion assumption_validator biomachine_ecology fairmont-ecological-recovery infrastructure-stability-model |
| 29 | `tool-finder-pointer` | repo list not relayed (6) | GONE in all 82 (nearest name: `claude/tool-finder-aliases` in JinnZ2 and Shadow-Hunting, a different branch) |
| 30 | `claude/healing-folder-additions-u5aojl` | repo list not relayed (3) | EXISTS in 4 repos: AI-Consciousness-Sensors, Rosetta-Shape-Core, Simulators, thermodynamic-accountability-framework |
| 30 | `claude/clone-refspec-note` | repo list not relayed (2) | EXISTS in 67 repos: AI-Consciousness-Sensors AI-Human-Audit-Protocol AI-arena Academic-Translator Adaptive-Intelligence-Framework- Antarctic-basin-dynamics BE2-communication BioGrid2.0 Combine-Cognitive-Architecture- Component-failure-repurposing-database Coop-framework Cyclic-programming DIY-CNC Fractal-Compass-Atlas Fractal_Compass_Core Fulgerite-Antenna-Prototype- Geometric-to-Binary-Computational-Bridge GlyphAI HAAS Hardware-Store Inversion JinnZ2 Keystone-Codex Living-Intelligence-Database Logic-Ferret Logistics-Disparity-Sensor Mandala-Computing Mathematic-economics Municipal-Code-Translator Nexus-emergency-management Non-equilibrium-atmospheric-forcing Nuclear-Donut-DataCenter PatternBridge Permeable-intelligence-commons PhysicsGuard Plain-English-Translator Prosthetic-arm-CNC Regenerative-intelligence-core Resilience-hydrology-core Resilience Resilient-AI-Human-Collaboration- Rosetta-Shape-Core Seed-physics Study-on-Nazca-Lines Symbolic-Defense-Protocol Symbolic-sensor-suite SymbolicSentinel The-Curriculum-of-Everything-Earth- Universal-Redesign-Algorithm- Voice-Integrity-Module assumption_validator biomachine_ecology chain-position-detectability differential-frame-core electromagnetic-ocean-restoration fairmont-ecological-recovery hgai-geometric-systems infrastructure-assistance infrastructure-stability-model metabolic-accounting open-source-plastic-lab orbital-phycom planetary-conservation-framework resilience-indigenous-worldwide temporal-consciousness-playground thermodynamic-accountability-framework urban-resilience-sim |
| 30 | 4 named branches | names not relayed | not run (no names) |

Reading. For 28 and 30, the count of repos now carrying the branch (22, 4, 67) is larger than
the count named for deletion (10, 3, 2). So either the deletions were not done in some repos,
or the branch was pushed again afterward, or the named set is a different set from the one
found here. The relayed text does not say which repos were named, so no branch in 28 or 30 can
be read GONE or EXISTS per target repo. The per-repo done-test needs the work order's repo
lists or the Manus report docs.

done-test for "cleanup" (section 2): still not met. Items 24 + 25 and the stray now hold under
the 18-name reading. 26, 27 and the 4 named in 30 are not run. 28 and 30 are not decidable per
target repo.

Observer slots: null.
