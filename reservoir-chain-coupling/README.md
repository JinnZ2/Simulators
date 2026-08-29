# reservoir-chain-coupling

Serial reservoir chains are evaluated per-structure — each node its own
design flood, its own breach study, its own emergency plan scoped to its
owner. The spec's claim is that this treats nodes as separable when they
are not: `outcome(node n)` **is** the initial condition of node `n+1`.

The error reduces to an **operator swap**:

    independent-node:  breach iff  max(wave, pool) >= crest
    coupled physics:   breach iff      wave + pool  >= crest

`SOURCE_DROP.md` is delivered verbatim.

## Why this one runs here, when the last did not

The sibling `columbia-chain-cascade` was a HEC-RAS build spec needing an
engine and terrain this environment cannot reach. **This drop's core
claim is not hydraulics — it is arithmetic**, and the spec's own minimal
falsifiable test is a two-run comparison of `max` against `sum`. That is
runnable with the standard library and no data.

    python3 reservoir-chain-coupling/operator_swap.py  # the arithmetic
    python3 reservoir-chain-coupling/chain.py          # the falsifiable test
    python3 reservoir-chain-coupling/selftest_rcc.py   # the checks

**Nothing here is a claim about any real reservoir.** All node values
are synthetic and labelled. Whether the coupling is load-bearing for a
real chain is the HEC-RAS run on published data — unreachable, and the
subject of the sibling folder.

## The arithmetic (`operator_swap.py`)

Three results, each provable:

**The bias is one-sided.** `max(a,b) ≤ a+b` for non-negative terms, so
independent-node evaluation **never** breaches a node coupled evaluation
does not. Every disagreement is the independent side understating — the
error has a sign, always toward reporting the chain as safer than it is.

**The disagreement band width equals the antecedent pool.** The two
operators disagree precisely for `crest − pool ≤ wave < crest`, an
interval of width exactly `pool`. The spec's *"antecedent state is the
gain"* is exact: a node near crest has a wide band of waves it passes as
safe and coupled physics does not; a node with full freeboard has no
band at all.

**Outside the band they agree**, in both directions — which is why the
same mechanism supplies the null test.

## The falsifiable test (`chain.py`)

The spec's RUN 1 (independent, `max`) versus RUN 2 (coupled, `sum`) on
constructed chains. `route()` is an **abstract combiner, not a hydraulic
solver** — it advances a scalar wave down a chain of scalar pools
against scalar crests, a breach adding a fixed release and an intact
node attenuating by a fixed factor, every coefficient synthetic and
marked. The only difference between the two runs is the combine
operator.

**Signal chain** (pools placing the wave in each node's band):

    RUN 1 (independent):  breach set none
    RUN 2 (coupled):      breach set [A, B, C, D]

Under independent evaluation the wave attenuates away; under coupled
physics a breach at A raises the wave into B, which breaches and raises
it into C — **the difference compounds downstream**, which a one-node
reach study cannot produce.

**Two nulls**, so the detector is not `CONSTANT_FIRES`:

    high freeboard:  breach sets identical -> REFUTED
    no freeboard:    breach sets identical -> REFUTED

The first has no wave reaching any crest (coupling genuinely
negligible); the second has every pool already at crest (even `max`
breaches all). The swap is decisive only in the intermediate
antecedent-state band.

## FIRM and SOFT

The one-sided bias, the band width, and the *existence* of downstream
compounding are **FIRM** — arithmetic, asserted to survive a sweep of
the synthetic coefficients. The specific magnitudes and the mapping to
real dam breach are **SOFT**. The selftest sweeps release gain × attenuation
over 16 settings and asserts the signal stays load-bearing and the null
stays refused throughout.

## Relation to `columbia-chain-cascade`

That folder's `CCC_001` recorded the delivered spec ending mid-sentence
in *"MODULE F — ANTECEDENT CONDITION COUPLING (the amplifier)"*, with
the amplifier not in hand and not reconstructed. **This is that
mechanism**, delivered as a separate initiator-agnostic spec. `CCC_001`
is cross-referenced, not marked continued — this document carries no
Columbia node list and no HEC-RAS build detail.

The governance section is the general form of the sibling's *"mixed
ownership → no single entity's plan spans the chain."* The sibling's
`eap_coverage.py` computed the Columbia instantiation; this spec has no
node list, so it is cross-referenced rather than recomputed.

## Files

| file | what |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim, not edited |
| `operator_swap.py` | the arithmetic of the swap; no chain, no data |
| `chain.py` | the falsifiable test on synthetic chains; abstract combiner |
| `selftest_rcc.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `RCC_001..RCC_009` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs of both modules |

Both modules refuse `--selftest` rather than exiting 0 on an invocation
that runs nothing. No `no_severity` exemptions — every screen hit was
reworded.

## Scope

Nothing here is a claim about any real reservoir, breach, or population.
The output products the spec names (velocity bands, time slices,
exposure overlay) are response-side extensions of the HEC-RAS run and
are not touched here. What is established is that the operator swap is
real arithmetic, one-sided, gated by antecedent state, and able to
compound down a chain — and that whether it bites for a real chain is a
study on published data this environment cannot reach.

CC0. Stdlib only, parses under 3.9, phone-buildable.
