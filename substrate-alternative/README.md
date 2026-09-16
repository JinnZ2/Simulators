# substrate-alternative

Two instruments. One locates money-frame assumptions in text. One models ICS
(Incident Command System) as a coordination substrate with no monetary terms in
the model.

stdlib only. No network. No build step. Runs on a phone.

A folder in `JinnZ2/Simulators`. It was built to a dispatch that named a
standalone repo, and landed here instead; nothing in it assumes a repo root.
The root CC0 licence covers it and the root `.gitignore` covers `__pycache__`,
so neither is duplicated in the folder.

NOTE, a name collision this tree already had twice. `frame_audit.py` is also
the name of `declared-frame/frame_audit.py` and `frame-token-audit/frame_audit.py`.
The three are not copies of each other and measure different objects: this one
locates money-frame tokens. Each resolves from its own folder, so imports are
unambiguous, but a grep for the name returns three files.

```
frame_audit.py      locate money-frame tokens in any text. Locate only.
pilot_loop.py       the ICS coordination loop
selftest_pilot.py   checks for pilot_loop
SOURCES.md          the documents, the provenance states, and what is unverified
params/*.json       scenarios
```

## Run it

```bash
python3 frame_audit.py somefile.txt        # or pipe text on stdin
python3 frame_audit.py --selftest

python3 pilot_loop.py params/baseline.json
python3 pilot_loop.py --provenance         # structure and where it came from
python3 pilot_loop.py --scan-only          # the monetary scan alone
python3 selftest_pilot.py
```

`pilot_loop.py` scans its own source for money-frame vocabulary before it runs
anything and **refuses the run** if any appears in model logic or model
vocabulary. The lexicon is imported from `frame_audit.py` rather than copied, so
there is one lexicon and it cannot drift.

## ENVELOPE

**Valid for.** Coordination of declared capacity against declared need, under a
**declared ICS activation**, within one operational period, where every resource
kind is typed by a catalog supplied with the scenario, and where the parties
have already agreed to coordinate.

**Not valid for.** Steady-state allocation. This does not model an economy, a
market, or any ongoing distribution outside an incident. It does not model
whether parties will declare honestly, whether they will participate at all, or
what happens across many periods. **Do not claim transfer to the non-incident
case.** A result from this loop says something about an activated incident
structure and nothing about the case where no incident has been declared.

**Degradation mode.** It degrades toward silence, not toward a wrong number.
A resource the catalog cannot type returns `UNTYPED` and is matched to nothing.
A need nothing reaches returns `UNMET` with a reason. A node that received
nothing reports `None` for its lag rather than zero. Where the model runs past
what doctrine supplies, it is marked `ASSUMED` in the structure and printed by
`--provenance`. The failure you should expect is an empty or partial assignment
log with reasons attached, not a plausible allocation that is wrong.

**Revalidation trigger.** Any of these invalidates a run:

```
a NIMS edition later than the Third (October 2017) exists   SOURCES.md V-1
a section number in SOURCES.md is read and does not match   SOURCES.md V-2
the span-of-control element moves from CARRIED to CITED     SOURCES.md V-3
a real typing catalog replaces a scenario's inline one      SOURCES.md V-4
the monetary scan stops returning clean
an element's provenance changes, in either direction
```

**Margin applied.** None. No safety factor, no rounding up, no buffer is added
anywhere. Quantities move as declared and lag is the arithmetic of distance
times the declared `time_per_distance_unit`. If you want a margin, it goes in
the scenario, where it is visible, not in the model, where it would not be.

## NOT CLAIMED

That ICS is a general substitute for price coordination. The pilot tests one
thing: whether the loop closes on documented structure alone. It closes on the
shipped scenarios. That is a statement about the loop, not about coordination in
general and not about any alternative to anything.

## Source discipline

Structure comes from the documents in `SOURCES.md` and is not invented. Every
element carries a provenance state:

```
CITED          taken from a source in SOURCES.md
ASSUMED        doctrine silent on something the model needs; the model supplies it
CARRIED        from memory, citation unconfirmed. Not a citation.
NOT_ACTIVATED  doctrine present, and doctrine itself provides for non-activation
EXCLUDED       doctrine present, and a spec requirement excludes it
```

`EXCLUDED` names the requirement that excluded it and what was omitted, and a
run carrying one reports it at the **top** of the output. This build uses it
zero times, and prints the zero.

**Every CITED element is VERIFIED LOCATOR / UNVERIFIED SECTION.** The documents
resolve. Their sections were not read by the party that wrote this model, whose
network cannot reach the host. `section_verified` is `False` on every row.

`Finance/Administration` is present in the structure with activation state
`NOT_ACTIVATED`, citing the doctrine that provides for its non-activation. It is
not deleted and it is not `EXCLUDED`. Modelling a documented non-activation
state is neither inventing structure nor excluding documented structure.
`Intelligence/Investigations` is represented the same way.

## The scanner's scope, and what it does not read

It reads the vocabulary the model **declares** — function, class, argument and
field names, and model data strings — plus scenario files. It does not read
attribute accesses, because `x.value` on a standard-library enum is language
surface rather than model vocabulary. A model-defined field named for money is
still caught, at its definition, which is where the model's vocabulary is set.
Docstrings are counted on their own line rather than silently dropped, so the
prose exemption is measured.

Structural identifiers carried from cited doctrine are exempt, and every
exemption carries its citation. Two are declared and **zero are used**, which is
printed rather than left to look load-bearing.

One thing the scanner changed while this was being built: `@property` is in the
ownership lexicon, so the two lag accessors are plain methods. The constraint
was easier to satisfy than to widen the exemption list for.

## Known limits

`frame_audit.py` is a word list, and a word list deciding a question of meaning
is the failure mode of this class of instrument. Tokens with a common non-money
sense are declared in `KNOWN_COLLISIONS` and every hit on one carries its note.
A hit is a candidate, not a finding, and nothing in either file promotes one.
