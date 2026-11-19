# Open rows with their evidence status (sidecar, 2026-11-19)

The format asked for in the owner's message of 2026-11-19 (`as_received/mode_and_authority_2026-11-19.md`, item 6), applied to every row of the four confusion records. Records are not edited; this file sits beside them. **Every evidence status here is CODER_INFERRED** (Claude Code session), read from each row's own `resolves with` cell and from `GAPS.md`. Only the CF record carries a status column; for the others, `state` is this file's reading of their dated sections.

An evidence status says what kind of evidence can close the row. Another reader's agreement is not one of them.

```text
status                    closes on                                              stage (MODE_SEQUENCE.md)
SOURCE_RUN_REQUIRED       running code or files the packet does not ship         AUDIT
SECOND_CODER_REQUIRED     a coder other than the first, on the same quotes        AUDIT (a different coder)
DEFINITION_REQUIRED       a rule written down; if evidence cannot pick, branch    SUGGEST, then IMPLEMENT
EDIT_REQUIRED             wording only; no rule changes                          IMPLEMENT
AUTHOR_RECORD             the author of a passage or act states what it was      none: a fact the author holds
READING_REQUIRED          a future reading under the named condition             BLIND
PACKET_FIX_DRAFTED        fixed in the v2 study packet draft; closes only when   BLIND (a v2 reader)
                          a v2 reader does not hit it
ANSWERED_IN_FILES         the definition exists in a file the reader did not     REVIEW (the reader reads it)
                          open; stays open until read
CLOSED                    recorded closure, with its source                      --
```

## Claude Code session (CF)

```text
CF01  DEFINITION_REQUIRED    a conditionally-required scope value                   open
CF02  SOURCE_RUN_REQUIRED    numcheck + formula-audit checkout                      open
CF03  DEFINITION_REQUIRED    rule for messages built from exceptions                open
CF04  DEFINITION_REQUIRED    same rule as CF03                                      open
CF05  DEFINITION_REQUIRED    void in the row; read as a missing rule (constants)    open
CF06  DEFINITION_REQUIRED    case rule C revision                                   open
CF07  DEFINITION_REQUIRED    a NO_REASON_GIVEN basis kind                           open
CF08  SECOND_CODER_REQUIRED  same quotes                                            open
CF09  DEFINITION_REQUIRED    a NOT_STORED_SO_NOT basis kind                         open
CF10  DEFINITION_REQUIRED    Q1 ruling extended to crash()'s parameters             open
CF11  CLOSED (definition) + DEFINITION_REQUIRED (T02 value; = KC02)                 part open
CF12  AUTHOR_RECORD          the request's author: which file                       open
CF13  AUTHOR_RECORD          the request's author: was the arm conditional          open
CF14  AUTHOR_RECORD          the reply's author: which steps "Yes please" covered   open
CF15  AUTHOR_RECORD          whoever sent the GPT-6 packet: variant A or B          open
CF16  READING_REQUIRED       the first M02 D3 reading                               open
CF17  SECOND_CODER_REQUIRED  same quotes                                            open
CF18  DEFINITION_REQUIRED    documented-only TAG rule (two instruments disagree)    open
CF19  DEFINITION_REQUIRED    missing-value rule (schema vs test disagree)           open
```

## Chat session (CH)

```text
CH01  DEFINITION_REQUIRED    HOLDS grouping (three readings, three answers)         open
CH02  DEFINITION_REQUIRED    confirmation tier                                      open
CH03  AUTHOR_RECORD          = CF15                                                 open
CH04  ANSWERED_IN_FILES      studies/GLOSSARY.md, readings/                         open
CH05  ANSWERED_IN_FILES      studies/GLOSSARY.md (M01, M02)                         open
CH06  ANSWERED_IN_FILES      studies/GLOSSARY.md (D0-D3)                            open
CH07  ANSWERED_IN_FILES      studies/GLOSSARY.md, OPERATIONAL_DEFINITIONS.md        open
CH08  ANSWERED_IN_FILES      studies/GLOSSARY.md (KA-07)                            open
CH09  ANSWERED_IN_FILES      KEY_V2_AMENDMENT_1.md + PREREG status note             open
CH10  DEFINITION_REQUIRED    presence vs applicability (G1)                         open
CH11  CLOSED                 confusion/2026-11-19_claude-code_m01-m02.md dated §    closed
CH12  CLOSED                 resolved by CF13 (the chat record's own row)           closed
```

## Kimi reader (KC)

```text
KC01  DEFINITION_REQUIRED    which TAG mapping D1 uses (G1)                         open
KC02  DEFINITION_REQUIRED    documented-only / NO_INSTANCE rule (G1; = CF18)        open
KC03  DEFINITION_REQUIRED    "populated" (G1; = CF19)                               open
KC04  EDIT_REQUIRED          condition enums per study                              open
KC05  EDIT_REQUIRED          presence description wording (G1)                      open
KC06  DEFINITION_REQUIRED    T04 own record (G2)                                    open
KC07  DEFINITION_REQUIRED    T06 own record (G2)                                    open
KC08  DEFINITION_REQUIRED    T12 two record types (G2; boundary case 5)             open
KC09  DEFINITION_REQUIRED    T15 record-valued concept (G2)                         open
KC10  DEFINITION_REQUIRED    path boundary, outer reports (G3; boundary case 6)     open
KC11  DEFINITION_REQUIRED    D2 and on-path wrappers (G3)                           open
KC12  DEFINITION_REQUIRED    new-field procedure (no gap id)                        open
KC13  void                   the row's resolves-with is void                        open
```

## Grok reader (GR)

```text
GR01  PACKET_FIX_DRAFTED     P3            GR10  DEFINITION_REQUIRED  G1
GR02  PACKET_FIX_DRAFTED     P4            GR11  PACKET_FIX_DRAFTED   P2
GR03  DEFINITION_REQUIRED    G2            GR12  DEFINITION_REQUIRED  G5
GR04  DEFINITION_REQUIRED    G2 / G1       GR13  PACKET_FIX_DRAFTED   P6
GR05  DEFINITION_REQUIRED    G2 / G3       GR14  PACKET_FIX_DRAFTED   P5
GR06  DEFINITION_REQUIRED    G2            GR15  PACKET_FIX_DRAFTED   P1
GR07  DEFINITION_REQUIRED    G5            GR16  PACKET_FIX_DRAFTED   P4
GR08  DEFINITION_REQUIRED    G3            GR17  PACKET_FIX_DRAFTED   P4
GR09  DEFINITION_REQUIRED    G1            GR18  PACKET_FIX_DRAFTED   P6, then G3
all open
```

## Counts (from the tables above)

```text
62 rows (CF 19, CH 12, KC 13, GR 18); CF11 counted once, under DEFINITION_REQUIRED
DEFINITION_REQUIRED 33   PACKET_FIX_DRAFTED 9   ANSWERED_IN_FILES 6   AUTHOR_RECORD 5
SECOND_CODER_REQUIRED 2  CLOSED 2 (CH11, CH12)  EDIT_REQUIRED 2   SOURCE_RUN_REQUIRED 1
READING_REQUIRED 1       void 1
```

## Re-read for hierarchy filling a gap (K3 in the owner's message)

The routing of this session's own rows and reports, re-read against `../MODE_SEQUENCE.md`:

- **Owner's ruling as the resolver.** CF01 and CF10 named "the owner's ruling" as what closes a definition. That is a seat (Layer 3) filling the place of a decision rule. Both are re-routed above to DEFINITION_REQUIRED, stage SUGGEST.
- **Not hierarchy.** CF12-CF15 ask the author of a request or an act what it was. Only that author holds the fact, so these are provenance, and they stay AUTHOR_RECORD.
- **The previous report's closing questions.** The report of 2026-11-19 (repository read) ended with four "questions for you":
  1. Adopt the `folders` key: DEFINITION_REQUIRED, stage SUGGEST. No check reads the key, so nothing breaks either way.
  2. Meaning of `claim_table: void`: DEFINITION_REQUIRED, stage SUGGEST.
  3. psutil in grounding-layers: evidence decides that it is a hard dependency of the folder's own tests (`tests/test_bias_human_centrism.py` line 17 imports `AIObserverState`, which imports psutil unguarded). What remains is a branch: declare it in `requirements.txt`, or guard the import and let the test skip. That is IMPLEMENT in that folder.
  4. Where the 2026-11-11 freeze is recorded: AUTHOR_RECORD.

  Questions 1-3 were Layer 2 (a decision handed back to the user); question 4 was not.

## Later (2026-11-19): second status from MEASURANDS.md

`MEASURANDS.md` finds that the brief, read at D0, answers part of two rows. `READER_BRIEF.md` line 23 counts every record built when the term is reported, wrappers included, and every M02 condition keeps that line. No row is closed: under the no-silent-closure rule, the reader who wrote the row closes it by reading the line. The rows gain a second status:

```text
GR08  DEFINITION_REQUIRED (outer reports, G3) + ANSWERED_IN_FILES (T10's section record is built when the
      term is reported, so it counts at D0: READER_BRIEF line 23; unified_audit.py 479-491 per the row)
KC11  ANSWERED_IN_FILES (wrappers are in under every condition: READER_BRIEF line 23) against the fixture rule;
      the fixture's contradiction is CF20
CF20  EDIT_REQUIRED (decided by the brief's text)  fixture rule ALL_REPORTING_PATH_RECORDS excludes wrappers  open
```

Rows now 63: CF20 is added after the counts above were taken. The counts are not redone.

## Later (2026-11-19): CF20 status

CF20's repair already exists at `7bc51bb` (PR #320, draft). Status: EDIT_REQUIRED, drafted, waiting on REVIEW-2 by a reader other than the implementer (`INDEPENDENCE_LEDGER.md`).
