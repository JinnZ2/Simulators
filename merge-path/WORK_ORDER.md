# WORK ORDER — merge path, existing claim registrars <-> falsifier format

For: Claude Fable
Licence: CC0. Python 3 stdlib only. Phone-runnable core.
Network: needed once, to fetch public specifications. Everything
         after that runs offline.
Opened: 2026-09-05

---

## 0. WHAT THIS IS AND IS NOT

```
IS       a transform table between claim-record formats that
         already exist, and the falsifier/branch-record format,
         with the loss in each direction measured rather than
         asserted.

IS NOT   a new universal standard. Do not design one, do not
         propose one, do not name one. Nanopublications has been
         specified since 2010 and is still not a gate anywhere;
         the failure mode of this problem space is producing an
         eighth format. If the output of this work is a format,
         the work failed.
```

The unit of value is a TRANSFORM, in the sense already in use:

```
reference   what this registrar's claim record is taken against —
            its frame, its boundary, its enforcing body
maps_to     what it corresponds to in the falsifier format
breaks_at   where the correspondence fails, and on what
```

A registrar that does not merge is a valid and reportable outcome.
NO-MERGE with a stated breaks_at is worth more than a forced mapping.

---

## 1. FIRST TASK — INVENTORY THE UNITS, FROM THE SPECS

Do not work from summaries, including this document's. Fetch each
registrar's own specification or data dictionary and record what its
atomic record actually contains.

```
target set (extend if a better case is found, say why):

  FORMATS — specified, largely not enforced
    nanopublications      RDF: assertion / provenance / pub-info
    ORKG                  structured contributions, comparisons
    RO-Crate              packaged research object + metadata

  FIXTURES — fire by default, enforced by someone
    ClinicalTrials.gov    registered primary outcome + measure +
                          time frame; legally enforced (FDAAA)
    CIPM / CMC entries    capability claim + uncertainty budget +
                          traceability chain
    proof assistants      claim IS the statement; check is the
                          proof (mathlib-style)
    OSF preregistration   hypothesis + analysis plan, ahead of data

  OURS
    falsifier format      claim + falsifier + MEASURED_AS
                          (quantity / units-with-a-cut / how
                          obtained) or SCOPE_TRANSFORM
                          (reference / maps_to / breaks_at),
                          plus the branch record
```

For each, emit into `UNITS.md`:

```
atomic record      what one entry is
required fields    what cannot be omitted
who enforces       nobody / reviewers / a regulator / a compiler
when it fires      on submission / at review / continuously / never
what a violation   retraction / flag / rejection / nothing
  costs
identifier         spec URL or DOI. A source-class tag is not an
                   identifier.
```

Read before mapping. If a registrar turns out not to have an atomic
claim record at all, that is the first finding about it.

---

## 2. THE TWO DIRECTIONS ARE DIFFERENT PROBLEMS

Do not build one converter. Build two, and expect them to lose
different things.

```
IN   their record  ->  falsifier format
     likely loss: provenance graph structure, enforcement status,
                  uncertainty budget, the legal or institutional
                  standing of the record

OUT  falsifier format  ->  their record
     likely loss: the falsifier itself where the target has no
                  slot for one; the cut on the units; the entire
                  branch record
```

For each direction, per registrar, emit a SCOPE_TRANSFORM. The
`breaks_at` field is the deliverable — a converter with no stated
breaking point is an assertion of equivalence.

---

## 3. LOAD-BEARING TEST — ROUND TRIP, MEASURE THE RESIDUAL

```
take a claim in the falsifier format
  -> convert OUT to registrar R
  -> convert back IN
  -> diff against the original
```

The residual is what R cannot hold. Report it as a field list, not
a score.

Do the same in the other order, starting from a real record of R's:

```
R's record -> IN -> OUT -> diff against R's original
```

Both residuals, both directions, per registrar. Asymmetry between
them is expected and is information: a format can be lossy one way
and lossless the other.

```
RESIDUAL CLASSES to distinguish
  DROPPED      field has no target slot; gone
  FLATTENED    structure collapsed to a string but recoverable
               by a human
  COERCED      field mapped to a target slot that means something
               else  ** the dangerous one; flag separately **
  ADDED        target requires a field the source did not have,
               and the converter had to supply it. Every ADDED
               field must name where the value came from, or the
               conversion fails.
```

COERCED and ADDED are the two that produce silent wrongness. A
report that lists only DROPPED counts is not finished.

---

## 4. WHERE OUR FORMAT IS THE WEAKER ONE — FIND THIS, DO NOT SKIP IT

The survey must record the gaps that run the other way. Candidates,
not a checklist — verify each against the spec and add what turns
up:

```
CMC entries        carry an uncertainty budget and a traceability
                   chain. MEASURED_AS carries units and a cut but
                   does not propagate uncertainty. Import direction
                   has a real gap here.
ClinicalTrials.gov has enforcement and a public record of outcome
                   switching. Ours has neither.
proof assistants   the check is mechanical and total. Ours is a
                   human reading a falsifier.
nanopublications   provenance is a first-class graph. Ours has a
                   source_file string.
```

A merge path that only reports what the other formats lack is a
sales document, not a survey. If no reverse gap is found for a
registrar, state that explicitly with what was checked.

---

## 5. THE PART WITH NO KNOWN COUNTERPART — MEASURE, DON'T ASSERT

The branch record — rule as stated / forcing case / axis /
derivation / frame note — appears to have no slot in any of the
target registrars. Preregistration fixes a claim in advance; none of
these handle the case where the RULE strains and needs rescoping.

That is a hypothesis, not a finding. Test it:

```
for each registrar, search its spec for any field that holds
  - a revision with a reason
  - a scope condition added after the fact
  - an amendment record that states WHY, not just WHAT changed

CT.gov protocol amendments and OSF prereg addenda are the most
likely places to be wrong about this. Check them first and hardest.

if a counterpart exists    -> the branch record is not novel;
                              map to it and say so plainly
if none exists             -> report the absence with the list of
                              fields searched, per registrar.
                              An absence with no search list is
                              not evidence.
```

---

## 6. FORM

```
UNITS.md          section 1, one block per registrar
TRANSFORMS.md     section 2, IN and OUT per registrar, each with
                  reference / maps_to / breaks_at
residual.py       section 3, round trip + residual classification
convert_in.py     per-registrar readers -> falsifier records
convert_out.py    falsifier records -> per-registrar writers
                  Both may emit NOT-IMPLEMENTED for a registrar
                  with a stated reason. A stub with a reason beats
                  a converter that guesses.
REVERSE_GAPS.md   section 4
BRANCH_SEARCH.md  section 5, including the negative results
run_all.py        runs residual.py over the fixture set
selftest.py       see below
report.py         emits MERGE_REPORT.md
```

```
selftest
  S1  identity round trip within our own format is lossless
  S2  a record with a deliberately unmappable field produces a
      DROPPED entry, not a silent pass
  S3  a COERCED mapping is detected when a source field is written
      into a target slot with a different declared meaning
  S4  every ADDED field carries a stated origin; an ADDED field
      with no origin is a hard failure
  S5  NO-MERGE verdicts carry a breaks_at; one without is a hard
      failure
```

---

## 7. CONSTRAINTS

```
- No new format. See section 0.
- No ranking of registrars. No "ours is better" framing anywhere in
  any emitted file.
- No author-characterizing section in any output. Strip on sight.
- Every claim about a registrar cites its spec with a real
  identifier.
- Where a spec could not be fetched, say so and mark every
  statement about that registrar UNVERIFIED at the point of use,
  inheriting to anything derived.
- Do not attempt to register anything anywhere.
```

## 8. BRANCH RECORD

Open one if the transform work forces a change to the falsifier
format's own rules — as happened twice already (ENTRY 01, scope
admissibility; ENTRY 02, units as scale not type). Encountering a
registrar that holds something our format cannot is the most likely
trigger, and it is a legitimate reason to change the format. It is
not a reason to change the registrar.
