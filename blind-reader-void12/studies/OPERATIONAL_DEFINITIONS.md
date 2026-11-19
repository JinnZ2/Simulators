# Operational definitions: one table (2026-11-19)

The table asked for in the owner's message of 2026-11-19 (`as_received/mode_and_authority_2026-11-19.md`, item 3). Each rule is quoted from the file that defines it. A rule no file defines is marked **OPEN**, with its gap and the stage that can decide it (`../MODE_SEQUENCE.md`). Nothing here changes a definition, the brief, D0, a key or a score. Checked at Simulators main `3b963e7`.

Three claims are kept apart (message item 5):
- **ambiguous:** the source admits more than one reading.
- **revised:** a document now states a rule.
- **correct:** the revised reading is right.

No row here asserts the third claim.

| concept | decision rule as written | where | boundary cases and what the files say | ambiguous / revised / correct |
|---|---|---|---|---|
| TAG | "defined on every instance of the term and on no instance of any other term" | `KEY_V2_AMENDMENT_1.md` §2 | "Defined" means a declared parameter, a key present, or a field a rule requires: presence OR requirement (`instrument/validate.py` `tag_by`, comment on `a1_defined`). **No instances:** UNRESOLVED (`validate.py`). **Documented only:** UNRESOLVED in `validate.py`, but **NO** in the fixture rule (`instrument/test_instrument.py` `tag()`; fixture M01-KA-05). The two instruments disagree. **Presence vs applicability:** both computed (`instrument/arms_report.txt`), neither adopted. | ambiguous: yes (G1). revised: no. correct: not claimed. Stage: SUGGEST |
| INDEPENDENCE | "an independent input of the term's record, that is, not computed from other candidate fields (it is passed in or recorded raw)" | `KEY_V2_AMENDMENT_1.md` §2 | **Derived field:** not independent. **Constructor-only parameter (not stored):** no rule. M01 codes it PARAMETER_ONLY, cell E (`M01_CRITERIA.md` §3), and key a1 excludes T08's `inputs` by the Q1 ruling, not by a rule. **Renamed parameter:** no rule. **Message built from an exception:** no rule (CF03, CF04). | ambiguous: yes (CF03, CF04, CF09, CF10). revised: no. Stage: SUGGEST |
| Populated | "populated (non-None, non-zero)" | `M01_SCHEMA.json`, note on `applicability_scope` | **`0`:** unpopulated by the schema note, but **populated** in the fixture test, which uses `is not None` only (`test_instrument.py`, `test_m01_ka07_keeps_the_alternative_reading`). The two disagree. **`False`, empty collections, `"void"`:** not stated anywhere. | ambiguous: yes (KC03; G1). revised: no. Stage: SUGGEST |
| Own record | D0: no rule. M02 D1 only: "the record whose status, kind, verdict or state value is this term" | `instructions/M02_D1.md` | **T04, T06, T12, T15:** a class-typed term, a nested token, two record types and a record-valued concept. The D1 rule does not settle them (KC06-KC09, GR03-GR06). **Two records both satisfying it:** no rule. | ambiguous: yes (G2). revised: in D1 only, which is a condition, not D0. Stage: SUGGEST |
| Reporting path | D0: no rule. M02 D2 only: "every record that the source builds, returns or documents on the path that reports this term, including a record built beside the term's own record" | `instructions/M02_D2.md` | **Start and stop:** not stated. **Adjacent record:** included under D2. **Wrapper:** not stated in D2. The fixture rule leaves wrappers out under ALL_REPORTING_PATH_RECORDS and takes the first wrapper only under FIRST_WRAPPER_ONLY (`test_instrument.py` `carried()`; KC11). **Outer aggregate report:** not stated (KC10, GR08, GR18). | ambiguous: yes (G3). revised: in D2 only. Stage: SUGGEST |
| Nested record | D0: no rule. D1, D2: "name that field and do not open it" | `instructions/M02_D1.md`, `M02_D2.md` | **Opened:** only under the fixture rule OPEN, which opens one level, the records counted before opening (`test_instrument.py` `carried()`). **Multiple nesting levels:** not stated in any criteria file. | ambiguous: yes (G3). revised: in D1 and D2 only. Stage: SUGGEST |

## Disagreements between files found while building this table

Each is recorded, not resolved:

1. Documented-only TAG: UNRESOLVED (`validate.py`) vs NO (`test_instrument.py`, KA-05).
2. Populated: non-None and non-zero (`M01_SCHEMA.json`) vs non-None (`test_instrument.py`).

Both come from instruments built in the Claude Code session. They are added to `OPEN_ROWS.md` as rows CF18 and CF19, which belong to that session's confusion record and are filed there in a dated section.
