# Check of the Grok reader's repository read (F1-F7), and the map state

Checked 2026-11-19 at Simulators main `1c89ab9` by the Claude Code session. The read itself is filed as received in `as_received/grok_repo_read_2026-11-19.md`. Verdicts: CONFIRMED (the files say it), PARTIAL (part holds, part does not, or part is not checkable), NOT (the files say otherwise). A claim about what readers will do is a prediction; it is marked *not checkable* and gets no verdict.

## F1-F7

| id | claim | verdict | evidence |
|---|---|---|---|
| F1 | 70+ folders; the reliable doors are five root files; the start-here signal is easy to miss | PARTIAL | **232** top-level folders, not 70+ (the CLAUDE.md index's "75 folders" is as of 2026-08-23). The five root files exist. The start-here signal is in `README.md`: line 1 points to `READING_PROTOCOL.md`, line 4 to `READ_ME_THIS_WAY.md`, line 15 has "## Read first". *Easy to miss*: not checkable. `00_APERTURE.md`, named in Grok's E2, exists in 1 folder. |
| F2 | `READ_ME_THIS_WAY.md` keeps mis-bins, dead ends, correction specimens, model-chosen names, workarounds and duplicates as data | CONFIRMED | `READ_ME_THIS_WAY.md` lines 7-22, all six kinds, under "Do not fix, merge, rename or delete these records". *Largest source of silent damage*: not checkable. |
| F3 | PREAMBLE notes on term collision (REVISION vs ASSERTION), self-questioning as calibration not anxiety, term-drift check | CONFIRMED | `PREAMBLE.md` line 50 (TERM COLLISION), 58 (REVISION), 67 (ASSERTION), 75-92 (calibration; "mis-type continuous calibration as anxiety"), 95 (TERM-DRIFT CITATION CHECK). *Reader behaviour*: not checkable. |
| F4 | META-PROTOCOL states HELD/OFF/SILENT/MIXED/UNREPEATED/BLOCKED plus record states, no FAILED/WRONG/REJECTED; VOID/UNRESOLVED in the playground material | CONFIRMED | `META-PROTOCOL.md` 4B lines 205-210 (the six states), line 212 ("there is no FAILED, no WRONG, no REJECTED"), 4A lines 190-199 (the record states MEASURED ... UNMEASURED). VOID occurs in `combined-playground/cplay/pins.py` and `gates.py`, UNRESOLVED in `tokens.py` and `closure.py`. *Readers reach for pass/fail*: not checkable. |
| F5 | blind-reader-void12, self-scan and audit instruments assume a reader can treat public material as unseen; the protocol acknowledges it but the boundary is hard to enforce | PARTIAL | For `blind-reader-void12`, CONFIRMED: `PREREG.md` line 15, "Blindness is declared, not enforced". The reader is itself an instance: it read the repository after its record (`packets/grok_2026-11-19/SENT_RECORD.json`, `later_2026-11-19`). For `self-scan`, NOT: it measures this repository's own CLAUDE.md, and no blind reader is assumed. *The various audit instruments*: not checked. |
| F6 | most folders stdlib; a few (grounding-layers, others) need numpy; not queryable in one place | PARTIAL | See below. Third-party imports are in **18** of 232 folders. Of the 18, 9 carry no `requirements.txt` or `pyproject.toml` anywhere in the folder, so "documented" holds for half; "not queryable in one place" holds. |
| F7 | claim tables and refutation protocol not uniform | CONFIRMED | Script counts (`drafts/folder_fields_draft.py`; filename and token presence, not content): a claim-table file in 139 of 232 folders; the token REFUTATION_PROTOCOL in 95; `--selftest` mentioned in 152. *Every folder is supposed to carry claims*: NOT as a repository rule. CLAUDE.md exempts `play-sims/` ("No claim tables, no REFUTATION_PROTOCOL"), and `READING_PROTOCOL.md` routes a break to "the folder's CLAIM_TABLE.md" without requiring one in every folder. |

## F6 in detail: grounding-layers

Non-stdlib top-level imports (ast over every `.py` in the folder):

| module | files | how imported |
|---|---|---|
| numpy | 38 | top level |
| matplotlib | 12 | requirements.txt says imported lazily for the demos |
| scipy | 8 | the same |
| psutil | 1 (`ai_observer_state.py`) | top level, line 11, unguarded |
| pynvml | 1 (`ai_observer_state.py`) | inside try/except ImportError, line 51 (optional) |

`requirements.txt` lists numpy, matplotlib and scipy, and says numpy is "the only hard dep for the audit-grade tests". **psutil is not listed.**

**AIObserverState is defined, not missing.** It is at `ai_observer_state.py` line 18. It becomes unimportable where psutil is absent:

- `ai_observer_state.py` line 11 imports psutil unconditionally.
- `observer_state.py` lines 174-177 re-export it inside `try: ... except Exception: pass`, so the failure is silent at import.
- It surfaces only at the caller: `from observer_state import AIObserverState` raises ImportError ("cannot import name 'AIObserverState' from 'observer_state'"). Observed here, with numpy installed and psutil and scipy not.

Callers: `tests/test_bias_human_centrism.py` line 17 and `run_grounding_pipeline.py` line 257.

Reconciling with numpy/psutil: Grok's "require numpy" holds. The missing piece is psutil, a hard import in one module that the declared dependency list omits; it reads as a missing class because the re-export swallows the error. Not repaired here.

## Item 2: the map's state

| object | exists | coverage |
|---|---|---|
| `CONCEPT_MAP.md`, `concept_map.json` (`as_of` 2026-11-11) | yes | 14 concept rows. They cite paths in 7 of 232 Simulators folders (3.0%). `check_concept_map.py`: rows 14, paths OK 20, NOT_CHECKED 17 (other repositories not checked out here), failed 0. |
| `COLLISIONS.md`, `collisions.json` | yes | 5 collisions. The same script: evidence paths OK 1, NOT_CHECKED 6, **failed 4**. All four failures are provenance-credit evidence pinned to refs that no longer resolve (`origin/claude/forest-toolkit-build` x3, `origin/archive/pr256-tip`). |
| `TOOL_FINDER/` (`finder.json` dated 2026-11-09) | yes | 71 entries (Simulators 58, Cross-Domain-Toolkit 5, method-layer 4, Shadow-Hunting 3, JinnZ2 1). The Simulators entries sit in 32 of 232 folders (13.8%). 11 name collisions, 6 gaps. `build_finder.py` refuses as of this check: two quotes MISSING_FILE in `corpus_prior_audit/README.md` (JinnZ2 repository, not checked out here). |
| path-check script | yes, `check_concept_map.py` | the counts above, from its own output |

**The 2026-11-11 feature freeze is not recorded in this repository**, as in force or otherwise. Searched: every `.md` and `.json` for "freeze", "frozen", "feature freeze" and "no new tools", and every commit message on every fetched branch for "freeze". The only freeze dated 2026-11-11 is `forest-model-ledger/ledger/toolkit/HELDOUT_FREEZE.md`, a freeze of one toolkit's thresholds before a held-out run, not a feature freeze. If the freeze is recorded, it is in a repository or a conversation not reachable here.
