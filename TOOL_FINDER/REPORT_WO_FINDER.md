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

Simulators, method-layer and Shadow-Hunting carry a CC0 LICENSE file.
Note 2026-11-09: JinnZ2/JinnZ2 has no LICENSE file; its README line 6 declares "All repos CC0". An earlier version of this line said all four carry a CC0 LICENSE, which was wrong for JinnZ2.

## Paths

Simulators:
- new: `TOOL_FINDER/` (TOOL_FINDER.md, finder.json, entries.py, build_finder.py, write_finds_by.py, status.json, this report)
- new: `tail-check/`, `cutoff-attribution/`, `tools/README.md`
- READMEs created because none existed: `criterion-symmetry/README.md`, `observer-exclusion/README.md`
- 22 existing READMEs had a Finds-by section appended; tail-check/ and cutoff-attribution/ carry one in their new READMEs; tools/README.md carries 4 (30 sections in Simulators)

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
- **WO-6 ledger.** Not located. Searches of the local clones and of GitHub code across the JinnZ2 repos for a WO-6 out-of-scope repo ledger found only the WO-6 work orders in assessor-coupling, criterion-externality and chain-position-detectability, none of which is a repo ledger. Out-of-scope was therefore read as "not reachable or not CC0". All four repos touched are declared CC0 (JinnZ2 by README, not by a LICENSE file).
- **ICSC functional selection.** The term `ICSC` returned no hit in any repo reachable this session. The NAME_COLLISION entry carries it from the work order, with its location marked not found.
- **Shadow-Hunting.** It was not in the session's starting scope. It was attached during this task because the work order names it as the motivating case.
- **Aliases** are ALIAS_PROPOSED. They were not tested against real AI search queries.

---

## Amendments A1 + A2 (2026-11-09)

### Repos touched (added)

| repo | branch | head | PR | merge SHA |
|---|---|---|---|---|
| JinnZ2/Cross-Domain-Toolkit | claude/tool-finder-aliases | ec3b38a | #13 | PENDING (not merged) |

Cross-Domain-Toolkit carries a CC0 LICENSE. Its four package test suites pass. telemetry_vocabulary is markdown only and has no check command.

### A1: precision + channel chain

**Finder.** Every one of the now 43 entries carries three new fields: `precision`, `assumes` and `chain`.
- These fields are **A1_READING**: a model reading of each tool's stated scope, not verbatim text.
- `chain` names which hops of sensor -> encoding -> transmission -> decoding -> inference the tool reads or ignores.

**New shared record: `tools/channel_chain.py`.**
- Per hop it holds the known deviation sources and a known-reference check, with state CHECKED, CHECK_FAILED or UNVERIFIED_HOP.
- The chain class is VIA_CHECKED_CHAIN, VIA_UNVERIFIED_HOP or VIA_FAILED_HOP. No DIRECT class exists, and an empty chain reads UNVERIFIED.

**cutoff-attribution.**
- Each candidate now sits at one hop.
- A log event counts as OBSERVED only when its hop passed a reference check supplied by the caller. Otherwise it is RECORDED_VIA_UNVERIFIED_HOP or RECORDED_VIA_FAILED_HOP, and it counts as ESTIMATED.
- On every run, the tool injects a known cut into its own reading and confirms it is detected; a broken detector reads CHECK_FAILED.

**tail-check.**
- SAID now means "a span of the user turns as supplied".
- The decoding hop is self-checked on every run against two known spans, one present and one absent.
- The transmission and encoding hops accept a caller sentinel with `observed: "AUTO"`: the tool looks for the injected string in the user turns.
- Unchecked hops are named in every render.

### A2: Cross-Domain-Toolkit

**Finder scan.** Five packages were added: multi_substrate_calibration, falsification_ledger, cascade_regime_audit, runner_up_trace and telemetry_vocabulary. Each got a Finds-by section in its README, five sections in all, adding lines only.

**3a terms.** ATTRIBUTION_DISPLACEMENT cites "Interiority substitution" and "Care inversion".
- The term names come from `telemetry_vocabulary/terms.md`, read at run time with a line locator (for example `terms.md:49`), and are not re-coined.
- The mapping from phrase to term is the tool's own reading.
- With no toolkit checkout present, a hit reads TERM_NOT_CHECKED.

**A1 record fields.** The record uses the field names of `multi_substrate_calibration.substrate.SubstrateReading`.
- When a toolkit checkout is present they are imported from it (fields source: IMPORTED); otherwise they come from a mirror copy.
- If the toolkit's fields and the mirror differ, the record build raises an error.
- The record widens `value` from a float to a label. This is stated in the module, and the toolkit's determinacy gate would rightly refuse such a record.

**ICSC manifest lock layer.**
- The amendment names falsification_ledger as the lock layer of the ICSC manifest.
- The ICSC manifest itself is **NOT_LOCATED**: code search across JinnZ2 for "ICSC" returns only ICSCommand (an ICS component) in Nexus-emergency-management.
- The binding is therefore recorded in the ICSC NAME_COLLISION note and not built. No manifest was invented.

**NAME_COLLISION "clean-room".**
- The software-rebuild sense is located at Cross-Domain-Toolkit README.md:112 and docs/METHOD.md:10.
- The lab-isolation sense is carried from the amendment; no file in this session's scope using it was located.

**GAP.** Added: the four-arm paired design instrument (arms 1-4, arm 4 = infeasibility record). No tool was located that holds all four arms or files an infeasibility record as an arm.

### Selftests after the amendments (verbatim)

`python3 tools/channel_chain.py --selftest`
```
fields source: IMPORTED
checks: 12   failed: 0
```

`python3 tail-check/selftest.py`
```
tail_check.py refuses --selftest; run: python3 tail-check/selftest.py
checks: 26   failed: 0
```

`python3 cutoff-attribution/selftest.py`
```
cutoff_attribution.py refuses --selftest; run: python3 cutoff-attribution/selftest.py
checks: 25   failed: 0
```

`python3 TOOL_FINDER/build_finder.py --selftest`
```
checks: 14   failed: 0
```

### Other results

**Finder status** (worktree run): 36 RUN, 6 NOT_RUN, 1 UNKNOWN. The UNKNOWN is evaluation-frame, unchanged.

**Simulators root suite:** 194 passed, 3 failed. All 3 failures are pinned: pins 25, MATCH 25, VERDICT PASS.

### Not done under A1/A2

- **The 33 tools that are not builds.** No per-hop reference checks were added to them. A1's build clauses were applied to the two builds, and the finder records each tool's chain as a reading.
- **The worktree runs** cannot see a sibling Cross-Domain-Toolkit checkout. In those runs, tail-check and cutoff-attribution use the field mirror and TERM_NOT_CHECKED. Their selftests pass in both modes.

## Amendment A3: findability (2026-11-09)

### 1. Symptom index
- TOOL_FINDER.md now opens with a SYMPTOM INDEX of **38** symptoms, written in plain observer language and marked ALIAS_PROPOSED.
- Each symptom is derived only from the stated scope of the tools it points to.
- The selftest (17/17) checks two things:
  - every symptom points at an indexed tool;
  - every one of the **45** indexed tools is reachable from at least one symptom.
- Two tools joined the index so that symptoms had a target: `claim-audits/` and `scope-bound-shapes/`. Each received a Finds-by section, and both checks report RUN in the worktree rerun at 7e4ba7a.
- The rerun gives 38 RUN, 6 NOT_RUN and 1 UNKNOWN (evaluation-frame, as before).

### 2. README pointer
`TOOL_FINDER/insert_pointer.py` (selftest 6/6) adds the pointer as follows:
- It inserts two lines directly after the leading `>` preamble that names READ_ME_THIS_WAY, which puts them at lines 3-4.
- It refuses any README that has no such preamble.
- It asserts that every original byte is unchanged: the preamble stays at the head and the rest of the file follows the inserted lines.
- Each diff is +2 -0.

The link is https://github.com/JinnZ2/Simulators/blob/main/TOOL_FINDER/TOOL_FINDER.md. It resolves only once #252 is merged.

**Inserted: 12 repos.**

| repo | branch | PR |
|---|---|---|
| Simulators | claude/tool-finder | #252 |
| method-layer | claude/tool-finder-aliases | #30 |
| JinnZ2 | claude/tool-finder-aliases | #43 |
| Shadow-Hunting | claude/tool-finder-aliases | #9 |
| Cross-Domain-Toolkit | claude/tool-finder-aliases | #13 |
| AI-Consciousness-Sensors | claude/tool-finder-pointer | #29 |
| Noise-as-Information-Sensor | claude/tool-finder-pointer | #9 |
| Polyhedral-Intelligence | claude/tool-finder-pointer | #17 |
| chain-position-detectability | claude/tool-finder-pointer | #6 |
| decision-aperture | claude/tool-finder-pointer | #4 |
| differential-frame-core | claude/tool-finder-pointer | #6 |
| drift-archive-audit | claude/tool-finder-pointer | #9 |

**Skipped, with reason:**
- **thermodynamic-accountability-framework.** It is CC0 but its README has no READ_ME_THIS_WAY preamble (it opens with a personal letter), so "after the preamble" is undefined there. `insert_pointer.py` reports it as SKIPPED_NO_PREAMBLE.
- **experiments.** It is private and has no LICENSE, so it is not CC0. It does have the preamble.
- **The other ~90 JinnZ2 repos.** They are not attached to this session, so this session cannot push to them. The script can be run on them once they are attached.

### 3. Topics
- `TOOL_FINDER/TOPICS_TODO.md` lists **103** repos, with current topics read from the GitHub search API.
- **13** have suggested topics. Each comes from a stated scope read this session, and every suggestion is ALIAS_PROPOSED.
- **90** are marked NOT_DERIVED because their scope was not read this session.
- Topics cannot be set from code here; they have to be pasted in by hand under Settings -> About.

## FINDER FOLLOW-UP (2026-11-09)

The amendments received in this session were A1, A2 and A3.

| item | state | what was done, or why not |
|---|---|---|
| A1 | DONE (earlier) | Finder entries carry precision, assumes and chain. Builds run a per-hop known-reference check, an unchecked hop reads UNVERIFIED_HOP, and no reading is DIRECT. |
| A2 | DONE (completed now) | The 5 Cross-Domain-Toolkit packages are in the finder; the "clean-room" NAME_COLLISION and the four-arm GAP were added earlier. Now: cutoff-attribution cites all four chain terms. Before this pass it cited only two. Telemetry refusal :33, Interiority substitution :49, Care inversion :72 and Unnamed universal :88 come from terms.md. A new flag, TELEMETRY_REFUSAL, was added. ATTRIBUTION_DISPLACEMENT hits now carry the stage term plus "Unnamed universal", the latter marked as this tool's reading. |
| A3 | DONE (earlier) | Symptom index, README pointer in 12 repos, TOPICS_TODO.md. |
| B ICSC | BLOCKED | ICSC_v0.1_spec_audit.md was not supplied: a filesystem search finds no ICSC file. Nothing landed. The NAME_COLLISION location stays NOT_LOCATED. |
| C null calibration | DONE, ILLUSTRATIVE | Details below. |
| D avoided term | DONE, 0 filled | Details below. |
| E converter | DONE (converter); 3c NOT_RUN | Details below. |
| F WO-6 ledger | BLOCKED | WO6_CORPUS_AUDIT.md was not supplied. The scope list is unchanged and no scope was inferred. |
| G stamps | DONE, model WITHHELD | Details below. |

### C. Null calibration

`cutoff-attribution/null_calibration.py` wraps cutoff-attribution as f(data) -> verdict and runs it through null-harness (imported, numpy 2.5.3). The GAP entry moved to PARTIAL.

- **Confusion matrix:** 15 rows at 300 draws each.
  - Planted sources come back on the diagonal.
  - The NONE-correct rows (UNRESOLVED, 6 unchecked-hop rows, sensor collision) all read NONE.
  - The measurement-only row is missed in 300 of 300 draws. That miss is the cost of the gating rule, and it is kept on the matrix.
- **Forced-attribution rate:** 0 / 2400.
- **Per-candidate gates:** all 6 read OK (FP 0.000, TP 1.000).
- **Not calibrated:** the false-positive rate of DETECTED cuts themselves.
- **Illustrative only:** the planted events are exactly the evidence the rules accept, so the diagonal is close to true by construction.

### D. Avoided terms

coinage-log/COINAGE_LOG.md and vocabulary-gap-slots.md were read for every indexed tool name.

- The only hit is null-harness at COINAGE_LOG.md:114. It cites the harness's CONSTANT_FIRES term for the log's own null caveat; it gives no avoided term or reason for any tool.
- All 45 entries therefore stay AVOIDED_TERM_UNSTATED.

### E. Converter

- `evidence-demotion-detector/txt_to_json.py` is the converter. The schema it writes is stated in that README.
- Its output loads through detect.load_transcript.
- It refuses NO_LABELS, UNASSIGNED_LEAD and EMPTY_TURN.
- The 3c run itself is NOT_RUN because gpt_pretrip_2026-11-09.txt was not supplied.

### G. Stamps

Append-only "Tested" sections were added to these READMEs:
- cutoff-attribution
- evidence-demotion-detector
- tail-check
- tools (channel_chain)
- TOOL_FINDER (README.md created to hold stamps, since TOOL_FINDER.md is regenerated)

Two limits on the stamps:
- **No model identifier.** The model field reads WITHHELD because this session runs under a rule against writing a model identifier into a pushed artifact; model-provenance's MP_006 records the same conflict. The stamp records date, surface and selftest result.
- **README-only repos.** method-layer, JinnZ2, Shadow-Hunting and Cross-Domain-Toolkit had no tool built or edited this session, only README text, so they carry no stamp.

### Selftests (verbatim)

```
$ python3 tail-check/selftest.py                          checks: 26   failed: 0
$ python3 cutoff-attribution/selftest.py                  checks: 25   failed: 0
$ python3 cutoff-attribution/selftest_terms.py            checks: 11   failed: 0
$ python3 cutoff-attribution/selftest_null.py             checks: 10   failed: 0
$ python3 evidence-demotion-detector/selftest.py          selftest: 38/38 checks PASS
$ python3 evidence-demotion-detector/selftest_convert.py  checks: 11   failed: 0
$ python3 tools/channel_chain.py --selftest               checks: 12   failed: 0
$ python3 TOOL_FINDER/build_finder.py --selftest          checks: 17   failed: 0
$ python3 TOOL_FINDER/insert_pointer.py --selftest        checks: 6   failed: 0
```

### PRs and merge SHAs

Nothing has been merged; every PR is open. Merging waits for CI and for the owner's go-ahead. There are no merge SHAs yet.

### Update 2026-11-09: item B landed

- **B ICSC: DONE.** The operator supplied the spec as `ICSC_v0_1_spec_audit.pdf` (12 pages, sha256
  b0a1d4f2...c111) rather than as the .md the order named. It lands at `Simulators/ICSC/`:
  - `SPEC_AUDIT_v0.1.pdf` keeps the bytes as delivered.
  - `SPEC_AUDIT_v0.1.md` holds the `pdftotext -layout` text, unedited, in one fence.
  - `check_landing.py` re-extracts the PDF and compares; it reports `checks: 3   failed: 0`.
  - Status PROPOSED, nothing built.
- The NAME_COLLISION entry now points at the new location. The falsification_ledger lock-layer binding
  stays recorded only, because the manifest lock the audit calls for is not built.
- **Other uploads in the same message.** `US_distillate_floor_and_refinery_measurands...pdf` (sha256 ecac803d...)
  and `Label_Welds_Pickaxe_Mountain_to_Training_Data.docx` (sha256 684d86b8...) are byte-identical to the
  copies already filed in thermodynamic-accountability-framework `docs/audits_2026_11/`. Neither was re-filed.
  The docx is still the PARTIAL copy that ends after Node 1.
- **Still open.** F (WO-6 ledger) remains BLOCKED, and the 3c run remains NOT_RUN: neither file has been supplied.

## FINDER ROUND 3 (2026-11-09)

| item | state | what was done, or why not |
|---|---|---|
| 1 ICSC | DONE (no change) | The re-sent `ICSC_v0_1_spec_audit.pdf` has the same sha256 (b0a1d4f2...c111) as the copy landed at a909e9c, so `Simulators/ICSC/SPEC_AUDIT_v0.1.md` already holds it. No `.md` source arrived; only the PDF. NAME_COLLISION already points at `Simulators/ICSC/`. |
| 1 WO-6 | BLOCKED | `WO6_CORPUS_AUDIT.md` was not supplied: no such file is in the upload directory or anywhere on disk. The scope list is unchanged and no scope was inferred. |
| 2 pretrip run | NOT_RUN | `gpt_pretrip_2026-11-09.txt` was not supplied, so neither txt_to_json + detect.py nor cutoff-attribution was run on it. No flags to report. When it is run, it will have no signal log: detection will read punctuation and timing only, and every source will stay unseparated. |
| 3 missed row | DONE | Details below. |
| 4 stamps | DONE | Details below. |
| 5 naming rule | DONE | Details below. |

### 3. Missed row

- **What it output before.** For "network lag, unflagged" (an rtt_ms spike with no flag), the tool returned status UNRESOLVED and a candidate set of `UNRESOLVED` only. NETWORK_LAG appeared only under evidence, as LOGGED_UNFLAGGED.
- **What it outputs now.** Status UNRESOLVED, candidate set `NETWORK_LAG, UNRESOLVED`. An unflagged candidate is kept in the set but never raises the status.
- **Pin moved on purpose.** The selftest pin was updated with a dated note.
- **null_calibration rerun.**
  - Forced attribution is still 0 / 2400.
  - The measurement-only row is still a miss (verdict NONE, 300 draws), and the planted source is retained in the candidate set in all 300.
- **Optional `radio_log` input.**
  - Schema: list of `{t, dbm, network}`.
  - dBm becomes an unflagged rssi_dbm measurement; no threshold is applied.
  - A change of network type becomes a `network_handover` event on the transmission hop.
  - The schema is stated in `RADIO_SCHEMA` and in the README.

### 4. Stamps

- **Trailer check.** Every commit this session carries a `Co-Authored-By` model trailer.
- **New stamp lines.** Six Tested sections got a new line: `tested: 2026-11-09 | commit 98ecd8f | Claude Code, cloud session (claude.ai/code) | model: see trailer | <selftest results>`. Older WITHHELD lines are kept.
- **model-provenance reads the trailer.** `parse_trailer` on 98ecd8f returns the stated version (non-None).
- **The date decode does not match.** `decode` by date returns an older table row (SINGLE). `releases.json` is an observed-bound table read 2026-08-25 and has no row for the version these commits state. So the stated trailer and the date-decoded model differ for this session's commits; that is the release table missing a row.
- **Table not extended.** The table was not changed here. Extending it is a change to model-provenance's own data and is left for its own pass.

### 5. Naming rule

- `TOOL_FINDER/README.md` now carries the rule.
- Every tool created from 2026-11-09 on records `avoided term:` and `reason:` at creation, in its alias section.
- Existing tools stay UNSTATED.

### Selftests (verbatim, at 98ecd8f)

```
$ python3 tail-check/selftest.py                          checks: 26   failed: 0
$ python3 cutoff-attribution/selftest.py                  checks: 25   failed: 0
$ python3 cutoff-attribution/selftest_terms.py            checks: 11   failed: 0
$ python3 cutoff-attribution/selftest_null.py             checks: 11   failed: 0
$ python3 cutoff-attribution/selftest_radio.py            checks: 7   failed: 0
$ python3 evidence-demotion-detector/selftest.py          selftest: 38/38 checks PASS
$ python3 evidence-demotion-detector/selftest_convert.py  checks: 11   failed: 0
$ python3 tools/channel_chain.py --selftest               checks: 12   failed: 0
$ python3 TOOL_FINDER/build_finder.py --selftest          checks: 17   failed: 0
$ python3 TOOL_FINDER/insert_pointer.py --selftest        checks: 6   failed: 0
$ python3 ICSC/check_landing.py                           checks: 3   failed: 0
```

Nothing is merged. All PRs are open and waiting for the owner's go-ahead.

## Update 2026-11-09: ICSC markdown source landed

- DONE. The operator pasted the markdown source of the ICSC v0.1 specification audit.
- `Simulators/ICSC/SPEC_AUDIT_v0.1.md` now holds it verbatim, the path the order named.
- The earlier `pdftotext -layout` stand-in moved to `SPEC_AUDIT_v0.1.pdftotext.md`, content unchanged, with a dated note.
- Source and PDF agree word for word: 2612 words each after stripping markdown and box-drawing characters, 0 differences.
- `check_landing.py` gained a fourth check for that agreement. Verbatim: `checks: 4   failed: 0`.
- A copy with one word changed (`"isolated"` -> `"sealed"`) fails it: `checks: 4   failed: 1`.
- The NAME_COLLISION path (`Simulators/ICSC/SPEC_AUDIT_v0.1.md`) is unchanged and now points at the source.
- Still nothing built; status PROPOSED.


## Round 4 (2026-11-09, relayed via the Claude app)

| Item | State | Summary |
|---|---|---|
| 1 ICSC commit + named landing | DONE | Commit **a909e9c** first landed `Simulators/ICSC/`. The round 2 NOT_LOCATED was the NAME_COLLISION target, not the folder. `ICSC/ICSC_v0.1_spec_audit.md` is now beside the PDF (see below). |
| 2 WO-6 audit as scope list | DONE | `TOOL_FINDER/WO6_CORPUS_AUDIT.md` landed verbatim. `TOOL_FINDER/wo6_scope.py` reads its ledger as the scope list. |
| 3 null_calibration three outcomes | DONE | Scoring added and rerun. The matrix is below; the literal rule puts every NONE-correct control in WRONG. |
| 4 model-provenance | DONE (note) / BLOCKED (table) | STALE_TABLE logged as MP_010 with the table untouched. Extending `releases.json` is held; the reason is below. `verify` rerun. |

### 1. ICSC

- No file named `ICSC_v0.1_spec_audit.md` was attached. The upload directory holds only the two PDF copies.
- The markdown pasted in the previous turn is the same document. It is already `ICSC/SPEC_AUDIT_v0.1.md` (0c03017).
- The round 4 name is added as a byte copy. Both files: sha256 `984c2f94083979b86a58f078fed2addc9aca4d2b8588799c98c7859291e93a75`. No rename.
- `check_landing.py` check 3 now requires the two to stay byte-identical. Verbatim: `checks: 5   failed: 0`.
- A plant (one word changed in the copy, passed via `ICSC_ALT`) gives `checks: 5   failed: 1`.

### 2. WO-6 scope list

- File: `TOOL_FINDER/WO6_CORPUS_AUDIT.md`, 482069 bytes, sha256 `674f18ab2b1043de83d30e969860ce0368090cd47bc3575b162c1674e1cfb4e6`. It was cut from the relayed message at the start of the round 4 order; trailing blank lines were trimmed to one newline.
- `wo6_scope.py` parses the ledger only and infers nothing. An unknown status stops the parse. Selftest: `checks: 10   failed: 0`, with three planted faults each stopping the parse.
- Ledger: 103 rows. In scope 79 (75 MERGED plus 4 CI-blocked). Excluded 22 SKIPPED_OUT_OF_SCOPE and 2 SCOPE_UNRESOLVED (gap-quantification-protocol, Nuclear-Donut-DataCenter).
- The 4 CI-blocked rows use three status spellings (`BLOCKED_CI` x2, `PR_OPEN_BLOCKED_FAILED_CI`, `PR_OPEN_CI_FAILED_UNMERGED`). The parser checks they equal the audit's CI-blocked section.
- Every repo this order has touched is in scope: the 5 finder repos and the 7 pointer repos read MERGED. thermodynamic-accountability-framework reads `PR_OPEN_BLOCKED_FAILED_CI`, which is in scope; it was SKIPPED_NO_PREAMBLE in round 2 and is still untouched.
- No repo that rounds 1-3 touched falls outside the list, so nothing is withdrawn.

### 3. null_calibration three-outcome matrix

`python3 cutoff-attribution/null_calibration.py`, 300 draws per row, same seeds as the confusion matrix:

```
                              CORRECT_NAME CORRECT_ABSTAIN   WRONG   wrong by reason
NETWORK_LAG                            300               0       0   -
ENDPOINTING                            300               0       0   -
TASK_PAUSE                             300               0       0   -
AMBIENT_NOISE                          300               0       0   -
TRANSCRIPTION                          300               0       0   -
MODEL_READ                             300               0       0   -
UNRESOLVED                               0               0     300   abstain_status_ESTIMATED 300
NETWORK_LAG/hop_unchecked                0               0     300   abstain_status_ESTIMATED 300
ENDPOINTING/hop_unchecked                0               0     300   abstain_status_ESTIMATED 300
TASK_PAUSE/hop_unchecked                 0               0     300   abstain_status_ESTIMATED 300
AMBIENT_NOISE/hop_unchecked              0               0     300   abstain_status_ESTIMATED 300
TRANSCRIPTION/hop_unchecked              0               0     300   abstain_status_ESTIMATED 300
MODEL_READ/hop_unchecked                 0               0     300   abstain_status_ESTIMATED 300
sensor_collision                         0               0     300   abstain_status_ESTIMATED 300
NETWORK_LAG/measurement_only             0             300       0   -
total                                 1800             300    2400
```

- True sources: the planted source on each planted row, including hop_unchecked; `UNRESOLVED` on the UNRESOLVED control; TASK_PAUSE and AMBIENT_NOISE on sensor_collision.
- **Finding.** Every control where NONE is the gating-correct verdict abstains with status ESTIMATED, not UNRESOLVED. The true source is in the candidate set on all of them. Under the order's rule they therefore score WRONG.
- Cause: each draw carries a distractor event through an unverified hop. That gives a RECORDED_VIA_UNVERIFIED_HOP candidate, which raises the status to ESTIMATED.
- Neither the classifier nor the rule was changed to move this. Whether ESTIMATED-with-NONE should count as an abstention is the operator's call.
- The only CORRECT_ABSTAIN row is measurement_only: an unflagged rtt_ms with no other evidence gives status UNRESOLVED.
- `selftest_null.py`: `checks: 16   failed: 0`. New checks: planted rows score CORRECT_NAME; measurement_only scores CORRECT_ABSTAIN; the UNRESOLVED control is WRONG for the ESTIMATED reason; the outcomes partition every draw; a constant-name classifier is right on its own row and WRONG elsewhere.

### 4. model-provenance

- **STALE_TABLE (DONE).** Logged as `model-provenance/CLAIM_TABLE.md` MP_010, dated, with `releases.json` untouched.
- `verify` on the full history (not shallow) reads: SINGLE matches 315, SINGLE differs 511, AMBIGUOUS contains 17, AMBIGUOUS excludes 3, no version stated 601.
- The history's trailers name 7 versions; the table has rows for 3, with counts as of 2026-08-25.
- **Table extension (BLOCKED).** The new row would write a model identifier into a pushed data file. That conflicts with this session's standing rule: identifiers appear only in the commit trailer. MP_006 recorded the same conflict as WITHHELD. The row is computed (first/last appearance and commit count from the trailers) and given in the chat reply only. It lands if the operator adds it or confirms the rule does not apply to this file.
- Because the table was not extended, `verify` was rerun but its counts did not move: they are the numbers above.
- `provenance.py --selftest`: `SELFTEST PASS (0 checks failed)`.

### Checks (verbatim, working tree before commit)

```
$ python3 TOOL_FINDER/wo6_scope.py --selftest            checks: 10   failed: 0
$ python3 TOOL_FINDER/build_finder.py --selftest         checks: 17   failed: 0
$ python3 ICSC/check_landing.py                          checks: 5   failed: 0
$ python3 cutoff-attribution/selftest_null.py            checks: 16   failed: 0
$ python3 cutoff-attribution/selftest.py                 checks: 25   failed: 0
$ python3 model-provenance/provenance.py --selftest      SELFTEST PASS (0 checks failed)
$ python3 tools/known_red_check.py --suite               pins: 25   MATCH 25   MISMATCH 0   VERDICT: PASS
$ python3 -m pytest tests -q                             3 failed, 194 passed (the 3 pinned)
```

Nothing is merged. All PRs are open and waiting for the owner's go-ahead.

## ICSC v0.2 landing (2026-11-09)
Note 2026-11-09: work order relayed via the Claude app. Checks run in a throwaway worktree at de97f90.

1. DONE. `ICSC/SPEC_v0.2.md` is the supplied text verbatim (landed at 6819b1a, sha256 5773584923e1...68791e),
   status PROPOSED. v0.1 (PDF, the supplied .md, the byte copy) is unchanged. No file named
   ICSC_v0.2_spec.md was attached; the pasted text is the landed file. The TOOL_FINDER entry for ICSC
   (name collision with encoding-selection) now names both specs.
   `checks: 5   failed: 0` (check_landing.py), `checks: 11   failed: 0` (check_v02.py),
   `checks: 17   failed: 0` (build_finder.py --selftest).
2. DONE. model-provenance `decode_commit()`: a trailer naming a model with no table row decodes
   `CONDITIONAL(stale_table)`, with no candidates and no model printed; `verify` counts these in their own row.
   This repository reads 419 such commits. releases.json is not edited. Selftest has a planted unknown-model case.
   The dated note is in the README and CLAIM_TABLE MP_011. `SELFTEST PASS (0 checks failed)`, 34 checks.
3. DONE, confirmed in place since round 4. The three-outcome score CORRECT_NAME / CORRECT_ABSTAIN / WRONG
   reads total 1800 / 300 / 2400. The 2400 WRONG are all abstain_status_ESTIMATED, and whether those count
   as required abstentions under T29/G2 is still the operator's call.
4. DONE. null_calibration output line 3 reads validity = CONDITIONAL(same_author). The README "breaks when"
   states it, and a selftest check is added. `checks: 17   failed: 0` (selftest_null.py),
   `checks: 25   failed: 0` (selftest.py).
5. DONE earlier (cd4e385); it was re-pasted and is identical apart from one trailing newline.
   It is the scope list. `checks: 10   failed: 0` (wo6_scope.py --selftest).
Tree: pytest tests 3 failed / 194 passed (the 3 pinned run_manifest failures); known_red_check --suite VERDICT: PASS.
Worktree git status clean after the runs. PR #252, branch claude/tool-finder.

## Round 6 (2026-11-09)

1. PARTLY DONE / BLOCKED.
   - BLOCKED: landing the revised v0.2. The order says the text was
     supplied with it, but the message carried no spec text and no file.
     SPEC_v0.2.md is unchanged; the "rev 2026-11-09 11:44" section is
     appended when the text arrives.
   - DONE: the label rename. CONDITIONAL(same_author) is now
     CONDITIONAL(circular_control) in null_calibration.py, its sample,
     selftest_null.py and the cutoff-attribution README, each with a dated
     note.
   - The old label is kept as VALIDITY_OLD. A selftest check asserts it is
     recorded and no longer emitted.
   - SPEC_v0.2.md section 4.1 and T30 still say same_author. That text
     changes only with the revised spec.
2. PARTLY DONE / AWAITING PICK.
   - DONE: designed identifiability per control, declared as data from
     the planted design, not from the tool. The 6 plain rows are yes. The
     other 9 are no: UNRESOLVED, the 6 hop_unchecked, sensor_collision and
     measurement_only.
   - All 2400 ESTIMATED abstentions are on rows not designed to identify a
     source. No identifiable row has an ESTIMATED abstention.
   - The matrix was rerun with every option as a readout. None is adopted,
     and the score stays at the current row until you pick:
       option    CORRECT_NAME CORRECT_ABSTAIN   WRONG  MISSED_IDENTIFIABLE
       current           1800             300    2400                    0
       A                 1800            2700       0                    0
       B                 1800             300    2400                    0
       AB                1800            2700       0                    0
   - On these controls B adds nothing and AB equals A. They would differ
     only on a control where the identifying evidence was planted and the
     tool still abstained.
3. BLOCKED, awaiting pick. releases.json is unchanged. Option 3 was dry-run
   in scratch, never pushed, with counts only:
   - The stale count is now 421, not 419. The tree gained commits since
     the last order.
   - In the snapshot, one observed_bound row was added for each of the 4
     missing versions. stale_table 421 -> 0; agree 315 -> 229; disagree
     94 -> 254; ambiguous_contains 17 -> 212; ambiguous_excludes 3 -> 155;
     unstated 601 -> 601.
   - Reverse-T21 FAILS its second clause. 390 of the 1030 non-stale commits
     changed decode, because the new rows' windows overlap the existing
     rows.
   - So option 3 as written cannot be confirmed on this repository. Option
     1 has the same overlap effect.
   - Any added row writes model names into a pushed file, which the
     standing no-identifier rule needs you to clear.

Selftest lines (throwaway worktree, commit 5fcb172): selftest_null "checks: 21   failed: 0"; cutoff selftest "checks: 25   failed: 0"; check_v02 "checks: 11   failed: 0"; check_landing "checks: 5   failed: 0"; build_finder "checks: 17   failed: 0"; pytest tests 194 passed, 3 failed (the pinned run_manifest set); known_red VERDICT: PASS.

## Round 7 (2026-11-09)

1. BLOCKED. The order names an attachment, ICSC_v0.2_spec.md. No such file reached this session;
   a filesystem search finds none. SPEC_v0.2.md is unchanged, and the "rev 2026-11-09 11:44"
   section is appended when the file arrives.
2. DONE.
   - Adopted scoring is the owner's pick "both". An abstention on a control not designed to
     identify is CORRECT_ABSTAIN. An abstention on a control designed to identify is
     MISSED_IDENTIFIABLE.
   - Added 12 noise controls, one per source at k = 3 and k = 6. Each is designed to identify:
     one flagged event on a checked hop inside the window, k distractors on unchecked hops, k
     unflagged measurements, and one same-hop or own-kind decoy outside the window. The data
     carries no field naming the source, which a selftest check asserts.
   - Results:
       noise controls only     CORRECT_NAME 3600   CORRECT_ABSTAIN 0     MISSED_IDENTIFIABLE 0   WRONG 0
       total (all controls)    CORRECT_NAME 5400   CORRECT_ABSTAIN 2700  MISSED_IDENTIFIABLE 0   WRONG 0
   - MISSED_IDENTIFIABLE is zero because the noise only touches inputs the rules already ignore.
     That is the CONDITIONAL(circular_control) result again: wiring, not validity.
   - A constant-NONE classifier scores MISSED_IDENTIFIABLE on every noise control, which shows
     the outcome is reachable.
   - The round-4 three-outcome table is still printed (1800 / 300 / 2400) as a correction
     specimen.
3. PARTLY DONE / BLOCKED.
   - DONE: MP_012 logged, with counts only. 421 stale commits. The dry run added rows for the 4
     missing versions. Reverse-T21 failed on 390 of the 1030 commits outside the stale set,
     because the rows' date windows overlap and so the rows are not independent.
   - BLOCKED: the owner picked option b (add rows). One of the four versions is the identifier
     of the session's own model, and this session may not write any model identifier into a
     pushed file. The four rows were given to the owner in chat to add by hand. releases.json
     is unchanged.

Selftest lines (throwaway worktree, commit e577c4e): selftest_null "checks: 28   failed: 0"; cutoff selftest "checks: 25   failed: 0"; provenance "SELFTEST PASS (0 checks failed)"; check_v02 "checks: 11   failed: 0"; check_landing "checks: 5   failed: 0"; build_finder "checks: 17   failed: 0"; pytest tests 194 passed, 3 failed (the pinned run_manifest set); known_red VERDICT: PASS.
