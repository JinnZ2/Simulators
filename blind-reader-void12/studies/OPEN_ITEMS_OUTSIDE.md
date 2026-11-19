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
