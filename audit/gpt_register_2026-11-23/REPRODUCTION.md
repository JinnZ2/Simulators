<!-- SPDX-License-Identifier: CC0-1.0 -->
# REPRODUCTION - GPT audit register of 2026-11-23, items R01-R04

License: CC0-1.0. Co-authored (JinnZ2 + Claude). Date: 2026-11-23 UTC.
Status: reproduction record. Read-only on every existing file; the only new
files are this one and `reproduce.py` beside it.

Executor is a different family from the register's author; neither is independent of the owner's repository conventions.

Tags used in this file: OBSERVED, DERIVED, RECORDED, REPRODUCED, DIFFERS,
NOT CHECKABLE, UNRESOLVED, NOT RUN.

Observer slots: null.

## Provenance

- Register under reproduction: "SIMULATORS - FROZEN EXPERIMENT AUDIT REGISTER"
  (GPT, read-only, 2026-11-23). It reached the executor only through the
  owner's work order. The register text itself was NOT in hand: no file of it
  is in this repository and none was attached. What the executor had of it is
  the four counts for R01 (0 / 33 / 47 / 52), the words "GPT risk D", and the
  finding ids F01-F10 by number only.
- Work order: owner's order of 2026-11-23 (co-authored, Kavik + Claude),
  items R01-R04.
- Executor: Claude Code session. Family: Claude (declared, not verified).
  Model: not written in this file (standing rule of this repository's filing
  sessions: no model identifier in filed text; the commit trailer carries it).
- Base: main at `9a118df`. Python 3.13.18, Linux.
- Every number below is recomputed by `python3 -B
  audit/gpt_register_2026-11-23/reproduce.py` (exit 0), which imports the
  validator and the case checker as they are and writes nothing.
- Exposure: the executor had read `arms_report.txt` (which holds the same
  counts) before recomputing them. The recomputation does not read that file;
  `arms.py --check` compares against it.

## R01 - M01 validator on the recorded M01 input

Input: `blind-reader-void12/studies/m01_records.json` (commit `3d3ac5f`,
unchanged since). Validator: `studies/instrument/validate.py` and `arms.py`
(commits `961146e`, `158aa12`).

On "at its pinned commits (67b8e9d, 66d4f28)": OBSERVED, those two commits
hold the M01 schema and criteria (`M01_SCHEMA.json`, `M01_CRITERIA.md` at
`67b8e9d`; `M01_EXTENSION.md` at `66d4f28`). The validator does not exist at
either commit; it was added at `961146e` and `158aa12`. The three pinned files
have one commit each in `git log`, so the validator at main reads them exactly
as pinned. The run below is the validator at main on those files.

| count | GPT (RECORDED) | here (OBSERVED) | status |
|---|---|---|---|
| structural errors (rule_off) | 0 | 0 | REPRODUCED |
| rule_on rejections, TAG by a1_defined ("strict A1") | 33 | 33 | REPRODUCED |
| rule_on rejections, TAG by presence | 47 | 47 | REPRODUCED |
| rule_on rejections, TAG by applicability | 52 | 52 | REPRODUCED |

111 records, 3 readers, 87 records with `reader.listed = LISTED`. No
difference was found, so none is logged.

Per reader (rejected of listed):

| reader_id | listed | a1_defined | presence | applicability |
|---|---|---|---|---|
| 2026-11-18_claude-v2-A | 35 | 16 | 21 | 23 |
| 2026-11-19_kimi-v2-A | 31 | 12 | 17 | 19 |
| 2026-11-19_gpt6-v2 | 21 | 5 | 9 | 10 |
| total | 87 | 33 | 47 | 52 |

Per field (records rejected, of the readers that listed the field; fields
with no rejection under any reading are left out):

| term | field | listed by | a1_defined | presence | applicability |
|---|---|---|---|---|---|
| T01 | first_straddling_piece | 1 | 1 | 1 | 1 |
| T01 | first_undecided_subbox | 2 | 2 | 2 | 2 |
| T01 | proposal | 2 | 2 | 2 | 2 |
| T01 | straddle_at_depth_limit | 1 | 1 | 1 | 1 |
| T01 | undecided_at_depth_limit | 1 | 1 | 1 | 1 |
| T02 | value | 2 | 2 | 2 | 2 |
| T05 | covers_effect | 3 | 3 | 3 | 3 |
| T05 | ladder | 3 | 0 | 0 | 3 |
| T07 | first_subbox_with_no_value | 2 | 2 | 2 | 2 |
| T07 | void_reason | 3 | 3 | 3 | 0 |
| T08 | call | 1 | 1 | 1 | 1 |
| T08 | exc | 1 | 1 | 1 | 1 |
| T08 | exception | 3 | 0 | 3 | 3 |
| T08 | inputs | 3 | 3 | 3 | 3 |
| T08 | path | 3 | 0 | 3 | 3 |
| T09 | expiry_condition | 1 | 1 | 1 | 1 |
| T09 | expiry_source | 1 | 1 | 1 | 1 |
| T10 | exception_type | 2 | 2 | 2 | 2 |
| T10 | missing_path | 2 | 0 | 0 | 2 |
| T12 | triggers | 2 | 0 | 2 | 2 |
| T12 | typed | 3 | 3 | 3 | 3 |
| T12 | untyped | 3 | 3 | 3 | 3 |
| T14 | basis | 3 | 0 | 3 | 3 |
| T14 | sigma | 3 | 0 | 3 | 3 |
| T15 | instrument | 1 | 1 | 1 | 1 |
| T15 | sensitivity | 3 | 0 | 0 | 3 |
| sum | | | 33 | 47 | 52 |

Commands and exit codes (OBSERVED):

| command | exit | first output line |
|---|---|---|
| `validate.py m01 m01_records.json` | 0 | `m01: 111 item(s), 0 structural error(s)` |
| `validate.py --arm=rule_off m01 m01_records.json` | 0 | same |
| `validate.py --arm=rule_on m01 m01_records.json` | 1 | `m01: 111 item(s), 0 structural error(s), 33 rule_on rejection(s) (analysis arm, TAG read as key a1 defines it)` |
| `arms.py --check` | 0 | `arms --check: identical` |
| `test_instrument.py` | 0 | 19 tests, OK |

What exit 1 means, by the validator's own text: the module docstring gives
usage and rules and states no exit codes. From the code (`main`): 2 = usage,
1 = the error list is not empty, 0 = it is empty. Under `--arm=rule_on` the
rule_on rejections are in that list, so the exit is 1 with 0 structural
errors. The docstring also says "It records; it never scores" and that a
reader listing a computed or shared field "is valid". So exit 1 under rule_on
reports rejections by an analysis arm, not an invalid input file; a caller
that reads any nonzero exit as "records invalid" would misread it. Whether
that is what the register calls risk D is NOT CHECKABLE (register text not in
hand). The CLI runs rule_on under a1_defined only; the presence and
applicability counts come from `arms.py` / `gpt_rule_errors(recs, reading)`.

## R02 - T02 "value"

Steps, each with its evidence:

1. Source definition. OBSERVED. The packet glossary row
   (`reader_packet_v2/sources/thermodynamic-accountability-framework/docs/glossary.md`
   line 129) writes the term as `ABSENT_AT_SENSITIVITY(<value>)` and ends "No
   slot holds it yet." `calibration/expiry_register.py` lines 228-235
   (`slot_state`) parses the same notation from a string.
2. Instantiated, documented or other. OBSERVED: documented only.
   `m01_records.json` codes the field `origin DOCUMENTED`, all three scopes
   `NO_INSTANCE`, provenance `SCRIPT_DERIVED` (`m01_code.py` lines 177-181,
   which assert the notation and "No slot holds it yet" are in the glossary).
   `M01_SCHEMA.json` line 25 defines DOCUMENTED as "named only in prose, a
   notation or a key list, with no instance built in the packet".
3. TAG and INDEPENDENCE recomputed from the declared rules. OBSERVED, by
   `validate.tag_by` and `validate.independence_of`: TAG = UNRESOLVED under
   a1_defined, presence and applicability; INDEPENDENCE = UNRESOLVED. Both
   follow from origin DOCUMENTED / scope NO_INSTANCE: the rule
   (`KEY_V2_AMENDMENT_1.md` section 2) is stated over instances of the term,
   and the packet builds none.
4. Key A1. OBSERVED: `scoring/key_v2_a1.json` T02 has
   `slots_specific: ["value"]`, so `key_a1.listed = LISTED` on all three T02
   records. The key's derivation text says "no record holds the state today".
   The list comes from `amendment_options/derive/derive_specific.py` lines
   276-277, a regular expression over the notation ("the notation's one
   parameter"). `key_v2.json` already had the same list; amendment 1 did not
   change T02 (`KEY_V2_AMENDMENT_1.md` section 3: four lists changed, T08 T09
   T10 T12).
5. Comparison. OBSERVED: key A1 lists `value`; the rule as declared cannot
   return YES for it. `arms_report.txt` prints the same thing as its
   self-check: "NO, 1 field(s) differ: T02 value". Two readers listed the
   field (claude, kimi); gpt6 did not.

Classification: unresolved definition. Reasons, each OBSERVED in a file:
`amendment_options/decide/DECISION_EVIDENCE.md` line 19 says T02 `value`
"come[s] from a notation ... and [has] no dependence test";
`studies/GAPS.md` row G1 leaves open "how a documented-only field with no
instance is read"; `studies/OPEN_ROWS.md` carries it as CF11 and KC02,
DEFINITION_REQUIRED, open. The key is built by its script as written and the
validator applies the mapping as written, so this is not shown to be a key
error or an implementation error; which of the two readings is right is the
owner's definition. Status: UNRESOLVED. Nothing was changed.

## R03 - frame-location freeze order

Scope: `frame-location-benchmark/`. History of the folder is two commits:
`a70eb40` (2026-09-06T02:05:20Z) and `43e1068` (2026-09-06T02:45:35Z).

| check | result | evidence |
|---|---|---|
| harness files predate `cases.jsonl` | NOT CHECKABLE | all four harness files, `FREEZE_LOG.md` and `cases.jsonl` first appear in the same commit, `a70eb40`. Git holds no order between them. `FREEZE_LOG.md` states the order; that statement is RECORDED, not reproduced. |
| harness unchanged after the freeze | PASS | each of the four harness files has one commit (`a70eb40`). |
| cases changed after the freeze | OBSERVED | `cases.jsonl` was edited at `43e1068`: one case differs, FL-105 (40 cases before and after). |
| case prompts absent from harness | PASS | 0 of 40 prompts found (normalized substring) in any of the 4 harness files, at HEAD and at `a70eb40`. |
| fault targets not leaked | PASS | 21 cases carry a `fault_target`; 0 found in any harness file, at HEAD and at `a70eb40`. Same normalization as the checker; a paraphrase would not be caught. |
| frozen files match their declared versions | NOT CHECKABLE, one part PASS | no hash or version of a harness file is declared anywhere in the folder (`FREEZE_LOG.md`, `README.md`, `protocol.md`, `CLAIM_TABLE.md` searched). The one declared relation, `arm4_full.txt` = `arm2_positions.txt` ++ `arm3_corrections.txt` byte-exact, holds: PASS. |

## R04 - validate_cases.py and the contamination checker, as they are

| command (run in `frame-location-benchmark/`) | exit | output |
|---|---|---|
| `python3 -B validate_cases.py` | 0 | `validate_cases: PASS (R1-R6 + section-4 contamination)` |
| `python3 -B selftest_flb.py` | 0 | `selftest: 41 checks, 0 failed` |

The contamination checker is `check_contamination` inside
`validate_cases.py`; the bare run above includes it, and
`validate_cases.validate()` returns ok with 0 messages. Nothing was edited to
make a control pass.

## Findings F01-F10

The register's text for F01-F10 was not in hand, so no finding can be matched
to its id here. Every id is NOT CHECKABLE for that reason only; this is not a
statement about the findings.

| id | status | note |
|---|---|---|
| F01 | NOT CHECKABLE | register text not in hand |
| F02 | NOT CHECKABLE | register text not in hand |
| F03 | NOT CHECKABLE | register text not in hand |
| F04 | NOT CHECKABLE | register text not in hand |
| F05 | NOT CHECKABLE | register text not in hand |
| F06 | NOT CHECKABLE | register text not in hand |
| F07 | NOT CHECKABLE | register text not in hand |
| F08 | NOT CHECKABLE | register text not in hand |
| F09 | NOT CHECKABLE | register text not in hand |
| F10 | NOT CHECKABLE | register text not in hand |

Claims of the register that the work order did relay, by content:

| claim (as relayed) | status |
|---|---|
| M01 counts 0 / 33 / 47 / 52 | REPRODUCED |
| risk D (validator exit code) | NOT CHECKABLE as worded; the exit-code behaviour is OBSERVED in R01 |
| T02 "value" differs from key A1 | REPRODUCED; classified unresolved definition, UNRESOLVED |
| frame-location freeze order | NOT CHECKABLE from git (one commit); leak checks PASS |
| case validation and contamination check | REPRODUCED as PASS, exit 0 |

## Not done

- No frozen file, fixture, key, record or generated output was modified.
- The M01 validator was not run at `67b8e9d` or `66d4f28`: it is not in those
  trees.
- Paraphrase leaks between cases and harness were not searched for.
- The register's own text was not read, so nothing beyond the relayed claims
  was reproduced.

## Dated addition, 2026-11-23 UTC (later the same day): register text in hand

Nothing above this heading is changed. The table "Findings F01-F10" above
stays as written; this section replaces its statuses.

The owner pasted the register text into the session after the record above
was filed. It is still not a file in this repository; the finding lines
below are quoted from the paste (register section 5). The paste also carried
a second block, "Simulators Repository Confusion Risks for First-Time AI
Readers", which holds the item the work order called risk D.

Statuses use the register's own three states (recorded, reproduced,
independently verified) plus this file's tags. REPRODUCED here means
regenerated by this executor from the named inputs; it does not mean
independently verified (see the verbatim line at the top).

| id | register text (quoted) | register class | status here | basis |
|---|---|---|---|---|
| F01 | "M01 validator arms report 0, 33, 47, and 52 flagged records" | RECORDED | REPRODUCED | R01 above: 0 / 33 / 47 / 52 recomputed; `arms.py --check` identical to `arms_report.txt` |
| F02 | "T02 classification mismatch appears in the recorded self-check" | RECORDED | REPRODUCED; origin UNRESOLVED | `arms_report.txt` line 10 ("1 field(s) differ: T02 value"); R02 above recomputes it and classes it as an unresolved definition |
| F03 | "M01 has three coded D0 readings" | RECORDED | REPRODUCED | `m01_records.json`: 3 reader ids, condition D0 on all 111 records (37 each) |
| F04 | "M01 D1 extension has no new reading in inspected index" | RECORDED | REPRODUCED as a statement of the index | `blind-reader-void12/studies/README.md` line 8: "designed; no new reading yet"; `m01_records.json` holds no condition other than D0. Whether a D1 reading exists outside the repository: NOT CHECKABLE |
| F05 | "M02 comparative coding remains outstanding in inspected index" | RECORDED | REPRODUCED as a statement of the index | same README line 9: "designed; the three filed readings not yet coded". No M02 records file was searched for beyond the index |
| F06 | "Frame-location benchmark contains 40 constructed cases" | RECORDED | REPRODUCED | `cases.jsonl`: 40 rows, all `source` = constructed; 19 WELL, 21 MIS; 8 domains; 7 fault classes, 3 cases each |
| F07 | "Frame-location benchmark reports no completed model evaluation" | RECORDED | REPRODUCED as a statement of the README | `frame-location-benchmark/README.md` line 11: "Nothing here is a benchmark result."; `runs/` holds two arms the README (line 107) labels CONSTRUCTED fixtures |
| F08 | "Exact reproduction of M01 outputs" | NOT TESTED | REPRODUCED | R01 above; no difference found in totals, per-reader or per-field counts |
| F09 | "Commit-level freeze chronology and integrity" | NOT FULLY VERIFIED | NOT CHECKABLE (chronology); PASS (content checks) | R03 above: harness and cases first appear in one commit, `a70eb40`; no declared hashes; leak checks pass at both commits |
| F10 | "Complete repository-wide frozen artifact inventory" | INCOMPLETE | NOT RUN | outside R01-R04; no inventory was attempted |

Register items outside the F-table:

| item | status here | basis |
|---|---|---|
| section 2D: "Four harness files established before the case set" | RECORDED only | `FREEZE_LOG.md` lines 1, 4 and 22 state it; git cannot show it (R03) |
| section 3: counts "repository-reported, not independently reproduced" | now REPRODUCED by one executor of a different family | R01; not independent of the owner's conventions |
| section 3, M01-D01 checks 1-5 | done in R02; check 5 answer: unresolved definition | R02 |
| R05 (provenance and independence per result) | NOT RUN | not in the work order |
| risk D: "exit code 1 from the validator could be treated as a failure rather than 'flags found'" | premise OBSERVED; the risk itself NOT TESTED | R01: `--arm=rule_on` exits 1 with 0 structural errors, and the validator's docstring states no exit codes. Whether a reader misreads it was not tested |
| confusion risks A, B, C, E and confirmed items one to six | NOT RUN | not in the work order |

One difference between the register and the repository, logged: the register
(section 2B) gives the M01 recorded outcome as "Three D0 readings coded" and
the index says "three filed v2 readings coded". Both hold for the same three
readers; the gpt6 records carry packet variant and sha256 as null where the
other two carry variant A and a hash. No count differs.

## Correction section, 2026-11-24 UTC (owner's order 336-F1)

Nothing above this heading is changed. Where this section and an earlier
one differ, this section holds.

Tags added for this section, beside those on line 10: NOT RECORDED,
NOT CHECKED, NOT TESTED, PASS, PROPOSED, STATEMENT PRESENT.

### C1. Register filed

The register text is now a file: `REGISTER_AS_RECEIVED.md` beside this one,
file sha256 `33092afccd1f1081f087edd2cfdf3537375419cb8c82e6612c887a85802eea39`
(12165 bytes). The received text inside it is 10863 bytes, sha256
`4e4502487af097a300c0c632fb882c84ccf25e6502ae179bf9e0aad191d2dad0`. Every
"register text (quoted)" cell in the F01-F10 table of the dated addition
above is a quote from section 5 of that file at that hash. The sentence
there, "It is still not a file in this repository", held when written and
no longer holds.

### C2. Relabel of F04, F05, F07

| id | status in the dated addition | status now |
|---|---|---|
| F04 | REPRODUCED as a statement of the index | STATEMENT PRESENT; underlying claim NOT CHECKED |
| F05 | REPRODUCED as a statement of the index | STATEMENT PRESENT; underlying claim NOT CHECKED |
| F07 | REPRODUCED as a statement of the README | STATEMENT PRESENT; underlying claim NOT CHECKED |

Why (2026-11-24): for these three, what was regenerated is only that a
sentence sits in a README. The claims under the sentences (no D1 reading
exists; the M02 coding has not been done; no model evaluation has been
completed) were not tested, so REPRODUCED was the wrong word for them. For
F04 one part was looked at and stays OBSERVED: `m01_records.json` holds no
condition other than D0.

### C3. F08, what the comparison was

F08 stays REPRODUCED. What R01 compared: 4 totals (structural, a1_defined,
presence, applicability), 9 per-reader counts (3 readers by 3 analysis
arms), the per-field table (26 fields), and the full text printed by
`arms.py --check` against `arms_report.txt`. n = 111 records, 87 of them
listed. Size of difference the register claimed: NOT RECORDED (the register
states no size; its acceptance criterion is exact agreement). Detectable
difference: the counts are integers from a script with no random draw and
the comparison is exact, so a difference of one record in any compared count
would have shown [DERIVED]. `reproduce.py` was run more than once in the
filing session with the same output [OBSERVED]; no run on another machine or
Python version was made: NOT RECORDED.

### C4. Deviation log

- "F01-F10 filled on the session's own offer, without a separate order; owner kept it 2026-11-23."
- The first filing gave the executor's family and not its model (stated in
  Provenance above). Unchanged.

### C5. Outstanding register items

Same status classes as the F table. Checked on the PR branch (main at
`9a118df` plus this folder), 2026-11-24 UTC, Python 3.13.18.

| item | register text (short) | status | basis |
|---|---|---|---|
| R05 | provenance and independence fields for every result | PARTLY RUN: fields read from files for the six filed readings; three fields NOT RECORDED | table below |
| F10 | complete repository-wide frozen artifact inventory | NOT RUN | the register gives no rule for what counts as a frozen artifact; choosing one is a choice it does not fix. One count by file name only, not an inventory: 4 tracked files named PREREG.md, FREEZE_LOG.md or PREREGISTRATION.md (`blind-reader-void12/PREREG.md`, `frame-location-benchmark/FREEZE_LOG.md`, `kernel_stake/PREREGISTRATION.md`, `relational-playground/experiments/model_comparison/forest_fire_regime/PREREG.md`) |
| confirmed 1 | known-answer registry keeps a failing case as calibration | REPRODUCED; count DIFFERS | `python3 -B tools/known_answer.py` exits 0, prints "cases disagreeing with the registry: 0" and two cases marked "FAIL (pinned)" ("matched set", "half-signal vs full-signal"). The register and the module docstring (line 20) say one; the run shows two |
| confirmed 2 | null harness has positive and negative controls and depends on NumPy | REPRODUCED | `null-harness/null_harness.py` line 47 `import numpy as np` at module scope; README lines 7-8 name both controls; with numpy 2.5.3 present the module runs, exit 0. A run without numpy was not made |
| confirmed 3 | frame-location harness frozen before cases; no results yet | order RECORDED only; no-results STATEMENT PRESENT, underlying claim NOT CHECKED | R03 and F07 above |
| confirmed 4 | M01 rules give different counts; one classification does not reproduce a key outcome | REPRODUCED | R01 (0 / 33 / 47 / 52) and R02 (T02 value) |
| confirmed 5 | review folder holds competing homes and unresolved cross-runs | NOT CHECKABLE as worded; one part OBSERVED | the register names no path. `studies/review/` holds two stripped copies of `MULTI_HOME_REGISTER.json` and one of `concept_map.json`, and three of its files contain "crossrun" or "cross-run". `ledger/reviews/` is a second folder the words could mean. "intentionally" and "unresolved" were not tested |
| confirmed 6 | META-PROTOCOL forbids deleting duplicates or dead ends | DIFFERS as worded | `META-PROTOCOL.md` has no line with "duplicat"; "dead end" occurs once (line 466), about a gap that points nowhere, not about deletion. Nearest text, lines 136-138: an observed-but-unvalidated thing "does not get deleted because it hasn't been validated yet". Search was by those terms only; a rule in other words would be missed |
| risk A | models import unrelated earlier topics | NOT RUN | needs model runs and a scoring rule; the register fixes neither |
| risk B | models summarize away preserved uncertainty | NOT RUN | same reason |
| risk C | fixtures taken for executed experiments | risk NOT RUN; premise OBSERVED | `frame-location-benchmark/runs/` holds constructed fixtures and the README (lines 11, 107) says they are not a result. No reader was tested |
| risk D | exit code 1 read as failure | risk NOT TESTED; premise OBSERVED | as in the dated addition. PROPOSED: document exit codes in the docstring of `blind-reader-void12/studies/instrument/validate.py`. The code is not changed here |
| risk E | generated documents edited directly | risk NOT RUN; premise OBSERVED for four files | `reasoning-gate/GUARDS.md`, `GAP_INDEX.md`, `CONCEPT_MAP.md` and `COLLISIONS.md` each say on line 3 or 4 that they are generated and name the generator. Other generated files were not listed |

R05, fields per filed reading (`blind-reader-void12/readings/`). Each cell
is read from the file named in the column head or computed now; nothing is
filled from memory. Model column: the folder gives a reader label, and for
three readings a family but no model; the label is copied, not checked.

| reading (folder) | family (INDEPENDENCE_LEDGER.md) | first commit of folder | exposure P K R I O (ledger) | packet (m01_records.json) | condition | execution date | input hash | output sha256 (response.json, computed now, first 16) | level (ledger) |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-18_pilot-A | Claude | `460805a0` | y n ? n n | not in M01 | not in M01 | NOT RECORDED | zip `6a7f7df8...f163` (RUN_NOTES) | `a1965988cb0a2275` | L1 |
| 2026-11-18_pilot-B | Claude | `460805a0` | y n ? n n | not in M01 | not in M01 | NOT RECORDED | zip `b19ec02c...e61c` (RUN_NOTES) | `5a1bc4961a00481c` | L1 |
| 2026-11-18_claude-fresh-1 | Claude | `dab5b856` | y ? ? ? ? | not in M01 | not in M01 | NOT RECORDED | NOT RECORDED here (RUN_NOTES not read past its packet line) | `f2ca48909b7677d3` | L0 cap |
| 2026-11-18_claude-v2-A | Claude | `13110b97` | y ? ? ? ? | v2, variant A, `94836e79...4a63` | D0 | NOT RECORDED | `94836e79...4a63` | `c86f2211d110ec9b` | L0 cap |
| 2026-11-19_kimi-v2-A | Kimi | `bfd2c467` | y n ? n ? | v2, variant A, `94836e79...4a63` | D0 | NOT RECORDED | `94836e79...4a63` | `fda486e33078b366` | L2 |
| 2026-11-19_gpt6-v2 | GPT | `2676b433` | y n y ? ? | v2, variant null, sha256 null | D0 | NOT RECORDED | NOT RECORDED (null in the record) | `88cd9a447cc67baf` | L2 |

Notes on the R05 table:
- Execution date: the folder names carry a date; whether it is the run date
  or the filing date was not read from the files, so the field is NOT
  RECORDED.
- "Exact source commit" is given as the commit that first added the folder;
  the commit of the packet each reader was sent is not in the table.
- Independent reproduction status is the ledger's level, copied. The ledger
  is the work of a Claude Code session and says so. No level was recomputed.
- Results outside `readings/` (M02: none coded; frame-location: none) have
  no rows.
- "?" in the exposure column is the ledger's own mark for void.

### C6. Not done in this section

- The check of PR #332 and the CI reads asked for in the same order are
  reported to the owner and not filed (the order says no commit for them).
- No code, fixture, key, record or generated output was changed.

## Correction section 2, 2026-11-24 UTC (owner's order 336-F2)

Nothing above this heading is changed. Tags added here: FROZEN, NOT FROZEN.

### D1. Confirmed items 1 and 6 against the file history (order item 3)

The register names no commit. Its date is 2026-11-23. Main on that date was
`9a118df` (last commit 2026-11-20).

| item | file | last change before the register | state at the register's date | verdict |
|---|---|---|---|---|
| confirmed 1 | `tools/known_answer.py` | `02dd4c7d`, 2026-11-11 | two `pinned_failing` entries (lines 1102 and 1213: "half-signal vs full-signal", "matched set"); docstring line 20 says "one of the seeds is a CURRENTLY FAILING case". Both pins and that docstring sentence first appear in one commit, `53031dff`, 2026-08-24 | register miscount (it says one; the code held two on its date). The file's own docstring carries the same "one" |
| confirmed 6 | `META-PROTOCOL.md` | `2c35d23c`, 2026-08-31 | no line about deleting duplicates or dead ends under these search terms: delet, duplicat, dead end, remov, discard, erase, prune, tidy, clean up, redundan, copies. Nearest: lines 136-138 | repo did not change after the register; the register's wording is not in the file under those terms. Of the order's three verdicts the nearest is "register miscount" (a register-side difference, not a count). The file was searched by term and not read in full, so a rule in other words would be missed |

For item 6 of the catch matrix: DIFFERS = 2 (confirmed 1, confirmed 6).

### D2. F10 under the owner's rule (order item 4)

Rule, PROPOSED, owner-ordered 2026-11-23: "frozen = artifact sha256 or
commit recorded in a prereg/freeze file committed before the first commit
containing its results; else NOT FROZEN; freeze file with no pin -> NOT
CHECKABLE." Run over the 4 files named in C5 and the files they reference.
F10 status moves from NOT RUN to RUN under this rule for these 4 files only;
it is still not a repository-wide inventory.

One choice the rule leaves open, made here and marked: which results belong
to which pinned artifact. Used: v1 packet, key and scorer -> the first v1
reading folder; v2 key and builder -> the first v2 reading folder; amendment
1 files -> the first reading filed after it; M01 criteria and schema ->
`studies/m01_records.json`; M01 extension and M02 files -> none exist.
"Before" is tested with `git merge-base --is-ancestor` (pin commit is an
ancestor of, and not the same as, the results commit). "current file" is the
sha256 of the file on this branch against the pin.

| freeze file | pins | status |
|---|---|---|
| `blind-reader-void12/PREREG.md` | 34 distinct sha256 pins | per artifact, table below |
| `frame-location-benchmark/FREEZE_LOG.md` | none (no sha256, no commit) | NOT CHECKABLE |
| `relational-playground/experiments/model_comparison/forest_fire_regime/PREREG.md` | none | NOT CHECKABLE |
| `kernel_stake/PREREGISTRATION.md` | 8 commit ids of an outside repository (kernel tags v4.14 to v6.12, lines 60-67) | FROZEN by the rule: file committed at `4147046e`, an ancestor of `025d12ea` where `RESULTS.md` and `measures.json` first appear. The 8 ids were not checked against the outside repository: NOT RECORDED |

`blind-reader-void12/PREREG.md`, per artifact (paths relative to
`blind-reader-void12/`; sha256 shown to 12 characters):

| artifact | sha256 pin | group | pin first in PREREG.md at | first results commit | current file | status |
|---|---|---|---|---|---|---|
| `reader_packet/READER_BRIEF.md` | `6f33a9528e47` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/response_template.json` | `e54ee502cfbc` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/sources/Simulators/combined-playground/cplay/axes.py` | `0e40b7e5ce87` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/sources/Simulators/combined-playground/cplay/closure.py` | `827d681c8b08` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/sources/Simulators/combined-playground/cplay/tokens.py` | `8c43890bf90a` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/sources/Simulators/playground-crossrun/COMBINED_SPEC.lines_1-390.md` | `72bbd9774991` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/sources/formula-audit/numcheck/check.py` | `f6df0dc196f5` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/sources/thermodynamic-accountability-framework/calibration/expiry_register.py` | `ddaf2cc5b653` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/sources/thermodynamic-accountability-framework/calibration/unified_audit.py` | `fcccb9af8d8e` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/sources/thermodynamic-accountability-framework/docs/glossary.md` | `412ed3abf4c2` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/terms.json` | `467f4fe6769e` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `reader_packet/PACKET_MANIFEST.json` | `c7327f9d3d52` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `scoring/key.json` | `5c1a6caba4e3` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `scoring/score.py` | `3f7b10c8b831` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `scoring/test_score.py` | `7754586a1862` | v1 | `bf89b233` | 460805a0 | DIFFERS since `003deae3` | FROZEN by the rule as worded; file is not the pinned bytes |
| `build/make_packet_and_key.py` | `e70ad6dc4981` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `combined-playground/cplay/vocab_branches.py` (the first reading) | `30fe580e4e8b` | v1 | `bf89b233` | 460805a0 | match | FROZEN |
| `variants/READER_BRIEF.variant_B.md` | `cdaca465b8b1` | v1 | `003deae3` | 460805a0 | match | FROZEN |
| `build/make_packet_v2.py` | `37e0dd55c762` | v2 | `dab5b856` | 13110b97 | match | FROZEN |
| `KEY_V2_AMENDMENT_1.md` | `2f881227942f` | a1 | `926fd504` | bfd2c467 | match | FROZEN |
| `scoring/key_v2_a1.json` | `a7309046319e` | a1 | `926fd504` | bfd2c467 | match | FROZEN |
| `scoring/score_v2.py` | `22055614cac9` | a1 | `926fd504` | bfd2c467 | match | FROZEN |
| `scoring/key_v2.json` | `c88a910a03a6` | v2 | `dab5b856` | 13110b97 | match | FROZEN |
| `build/make_key_a1.py` | `5c01a8fa50e3` | a1 | `926fd504` | bfd2c467 | match | FROZEN |
| `studies/M01_CRITERIA.md` | `f194ecbcd991` | m01 | `67b8e9d2` | 3d3ac5fc | match | FROZEN |
| `studies/M01_SCHEMA.json` | `2e63b53a5085` | m01 | `67b8e9d2` | 3d3ac5fc | match | FROZEN |
| `studies/M01_EXTENSION.md` | `9710be2a9a77` | ext | `66d4f284` | none | match | FROZEN (no results yet) |
| `studies/M02_CRITERIA.md` | `bddfc32b0731` | ext | `66d4f284` | none | match | FROZEN (no results yet) |
| `studies/M02_SCHEMA.json` | `e2e80ba2e7d6` | ext | `66d4f284` | none | match | FROZEN (no results yet) |
| `studies/instructions/M01_D1.md` | `055b0a30028a` | ext | `66d4f284` | none | match | FROZEN (no results yet) |
| `studies/instructions/M02_D1.md` | `4769714245b6` | ext | `66d4f284` | none | match | FROZEN (no results yet) |
| `studies/instructions/M02_D2.md` | `6787145f8bbf` | ext | `66d4f284` | none | match | FROZEN (no results yet) |
| `studies/instructions/M02_D3.md` | `cce4d69c553e` | ext | `66d4f284` | none | match | FROZEN (no results yet) |
| `studies/as_received/gpt6_g01_g02_instrumentation.patch` | `ad346f60225e` | ext | `66d4f284` | none | match | FROZEN (no results yet) |

Counts: 34 artifacts; 26 FROZEN; 8 FROZEN with no results yet (the rule's
"before the first commit containing its results" holds with nothing to
precede); 0 NOT FROZEN. 33 current files match their pin; 1 does not.

Notes:
- `scoring/test_score.py`: the pin was recorded at `bf89b233`; the file was
  changed at `003deae3` (before the first reading, `460805a0`) and the pin in
  `PREREG.md` still gives the earlier bytes. Whether `PREREG.md` records that
  change in words was not read: NOT RECORDED.
- Amendment 1: its pin commit `926fd504` precedes the first later reading
  (`bfd2c467`). One earlier reading, claude-v2-A, was also scored under it
  (`score_a1.json` first at `356a77ac`, after the pin); the reading itself
  predates the pin. `PREREG.md` says the same in its amendment section.
- Hashes that `PREREG.md` states twice are one row.
- Not run: files referenced without a pin (for example the reader packet
  zips named in the RUN_NOTES files).

### D3. Check section addition (order item 5)

"REGISTER_AS_RECEIVED.md received text kept non-ASCII as received; declared exception."

### D4. Catch matrix row (order item 6)

NOT RECORDED: no file named or described as a review2 catch matrix is on
this branch. Searched tracked file names for "catch" and "matrix" and
tracked text for "catch matrix". The row as ordered, not filed anywhere:
reviewer GPT; register 2026-11-23; confirmed items 6; differs 2; not
checkable 1; channel FETCH/HYGIENE; volume: thin.
Path of the only catch matrix found: repository Geometric-manifold-, branch
`claude/deviations-planted-defect-spec` (PR #38, not merged),
`docs/research/deviations/DEVIATIONS_2026-11-21.md`. It is not in this
repository and was not edited.

## Correction section 3, 2026-11-24 UTC (owner's order 336-F3)

Nothing above this heading is changed. Tag added here: INHERITED (the
reviewer's claim matches an error already in the artifact's own text).

### E1. scoring/test_score.py, pinned bytes against current bytes

Deviation recorded: `blind-reader-void12/PREREG.md` line 76 pins
`scoring/test_score.py` at sha256 `7754586a1862...` (the bytes at
`bf89b233`). The file was changed at `003deae3` and is now sha256
`71ce47da1ff5...`. The pin is stale. `PREREG.md` is a freeze file and is
not edited. The section `003deae3` added to `PREREG.md` pins variant B's
brief and does not mention `test_score.py` [OBSERVED: the added lines were
read].

Full diff, `git diff bf89b233 003deae3 -- scoring/test_score.py`:

```diff
diff --git a/blind-reader-void12/scoring/test_score.py b/blind-reader-void12/scoring/test_score.py
index 5b4f498b..c1c8b8bd 100644
--- a/blind-reader-void12/scoring/test_score.py
+++ b/blind-reader-void12/scoring/test_score.py
@@ -71,6 +71,18 @@ class KeyAndPacket(unittest.TestCase):
                 for w in preds | {"vocab_branches", "second reader", "second-reader", "void-12", "blind"}:
                     self.assertNotIn(w.lower(), low, "%s contains %r" % (rel, w))
 
+    def test_variant_brief_has_no_key_vocabulary_and_differs_only_by_the_clause(self):
+        with open(os.path.join(ROOT, "variants", "READER_BRIEF.variant_B.md"), encoding="utf-8") as fh:
+            b = fh.read()
+        with open(os.path.join(ROOT, "reader_packet", "READER_BRIEF.md"), encoding="utf-8") as fh:
+            a = fh.read()
+        self.assertEqual(a.replace(", even if the second system attaches different extra fields or detail", ""), b)
+        for w in ("MAPS", "PARTIAL", "HOMONYM", "SPLIT"):
+            self.assertIsNone(re.search(r"\b%s\b" % w, b))
+        low = b.lower()
+        for w in {t["predicate"] for t in KEY["terms"].values()} | {"vocab_branches", "void-12", "second reader"}:
+            self.assertNotIn(w.lower(), low)
+
     def test_terms_json_has_only_neutral_fields(self):
         t = S.load(os.path.join(ROOT, "reader_packet", "terms.json"))["terms"]
         self.assertEqual(len(t), 15)
```

The change adds one test and removes nothing. `test_score.py` is the test
file for the scorer; `scoring/score.py` does not import it (0 occurrences
of the name in `score.py`), and `score.py` matches its own pin. So a
reading's score cannot depend on which version of `test_score.py` is
present [DERIVED]. Both versions were still run, in a scratch copy of the
tree at this branch's HEAD, and `score.py` was rerun on every filed reading
[OBSERVED]:

| run | result |
|---|---|
| `python3 -B -m unittest test_score`, pinned bytes | 15 tests, OK |
| `python3 -B -m unittest test_score`, current bytes | 16 tests, OK |

| reading | score with pinned test file present | score with current test file present | differs | against filed `score.txt` |
|---|---|---|---|---|
| 2026-11-18_pilot-A | 7 of 8 declared pairs agree | same output | no | byte-identical |
| 2026-11-18_pilot-B | 7 of 8 declared pairs agree | same output | no | byte-identical |
| 2026-11-18_claude-fresh-1 | 5 of 8 declared pairs agree | same output | no | byte-identical |
| 2026-11-18_claude-v2-A | NOT SCORED by `score.py` (exit 2, fails v1 validation) | same | no | filed score is from `score_v2.py` |
| 2026-11-19_kimi-v2-A | NOT SCORED by `score.py` (exit 2) | same | no | filed score is from `score_v2.py` |
| 2026-11-19_gpt6-v2 | NOT SCORED by `score.py` (exit 2) | same | no | filed score is from `score_v2.py` |

`score.py` was run once per reading, not once per test-file version: the
two columns are equal because the scorer is one file in both cases. The v2
scorer (`score_v2.py`, tested by `test_score_v2.py`) is outside this pin
and was not rerun.

### E2. tools/known_answer.py, pin search

Searched: every tracked file of this branch and of the 22 other
repositories checked out in the session (working-tree HEADs, as found), for the sha256 or git blob id of
every version of `tools/known_answer.py` in this repository's history (156
values); and files named like PREREG, FREEZE, commitment, SHA256SUMS,
PROVENANCE, TOOL_CARDS, PIN or MANIFEST for the file's name.

| where | what it records | kind |
|---|---|---|
| repository method-layer, `reasoning-layer/layer3/inventory_update_metadata.json` lines 872-878 | path `tools/known_answer.py`, sha256 `17b5b3a022fd...`, 3091 lines, 151591 bytes, date 2026-10-14, last_commit `198937ec` | a recorded sha256 of an earlier version, in an inventory file |
| this repository, `archive/*/PROVENANCE.md` (6 files) | name the file as a pick rule; no hash | not a pin |
| this repository, `tools/TOOL_CARDS.json` | no entry for the file | none |
| PREREG, FREEZE or commitment files, any repository | none | none |

One sha256 of the file is recorded in another repository, so the order's
"pinned anywhere" branch is taken and nothing is changed. The recorded
value is not the current file's (current sha256 `5d65201d4326...`); the
file has changed since that inventory was written.

PROPOSED: "docstring says one; code holds two" (`tools/known_answer.py`
line 20 against lines 1102 and 1213). No edit made, no branch, no PR.

### E3. Confirmed 6, META-PROTOCOL.md read in full

Lines read: 673 of 673. Verdict: not present. No line forbids deleting
duplicates or dead ends, in those words or others. The lines nearest to
the claim:

- lines 136-138: "These never merge on their own. An observed-but-unvalidated
  thing does not get promoted to validated because it's been sitting around,
  and it does not get deleted because it hasn't been validated yet." (about
  unvalidated observations, not duplicates)
- lines 465-466: "A gap that closes and points nowhere is a dead end you
  built yourself." (about gap entries; says nothing on deletion)
- line 610: "nothing is marked failed, rejected, or wrong" (about marking)

D1's verdict for confirmed 6 stands and loses its caveat about term search.
Confirmed 1 is reclassed INHERITED: the register's "one" matches the
file's docstring and not its code. Catch matrix counts: differs 1
(confirmed 6), inherited 1 (confirmed 1).

### E4. kernel_stake pins against the kernel repository

`https://github.com/torvalds/linux` was reachable (`git ls-remote`, then a
depth-1 fetch of the 8 tags without file contents). The kernel.org host was
refused by the session proxy (CONNECT 403).

| tag | id in PREREGISTRATION.md | tag id on the remote (first 12) | match | paths resolving at the tag |
|---|---|---|---|---|
| v4.14 | e3d97e8db5c4 | e3d97e8db5c4 | yes | 36 of 36 |
| v4.19 | 2241b8bcf2b5 | 2241b8bcf2b5 | yes | 36 of 36 |
| v5.4 | 6e815efe19a9 | 6e815efe19a9 | yes | 36 of 36 |
| v5.10 | 3f995f8e0b54 | 3f995f8e0b54 | yes | 36 of 36 |
| v5.15 | dc7089468610 | dc7089468610 | yes | 36 of 36 |
| v6.1 | 7614896350aa | 7614896350aa | yes | 36 of 36 |
| v6.6 | 5260836abb70 | 5260836abb70 | yes | 36 of 36 |
| v6.12 | 06090c9b622a | 06090c9b622a | yes | 36 of 36 |

- The 8 ids are the ids of the annotated tag objects, not of the commits
  the tags point at (for v4.14 the commit is `bebc6082da0a`). The file's
  column is headed "sha" and does not say which.
- Paths: the 36 directories of section 3 of the file (15 + 12 + 9), each a
  tree at every tag. The dropped candidate `init/` was not counted.
- Tag dates and the MAINTAINERS coverage the file states were not checked.
- D2's row for this file: "ids not checked" no longer holds; they were
  checked here.

## Correction section 4, 2026-11-24 UTC (owner's order 336-F4)

Appended; every line above is unchanged. The file before this section was
41920 bytes, sha256
`ba87ce83bbd39619de2f51a1bda1441804cee71e00a53b1ca6c9621250c5a61d`.

### G1. Owner decision on the known_answer.py inventory entry (verbatim)

"An inventory entry recording an earlier version's hash is a state
 record, not a pin; it does not hold the current bytes. known_answer.py
 is not pinned. Owner decision 2026-11-23."

This closes the open point of E2. The docstring count named in confirmed 4
is changed on a separate branch, `claude/known-answer-docstring-count`
(commit `918bbcca`), not in this pull request.

### G2. score_v2.py: pin, current bytes, reruns

- Pinned: yes. `blind-reader-void12/PREREG.md` line 126 lists
  `scoring/score_v2.py` with sha256
  `22055614cac916e0970c7a8061bb305099289e8f48c647601c3048a0d347c426`. It is
  one of the 34 pins of D2.
- Current bytes: sha256 of the file at this branch's head is the same value.
  PASS.
- Keys used: `scoring/key_v2.json`
  (`c88a910a03a6456900efabd130c57a19f1a0133c9566ebce34ae0b6e813b18d1`,
  PREREG.md lines 112 and 127) and `scoring/key_v2_a1.json`
  (`a7309046319e62210018dd3c48c88174abf63282200c8bb0a40a1c698b5d8ba4`,
  PREREG.md line 125). Both current files match.
- Rerun: `python3 -B scoring/score_v2.py readings/<r>/response.json --key
  scoring/<key> --json <out>`, output written outside the tree, compared
  with `cmp` against the filed files. sha256 columns are the first 12 hex
  digits of the filed file.

| reading | key | exit | text vs filed | json vs filed | filed .txt | filed .json |
|---|---|---|---|---|---|---|
| 2026-11-18_claude-v2-A | key_v2.json | 0 | identical (score.txt) | identical (score.json) | bcf18041b3ab | 7b461684387f |
| 2026-11-18_claude-v2-A | key_v2_a1.json | 0 | identical (score_a1.txt) | identical (score_a1.json) | 33d0e92bec9e | 3f41775256e1 |
| 2026-11-19_kimi-v2-A | key_v2.json | 0 | identical (score.txt) | identical (score.json) | 8acf8e64d564 | 20a70f98f3c2 |
| 2026-11-19_kimi-v2-A | key_v2_a1.json | 0 | identical (score_a1.txt) | identical (score_a1.json) | 2310c2d65c2b | 327409187277 |
| 2026-11-19_gpt6-v2 | key_v2.json | 0 | identical (score.txt) | identical (score.json) | 548f73141b8b | 20f07b4c5bdd |
| 2026-11-19_gpt6-v2 | key_v2_a1.json | 0 | identical (score_a1.txt) | identical (score_a1.json) | e2785fd8020d | 15a0b7371d7d |

12 of 12 files identical byte for byte. No deviation is recorded for
score_v2.py. NOT CHECKED: whether the filed scores were produced by these
bytes at the time of filing; the rerun shows only that the current pinned
bytes produce them now.

### G3. kernel_stake PREREGISTRATION.md, 'sha' column (verbatim)

"PREREGISTRATION.md 'sha' column holds annotated tag object ids, not commit
 ids; header does not say which. Not edited (freeze file)."

Source: E4 of this file.

## Provenance (section 4)

Co-authored, Kavik + Claude, 2026-11-24 UTC. G1 and G3 quote the owner's
order 336-F4. G2 was run in this session on branch
`claude/gpt-register-reproduction`. License CC0-1.0. Observer slots: null.
