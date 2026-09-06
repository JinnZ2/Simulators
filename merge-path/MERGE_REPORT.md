# MERGE_REPORT — claim registrars <-> falsifier format

Emitted by `report.py`. A transform survey, not a new format (§0). No
ranking; every registrar is reported on its own terms.

## Egress status (load-bearing)

The work order's §1 requires fetching each registrar's own specification
before mapping. In this environment the egress proxy is an allowlist and
every registrar spec host answered **403 to CONNECT** (probed
2026-09-05T03:30Z). So **no spec was fetched**, every real registrar below
is **UNVERIFIED**, and per §7 every statement about it inherits UNVERIFIED.
What is verified is the machinery, exercised on declared test doubles.

## Real registrars — UNVERIFIED, NO-MERGE (§0: a valid outcome)

| registrar | verified | verdict | breaks_at | spec (identifier, unfetched) |
|---|---|---|---|---|
| `nanopublications` | False | NO-MERGE | spec unfetched (egress 403) | https://nanopub.net/ (RDF; W3C provenance PROV-O https://www.w3.org/TR/prov-o/) |
| `orkg` | False | NO-MERGE | spec unfetched (egress 403) | https://orkg.org/ (Open Research Knowledge Graph) |
| `ro_crate` | False | NO-MERGE | spec unfetched (egress 403) | https://www.researchobject.org/ro-crate/ |
| `clinicaltrials_gov` | False | NO-MERGE | spec unfetched (egress 403) | https://clinicaltrials.gov/ (FDAAA 801; PRS data element definitions) |
| `cipm_cmc` | False | NO-MERGE | spec unfetched (egress 403) | https://www.bipm.org/ (CIPM MRA; CMC entries in the KCDB) |
| `proof_assistant` | False | NO-MERGE | spec unfetched (egress 403) | https://leanprover-community.github.io/ (mathlib) / https://coq.inria.fr/ |
| `osf_prereg` | False | NO-MERGE | spec unfetched (egress 403) | https://osf.io/prereg/ (OSF preregistration) |

Every NO-MERGE carries a `breaks_at` (§0, S5): the correspondence cannot
be established because the spec was not fetched. A NO-MERGE with a stated
breaks_at is worth more than a forced mapping — filling these in requires a
network fetch by someone whose egress reaches the spec hosts.

## Machinery — the residual classes, on declared test doubles

No row below is a claim about any real registrar; each mock is built to
exercise one residual class so the classifier is shown to fire on it.

| fixture | test double | residual classes |
|---|---|---|
| the RATES reading reproduces the p… | `MOCK_identity` | lossless |
| the RATES reading reproduces the p… | `MOCK_drops_branch` | lossless |
| the RATES reading reproduces the p… | `MOCK_coerces_falsifier` | COERCED=2 |
| the RATES reading reproduces the p… | `MOCK_flattens_measured` | FLATTENED=1 |
| the RATES reading reproduces the p… | `MOCK_requires_id` | DROPPED=1, ADDED=1 |
| SCOPE-DIFFERENT requires a transfo… | `MOCK_identity` | lossless |
| SCOPE-DIFFERENT requires a transfo… | `MOCK_drops_branch` | DROPPED=1 |
| SCOPE-DIFFERENT requires a transfo… | `MOCK_coerces_falsifier` | COERCED=2 |
| SCOPE-DIFFERENT requires a transfo… | `MOCK_flattens_measured` | lossless |
| SCOPE-DIFFERENT requires a transfo… | `MOCK_requires_id` | DROPPED=1, ADDED=1 |

`COERCED` and `ADDED` are the silent-wrongness classes and are counted
alongside `DROPPED` (visible as a zero when zero); a report of only
`DROPPED` counts is not finished (§3).
