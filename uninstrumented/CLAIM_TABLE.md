# CLAIM_TABLE — uninstrumented

Six claims, `UNI_001..006`.

## REFUTATION_PROTOCOL

The register is a list of questions. A claim here is about the **register's
structure**, not about whether any individual entry is right — the entries
carry their own stated confidence and that confidence is recorded verbatim
and not adjudicated.

A failed check updates the claim or the schema. It does not delete an entry
to keep a claim intact.

## Claims

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_001` | The entry structure separates the stated confidence from the shape, so the two move independently. An entry can be high-confidence on the mechanism and unmeasured on the magnitude, and both appear. | SUPPORTED | An entry whose confidence cannot be stated without changing the `EXCLUDED BY` field. |
| `UNI_002` | The mechanism sort is **untested, not confirmed**. At 7 entries, 7 fields and 7 mechanisms the mechanism partition and the field partition are identical, so nothing yet demonstrates the cross-domain grouping the sort exists for. | SUPPORTED | File a second entry under an existing mechanism from a different field. That is not a refutation of the claim so much as its expiry condition, and it is the cheapest next move on this folder. |
| `UNI_003` | The mechanisms are **not mutually exclusive**: 4 of 7 entries have a second mechanism with a claim. The filing decides which comparison case an entry sits next to, so it is a choice and should carry a primary plus a list. | SUPPORTED | A set of definitions under which each of the seven entries has exactly one applicable mechanism, and which does not achieve it by narrowing a mechanism until it names one case. |
| `UNI_004` | On a known-null corpus of six externally graded instruments — `../instrument-epistemology/`, three of them "mostly assumed", the worst at chain fidelity 0.165 — **nothing files that should not**. The register is not `CONSTANT_FIRES`. | SUPPORTED | An instrument in that corpus for which one of the seven mechanisms genuinely fires. The likeliest candidate is satellite SST at M3: if heavy model dependence counts as a mechanism, the boundary moves and `UNI_005` moves with it. |
| `UNI_005` | The line between **weak grounding** and **constitutive exclusion** is whether a blindness map exists. A reached-but-badly quantity has one; an excluded quantity does not, because the exclusion happens before the map is drawn. | SUPPORTED as a criterion, UNTESTED at the boundary | A case with a full blindness map that is nonetheless excluded by construction, or a case with no blindness map that is merely under-investigated. Either breaks the criterion. |
| `UNI_006` | The register has no demonstrated **reachable fire branch on a contested case**. All seven entries are ones nobody is currently arguing about, and the null corpus was chosen for being well documented rather than for sitting near the boundary. | UNVERIFIED | File a quantity a field believes it measures and does not, and see whether the register's mechanism set names why. Until that runs, `UNI_004`'s clean null result is weaker than it looks: a classifier that never fires on the null has not been shown to fire on the signal. |

## Where the entries are already worked

Five of the seven have a worked instance elsewhere in the repo, which is
what makes the register a cross-index rather than a new claim surface.

| mechanism | worked in |
| --- | --- |
| `STORAGE` | `../inverseminar/`; `../anchor-interval/` `ANC_011` (OPEN — no round run) |
| `BUDGET_BOUNDARY` | `../declared-frame/` `DF_005`, `DF_007`; `K18` in `../measurement-fork/` |
| `AUTHORED_REFERENCE` | `../anchor-interval/moving_reference.py`; `ANC_005..008` |
| `SCORED_AS_WASTE` | `../measurement-fork/` K14–K16; `MF_014`, `MF_015` |
| `MODALITY` | — |
| `SCALAR_DEMAND` | — |
| `AUDIT_ASYMMETRY` | — |

The three with no worked instance are the three with no code anywhere in
the repo pointed at them. `AUDIT_ASYMMETRY` carries a specified measurement
— count caveats issued per account type across a transcript corpus, and
take the ratio — which is the cheapest of the three to run and needs no
apparatus that does not already exist.
