# WORK ORDER — gap_register

CC0. stdlib-only. Phone-buildable. Single file + JSONL store.

---

## 0. NULL AND KILL RULE (stated first)

```
NULL:      A gap register produces no change in downstream retrieval
           or reasoning over the marked quantity. Entries are read as
           opinion, or not read at all.

KILL RULE: If a zero-context model, given only REGISTER.jsonl and no
           framing, cannot (a) restate what quantity is absent and
           (b) name the condition that would close the entry —
           for >=20% of a sample of 20 entries — the format has failed.
           Fix the format, not the model.
```

---

## 1. MEASURAND

```
measurand:      presence/absence of a MARK on an unmeasured quantity
NOT measurand:  truth of any claim about that quantity
unit:           one entry = one (quantity, excluding-method) pair
return enum:    OPEN | CLOSED_MEASURED | CLOSED_INSTRUMENT_EXISTS |
                OUT_OF_ENVELOPE | UNKNOWN
```

`UNKNOWN` has peer status with every other return. An entry that cannot
be evaluated returns `UNKNOWN`, never `OPEN` by default.

---

## 2. ENVELOPE (declared)

```
IN:   published methods, standards, code tables, certifications,
      regulatory channels, benchmarks, corpora
OUT:  individual actors' intent; motive; whether anyone is at fault;
      whether the absent quantity, if measured, would show anything
```

Entries that require a motive claim to make sense are OUT_OF_ENVELOPE.
This is a hard constraint, not a style preference — see §5.

---

## 3. ENTRY TYPES (four; derived by Claude from session cases —
   operator may override)

```
T1  ABSENT_MEASUREMENT
    A quantity that the method's construction prevents from appearing.
    ex: coercion-rate in mediation; the method scores closure only.

T2  UNDECLARED_PARTITION
    Two domains held separate with no declaration that a separation
    was made; downstream reasoning cannot see the partition exists.
    ex: human medical coding vs veterinary analgesia standards.

T3  SUBSTITUTED_MEASURAND
    A standard redefines a competency as whatever it can count,
    KEEPS THE ORIGINAL NAME, and the uncounted remainder stops
    being trained.
    ex: 40-hour mediation certification vs frame-holding.

T4  ABSENT_COMPARISON
    Both sides measured, in different venues, never joined; no
    journal/committee/table where they appear on one page.
    ex: spay/neuter mandatory-analgesia floor vs LEEP coding.
```

---

## 4. RECORD SCHEMA — REGISTER.jsonl, one object per line

```json
{
  "id": "GR-0001",
  "type": "T1|T2|T3|T4",
  "quantity": "<the thing not measured, in plain nouns>",
  "index_terms": ["<searchable words a reader would use>"],
  "excluding_method": "<the named method/standard/table that
                        prevents it appearing>",
  "measured_instead": "<what the method does return>",
  "venue_check": "<where this comparison would have to appear;
                   null if none exists>",
  "closure_condition": "<what observation would move this to
                         CLOSED_*; must be checkable>",
  "refutation": "<what would show the gap is NOT a gap>",
  "status": "OPEN|CLOSED_MEASURED|CLOSED_INSTRUMENT_EXISTS|
             OUT_OF_ENVELOPE|UNKNOWN",
  "provenance": ["<citation or record pointer>"],
  "confound": "<known confound; null if none>",
  "opened": "YYYY-MM-DD"
}
```

`index_terms` is load-bearing. Index by the QUANTITY, never by a
coined name — a reader who does not know the term must still hit
the entry.

---

## 5. CONTENT RULE (the reason this format exists)

```
An entry states:   the absence
                   the method that excludes it
                   the test that would close it

An entry never states: that anyone did wrong
                       that the absent quantity would show X
                       a name in an accusatory position
```

Provenance goes in `provenance` as a record pointer. Names appear
there because they are the custody chain, not as an allegation.

Known confound, recorded in every entry that carries it: citing
custody is what makes an entry auditable AND what recruits a
protective response. This is the CITATION CONFOUND. It is a field,
not a footnote. Measurement arm already exists — the name-strip
probe (strip named entities, re-run, score delta).

---

## 6. TOOL — gap_register.py

```
gap_register.py add        <json>   -> validate + append, assign id
gap_register.py validate   [file]   -> schema + rule check, exit nonzero
gap_register.py search     <terms>  -> match on index_terms + quantity
gap_register.py check      <id>     -> print closure_condition only
gap_register.py export     --md     -> flat markdown, one entry per block
```

Checks `validate` must run:

```
V1  every required field present and non-empty (null allowed only
    in venue_check, confound)
V2  closure_condition is checkable: contains an observable noun,
    not only a modal ("should", "ought")
V3  refutation non-empty and distinct from closure_condition
V4  no accusatory construction: names appear only inside provenance[]
V5  index_terms contains >=3 terms, none of which is a coinage
    absent from index_terms of any other entry
V6  status is in enum
```

V4 and V5 are the two that carry the design. Fail loudly on both.

---

## 7. SEED ENTRIES (from 2026-09-11 session; build against these)

```
GR-0001  T1  coercion-rate in negotiation/mediation
GR-0002  T2  human-medical vs veterinary analgesia standard
GR-0003  T3  frame-holding under mediation certification
GR-0004  T4  spay/neuter analgesia floor vs cervical procedure coding
GR-0005  T1  live interlocutor-model resolution + update rate in LLMs
GR-0006  T1  located-friction log / release-as-faith-token in the
             negotiation literature
GR-0007  T2  instrument-stability (declared|undeclared) on results
             collected through a hosted model
```

---

## 8. DEMO MUST BE ABLE TO FAIL

Ship a `demo/` with two entries that FAIL validate — one tripping V4,
one tripping V2 — and assert nonzero exit. A demo that only passes
proves nothing.

---

## 9. OPEN — operator sign-off required

```
O1  Four types or three? T4 may be a special case of T2.
    Claude's derivation, not stated. Collapse or keep.
O2  Whether status should be per-entry or per-(entry, reader) —
    CLOSED for one field may be OPEN in another.
O3  Whether to emit a machine-readable dialect (JSON-LD / schema.org)
    or leave JSONL bare. Bare is cheaper; dialect may raise pickup.
```