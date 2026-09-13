# gap-register -- claim table

Prefix `GRG_`. Ids are permanent and are never renumbered. These are
claims about the INSTRUMENT and about the shipped register, and they are
distinct from the order's own rules `V1..V6` and from its entry ids
`GR-000N`.

`WORK_ORDER.md` is delivered verbatim and is edited by nothing here.

---

## GRG_001 -- V5 carries a term the order does not define, and the two available readings part on every shipped entry

**Status: SUPPORTED (computed).**

V5 refuses an index term that is *"a coinage absent from index_terms of
any other entry"* and supplies no test for **coinage**. Two readings:

- **STRICT** -- coinage is the singleton itself, so any term no other
  entry uses is refused.
- **LOOSE** -- a singleton is refused only where the entry has no shared
  term at all, i.e. where nothing reaches the entry from vocabulary used
  elsewhere.

They are not close. On the shipped register STRICT refuses **7 of 7** and
LOOSE admits **7 of 7**, so the rule the order calls load-bearing returns
the opposite verdict on every entry depending on a word it does not
define. `v5_index` scores both and returns `UNDETERMINED` naming the
terms; it does not pick.

*Falsifier:* the operator supplies a coinage test, or states that coinage
is the singleton, and the check collapses to one reading.

---

## GRG_002 -- under STRICT, no register spanning unrelated domains can satisfy V5

**Status: SUPPORTED (computed).**

A term specific enough to find an entry by is a singleton until a second
entry in the same domain arrives. On the seed register the shared terms
are exactly the six that pair two entries inside one domain --
`mediation` (GR-0001, GR-0003), `negotiation` (GR-0001, GR-0006),
`analgesia` / `pain management` / `veterinary` (GR-0002, GR-0004),
`language model` (GR-0005, GR-0007) -- and every other term is a
singleton.

This is not obviously a defect: section 4's stated purpose is *"a reader
who does not know the term must still hit the entry"*, and STRICT forces
index terms toward ordinary words. It has a cost the order does not
state, which is that the register's index vocabulary is then set by what
the register already contains.

The seeds could have been written to pass STRICT by curating a shared
vocabulary. That was declined: it fits the entries to the checker, and
the resulting 7-of-7 reading would then be a measurement of the curation
rather than of the rule.

---

## GRG_003 -- the shipped register is 7 of 7 UNKNOWN, and that is what section 1 forces

**Status: SUPPORTED.**

`OPEN` records that someone checked and the quantity was absent. Nobody
checked: every publisher, registry and standards host refuses CONNECT
from this environment, so no `venue_check` in the register has been run.
Section 1 says an entry that cannot be evaluated returns `UNKNOWN`,
**never `OPEN` by default**, so all seven land there.

The consequence is stated rather than smoothed: the `OPEN`,
`CLOSED_MEASURED`, `CLOSED_INSTRUMENT_EXISTS` and `OUT_OF_ENVELOPE`
returns are unexercised by the shipped data and are shown reachable only
in constructed fixtures inside `selftest_gr.py`.

The operator holds the 2026-09-11 session record and is the party who can
set these to `OPEN`. That is the same class of decision as section 9.

---

## GRG_004 -- V5 is not evaluable on the first entry, because it is a property of the register and not of the entry

**Status: SUPPORTED (computed).**

`add` on an empty register cannot be scored on V5: *"any other entry"*
has no referent. `v5_index` returns `NOT_EVALUABLE` with that reason
rather than passing the entry or refusing it. Every other check in
`V1..V6` reads one entry; V5 reads the register, and the order does not
mark the difference.

---

## GRG_005 -- V4 rests on two word lists and a word shape

**Status: SUPPORTED.**

`ACCUSATORY`, `MOTIVE` and the modal list are word lists, and the name
test is a word shape. Any paraphrase steps around all four, which is the
limit this repository records as `T1-1`, `UNI_009`, `DF_010` and
`ACL_017`; it is stated at the top of the module rather than the bottom.

One direction is chosen and declared. An ALL-CAPS token is read as an
acronym and never as a name, because an acronym in `excluding_method` is
the ordinary content of that field. That under-fires on an all-caps
surname. The alternative over-fires and refuses a legitimate entry, which
on a register whose whole point is that entries can be written without an
allegation is the costlier direction.

---

## GRG_006 -- a defect in the name shape, found by the arm that could have been covered for

**Status: SUPPORTED (found by running).**

An honorific ends in a period, and the sentence splitter in
`name_shaped` treated `Dr.` as a sentence boundary -- severing the
honorific from the name it introduces, so the honorific arm returned
nothing. The run-of-capitals arm fires on `Dr Alvarez` anyway, so the
suite would have stayed green on the wrong mechanism if that one check
had not been written separately. Repaired by masking honorific periods
before the split; both arms are pinned.

---

## GRG_007 -- V2 checks vocabulary, not checkability

**Status: SUPPORTED.**

The rule asks that a closure condition be *checkable*. The
implementation asks that it contain a noun from a list of twenty-odd
observable nouns, which is the shape this repository records under
`G-FIT` in `reasoning-gate/` and again at `RD_002`: the rule says *name
why it can discriminate*, the implementation checks that a string is
non-empty.

Measured: the seven shipped closure conditions match 2 to 4 observable
nouns each. A closure condition naming *"a published table"* with no
statement of what is in the table passes, and is not checkable. The list
is the checker's, marked `[CHOICE 1]`, and is short on purpose -- a long
list passes everything.

---

## GRG_008 -- the exit code is a choice, and under the other reading nothing in the folder validates

**Status: SUPPORTED (declared, `[CHOICE 5]`).**

`validate` exits nonzero on `FAIL` only. `UNDETERMINED` exits zero and is
printed in a `LOUD` block naming every term. Under the other reading --
`UNDETERMINED` exits nonzero -- the shipped register would not validate,
and the section 8 contrast between a register that passes and a demo that
does not would disappear along with it.

The choice is printed at the foot of every `validate` render rather than
kept here.

---

## GRG_009 -- the KILL RULE is not runnable from here

**Status: UNVERIFIED.**

Section 0 asks for a zero-context model given only `REGISTER.jsonl`,
scored on restating the absent quantity and the closure condition for a
sample of 20 entries. There is no model endpoint in this environment,
there are 7 entries rather than 20, and the session that wrote the
entries is the wrong party to run a zero-context test on them.

What is checkable is the precondition, and it holds: all seven entries
carry a non-empty `quantity` and a non-empty `closure_condition`, which
are the two things the rule asks a reader to restate.

---

## GRG_010 -- the three section 9 items are left open, and the openness is asserted

**Status: SUPPORTED.**

O1, O2 and O3 require operator sign-off and none is decided here. Each is
made mechanically checkable so a later build cannot quietly settle one:

| item | left as | asserted by |
|---|---|---|
| O1 four types or three | `TYPES` has four; T4 is not collapsed | selftest |
| O2 status per entry or per reader | one `status` string per entry | selftest |
| O3 dialect or bare JSONL | bare; no `@context` in module or store | selftest |

---

## GRG_011 -- no entry's factual content is verified, and the register introduces no name the order does not supply

**Status: SUPPORTED.**

Every host that would carry a standard, a guideline, a coding table or a
benchmark refuses CONNECT from this environment, so no `excluding_method`
in the register has been checked against a published document. Every
entry is at the status this repository records as `MS_004` / `ANC_010`:
carried, unverified.

The discipline taken instead is mechanical. The register names no
standards body, programme, certification or publication the order does
not name, and `selftest_gr.py` checks it: every all-caps identifier
appearing in any V4-scanned field of the register also appears in
`WORK_ORDER.md`. The check is non-vacuous -- the register does use one.

---

## GRG_012 -- the citation confound is recorded in 3 of 7 entries, and which entries carry it is a judgement

**Status: SUPPORTED.**

Section 5 says the citation confound is recorded *"in every entry that
carries it"*. It is recorded in GR-0001, GR-0003 and GR-0007 -- the three
whose `excluding_method` is a body's own reporting practice. The other
four record a different confound: a comparison class that rests on an
unmeasured judgement (GR-0002, GR-0004), a self-report standing in for
the quantity (GR-0005), an instrument inside the system it measures
(GR-0006).

Which entries carry it is not computed from any field. It is this
auditor's reading, and a reader who disagrees would change the field, not
the checker.

The measurement arm the order names -- the name-strip probe -- is named
and **not built** here.

---

## GRG_013 -- `check` prints the closure condition and nothing else, exactly as asked

**Status: SUPPORTED (computed).**

`check <id>` emits one line: the closure condition, with no id, no
status, no quantity and no context. The selftest asserts both the content
and the line count. The cost is that a mistyped id returns exit 2 with no
near-match offered, which is the same refusal to add unasked context.

---

## GRG_014 -- on the only pair available, the T2/T4 distinction sits in a field rather than in the type

**Status: OPEN (n = 2; the order's O1 is the operator's).**

GR-0002 (T2) and GR-0004 (T4) share three of five index terms and their
`excluding_method` is the same shape: two systems, each complete inside
its own scope, with nothing joining them. What separates them is
`venue_check` -- T2 asks whether the separation was ever declared, T4
asks whether a venue exists where the two would have to meet -- and that
is a field both types already carry.

This is evidence toward O1's collapse and it is n = 2, on entries written
by one hand, which is the shared-bias limit recorded at `TP_003`. It is
recorded, not decided.
