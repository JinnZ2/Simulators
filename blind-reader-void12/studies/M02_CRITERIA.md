# M02 criteria: slots_carried record boundary and traversal (fixed before any coding)

Written 2026-11-19, before any M02 instrument code, coded record or new reading. Schema: `M02_SCHEMA.json`. Design from the GPT-6 reader's proposal (`as_received/gpt6_g01_g02_instrumentation.patch`), reshaped as in `M01_EXTENSION.md` section 5.

## 1. Question

For `slots_carried`, which records does a reader count, and how far does the reader follow a field that holds another record? These are two different choices and are recorded separately:

- **scope**: which records are in (the term's own record; records built beside it on the reporting path; wrappers that carry it; everything reachable);
- **traversal**: whether a record-valued field is named and left closed, or opened.

Two readers can disagree about **record identity** (they picked different records) or about **depth** (the same records, opened to different levels). The analysis reports the two kinds apart, because they are different failures.

## 2. Conditions and arms

```text
D0   the v2 packet and brief, unchanged
D1   + instructions/M02_D1.md   the term's own record only; name nested fields, do not open
D2   + instructions/M02_D2.md   every record built, returned or documented on the reporting path; name, do not open
D3   + instructions/M02_D3.md   the reader states their own rule first, in attestation.notes; none is suggested
```

Parallel and sequential arms as in `M01_EXTENSION.md` section 2. D1, D2 and D3 are separate comparisons and are never merged into one "clarified" condition. None is presented as the correct reading of the brief. D3 is run before D1 and D2 if readers are scarce, because it measures interpretation directly; D1 and D2 mostly measure compliance with an explicit instruction.

## 3. Specimens

- **Primary: T10** (`taf:GAP_INSTRUMENT_CRASH`). The coverage entry and the raise handler's section record are both built on the reporting path; key v2's carried list is the coverage entry's six fields, and whether the section record also counts is open (`KEY_V2_AMENDMENT_1.md` section 6.1).
- **Secondary:** T08 (a Reading and a CoverageEntry from one `crash()` call), T04 (ExpiryTrigger, held as a value inside UNKNOWN tokens: tests "name, do not open"), T06 (a FieldToken holding a Token), T09 (the case where readers already chose different records: coverage entries vs register rows).
- All 15 terms stay in the task; the specimens are where the analysis looks first, not a reduced packet.

## 4. Coding

One record per (reader, term, record the reader names or the catalog lists), with every value's provenance marked as in M01. The record catalog per term (the records the packet's sources build on each term's reporting path, with depth from the term's own record) is built from the sources and is SCRIPT_DERIVED where the code can be run or parsed, CODER_INFERRED otherwise. The reader half: which records the reader's `slots_carried` names draw on (a name belonging to several catalog records is recorded against each, flagged), the stated scope and traversal rules (READER_STATED under D3, CODER_INFERRED or null otherwise), and quotes checked verbatim as in M01.

**The three filed D0 readings will be coded first, as a descriptive table** (the coder has seen them), in a later commit, under this file unchanged.

## 5. What is reported (counts only)

Per term and condition: records counted per reader; fields per record; scope-rule and traversal-rule distributions; nested-record open rate; T10's section record counted / not counted; identity-vs-depth classification of each pairwise disagreement; within-reader transitions (sequential arm). No majority answer, no composite score, no change to any key.

## 6. Limits stated now

One coder (the Claude Code session, same family as one filed reader). The catalog of records is the coder's; a record the catalog misses shows up as a reader name with no catalog record, which is reported, not dropped. Readers per arm will be few; counts, not rates, are the honest unit.
