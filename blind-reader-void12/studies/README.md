# studies

Instrumentation studies on the readings. Each study's criteria and schema are pinned in `PREREG.md` before its coding exists. Nothing here changes the brief, the packet, a key, a score, a status or a reading.

| study | files | status |
|---|---|---|
| M01, `slots_specific` membership | `M01_CRITERIA.md`, `M01_SCHEMA.json` (pinned 2026-11-19, commit `67b8e9d`), `m01_code.py`, `m01_records.json`, `m01_report.txt` | three filed v2 readings coded; descriptive only |
| M01 extension (D1 condition, parallel / sequential arms, fixtures) | `M01_EXTENSION.md`, `instructions/M01_D1.md` (pinned `66d4f28`) | designed; no new reading yet |
| M02, `slots_carried` scope and traversal | `M02_CRITERIA.md`, `M02_SCHEMA.json`, `instructions/M02_D1.md`..`M02_D3.md` (pinned `66d4f28`) | designed; the three filed readings not yet coded |
| instrument | `instrument/validate.py`, `instrument/fixtures/`, `instrument/test_instrument.py` | structural validator for M01 and M02; never rejects a reader's choice for disagreeing with key a1; fixtures use neutral names and are checked by rule |
| arms | `instrument/arms.py`, `instrument/arms_report.txt` | the GPT-6 proposal's validator rule kept as an analysis arm (`validate.py --arm=rule_on`; default `rule_off`), and TAG computed under presence and applicability on every record with the divergence list; nothing chosen. Lives here because `scoring/score_v2.py` is hash-pinned |
| as received | `as_received/gpt6_g01_g02_instrumentation.patch` | the GPT-6 reader's proposal these designs come from, unedited |

Re-run: `python3 -m unittest test_instrument` (in `instrument/`); `python3 m01_code.py` (writes both outputs); `python3 m01_code.py --check` (fails if they would change). Stdlib only; imports the packet's cplay code without writing bytecode; parses numcheck and TAF text.

## M01: what the coding shows (descriptive; the coder had seen all three readings)

Numbers are from `m01_report.txt`; 37 catalog fields, 111 records.

1. **Exclusive raw fields (cell A) are where readers agree**: 19 fields, listed by Claude 19, Kimi 19, GPT-6 17, key a1 18. Disagreement is not spread evenly; it sits in the other cells.
2. **Computed fields (B)**: 5 fields; Claude 5, Kimi 5, GPT-6 3, key a1 0. All three readers list `covers_effect`, `typed`, `untyped`; the two readers who say why call `covers_effect` derived and list it anyway (READER_STATED). So the readers' membership rule does not use the key's INDEPENDENCE test; that is stated by them, not inferred.
3. **Shared and nested fields (C) separate the readers most**: 9 fields; Claude 7, Kimi 5, GPT-6 1, key a1 0. The readers differ here in how far they treat "tied to this verdict" as enough.
4. **Same list, different reasons**: 6 fields listed by all three carry stated reasons of different kinds (T05's five parameters: "parameter" for one reader, "stored field" for another; T08 `inputs`: "documented" for two, "parameter" for one). A lower bound, since a reader's silence is not coded as a reason.
5. **Readers agree and key a1 does not** on five fields: `covers_effect`, `typed`, `untyped` (computed, cell B), `inputs` (a crash() parameter, cells G E C), and `void_reason`.

**`void_reason` is the one worth the owner's attention.** Coded by this study's three-way scope, it is SHARED by presence (a `_blank` key on every record, None off the VOID paths) but ALL_EXCLUSIVE by applicability (set on every VOID path and on no other). Key a1's TAG test reads presence, so it drops the field; all three readers read applicability and keep it. This is Kimi's branch C11 (present vs applicable vs required) found in the key itself. It is an observation from one coder, not a finding that the key is wrong; whether TAG should read presence or applicability is a definition, and the owner's to make.

## Limits

One coder, the same model family as one reader. The numcheck applicability values are CODER_INFERRED from the code's branches (numcheck cannot run from the packet), marked `[coder]` in the report. The case rule is applied as fixed in the criteria; one of its effects is that a parameter stored under no field (scopes all NONE) also lands in cell C. Three readings, one each.
