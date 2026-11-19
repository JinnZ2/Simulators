# AUDIT request: design of EMBEDDED_AUDIT_TESTS.md (DRAFT, not sent)

Drafted 2026-11-19 at the owner's request (`MODE: IMPLEMENT (filing only)`). The design is not hashed or preregistered until this audit returns.

Send rules:
- **Reader:** a model family other than Claude, in a fresh conversation with memory off.
- **Level:** expected L2. The reader is exposed to the design by design; it must not be exposed to the other study files or to any prior reading, which L3 would need. Its attestation decides the level, and a void field caps it.
- **What is sent:** the text below the line, plus the attached file `EMBEDDED_AUDIT_TESTS.md` as at `30c7fd0` (sha256 `d8dc77b733fa5065e3c0aa9f44d0032e1ca7f746b1c36e6eca235092e5c0dc95`, byte-identical to the file the owner delivered).
- **Filing:** the answer is filed as received in `../confusion/`, with its level.

---

```text
MODE: AUDIT (design audit; records only)
READ: EMBEDDED_AUDIT_TESTS.md@30c7fd0 only (attached)
AUTHORITATIVE WHEN FILES DISAGREE: there is one file; where it disagrees with itself, record a row
DO NOT USE: any other study file, prior readings, keys, scores, other readers' answers, any repository,
  the web, memory, earlier sessions
SESSION: new conversation; memory off; no project knowledge; no connected repositories
CODE EXECUTION: not allowed
RETURN, in this order:
  1. the exposure attestation below
  2. confusion rows: one per point where you were unsure, guessed, stopped, or needed evidence
     not in the file
  3. design gaps: one per place where a test, measure or reading cannot do what the file says
     it does, or where two parts of the file conflict
  4. missing codes: firings the codebook (F01-F12) has no code for, each with an example shape
Mark every guess as a guess. Use void for an unknown cell. Do not merge rows. If you find none
in a part, write "none found" for that part and list what you read.
```

**Row formats**

```text
confusion:    id | passage (section, line) | what was missing | what you did (guessed / stopped / read X as Y) | resolves with
design gap:   id | section or test | the gap | what it would affect (which reading, which measure) | guessed? | what would close it
missing code: id | the firing | example shape | which test would see it | guessed?
```

**Exposure attestation** (first; "unknown" is an answer):

```text
prior exposure, before this task:
  this file, or an earlier version of it                           yes / no / unknown
  other files of the study it belongs to                           yes / no / unknown
  the repository it comes from (any part)                          yes / no / unknown
  other readers' answers about it                                  yes / no / unknown
memory from other conversations                                   on / off / unknown
project or context features (project knowledge, connected
  repositories, custom instructions, attached files)              <list, or "none", or "unknown">
tools used in this task                                            <list, or "none">
```
