# TRANSFORMS — section 2, IN and OUT per registrar

Each transform is a SCOPE_TRANSFORM: `reference` (what the registrar's
record is taken against), `maps_to` (its correspondent in the falsifier
format), `breaks_at` (where the correspondence fails). The `breaks_at` is
the deliverable — a converter with no stated breaking point is an assertion
of equivalence (§2).

**All UNVERIFIED, and every one is a NO-MERGE here, for one reason.** The
specs were not fetched (egress 403 CONNECT, 2026-09-05T03:30Z), so no
`maps_to` can be established and the honest `breaks_at` for every registrar
in both directions is the same: *the specification was not fetched, so the
correspondence cannot be established*. This is a valid, reportable outcome
(§0): NO-MERGE with a stated breaks_at, worth more than a forced mapping.
Filling in a real `maps_to`/`breaks_at` requires a network fetch by someone
whose egress reaches these hosts.

The two directions lose different things even before the spec is read —
those general losses (from §2, carried unverified) are stated so the shape
of the eventual transform is on record.

```
IN   their record  ->  falsifier format
     general loss (§2): provenance graph structure, enforcement status,
     uncertainty budget, the legal/institutional standing of the record

OUT  falsifier format  ->  their record
     general loss (§2): the falsifier itself where the target has no slot;
     the cut on the units; the entire branch record
```

---

Per registrar, both directions, as the state stands here:

| registrar | direction | reference | maps_to | breaks_at |
|---|---|---|---|---|
| nanopublications | IN | RDF assertion/provenance/pub-info graphs (unverified) | UNVERIFIED | spec not fetched (egress 403); correspondence not established |
| nanopublications | OUT | the falsifier format | UNVERIFIED | spec not fetched; and (§2) our format has no first-class provenance graph, only a source string |
| ORKG | IN | structured contribution (unverified) | UNVERIFIED | spec not fetched; correspondence not established |
| ORKG | OUT | the falsifier format | UNVERIFIED | spec not fetched |
| RO-Crate | IN | packaged research object + metadata (unverified) | UNVERIFIED | spec not fetched; correspondence not established |
| RO-Crate | OUT | the falsifier format | UNVERIFIED | spec not fetched |
| ClinicalTrials.gov | IN | registered outcome + measure + time frame (unverified) | UNVERIFIED | spec not fetched; and (§4) our format has no enforcement or outcome-switch record |
| ClinicalTrials.gov | OUT | the falsifier format | UNVERIFIED | spec not fetched |
| CIPM / CMC | IN | capability claim + uncertainty budget + traceability (unverified) | UNVERIFIED | spec not fetched; and (§4) MEASURED_AS carries a cut but does not propagate uncertainty |
| CIPM / CMC | OUT | the falsifier format | UNVERIFIED | spec not fetched |
| proof assistant | IN | the statement; the proof is the check (unverified) | UNVERIFIED | spec not fetched; and (§4) our check is a human reading a falsifier, not a total mechanical proof |
| proof assistant | OUT | the falsifier format | UNVERIFIED | spec not fetched |
| OSF prereg | IN | hypothesis + analysis plan ahead of data (unverified) | UNVERIFIED | spec not fetched; correspondence not established |
| OSF prereg | OUT | the falsifier format | UNVERIFIED | spec not fetched |

The machinery that would classify the residual of each transform once a
`maps_to` exists is implemented and tested (`residual.py`, `convert_out.py`,
`convert_in.py`, `selftest.py`): DROPPED / FLATTENED / COERCED / ADDED, with
COERCED and ADDED — the silent-wrongness classes — reported alongside
DROPPED. It runs today on declared test doubles; it runs on a real registrar
the moment that registrar's slot map is filled from a fetched spec.
