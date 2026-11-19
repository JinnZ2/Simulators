# M01 criteria: slots_specific membership (fixed before coding)

Written 2026-11-19, before `m01_code.py` exists and before any record is coded. Committed and pushed alone, so the commit that adds the coding comes after it in history. Schema: `M01_SCHEMA.json`. Proposed by the GPT-6 reader (the test matrix A-G, the "same list, different reasons" point) and reshaped in the Claude Code session; the owner said "Yes please" to building it.

## 1. What this is, and what it is not

**Descriptive, not a test.** The coder (the Claude Code session) has already seen all three readings' lists and their scores, and has seen key a1 derived. So nothing coded here tests a hypothesis: any pattern it shows was visible to the coder beforehand. Its use is to put the three readings into one table with every value's provenance marked, so that the next readings (taken after this file is fixed) can be coded the same way and compared. A test needs readers this coder has not seen.

**Owner's decisions are not made here.** Nothing in M01 changes the brief, the packet, a key, a score, a status or a reading.

## 2. What is coded

- Readings: the three filed v2 readings, by folder: `2026-11-18_claude-v2-A`, `2026-11-19_kimi-v2-A`, `2026-11-19_gpt6-v2`. Condition D0 (brief unchanged). Packet v2; variant A for the first two, null for GPT-6 (not stated).
- Fields: for each of the 15 terms, every name that any of the three readers or key a1 lists in `slots_specific`, after N1 normalisation (strip one pair of backticks, then of `< >`). One record per (reader, term, field).
- `slots_carried` is not coded here (that is M02, whose schema and criteria come later and separately).

## 3. The source half: how each value is obtained

Every value carries `provenance` SCRIPT_DERIVED or CODER_INFERRED, and `source_basis` says how.

- **cplay terms** (T03 T04 T05 T06 T08 T12 T13 T14): SCRIPT_DERIVED by importing the packet's `cplay` modules (isolated interpreter, no bytecode written into the packet): constructor parameters by `inspect.signature`; stored fields by `vars()` or `_fields`; COMPUTED = stored but not a parameter; requirement by removing the field and seeing whether the constructor raises, for every status that shares the record.
- **TAF terms** (T02 T09 T10 T15): SCRIPT_DERIVED by parsing the packet's `unified_audit.py`, `expiry_register.py` and `glossary.md` (dict-literal keys per coverage kind; the raise handler's section record; `EXPIRY_KEYS`; the notation `ABSENT_AT_SENSITIVITY(<value>)`).
- **numcheck terms** (T01 T07 T11): numcheck cannot run from the packet (it imports modules the packet does not ship). Presence is SCRIPT_DERIVED by parsing `_blank` and the unconditional `rec[...] =` assignments in `check.py`. Applicability is CODER_INFERRED from the code's verdict branches, citing lines, cross-checked against the filed `amendment_options/evidence/check_rules_output.txt` (Manus's 12-record run) where that file covers the field.
- **COMPUTED vs RAW_INPUT for TAF and numcheck fields** is CODER_INFERRED with the expression cited (for example `error = f"{type(e).__name__}: {e}"` makes `exception_type` COMPUTED from `error`).
- **routes**: 2 for T08 and T09 (the two terms with disagreeing routes in `derive_specific_output.txt`), 1 otherwise.

**Case cells (fixed rule, applied in this order, a field may collect several):**

```text
G  routes >= 2
D  origin DOCUMENTED
E  origin PARAMETER_ONLY
B  origin COMPUTED and some scope is ALL_EXCLUSIVE or SOME_EXCLUSIVE
A  origin RAW_INPUT and some scope is ALL_EXCLUSIVE
F  no scope is ALL_EXCLUSIVE and some scope is SOME_EXCLUSIVE
C  every recorded scope is SHARED or NONE
```

## 4. The reader half

- `listed`: LISTED if the name (after N1) is in that reader's `slots_specific`, else NOT_LISTED. Read from the file. NOT_LISTED is never written as "excluded".
- `basis_quote`: only a verbatim substring of that reader's `source_lines_read` for that term that mentions the field by name; the script fails if a quote is not found in the file. Otherwise null.
- `basis_kind`: the coder's classification of the quote, CODER_INFERRED; null when there is no quote.
- `uncertainty_stated`: true only where the reader's text says it is unsure about the field; otherwise null.

## 5. What is reported (counts only; no threshold, no score)

1. Per field: how many of the three readers list it, beside key a1.
2. Per case cell A-G: listing rate per reader, and key a1's.
3. Same list, different reasons: fields all three readers list where the coded `basis_kind` differs between readers.
4. Uncertainty: fields with `uncertainty_stated` true.
5. Where the three readers agree with each other and not with key a1 (PREREG v2's case (a): the key's derivation deserves a second look; not evidence about the first reading).

## 6. Limits stated now

One coder, the same model family as one of the three readers and the drafter of a superseded amendment; no second coder, so CODER_INFERRED values carry no agreement estimate. Three readings, one each. A reader's silence about a reason is recorded as silence, which makes the "different reasons" count a lower bound.
