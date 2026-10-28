# Relay log

One row per drop from any model. Rows are appended, never edited; a
correction is a new row pointing at the old one. `relay.py` checks the
table (`python3 relay.py`).

Fields:

- `parent`: the row this drop builds on, or `-`.
- `relay`: one of SPEC_ONLY (spec or prose, no code), EXTENDED (kept the
  parent's code and added), CALLED (imported or ran an existing tool
  unchanged), REBUILT (rewrote something that already existed),
  INDEPENDENT (no parent), UNASSESSED.
- `boundary`: claims that touch the outside world (dates, citations,
  outside figures): `traced k/n`, `none`, or UNASSESSED.
- `sha12`: first 12 hex of the landed file's sha256.

| id | landed | model | product | artifact | sha12 | parent | relay | relay_basis | boundary | audit |
|---|---|---|---|---|---|---|---|---|---|---|
| R001 | 2026-10-27 | GPT | ChatGPT | scope-audit-lab/lab_0_1/scope_audit_lab/core.py | e7b30e82e2ef | - | INDEPENDENT | first prototype; spec for the next step was in its final message | none | SAL_016 |
| R002 | 2026-10-27 | Kimi | OK Computer | scope-audit-lab/CONTINUATION_REPORT_V1.md | 4b9dd43d46d5 | R001 | EXTENDED | lab 0.2 core keeps 206 of 209 R001 lines; tests byte-identical | UNASSESSED | SAL_001..010, SAL_015 |
| R003 | 2026-10-27 | Kimi | OK Computer | scope-audit-lab/CONTINUATION_REPORT_V2.md | 67e9a92c7192 | R002 | EXTENDED | lab 0.3 adds experiments.py; 0.2 tree byte-identical inside the drop | UNASSESSED | SAL_011..014 |
| R004 | 2026-10-27 | GPT | ChatGPT | scope-audit-lab/GPT_SPEC_0_2.md | 5178eef79b75 | R001 | SPEC_ONLY | baseline 0.1; does not reference R002 or R003 | none | SAL_017..019 |
| R005 | unrecorded | Perplexity | Perplexity | dependency-survey/RESULT_taxonomy_crossmodel.md | 04691acb5018 | - | INDEPENDENT | blind sort, no repo access | UNASSESSED | DS_011..013 |
| R006 | unrecorded | DeepSeek | DeepSeek | dependency-survey/RESULT_repair_adjacency.md | 7e3e1735b917 | R005 | UNASSESSED | sorts the same 19 records as R005; whether it saw R005 is not recorded | UNASSESSED | DS_014..017 |
