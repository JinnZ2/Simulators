# Open items outside this folder (2026-11-19): listed only, nothing implemented

From the owner's IMPLEMENT (records only) request of 2026-11-19, item 5. Each item needs an AUDIT of the fix choice before any IMPLEMENT. The feature freeze is in force (`../../COLLISIONS.md`, CONDITIONS).

```text
item                              where                                       what is open                                          next stage
grounding-layers psutil           grounding-layers/ai_observer_state.py:11    psutil imported unguarded, not in requirements.txt;   AUDIT of the fix
                                  (import); observer_state.py:174-177          the re-export swallows the ImportError, so            choice: declare in
                                  (silent re-export); callers:                 AIObserverState reads as missing                      requirements vs
                                  tests/test_bias_human_centrism.py:17,                                                              guard the import
                                  run_grounding_pipeline.py:257
COLLISIONS evidence pins          collisions.json, row "provenance credit"    evidence pinned to refs that no longer resolve:       AUDIT: re-pin to a
                                                                              origin/claude/forest-toolkit-build, origin/archive/   commit, or record
                                                                              pr256-tip; check_concept_map.py on 2026-11-19 (after  GONE as the state
                                                                              a full fetch): paths OK 2, NOT_CHECKED 6, failed 3
                                                                              (4 failed before the fetch)
TOOL_FINDER quotes                TOOL_FINDER/finder.json, entry              build_finder.py refuses: quote MISSING_FILE in        AUDIT: needs the
                                  JinnZ2:corpus_prior_audit/                  corpus_prior_audit/README.md, twice (the JinnZ2       JinnZ2 repository
                                                                              repository, not checked out here)                     checked out
```

## Later (2026-11-19): state of the three items after the AUDIT round

Records only. Each line says what was measured and where; no fix is chosen here.

- COLLISIONS evidence pins: repinned (owner's IMPLEMENT of 2026-11-19). The three `origin/claude/forest-toolkit-build` pins now point at `origin/archive/pr256-tip` @ d402fa8 (exact tip; the two sha256 values still match), and the `unknown-axis-followup-2` pin at TAF `origin/archive/unknown-axis-followup` @ a2c5d99. The old pins are kept inside each entry as `repinned_2026-11-19.old_pin`. `check_concept_map.py --strict` with all siblings present: collisions OK 11, NOT_CHECKED 0, failed 0, exit 0.
- TOOL_FINDER quotes: the two MISSING_FILE quotes are not about the JinnZ2 repository. In this container `../jinnz2` is a plain directory holding a Simulators copy (no `.git`), and `build_finder.py` takes any existing directory as the checkout. With the JinnZ2 repository at FINDER_JINNZ2_PATH all quotes are FOUND. The new `sibling_state` line shows the case as `JinnZ2@UNREADABLE`. Open item: `repo_dir` checks that a directory exists, not that it holds the named repository (AUDIT of the fix choice first).
- build_finder.py fails open: without siblings it exits 0 with QUOTE_NOT_CHECKED rows and "?" line numbers, and rewrites the tracked TOOL_FINDER.md and finder.json with that output. Open item; no fix (AUDIT first).
- grounding-layers psutil: unchanged.
- ai-arena (outside this repository): at 732458a its suite passes with formula-audit at `main` (c1acb59, which is also the CI pin) and fails 1 test with formula-audit at its default branch HEAD (7df0d81, default branch `claude/quasicrystal-projection-properties-448bx7`, which does not contain main). Failing test: `tests.test_word_slots.TestPins.test_hash_mismatch_is_not_run`. At 7df0d81 `wordslots/places.json` is absent, so `report()` returns NOT_RUN with the reason "not found", which matches neither string the test accepts ("sha256", "no checkout"). The 18 pinned tests read NOT_RUN there. Local runs, Python 3.13 only; ai-arena CI logs NOT READ (api.github.com returns 403 here).

## Fail-open list (dated 2026-11-19, second pass)

Collected from the two bullets above; no fix (AUDIT of the fix choice first).

1. build_finder.py, no siblings present: exits 0 with QUOTE_NOT_CHECKED rows and "?" line
   numbers, and rewrites the tracked TOOL_FINDER.md and finder.json with that output.
2. build_finder.py `repo_dir`: accepts any existing directory as a sibling checkout. It checks
   that the directory exists, not that it holds the named repository. Instance: in this container
   `../jinnz2` is a plain directory holding a Simulators copy (no `.git`). build_finder read it as
   the JinnZ2 checkout and reported two quotes MISSING_FILE. The `sibling_state` line shows the
   case as `JinnZ2@UNREADABLE`. With the JinnZ2 repository at FINDER_JINNZ2_PATH all quotes are
   FOUND. build_finder's own selftest fails 1 of 17 in this layout for the same cause.

## Later (2026-11-19): study-aperture, author note for the 2026-11-17 outside audit

- Open: study-aperture's notes name the 2026-11-17 outside audit, and its author is not recorded there. The record to add: author Kimi-or-GPT, UNRESOLVED (owner-stated, neither confirmed); the audit's text is not filed.
- Reason it is open: the filing session has no push access to study-aperture, and the GitHub API is denied for that repository there.
- Where the same note is filed: formula-audit `READING_NOTES.md`, "Note 2026-11-19: the outside audit's author" (merged by formula-audit PR #13, `a1513b9`).
- Next stage: IMPLEMENT (records) by a session with study-aperture push access.
- Follow-up 2026-11-20 (the lines above are kept as written): filed. The author note is in study-aperture `READING_NOTES.md`, merged by study-aperture PR #37 at `8164f9d` (commit `6c45954`). The session gained push access to study-aperture on 2026-11-19. Still open from the note itself: the author (Kimi or GPT, UNRESOLVED) and the audit text, which is in no repository.

## Later (2026-11-20): study-aperture CI and the Python floor

- Open: study-aperture's CI (`.github/workflows/checks.yml`) runs Python 3.11 to 3.14. The ecosystem floor recorded in housekeeping is 3.10 (owner-stated, 2026-11-20). Python 3.10 is not run there.
- No change made. Recorded only.
- Next stage: owner's decision (add 3.10 to the matrix, or record study-aperture's floor as 3.11).
