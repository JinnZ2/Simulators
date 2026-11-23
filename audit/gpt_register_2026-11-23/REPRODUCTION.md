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
