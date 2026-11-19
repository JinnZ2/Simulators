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
