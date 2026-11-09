# REPORT_WO_FINDER

This report is for WORK ORDER TOOL FINDER + GAP BUILDS, 2026-11-09. CC0. Co-authored (JinnZ2 + Claude).

The work followed `READ_ME_THIS_WAY.md`: additions only, nothing renamed, model-chosen names kept, every added section dated.

## Repos touched

None of the four PRs below is merged. Each is waiting for the owner's go-ahead, and no CI check was bypassed.

| repo | branch | head | PR | merge SHA |
|---|---|---|---|---|
| JinnZ2/Simulators | claude/tool-finder | (this commit) | #252 | PENDING (not merged) |
| JinnZ2/method-layer | claude/tool-finder-aliases | f7b607d | #30 | PENDING (not merged) |
| JinnZ2/JinnZ2 | claude/tool-finder-aliases | 1345818 | #43 | PENDING (not merged) |
| JinnZ2/Shadow-Hunting | claude/tool-finder-aliases | f9176b6 | #9 | PENDING (not merged) |

All four repositories carry a CC0 LICENSE.

## Paths

Simulators:
- new: `TOOL_FINDER/` (TOOL_FINDER.md, finder.json, entries.py, build_finder.py, write_finds_by.py, status.json, this report)
- new: `tail-check/`, `cutoff-attribution/`, `tools/README.md`
- READMEs created because none existed: `criterion-symmetry/README.md`, `observer-exclusion/README.md`
- 26 existing READMEs had a Finds-by section appended

method-layer:
- `README.md` (+3 sections)
- `premise-traceability/README.md` (+1)

JinnZ2:
- `corpus_prior_audit/README.md` (+1)

Shadow-Hunting:
- `shadow_hunting/knowledge/README.md` (+3)

## Aliases added

38 Finds-by sections were written, one per indexed tool, each carrying 3 to 8 phrases. `git diff` shows 0 deleted lines in every repo.

Every `measures` and `breaks when` field is a quote that `build_finder.py` checks as a literal substring of the cited file, with whitespace normalised.

The avoided-term field reads AVOIDED_TERM_UNSTATED for all 38 tools. None of the READMEs read for the index names a common term it avoids, so no avoided term was invented.

## GAPS

These are needs with no tool found in the four repos read for this index:

1. **distribution:** placing a person on an axis from their own words. tail-check refuses to do this; the position must be declared by the caller.
2. **channel:** voice and live losses other than cuts, such as prosody, tone and affect dropped by transcription.
3. **floor:** null calibration of cutoff-attribution's own DETECTED-cut rate. It has fixtures but no null-harness run.
4. **fill-source:** tagging user-said versus templated content in arbitrary model output. ai_provenance tags only what its own pipeline emits.
5. **observer:** a command-line search over this index. finder.json is machine-readable, but no search CLI ships with it.

## Build selftests (verbatim)

`python3 tail-check/selftest.py`
```
tail_check.py refuses --selftest; run: python3 tail-check/selftest.py
checks: 18   failed: 0
```

`python3 cutoff-attribution/selftest.py`
```
cutoff_attribution.py refuses --selftest; run: python3 cutoff-attribution/selftest.py
checks: 15   failed: 0
```

`python3 TOOL_FINDER/build_finder.py --selftest`
```
checks: 12   failed: 0
```

## 3c: evidence-demotion-detector on gpt_pretrip_2026-11-09.txt

Status: **NOT_RUN.**

- No file matching `gpt_pretrip*` exists anywhere on this machine. `find /` returned 0 hits.
- Nothing was fabricated in its place.
- When the file arrives, note that `detect.py` reads a JSON list of `{"role", "text"}` records. A `.txt` transcript will have to be converted to that format first, and the conversion is a reading step that should be stated.
- For the record, the detector's own selftest passed: `selftest: 38/38 checks PASS`

## Status column in the index

Each indexed tool's own check was run in a throwaway git worktree at each repo's committed HEAD. Totals: 32 RUN, 5 NOT_RUN, 1 UNKNOWN.

- **NOT_RUN** (no check command stated): three Shadow-Hunting modules, declared-frame, and null-harness (its README states no selftest).
- **UNKNOWN**: evaluation-frame, where 5 of 66 checks fail. Its corpus path lies outside the repo, as already recorded at EA_023 in `external-audit/`.

Running the checks in place first had modified the tree being indexed:
- falsifier-audit regenerated its tracked `QUEUE.md` and its samples, because it scans the whole tree and the tree now included the new folders.
- the reasoning-gate tests wrote `gate_T.denied.json` to the repo root.

Both changes were reverted, and the runner now uses worktrees. This is the `self-scan` SS_009 shape.

The Simulators root suite was also run in a worktree at the branch head: `pytest tests` gave 194 passed and 3 failed. All 3 failures are pinned: `tools/known_red_check.py --suite` reports pins 25, MATCH 25, VERDICT PASS.

## Skipped, and why

- **Part 1 across all CC0 JinnZ2 repos.** This was not done. `tools/tool_inventory.json` lists 3469 modules in 81 repos, and writing scope-derived aliases means reading each tool's own text. That reading was done for the 38 tools in the index, across 4 repos. The rest are out of this pass and are not marked as done.
- **WO-6 ledger.** Not located. Searches of the local clones and of GitHub code across the JinnZ2 repos for a WO-6 out-of-scope repo ledger found only the WO-6 work orders in assessor-coupling, criterion-externality and chain-position-detectability, none of which is a repo ledger. Out-of-scope was therefore read as "not reachable or not CC0". All four repos touched are CC0.
- **ICSC functional selection.** The term `ICSC` returned no hit in any repo reachable this session. The NAME_COLLISION entry carries it from the work order, with its location marked not found.
- **Shadow-Hunting.** It was not in the session's starting scope. It was attached during this task because the work order names it as the motivating case.
- **Aliases** are ALIAS_PROPOSED. They were not tested against real AI search queries.
