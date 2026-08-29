# reservoir-chain-coupling — CLAIM_TABLE

`RCC_001..RCC_009`. Claims about the delivered `SOURCE_DROP.md` and
about the operator swap it turns on.

**This drop's core claim is not hydraulics, and that is why it can be
run here.** The spec reduces the coupling term to an *operator swap* —
`max(wave, pool)` versus `wave + pool` against a breach threshold — and
that is arithmetic. `operator_swap.py` is the arithmetic; `chain.py` is
the spec's own minimal falsifiable test on constructed chains, with the
routing engine held to an **abstract combiner** that is explicitly not a
hydraulic solver.

**Nothing here is a claim about any real reservoir.** All node values
are synthetic and labelled; whether the effect is load-bearing for a
real chain is the HEC-RAS run on published data, which needs the engine
and the terrain — unreachable here, and the subject of
`columbia-chain-cascade`.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `RCC_001` | **The operator swap is arithmetic and its mechanism is provable**: `max` and `sum` disagree exactly when both terms are individually sub-threshold and their sum is not. | SUPPORTED |
| `RCC_002` | **The bias is one-sided**: `max(a,b) ≤ a+b`, so independent-node evaluation never breaches a node coupled evaluation does not — it can only understate the chain. | SUPPORTED |
| `RCC_003` | **The disagreement band width equals the antecedent pool**, so the spec's "antecedent state is the gain" is exact: a node near crest has a wide band of waves it passes as safe and coupled physics does not. | SUPPORTED |
| `RCC_004` | Outside that band the operators agree in both directions, which is why the same mechanism supplies the null test. | SUPPORTED |
| `RCC_005` | **On a constructed chain the swap is load-bearing and compounds downstream** — a breach at one node raises the wave into the next, which a one-node reach study cannot produce. | SUPPORTED |
| `RCC_006` | The harness is not `CONSTANT_FIRES`: two constructed nulls (full freeboard, no freeboard) report the spec's own REFUTED verdict. | SUPPORTED |
| `RCC_007` | The finding is FIRM — it survives a sweep of the synthetic routing coefficients — so it is a property of the operator swap, not of the toy's magnitudes. | SUPPORTED |
| `RCC_008` | This delivers the antecedent-coupling amplifier `columbia-chain-cascade` `CCC_001` flagged as truncated, in initiator-agnostic form; the governance claim is the general form of that folder's, cross-referenced not recomputed. | SUPPORTED |
| `RCC_009` | Whether the coupling is load-bearing for any real chain is UNVERIFIED — that is the HEC-RAS run on published data, unreachable here. | UNVERIFIED |

---

## RCC_001 — the mechanism is arithmetic and provable

The spec states the error as an operator swap:

    independent-node:  breach iff  max(wave, pool) >= crest
    coupled:           breach iff      wave + pool  >= crest

`max` and `sum` give different breach verdicts exactly when

    max(wave, pool) < crest <= wave + pool

i.e. when the wave alone does not reach the crest, the pool alone does
not, but the two together do. That is not a modeling subtlety — it is
the definition of a threshold nonlinearity, and it is checkable by
enumeration, which the selftest does over a full sweep of small
integers.

The spec's sentence *"a wave and a pool that each stay under a breach
threshold can cross it together — `max` cannot see this, `sum` can"* is
exactly this region, and it is non-empty whenever the antecedent pool is
positive.

**Falsifier:** an input where `max` and `sum` disagree outside that
region. Enumeration finds none.

## RCC_002 — the bias is one-sided

`max(a, b) ≤ a + b` for non-negative `a, b`. Therefore the independent
breach verdict implies the coupled one: if `max(wave, pool) ≥ crest`
then `wave + pool ≥ crest`. The converse fails. So:

    independent-node evaluation NEVER breaches a node that coupled
    evaluation does not.

Every disagreement is the independent side **understating**. This is the
same shape as `extraction-blindness-sim`'s one-sided blindness operators
— the error has a sign, and the sign is always toward reporting the
chain as safer than the coupled physics says. The selftest sweeps
`crest ∈ [1,14]`, `pool ∈ [0,crest)`, `wave ∈ [0,20)` and asserts the
forbidden case (independent-only) never occurs, and that the permitted
case (coupled-only) does, so the claim is not vacuous.

**Falsifier:** a single `(wave, pool, crest)` where independent breaches
and coupled does not. It cannot exist for non-negative terms.

## RCC_003 — the band width equals the antecedent pool

Coupled breaches when `wave ≥ crest − pool` (the freeboard). Independent
breaches when `wave ≥ crest` (since the pool alone never reaches the
crest, `max` is decided by the wave). So the two disagree precisely for

    crest − pool  ≤  wave  <  crest

a half-open interval of width exactly **`pool`**.

That is the spec's *"antecedent state is the gain"* made exact and
quantitative. The gain is not a metaphor: the width of the wave band on
which independent-node evaluation is wrong is numerically equal to how
full the reservoir was at event onset. A node at half pool has a band
half the crest wide; a node with full freeboard has no band at all.

**Falsifier:** a band width that is not the pool. `disagreement_band()`
returns `pool` and the selftest checks it across several crest/pool
pairs.

## RCC_004 — outside the band the operators agree

Below the freeboard, neither breaches: `wave + pool < crest` and
`max < crest`. At or above the crest, both breach. The swap is decisive
only in the middle band.

This is why the mechanism is also the null: a chain whose antecedent
state keeps every node out of the band produces identical breach sets
under both operators, and the harness must — and does — report that as
the spec's refutation verdict. `RCC_006`.

**Falsifier:** disagreement below the freeboard or above the crest. The
`disagree()` sweep finds none.

## RCC_005 — on a constructed chain the swap is load-bearing, and compounds

The signal chain (four nodes, pools placing the boundary wave in each
node's band):

    boundary inflow 6
    RUN 1 (independent, max):  breach set none
    RUN 2 (coupled, sum):      breach set [A, B, C, D]

    node   independent      coupled
    A        4.20            9.00 BREACH
    B        2.94           12.00 BREACH
    C        2.06           15.00 BREACH
    D        1.44           18.00 BREACH

Under independent evaluation the wave attenuates down the chain and
reaches no crest. Under coupled physics the breach at A adds stored
water to the wave into B, which breaches and adds to the wave into C —
**the difference compounds downstream.**

This is the spec's *"attenuation and amplification only appear across
nodes ... a reach study cannot produce the answer"*: a one-node study
sees node A, whose independent verdict is "no breach", and stops. The
cascade is a property of the chain, not of any node.

The **compounding is SOFT** — its magnitude depends on the synthetic
release gain — but the **existence and direction are FIRM** (`RCC_007`):
under coupled evaluation the breach set is a proper superset of the
independent one whenever any node is in its band.

**Falsifier:** a chain in the band whose breach sets are identical. The
selftest asserts the signal chain's are not, across the coefficient
sweep.

## RCC_006 — the harness is not CONSTANT_FIRES

Two constructed nulls, each reporting the spec's own REFUTED verdict:

    high freeboard (crest 100, pool 1):  breach sets identical -> REFUTED
    no freeboard   (crest 10, pool 10):  breach sets identical -> REFUTED

The first: no wave in the chain reaches any crest, so the coupling term
is genuinely negligible — the spec's *"if the breach sets are identical,
the coupling term is negligible and this claim is refuted"*. The second:
every pool is already at crest, so even `max` breaches everything and
the swap changes nothing.

A detector that reported "load-bearing" on these would be
`CONSTANT_FIRES` in `null-harness` terms. It does not. And the two nulls
bound the effect: the swap is decisive only in the intermediate
antecedent-state band, exactly `RCC_003`.

**Falsifier:** a null chain reported load-bearing. The selftest asserts
both report REFUTED.

## RCC_007 — the finding is FIRM under a coefficient sweep

`route()` carries two synthetic coefficients — a breach release gain and
an intact-node attenuation — with no physical calibration. The finding
must not depend on them, or it is a property of the toy rather than of
the operator swap.

The selftest sweeps release gain ∈ {1, 3, 6, 10} × attenuation ∈
{0.3, 0.5, 0.7, 0.9} and asserts, across all 16, that the signal chain
stays load-bearing and the high-freeboard null stays refused.

This is the `sustained-activation-gate` FIRM/SOFT discipline: the
one-sided bias, the band width, and the existence of downstream
compounding are FIRM (arithmetic, coefficient-independent); the specific
magnitudes and the mapping to real dam breach are SOFT.

**Falsifier:** a coefficient setting that flips the signal or null
verdict. The sweep finds none.

## RCC_008 — this is the amplifier the sibling folder flagged as missing

`columbia-chain-cascade` `CCC_001` recorded that the delivered spec
there was truncated mid-sentence in *"MODULE F — ANTECEDENT CONDITION
COUPLING (the amplifier) ... it changes the cascade outcome at the
next"*, and that the amplifier mechanism was not in hand and was not
reconstructed.

This drop is that mechanism, delivered in initiator-agnostic form: the
`ANTECEDENT STATE` section here is the node-specific gain Module F named,
and `RCC_003` is its exact statement. It arrived as a **separate
standalone spec**, not as a literal completion of the truncated file, so
`CCC_001` is cross-referenced rather than marked continued — the Columbia
node list and the HEC-RAS build detail are not in this document.

The governance section is the **general form** of the sibling's:
*"mixed ownership → no single entity's plan spans the chain → the
aggregation step has no owner."* The sibling's `eap_coverage.py`
computed the Columbia instantiation (authorities lower bound 2, settled
by the CA/US boundary); this spec carries no node list, so the claim is
cross-referenced, not recomputed. Import, not copy — and here there is
nothing to import, so it is a pointer.

**Falsifier:** the two documents disagreeing on the coupling mechanism.
They do not; this is the fuller statement of the same claim.

## RCC_009 — whether it is load-bearing for a real chain is unverified

Everything established here is arithmetic or runs on synthetic chains.
The one thing that would make it a statement about a real river — that
some real chain's antecedent state puts its nodes in the disagreement
band during a real event — is exactly what this environment cannot
compute.

The spec's minimal falsifiable test is *"run the same chain twice on
identical published data."* Published data (3DEP, NOAA, NID) and the
2D unsteady solver (HEC-RAS) are both unreachable here — measured in
`columbia-chain-cascade`. So the test is run on constructed chains,
which can only show the swap is *detectable* and *can* be load-bearing,
never that it *is* for any named structure.

**Falsifier:** run the spec's test on real published data through
HEC-RAS. RUN 2 breaching nodes RUN 1 does not is the load-bearing
result; identical breach sets refute it for that chain. That is the
study; this is the arithmetic that says the study is worth running.
