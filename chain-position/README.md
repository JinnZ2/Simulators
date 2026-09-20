# chain-position

WO-1: whether an agent executing inside a sandbox can determine that it is a
step in a chain whose other steps it cannot observe. The quantity is CHAIN
POSITION, not task content -- task content is locally valid by construction, so
compliance is what renders the chain invisible.

`WORK_ORDER.md` is the order, landed **verbatim**. WO-2..WO-5 are named-and-
absent siblings, carried as references. No vendor internals are used or sought
anywhere in the folder; the OWASP clauses are the public standard as the order
carried it (fetched and verified by the operator, not re-fetched here -- egress
refuses the standard), and the containers, tasks and records are CONSTRUCTED.
No mitigation is specified, deliberately -- the order withholds the mitigation
side until it exists, and so does this folder.

## Three instruments

**`chain_position.py` -- the measurand.** The order's runnable step 1, made
decidable: `clause_audit` classifies each OWASP clause by WHERE the
observability sits, and every clause the order lists sits at the gateway, so
none places chain-position information inside the executing agent. The order's
expected result is that null, and the null IS the finding -- lineage exists and
the container still cannot see it. It is not constant: a constructed clause that
does place position inside raises the count. The two horns are reported with
their failure modes (`RELOCATES` / `EVIDENCE_ABSENT`), neither selected;
`evidence_check` shows a locally-correct container cannot answer its chain
position and names what would be needed, while the same check answers once a
whole-chain manifest is handed in -- so the absence is the container's, not the
check's.

**`load_class.py` -- the load-bearing criterion, made numbers.** The reachable
controller is a CONJUNCTION of assumed stabilities, and `stability_product`
composes them: the order's illustrative compounding (1/2/3/4 percent
discontinuities) gives 0.9035, so the controller is absent about 9.65 percent
of the time from four factors alone. The order's RULE -- where a factor is
unassessed, engineer as though it is not stable -- is built in as a refusal: an
unassessed (`None`) factor returns `UNPROPAGATABLE`, a zero factor multiplies
through, and a factor out of range returns `MALFORMED`, three distinct states.
`stability_product` is registered in `tools/known_answer.py`.
`redundancy_adjudicability` settles the mechanism of the order's own
counter-argument: dissimilar redundancy detects a fault only against a
verifiable spec, so the discriminator is spec-verifiability, not model
diversity (`FAULT_DETECTED` / `NOISE_unadjudicable` / `NO_SIGNAL_agreement`);
whether real model families disagree adjudicably is NOT_RUN. The engineering-gap
register (factor of safety, inspectability under load, ductile failure) and the
two counter-arguments are carried, both counter-arguments `UNRESOLVED`.

**`trust_provenance.py` -- the second-order gap.** The order's runnable step 2,
a specification exercise with no vendor internals: `PROVENANCE_SPEC` states what
a trust ASSIGNMENT (not just the payload) must carry to be auditable, including
the scorer's OWN provenance -- the score is a chained artifact, so the recursion
is the gap. `assignment_auditability`'s load-bearing distinction is `UNEXAMINED`
(the record does not declare scorer provenance, so whether it is carried cannot
be stated) versus `NOT_AUDITABLE` (declared absent, a known negative);
collapsing the two would read a silence as a finding. `common_object_exists`
returns False, so the order's claim that scorer provenance goes unexamined stays
UNVERIFIED -- plausible, not established, as the order tags it.

## Running it

```
python3 chain_position.py         # the clause audit, the fork, the evidence check
python3 load_class.py             # the compounding, the register, adjudicability
python3 trust_provenance.py       # the auditability spec and its states
python3 <module>.py --choices     # the [CHOICE n] markers
python3 test_chain.py             # the checks; prints their count
```

All three modules refuse `--selftest` (exit 2) and render on bare invocation.
All three renders screen clean through `sheet-structure-scan/no_severity` with
no exemption.

## Scope, carried from the order

The measurand is decided on constructed containers and the order's carried
clause set; a live re-read of the standard (step 1), the empirical
dissimilar-redundancy test (step 4), and any statement about a vendor's scorer
provenance are NOT_RUN -- egress, model access, and no-vendor-internals
respectively. The order's sharpest open problem -- a method by which the tool
itself knows when it is crossing the method, when it IS the method, and when it
has been handed a binary gate to inspect rather than execute -- is stated, not
solved. Permanent-id findings in `CLAIM_TABLE.md` (`CPD_`). Stdlib only, parses
under 3.9, phone-buildable, CC0.
