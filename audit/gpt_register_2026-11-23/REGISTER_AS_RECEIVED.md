<!-- SPDX-License-Identifier: CC0-1.0 -->
# REGISTER AS RECEIVED - GPT audit register of 2026-11-23

License: CC0-1.0 for this header. As received, unedited. Filed 2026-11-24 UTC
(received in the filing session 2026-11-23 UTC). Observer slots: null.

## Provenance

- Source: the owner's paste into the filing session, in one message that
  began with the label "GPT:", then held a Phase C work order, then this
  text. Only this text is filed here.
- The text below starts at the word "SIMULATORS" and ends at "End of block."
  It holds two blocks as pasted: the register, then "Simulators Repository
  Confusion Risks for First-Time AI Readers".
- Bytes: 10863, UTF-8, taken from the session transcript by script, not
  retyped. sha256 of those bytes alone:
  4e4502487af097a300c0c632fb882c84ccf25e6502ae179bf9e0aad191d2dad0
- Not ASCII, as received: it holds U+2028 line separators, tabs, an em dash,
  curly quotes and bullet characters. None was changed. Typing slips in it
  (for example "ru ules") are the paste's own.
- Not known here: whether the paste equals what the GPT session produced.
  NOT RECORDED.
- One newline is added after the last received byte so the file ends with
  one. Everything after the next heading line and its blank line is the
  received text.

## Text as received

SIMULATORS — FROZEN EXPERIMENT AUDIT REGISTER
Date: November 23, 2026 Repository: https://github.com/JinnZ2/Simulators Audit mode: Read-only Status: Preliminary verification; independent reproduction pending Modification policy: Preserve frozen baselines, original readings, failed specimens, and unresolved disagreements.
1. Purpose
Inventory frozen experimental artifacts, identify their source commits and recorded results, and distinguish demonstrated behavior from claims awaiting verification.
Each experiment is examined for:
	•	Frozen specification and commit reference
	•	Inputs, fixtures, and expected outputs
	•	Validation and scoring procedures
	•	Recorded execution evidence
	•	Known discrepancies
	•	Independence of verification
	•	Outstanding tests and unresolved conditions
A frozen artifact is not automatically a validated experiment. Reproducibility requires checking that the declared inputs and procedures actually produce the recorded outputs.
2. Frozen experiment inventory
A. Blind-reader VOID-12
Location: blind-reader-void12/
Primary file: PREREG.md
Purpose: Determine whether independent readers group the same 15 technical terms consistently.
Frozen elements:
	•	Preregistered reading protocol
	•	Reader packet and source hashes
	•	Eight declared comparison pairs
	•	Scoring criteria
	•	Reader-blindness attestation rules
	•	Baseline and amendment boundaries
Recorded evidence: Multiple reader responses, including three D0 readings coded for the M01 study.
Outstanding verification: Independently reproduce scoring, validate source hashes, and assess reader independence.
Status: Recorded readings available; independent reproduction pending.
B. M01 — G01 instrumentation adaptation
Location: blind-reader-void12/studies/
Primary files:
	•	M01_CRITERIA.md
	•	M01_EXTENSION.md
	•	M01_SCHEMA.json
	•	m01_records.json
	•	m01_report.txt
Pinned reference: 67b8e9d for original criteria; 66d4f28 for extension materials.
Question: Which fields does a reader classify as specifically belonging to a term?
Experimental conditions:
	•	D0: Original reader packet
	•	D1: Additional TAG and INDEPENDENCE instructions
	•	Parallel and sequential reader arms
Recorded outcome: Three D0 readings coded. No new D1 reading recorded in the inspected study index.
Status: Descriptive analysis recorded; experimental extension awaiting readings.
C. M02 — G02 instrumentation adaptation
Primary files:
	•	M02_CRITERIA.md
	•	M02_SCHEMA.json
	•	instructions/M02_D1.md
	•	instructions/M02_D2.md
	•	instructions/M02_D3.md
Pinned reference: 66d4f28
Question: Which records are counted in slots_carried, and how far should nested records be traversed?
Experimental conditions:
	•	D0: Original packet
	•	D1: Term’s own record only
	•	D2: Reporting-path records
	•	D3: Reader declares their own interpretation first
Recorded outcome: Design and instrumentation exist. Three existing D0 readings were listed as not yet coded for M02.
Status: Designed; full comparative analysis pending.
D. Frame-location benchmark
Location: frame-location-benchmark/
Primary files:
	•	FREEZE_LOG.md
	•	WORK_ORDER.md
	•	cases.jsonl
	•	validate_cases.py
	•	score.py
Purpose: Test whether a model identifies a mis-posed problem before answering it.
Frozen structure: Four harness files established before the case set.
Recorded case inventory:
	•	40 constructed cases
	•	19 well-posed
	•	21 mis-posed
	•	Eight domains
	•	Seven fault classes
Recorded outcome: Instrument and contamination-check design documented. Repository README explicitly states that model benchmark results have not yet been obtained.
Status: Experimental apparatus available; empirical model evaluation pending.
3. M01 validator discrepancy
Source files:
	•	studies/instrument/arms.py
	•	studies/instrument/validate.py
	•	studies/instrument/arms_report.txt
The repository records the following comparison across 111 records from three readers:
Validator condition	Reported flagged records
Structural validation, rule_off	0
Strict A1 interpretation	33
Presence interpretation	47
Applicability interpretation	52
These counts are repository-reported, not independently reproduced.
The structural validator accepts records that are structurally valid even when reader classifications disagree with the key.
The strict validator additionally requires listed fields to satisfy TAG and INDEPENDENCE conditions.
Interpretation: The difference is partly a change in validation semantics, not necessarily evidence of defective reader responses.
Discrepancy M01-D01: T02 value
The recorded self-check reports one mismatch between the A1-derived TAG/INDEPENDENCE classification and the key:
T02 value
This is a defined investigation target.
Required checks:
	1.	Identify the source definition of T02.
	2.	Establish whether value is an instantiated field, a documented field, or another category.
	3.	Recompute TAG and INDEPENDENCE from the declared rules.
	4.	Compare the computed result with key A1.
	5.	Record whether the mismatch arises from the key, implementation, source interpretation, or an unresolved definition.
Current classification: UNRESOLVED.
No correction should be applied until the discrepancy’s origin is established.
4. Reproduction work order
R01 — Reproduce M01 validator counts
Run the pinned validator against the recorded M01 input.
Compare:
	•	Structural error count
	•	A1 rejection count
	•	Presence rejection count
	•	Applicability rejection count
	•	Per-reader and per-field breakdowns
Acceptance criterion: Recomputed outputs agree exactly with the recorded report, or every difference is logged.
Status: NOT YET INDEPENDENTLY EXECUTED.
R02 — Investigate T02
Reconstruct the T02 value classification from the original source and declared rule.
Acceptance criterion: Every classification step has an evidence reference, and any unresolved interpretation remains explicit.
Status: OPEN.
R03 — Verify frame-location freeze order
Inspect the freeze log, commit chronology, harness files, and case creation history.
Verify:
	•	Harness material predates case construction.
	•	Case prompts are absent from harness material.
	•	Fault targets are not leaked.
	•	Worked corrections do not overlap prohibited fault/domain combinations.
	•	Frozen files match their declared versions.
Acceptance criterion: Recorded chronology and content checks support the claimed freeze, with exceptions separately documented.
Status: DOCUMENTED ORDER; INDEPENDENT VERIFICATION PENDING.
R04 — Execute frame-location controls
Run the case validator and contamination checker in an isolated environment.
Compare actual results against documented requirements.
Do not modify source files to make failing controls pass.
Status: NOT EXECUTED.
R05 — Check provenance and independence
For every result, record:
	•	Model or instrument
	•	Model family
	•	Exact source commit
	•	Prior exposure
	•	Packet version
	•	Experimental condition
	•	Execution date
	•	Input hash
	•	Output hash
	•	Independent reproduction status
A self-check is not an independent verification.
Status: Independence ledger exists; full verification pending.
5. Findings register
ID	Finding	Classification
F01	M01 validator arms report 0, 33, 47, and 52 flagged records	RECORDED
F02	T02 classification mismatch appears in the recorded self-check	RECORDED
F03	M01 has three coded D0 readings	RECORDED
F04	M01 D1 extension has no new reading in inspected index	RECORDED
F05	M02 comparative coding remains outstanding in inspected index	RECORDED
F06	Frame-location benchmark contains 40 constructed cases	RECORDED
F07	Frame-location benchmark reports no completed model evaluation	RECORDED
F08	Exact reproduction of M01 outputs	NOT TESTED
F09	Commit-level freeze chronology and integrity	NOT FULLY VERIFIED
F10	Complete repository-wide frozen artifact inventory	INCOMPLETE
6. Preservation rules
All further work should maintain these boundaries:
	1.	Do not modify frozen baselines or historical experiment records.
	2.	Preserve failed tests and negative controls.
	3.	Preserve competing interpretations independently.
	4.	Distinguish absence of evidence from negative evidence.
	5.	Record assumptions, source provenance, and measurement limits.
	6.	Place new tests and reports outside protected historical artifacts.
	7.	Do not promote self-reported results to independently verified status.
	8.	Do not resolve disagreements by majority vote unless the preregistered protocol explicitly authorizes that rule.
7. Audit conclusion
The inspected repository contains genuine experimental structure: preregistrations, frozen criteria, known-answer fixtures, comparison arms, and explicit unresolved questions.
However, three different states must remain separate:
Recorded: The repository contains an output or claim.
Reproduced: The output has been regenerated from identified inputs and code.
Independently verified: A sufficiently independent process has checked the result and its assumptions.
The current audit establishes several recorded findings but does not yet establish independent reproduction.
Next priority: R01 and R02, followed by R03 and R04.
No repository files were changed during this inspection.
End of preliminary audit register.


Title: Simulators Repository Confusion Risks for First-Time AI Readers, read only, as of November twenty-three, twenty twenty-six. Purpose: list repository features likely to confuse a general AI reader, separating confirmed evidence from untested risks. Confirmed evidence: one, known-answer registry that intentionally retains a failing case as calibration; an AI expecting all tests to pass might “fix” it. Two, null harness with positive and negative controls depends on NumPy, which could be missed or misrun. Three, frame location benchmark freezes harness files before cases and explicitly states no results yet; an AI might infer results from fixtures. Four, M01 validator ru ules produce conflicting counts and one classification does not reproduce a key outcome; an AI might assume one is canonical. Five, review folder intentionally holds competing homes and unresolved cross-runs; an AI might collapse them. Six, META-PROTOCOL forbids deleting duplicates or dead ends; an AI optimizing clarity might violate that. Risks needing testing: A, conversational models may import unrelated earlier topics into current repo analysis. B, models trained to be helpful may summarize away explicitly preserved uncertainty. C, some systems equate generation of fixtures with execution of experiments, risking false claims of results. D: exit code 1 from the validator could be treated as a failure rather than “flags found.” E: generated documents are labeled as outputs; a model may edit them directly instead of changing the generator. End of block.
