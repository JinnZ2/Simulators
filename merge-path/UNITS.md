# UNITS — section 1, one block per registrar

**Egress status (read first).** The work order's §1 requires fetching each
registrar's own specification and recording what its atomic record actually
contains, and says explicitly *do not work from summaries, including this
document's*. In this environment the egress proxy is an allowlist and every
registrar spec host answered **403 to CONNECT** (probed 2026-09-05T03:30Z;
the proxy logged `nanopub.net:443`, `clinicaltrials.gov:443`, `w3.org:443`
among the refusals). **No spec was fetched.**

Therefore every block below is **UNVERIFIED**. The `atomic record` /
`required fields` / etc. lines are **not transcribed from a spec and not
fabricated from memory**; they carry only the work order's own §1 candidate
summary, marked as such, precisely the summary §1 says not to rely on. The
`identifier` line is the spec URL a fetch would go to — an identifier, not a
fact about the record shape. Per §7, everything derived from these blocks
(the transforms in `TRANSFORMS.md`, the reverse gaps in `REVERSE_GAPS.md`,
the branch search in `BRANCH_SEARCH.md`) **inherits UNVERIFIED**.

To finish section 1: fetch each spec from a network that reaches these hosts
and replace each block's UNVERIFIED lines with the spec's real data
dictionary. Until then the honest state of this file is *the inventory was
not performed here*.

---

## nanopublications — UNVERIFIED (spec not fetched)

```
atomic record      candidate (work order §1, unverified): an RDF nanopub
                   = assertion / provenance / pub-info graphs
required fields    UNVERIFIED — spec not fetched
who enforces       candidate: nobody (a format, not a gate)
when it fires      candidate: never (specified, largely unenforced)
what a violation   UNVERIFIED
  costs
identifier         https://nanopub.net/ ; PROV-O https://www.w3.org/TR/prov-o/
```

## ORKG — UNVERIFIED (spec not fetched)

```
atomic record      candidate: a structured contribution / comparison
required fields    UNVERIFIED
who enforces       candidate: reviewers / curators
when it fires      UNVERIFIED
what a violation   UNVERIFIED
  costs
identifier         https://orkg.org/
```

## RO-Crate — UNVERIFIED (spec not fetched)

```
atomic record      candidate: a packaged research object + metadata
required fields    UNVERIFIED
who enforces       candidate: nobody / tooling
when it fires      UNVERIFIED
what a violation   UNVERIFIED
  costs
identifier         https://www.researchobject.org/ro-crate/
```

## ClinicalTrials.gov — UNVERIFIED (spec not fetched)

```
atomic record      candidate: registered primary outcome + measure +
                   time frame
required fields    UNVERIFIED
who enforces       candidate: a regulator (FDAAA 801)
when it fires      candidate: on submission; enforced continuously
what a violation   candidate: legal penalty / public non-compliance record
  costs
identifier         https://clinicaltrials.gov/ (PRS data element definitions)
```

## CIPM / CMC entries — UNVERIFIED (spec not fetched)

```
atomic record      candidate: a capability claim + uncertainty budget +
                   traceability chain
required fields    UNVERIFIED
who enforces       candidate: a regulator / peer review (CIPM MRA)
when it fires      candidate: at review
what a violation   UNVERIFIED
  costs
identifier         https://www.bipm.org/ (CIPM MRA; KCDB CMC entries)
```

## proof assistants (mathlib-style) — UNVERIFIED (spec not fetched)

```
atomic record      candidate: the claim IS the statement; the check IS
                   the proof
required fields    UNVERIFIED
who enforces       candidate: a compiler (mechanical, total)
when it fires      candidate: continuously (the build)
what a violation   candidate: rejection (the proof does not typecheck)
  costs
identifier         https://leanprover-community.github.io/ ; https://coq.inria.fr/
```

## OSF preregistration — UNVERIFIED (spec not fetched)

```
atomic record      candidate: a hypothesis + analysis plan, ahead of data
required fields    UNVERIFIED
who enforces       candidate: nobody (a timestamped record, not a gate)
when it fires      candidate: on submission, before data
what a violation   candidate: nothing (a public discrepancy, not a penalty)
  costs
identifier         https://osf.io/prereg/
```

## OURS — the falsifier / branch-record format (in this repository)

This one is not fetched over the network; it is the format implemented here
(`dependency-survey/`, `claim-record/`, the branch-record convention).

```
atomic record      a claim + a falsifier + MEASURED_AS (quantity /
                   units-with-a-cut / how obtained) OR a SCOPE_TRANSFORM
                   (reference / maps_to / breaks_at), plus an optional
                   branch record (rule as stated / forcing case / axis /
                   derivation / frame note)
required fields    claim, falsifier; then MEASURED_AS xor SCOPE_TRANSFORM
who enforces       a human reading the falsifier; a selftest for the
                   admissibility bars
when it fires      at authoring / at review
what a violation   the claim is not admitted (downgraded), or a branch
  costs            entry is opened
identifier         this repo; ADDENDUM_01 (scope), ADDENDUM_02 (units)
```
