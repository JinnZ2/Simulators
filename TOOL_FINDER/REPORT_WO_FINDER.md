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
