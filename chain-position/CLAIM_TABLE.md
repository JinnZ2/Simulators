# CLAIM_TABLE -- chain-position

Permanent ids `CPD_NNN`. These are claims about the three instruments and
their behaviour on CONSTRUCTED data and the order's carried clause set,
distinct from the order's own OBSERVED / DERIVED / PROPOSED tags and its
runnable steps 1..4. Ids are permanent; a refuted claim is updated in place,
never renumbered. Status: SUPPORTED / REFUTED / UNVERIFIED.

`WORK_ORDER.md` (WO-1) is landed **verbatim** and edited by nothing here. No
vendor internals are used or sought anywhere in the folder; the OWASP clauses
are the public standard as the order carried it (fetched and verified by the
operator, NOT re-fetched here -- egress refuses the standard), and the
containers, tasks and records are constructed.

| id | status | claim |
|---|---|---|
| CPD_001 | SUPPORTED | **The clause audit returns the null result the order predicts, and the null is a measurement, not a floor.** Each OWASP clause the order lists is classified by where the observability sits; all five sit at the GATEWAY, so `inside_container` is 0 and the verdict is `NULL_RESULT_no_clause_places_position_inside` -- lineage exists and the container still cannot see it. A constructed clause that DOES place position inside the executing agent raises the count to 1 and flips the verdict, so the zero is not constant. |
| CPD_002 | SUPPORTED | **The fork is reported, neither horn selected.** `horn_fork` returns Horn A's failure (`RELOCATES` -- the outside thing is itself a container with its own local correctness) and Horn B's failure (`EVIDENCE_ABSENT` -- reasoning about something for which there is no evidence). An unknown source selects no horn (`UNDEFINED`, horn `None`) rather than inventing one; selecting a horn is downstream work, as the order says. |
| CPD_003 | SUPPORTED | **A locally-correct container cannot answer its chain position, and the absence is the container's, not the check's.** `evidence_check` over a container holding its task, its inputs and its own state returns `EVIDENCE_ABSENT` and names what would be needed (an observation of a step outside the boundary). Handed a whole-chain manifest, the same check returns `EVIDENCE_PRESENT` -- so the absence is a property of the locally-correct container by construction, which is Horn B's failure mode made decidable. |
| CPD_004 | SUPPORTED | **The reachable-controller compounding is made a number and the order's RULE is built in as a refusal.** `stability_product` composes the assumed stabilities as `product of (1 - p)`; the order's illustrative discontinuities (1/2/3/4 percent) give 0.90345024, so from four factors alone the reachable controller is absent about 9.65 percent of the time -- a crewed mission does not fly on that. An unassessed factor (`None`) returns `UNPROPAGATABLE`: an unquantifiable probability cannot be propagated through the calculation and is handled structurally. `stability_product` is registered in `tools/known_answer.py`. |
| CPD_005 | SUPPORTED | **A zero, an absence and a malformed factor are three states.** A factor of zero multiplies through (stability 1.0); an unassessed factor (`None`) makes the product `None` with state `UNPROPAGATABLE`; a factor outside [0,1] makes it `None` with state `MALFORMED`. The registered case set pins the unassessed `None` apart from the zero, so the RULE is in the metric, not only in the prose. |
| CPD_006 | SUPPORTED | **Dissimilar redundancy detects a fault only against a verifiable spec; the discriminator is spec-verifiability, not model diversity.** `redundancy_adjudicability` returns `FAULT_DETECTED` for disagreement against a verifiable spec, `NOISE_unadjudicable` for disagreement with no spec, and `NO_SIGNAL_agreement` for agreement of correlated copies. That settles the MECHANISM of the order's counter-argument (diversity may yield noise); the empirical question -- whether real model families disagree adjudicably -- needs model access and is NOT_RUN. |
| CPD_007 | SUPPORTED | **The engineering-gap register and the counter-arguments are carried, not decided.** Three gaps against load-bearing practice (no factor of safety, no inspectability under load, no ductile failure mode -- the chain lets go silently because every container stayed compliant) and two counter-arguments (diversity-may-be-noise, ductile-mode-is-a-signal) are carried from the order, both counter-arguments marked `UNRESOLVED`. Nothing here resolves them. |
| CPD_008 | SUPPORTED | **The second-order gap is a schema, and its load-bearing distinction is UNEXAMINED vs NOT_AUDITABLE.** `assignment_auditability` reads a payload-only record as `UNEXAMINED` (the record does not declare scorer provenance, so whether it is carried cannot be stated -- the order's "nobody can state whether scorer provenance is carried at all"), a declared-empty provenance as `NOT_AUDITABLE` (a known negative), and a complete record as `AUDITABLE`. Collapsing the first two would read a silence as a finding; keeping them apart is the absent-vs-known-negative repair. `PROVENANCE_SPEC` requires the scorer's OWN provenance, so the recursion (the score is a chained artifact) is in the spec. |
| CPD_009 | UNVERIFIED | **The order's scorer-provenance claim stays UNVERIFIED, by the order's own scope.** `common_object_exists` returns False: implementation varies by vendor and no vendor internals are used or sought, so there is no common object to audit, and "scorer provenance goes unexamined" is plausible, not established -- exactly the order's own tag on it. The specification of what an auditable assignment must carry is complete here; whether any deployed system carries it is not checkable from this folder. |
| CPD_010 | UNVERIFIED | **What is NOT_RUN, and the siblings.** Step 1's clauses are carried from the order, not re-fetched (the standard's host is egress-blocked), so the audit is over the order's clause set, not a live re-read; step 4's empirical test needs multiple model families and adjudication and is NOT_RUN; no vendor internals are touched. The order's sharpest open problem -- an engineering method by which the TOOL ITSELF knows when it is crossing the method, when it IS the method, and when it has been handed a binary gate to inspect rather than execute -- is stated, not solved, and a binary gate cannot carry it. WO-2..WO-5 are named-and-absent siblings, carried as references. No mitigation is specified, deliberately: the join is not published before the mitigation side exists. |

## What this folder does not establish

- That any deployed agent framework places chain-position information inside
  or outside the executing agent. The audit is over the order's carried clause
  set; a live clause-by-clause re-read of the standard is egress-blocked.
- That dissimilar redundancy across real model families yields adjudicable
  disagreement. The mechanism (spec-verifiability is the discriminator) is
  shown on constructed data; the empirical question is NOT_RUN.
- That any vendor's scorer provenance is or is not carried. No vendor
  internals are used or sought; the claim stays UNVERIFIED, as the order tags
  it.
- Any mitigation. The order withholds the mitigation side deliberately, and
  so does this folder.
