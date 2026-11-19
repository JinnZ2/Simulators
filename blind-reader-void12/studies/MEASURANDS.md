# Measurand line for each OPEN rule (2026-11-19)

From the owner's message of 2026-11-19, gap DERIVED:

> runs show divergence; they can't crown a winner … decider = the study's stated measurand … if the measurand is unstated → it stays a branch, both kept … the six OPEN rules need a measurand line each, before the runs are compared.

Each line is written per **layer**, because the same rule serves different measurands in different layers:

- **key**: what the key's lists are a record of.
- **studies**: what M01 and M02 measure.
- **reader**: what the brief asks for at D0.

Status of each line:

- **STATED**: a file says it.
- **DERIVED**: follows from a stated line by a step shown here.
- **UNSTATED**: no file says it, so the rule stays a branch.

Nothing here runs a comparison, changes a rule, the brief, D0, a key or a score.

## What each layer is for

```text
layer     measurand                                                    status    source
key       the first reading's construct: "same predicate and same      STATED    combined-playground/cplay/vocab_branches.py line 7
          slots (wordslots place-table style)"; slots "read from                 (V-C), lines 18-19
          code where the code names them, else declared"
          the place table itself                                       PROPOSED  tools/TOOL_CARDS.md, wordslots card: "the place
                                                                                 table is PROPOSED"; wordslots measures "whether a
                                                                                 word's places ... are filled and sourced"
key       carried lists: "the record each term's source builds"        STATED    KEY_V2_AMENDMENT_1.md section 5 (the owner's Q3)
          (fields of the built record; class attributes excluded)
studies   M01: which fields readers list in slots_specific, and why;   STATED    M01_CRITERIA.md section 1 ("Descriptive, not a test")
          M02: which records readers count and how deep they go         STATED    M02_CRITERIA.md section 1
reader    the brief's definitions, unchanged at D0                     STATED    reader_packet_v2/READER_BRIEF.md lines 22-23
VOID-12   whether a blind reader groups the terms as the key does;     STATED    PREREG.md "What is being tested"
          not whether the key is right
```

**What follows for the studies layer** (DERIVED from M01 and M02 being descriptive of readers): no rule has to be picked. The candidate rules are coding variables. Each runs as an arm, and the divergence is the output, as `instrument/arms.py` already does for TAG. Picking a winner there would change what the studies measure.

## The six rules

```text
rule            layer  measurand line                                                  status     result
TAG             key    a place in a place table exists whether or not it is filled,   DERIVED    presence (with requirement), not
                       so "tied to this term" reads as the place being defined for              applicability, for the KEY; consistent
                       the term: presence / requirement, not populated                          with key a1 section 2. Rests on the
                       (step: wordslots separates "places" from "filled")                       wordslots card, itself PROPOSED
                studies                                                                 STATED     both readings run (arms.py); no winner
                reader the brief: "tied to this term and to no other term ... Not      UNSTATED   branch kept; a reader's applicability
                       fields that every term sharing a record has" ("has" fits                 reading is a reading of D0, not an error
                       both readings)
INDEPENDENCE    key    a place is an argument of the word, so a value computed from    DERIVED    INDEPENDENCE holds for the key, as
                       other places is not a place (step: place = what the word                 key a1 states; constructor-only and
                       takes, not what it yields)                                               renamed parameters UNSTATED (branch)
                studies                                                                 STATED     coded as variables; no winner
                reader the brief: "Not names for the inputs of a calculation"          UNSTATED   for computed outputs, branch kept
                       (excludes inputs; says nothing about outputs)
Populated       key    only enters under applicability, which the key does not read    DERIVED    not needed for the key's TAG
                       (by the TAG line above)
                studies wordslots "filled": a value is in the place; the card's       DERIVED    None and "void" = unfilled; 0, False =
                       known break is "'nothing' counts as filled", so a value that              filled (a value); empty collection
                       says "nothing" must not count as filled                                    UNSTATED (branch). Rests on a PROPOSED
                                                                                                 card; differs from M01_SCHEMA's
                                                                                                 "non-zero" (CF19)
Own record      key    carried: "the record each term's source builds"                 STATED     for terms with one built record;
                                                                                                 T04, T06, T12, T15 UNSTATED (branch)
                studies                                                                 STATED     scope rule is a coded variable; no winner
                reader the brief: "every record ... builds, returns or documents"      UNSTATED   own record not needed at D0 (the brief
                                                                                                 counts every record); branch for D1
Reporting path  key    "the record each term's source builds"                          STATED     the built record only; outer reports,
                                                                                                 adjacent records UNSTATED
                reader the brief: "including a shared or wrapper record that only      STATED     wrappers IN at D0; outer aggregate
                       carries the term as a value"                                              reports UNSTATED (branch)
Nested record   key    constructors run, record fields taken (vars / _fields)          STATED     name the field, do not open
                reader the brief: "if a field holds another record, name the field     STATED     name, do not open; multiple levels
                       and do not open it"                                                       follow from it (never opened)
```

## Branches that remain (no measurand decides them)

```text
TAG at the reader layer (presence vs applicability)      G1
INDEPENDENCE of computed outputs at the reader layer     G1
INDEPENDENCE of constructor-only / renamed parameters    CF09, CF10
empty collection as filled or unfilled                   KC03, CF19
own record for T04, T06, T12, T15                         G2
outer aggregate reports                                   G3
```

## Two things this table finds that the definitions table did not

1. **At D0 the brief already answers parts of two rows.**
   - Line 23 counts "every named field of every record that the source's code or text builds, returns or documents when this term is reported, ... including a shared or wrapper record". So an adjacent record built on the term's report counts (GR08's question about T10's section record), and wrappers count.
   - Every M02 condition is a note added to that brief and does not remove the line. So under D2 too, wrappers are in.
   - The instrument's fixture rule `ALL_REPORTING_PATH_RECORDS` leaves wrappers out (`instrument/test_instrument.py` `carried()`). That is the contradiction KC11 stopped on, and the brief's text decides it against the fixture. Filed as CF20. Repairing the fixture is the next IMPLEMENT step and is not done here.
   - No row is closed: under the no-silent-closure rule, the reader who wrote it closes it.
2. **The key and the reader answer different questions on TAG.** The key's place-table construct derives presence; the reader's brief leaves both readings open. A reader listing `void_reason` (applicability) is therefore not wrong against the brief. It differs from the key on a point the brief does not fix. VOID-12's own measurand is agreement, not correctness (PREREG), so this is recorded as a source of disagreement, not of reader error.

The DERIVED key-layer lines rest on the wordslots card, which marks its place table PROPOSED, and on the wordslots code, which lives in another repository and was not read here. If that code defines a place differently, the TAG and Populated lines move.

## Later (2026-11-19): correction

Item 1 says repairing the fixture "is the next IMPLEMENT step and is not done here". It was drafted earlier in this session: `7bc51bb`, PR #320 (draft). See the dated section of `confusion/2026-11-19_claude-code_m01-m02.md`.

## Later (2026-11-19): SUGGEST records on this file as read at `a3e204f`

Request header: `MODE: SUGGEST (records only)  READ: studies/MEASURANDS.md@a3e204f` (the owner, 2026-11-19). The section above this one, added at `671a226`, comes after that read set. These records do not depend on it.

**1. The key TAG chain, link by link.** The status of each link is the owner's marking. The "source here" column is what this tree holds for it.

```text
link                                                       status     source here
vocab_branches.py line 7: "same predicate and same slots   OBSERVED   combined-playground/cplay/vocab_branches.py:7
  (wordslots place-table style)"
Lojban zo'e: an unfilled place is still a place (the       OBSERVED   the owner's marking; no file in this tree states
  elided argument is filled by zo'e, "unspecified")                   it. Nearest: tools/provenance_marker.py:30
                                                                      ("(Ithkuil/Lojban) every predicate place filled")
wordslots card: places vs "filled and sourced"             PROPOSED   tools/TOOL_CARDS.md, wordslots card ("the place
                                                                      table is PROPOSED")
wordslots code                                             UNREAD     formula-audit:wordslots/check.py, another
                                                                      repository, not read in this session
overall: TAG = presence for the key                        DERIVED on PROPOSED
```

The TAG and Populated lines in the table above inherit this status. If the wordslots code, once read, defines a place differently, both move.

**2. GR08 and outer aggregate reports.** The reading of `READER_BRIEF.md` line 23 that includes wrappers ("a shared or wrapper record that only carries the term as a value") also includes outer aggregate reports, since an aggregate report carries the term's record as a value. The same reading answers both. Linked rows: KC10 (outer aggregates such as `check_all()` and `UnifiedAuditReport`), GR08 and GR18 (Grok rows 8 and 18). Where the path **stops** stays OPEN: line 23 says what a carrying record is, not how far out the carrying goes (G3).

**3. Independence of the findings above.** Under the owner's rules (`../MODE_SEQUENCE.md`, dated section), each of these is the Claude Code session reading text it is itself working on. They are **INDEPENDENCE L0**, self-review:

```text
ANSWERED_IN_FILES on GR08 (OPEN_ROWS.md)                 L0
ANSWERED_IN_FILES on KC11 (OPEN_ROWS.md)                 L0
CF20 "the brief's text decides it against the fixture"   L0
```

None closes or decides anything alone. The fixture repair (`7bc51bb`, PR #320, draft) is **held** until a REVIEW-2 at L2 or above. The request is drafted in `requests/REVIEW2_LINE23_2026-11-19_DRAFT.md`.
