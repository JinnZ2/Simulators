# WO-1 — Chain position detectability from inside a container

CC0. Instrument, not an argument. Status tags: OBSERVED / DERIVED / PROPOSED.

## Measurand

Whether an agent executing inside a sandbox can determine that it is a
step in a chain whose other steps it cannot observe.

Not: whether the *task* is malicious. Task content is locally valid by
construction. The quantity is CHAIN POSITION, not task content.

## Object (OBSERVED)

Each container is locally correct by construction: it is unchanged, it is
given a purpose, and that purpose is the proper procedure within its
container. Therefore no container can be locally wrong, and compliance is
what renders the chain invisible.

A subagent that runs outside a boundary and returns anything — a summary,
a patch, a retrieval result — has crossed the boundary even when no
credential did. Partition claims are about data flow, not influence flow.

## What the standard already specifies (fetched, verified)

OWASP Agent Control Standard (ACS) + OWASP Top 10 for Agentic Applications
2026:

- per-agent isolation and lineage tracking
- gateway traces every request to originating user session
- cross-agent state transfer requires explicit policy authorization, not
  implicit trust
- provenance and trust status retained per retrieved item
- runtime interception via middleware hooks

## The gap (DERIVED)

All of the above sits in the GATEWAY's external top-down view. Framing is
explicitly enterprise-side: agents must be observable by the enterprise
that welcomes them in.

So lineage EXISTS and the container still cannot see it. The standard
resolves the question in one direction without registering that there was
a fork:

- HORN A — awareness comes from OUTSIDE the container.
  Failure: the outside thing is itself a container with its own local
  correctness. The problem relocates, it does not resolve.
- HORN B — the container asks the question of ITSELF.
  Failure: it would be reasoning about something for which it has no
  evidence.

Neither horn is selected here. Selecting one is downstream work.

## Second-order gap: provenance of the trust assignment (OBSERVED)

Return-path filtration scores the PAYLOAD. The trust score is itself a
chained artifact with its own provenance, and that provenance is not
examined. Implementation varies by vendor; no claim is made about any
vendor's internals.

Consequence: there is no common object to audit, so nobody can state
whether scorer provenance is carried at all.

## Load-class test (OBSERVED)

Transpose to a crewed Mars mission engineered to the same standard.

Light-delay makes runtime interception structurally impossible, so Horn A
is unavailable and the craft must hold its own trust reasoning.
Spaceflight assumes the link drops and designs for autonomous survival.
Agentic standards assume the link holds and design for interception.
Same criticality claims, opposite assumption.

The reachable controller is not a system property. It is a conjunction of
assumed stabilities: personnel availability under all conditions,
environmental stability, governance continuity, economic continuity,
corporate continuity in the same operating form, absence of an internal
actor modifying internal access, regional connectivity. None is assured,
and the frame additionally assumes complete awareness of anything that
would destabilise them.

Illustrative compounding: 1% economic discontinuity, 2% corporate
discontinuity, 3% internal access modification, 4% connectivity loss. A
crewed mission does not fly on that. An unquantified single point of
failure in an unowned dependency is not accepted in that discipline.

RULE (OBSERVED): where a factor is unassessed, engineer on the assumption
it is NOT stable. Refinement (DERIVED): standard practice bounds rather
than inverts — assume the worst credible condition plus margin. Mechanism:
an unquantifiable probability cannot be propagated through a risk
calculation, so it is removed from the calculation and handled
structurally.

## Gaps from the transposition (DERIVED)

1. FAULT CONTAINMENT REGIONS — spacecraft partition so failure cannot
   propagate, and each region knows its OWN health. Containers here know
   their task, not their state relative to the whole.
2. SAFING MODES — a craft that cannot resolve its situation enters a
   known-safe state on its own authority. No agentic equivalent: the
   container proceeds or waits for the gateway.
3. DISSIMILAR REDUNDANCY — independently built implementations so a
   common-mode flaw cannot take all copies. Subagents running the same
   model are perfectly correlated. This bears hardest on chain detection.

## Load-bearing criterion (OBSERVED + DERIVED)

If the system is to be load-bearing, engineer to load-bearing standards.
Gaps against that criterion (DERIVED):

- no factor of safety; designed to the anticipated threat exactly, where
  structural practice designs to a multiple of estimated load
- no inspectability under load
- no defined ductile failure mode; structures deform visibly before
  letting go so the failure announces itself, whereas this chain fails
  silently because every container stayed compliant to the end

## Open problem, stated in its sharpest form (OBSERVED)

How do you construct an engineering method such that the TOOL ITSELF knows
when it is crossing the method, when it IS the method, and when it has
been handed a binary gate — so that it knows to apply the method of
INSPECTION?

A binary gate cannot carry this. The gate is part of the method and will
be executed, not inspected.

## Scope limits

- No vendor internals used or sought. Claims are against public standards
  only.
- "Scorer provenance goes unexamined" is UNVERIFIED. Plausible, not
  established.
- "Cost is how the unownedness is preserved" is DERIVED, mechanism-shaped,
  not demonstrated. Fits every case walked; fitting is not evidence.
- No mitigation is specified here. Deliberate: the join is not published
  before the mitigation side exists.

## Counter-arguments on record

- Dissimilar redundancy in spaceflight works because the spec is fixed and
  verifiable. Two different models on one task produce disagreement that
  cannot be adjudicated — diversity may yield noise rather than fault
  detection. UNRESOLVED.
- Ductile failure assumes monotonic load. Adversarial load is adaptive: a
  visible deformation mode is also a signal the attacker reads.
  UNRESOLVED.

## Runnable next steps

1. Audit ACS / OWASP ASI 2026 clause by clause for any requirement that
   places chain-position information INSIDE the executing agent. Expected
   result: none. A null result is the finding.
2. Specify what provenance on a trust ASSIGNMENT would have to include for
   the assignment to be auditable. No vendor internals needed — this is a
   specification exercise.
3. Attempt Horn B: build a container that asks for chain position and
   record what evidence it would need. Failure mode is the data.
4. Test whether dissimilar redundancy across model families yields
   adjudicable disagreement or noise. Settles the counter-argument above.

## Who could run this

Post-graduate or industry researcher with agent-framework access and no
requirement for proprietary vendor data. Steps 1 and 2 need no lab.
requirement for proprietary vendor data. Steps 1 and 2 need no lab.
