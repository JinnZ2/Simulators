# CLAIM_TABLE — model-ecology

Every claim is refutable. **Refutation protocol: when a claim fails, update the
claim. Never retune the detector.** Results below are from a 12-seed sweep on the
synthetic regime-shift signal in `demo.py`, not from a single favorable run.

## Status legend
`SUPPORTED` · `REFUTED` · `UNTESTABLE` (detector has no dynamic range) · `SCOPE-LIMITED`

---

## Phylogeny

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **P1** | Same-family models correlate more than cross-family models, above chance. | **REFUTED** | within \|r\|=0.534 vs cross \|r\|=0.533. Permutation null over family labels: **p=0.42, mean p=0.755 across 12 seeds, significant in 0/12.** The gap is noise. |
| **P2** | The family tree (`N_phylo`) tracks the correlation spectrum (`N_empirical`). | **REFUTED** | \|N_phylo − N_empir\| = 6.60. Tree predicts 9.07 independent votes; spectrum shows 2.48. **The tree is wrong. The spectrum is not.** |
| **AC** | Naive model count massively overstates independent evidence. | **SUPPORTED** | 15 models → **N_eff = 2.48**. Inflation **6.29× mean (5.00–7.51) across 12 seeds.** 12.5 phantom votes. |

**Consequence of P1+P2 failing.** The *mechanism* proposed by the source document —
"discount agreement between close relatives, grouped by inherited assumptions" —
is **not validated by this data.** Consensus inflation is real and large, but
**declared mathematical ancestry does not explain it.** The correlation structure
is real; the taxonomy laid over it is decoration. Either the family labels are
wrong, or correlation among estimators is driven by something other than declared
ancestry (window length, smoothing, shared preprocessing). Revise the tree.

This is the repo's own thesis applied to the repo: *artificial consensus, detected
in the module built to detect artificial consensus.*

---

## Disagreement

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **D1** | Structured disagreement rises *before* a regime transition, more than isolated disagreement does. | **REFUTED** | Across discriminating thresholds: Δstructured = **−0.292**, Δisolated = +0.033. It *falls*. |
| **D1′** | *(rejected candidate)* Models **synchronize** before the transition — consensus is the leading indicator. | **REFUTED** | Looked compelling on seed 3 (total 15-model consensus spanning the shift). **Held in only 7/12 seeds — a coin flip.** Promoted to a claim, it would have been a single-seed artifact. Recorded here as a near-miss, not a finding. |
| **D1″** | Cluster-regime (consensus / structured / isolated) is a leading indicator of transition *in any direction*. | **REFUTED on this signal class** | Neither direction survives the seed sweep. Scope: AR(1)+sinusoid with a period/noise/φ shift. Untested on real geophysical data. |
| **D2** | "Wrong" partitions into prophet / crank / conformist / workhorse; a model with low accuracy can carry the highest information contribution. | **SUPPORTED** | Prophets (negative pre-skill, strongly positive post-skill, high dissent) recur across seeds: **koopman 10/12, gaussian_process 9/12, hmm 8/12, persistent_homology 7/12.** IC ranks them top-4 while accuracy ranks them near the bottom pre-shift. |

**D1 required a threshold sweep to be testable at all.** At thresh 0.60 the detector
labeled 100% of windows "structured" — no dynamic range. That is not evidence
against D1; it is *no evidence*. Reporting saturation as refutation would have been
a measurement error dressed as a result.

---

## Meta / observer / representation

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **M1** | Observer-invariance is measurable: perturb only observer parameters, measure rank churn. | **SUPPORTED as a method** | churn = 0.257 (seed 3); mean 0.245 across seeds. Non-invariant in **6/12** seeds — i.e. right at the tolerance boundary. |
| **M1a** | This dataset's model ranking is observer-invariant. | **SCOPE-LIMITED / borderline** | Ranking churns (0.245 mean), but the *winner* is stable: hilbert wins under 30/32 observer profiles. **Rank order is observer-sensitive; the argmax is not.** These are different claims and must not be conflated. |
| **M2** | A conclusion surviving k representations is more trustworthy than one surviving 1. | **SUPPORTED as a method; untested as an epistemics claim** | The conclusion "a regime transition occurred" survives time, frequency, rank, difference — and **fails under `manifold` in 11/12 seeds.** |

### The manifold result

`manifold` was registered as one representation among five, with no special
standing, precisely because the source document proposed it as the privileged
final representation. It is **the only representation that fails to support the
conclusion, in 11 of 12 seeds.**

Read this carefully. It does **not** show manifold representation is wrong. The
projection onto the first principal delay-coordinate direction discards the
variance change that the conclusion function tests for — so the failure is
partly a property of *this* conclusion function. What it does show:

> A representation chosen because it is fashionable will not announce which
> structures it destroys. Only auditing it against rivals reveals that. The
> framework proposed manifolds as the answer; the framework's own audit flags
> manifolds as the one lossy channel.

---

---

## Confound decomposition (`confound_sweep.py`)

P1 failed but inflation was real. The correlation matrix was reporting **one number
that was a sum of four sources**: real signal structure, shared measurement window,
shared preprocessing, and genuine estimator kinship. Attributing it to kinship was
never licensed by the data. This module separates them.

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **C1** | Inflation on pure noise is ~1.0× — no phantom consensus without signal. | **REFUTED. There is an apparatus floor.** | White noise, *nothing to agree about*: **N_eff = 5.97, inflation 2.53×.** ~9 of 15 votes are manufactured before the world contributes anything. |
| **C2** | Breaking input coupling (per-model window offsets) reduces inflation. | **SUPPORTED** | 6.29× → 5.54× (**−0.76×**) |
| **C3** | Diversifying preprocessing reduces inflation. | **SUPPORTED** | 6.29× → 5.25× (**−1.04×**) |
| **C2+C3** | Both together. | **SUPPORTED** | 6.29× → **4.49×** (−1.80×). N_eff rises 2.42 → 3.57. |
| **C4** | Inflation depends on window length. | **SUPPORTED, and it is the largest single axis.** | W=10 → 2.91×; W=20 → 4.58×; W=40 → 6.29×; W=80 → **7.39×**. Span **+4.48×**. At W=80, N_eff = 2.06 out of 15. |
| **C5** | Phylogeny *emerges* once confounds are removed (P1's failure was an artifact). | **INCONCLUSIVE — deliberately not promoted.** | Mean p moved 0.749 → 0.464, correct direction. But significant in **1/8 seeds**, and chance expects 0.4/8. **One hit is not evidence.** Reporting `1 > 0 ⇒ supported` is the exact knife-edge error this repo exists to catch. It was in the first draft of the verdict logic and was removed. |

### The inflation decomposition

```
  apparatus floor        2.53x    white noise — nothing to agree about
  + autocorrelation     +1.43x -> 3.96x    red noise — memory, no events
  + real structure      +2.33x -> 6.29x    regime shift present
```

**40% of the observed consensus is present with no signal at all.** The estimators
agree because they are all squinting through the same 40-point window, not because
the world has structure.

### What this means for ensembles

An ensemble of 90 models reporting agreement about ENSO has not shown that its
agreement exceeds the apparatus floor — because **almost nobody computes the floor.**
The floor is computable: run the identical ensemble on white noise and red noise
matched to the data's autocorrelation, and measure `N_eff`. Anything below that is
the instrument talking to itself.

This is the metrology identity applied to models rather than thermometers:

> `corruption(trend) = corruption(measurement) ⊗ corruption(framework)` — multiplicative.
> **You cannot audit the framework while the measurement is shared.**

And the largest confound is the most invisible one: **window length**. It is chosen
early, chosen once, applied to everything, and never varied. It manufactures more
consensus (+4.48×) than input sharing and preprocessing combined (+1.80×).

---

## Scope bounds

- All results are from **one synthetic signal class** (AR(1) + sinusoid, shift in period/noise/φ at t=170), 12 seeds. Nothing here has touched real ENSO data. Nothing here should be quoted as a claim about ENSO.
- `N_eff` via participation ratio of the correlation spectrum assumes linear dependence. Nonlinearly-dependent estimators can appear independent to it. The 6.29× inflation is therefore a **lower bound** on artificial consensus.
- The four "species" thresholds in `information_contribution` are hand-set. They are a taxonomy, not a test.
- 15 estimators is small. `N_eff = 2.48` from 15 models says little about what `N_eff` would be from 90.

## What this repo actually established

1. **Artificial consensus is real, large, and measurable** (6.29× inflation). ✅
2. **Declared mathematical ancestry does not explain it.** The proposed mechanism is refuted. ❌
3. **Low-accuracy models carry the most information across a transition** — the prophet class is real and reproducible. ✅
4. **Disagreement structure is not a leading indicator** on this signal class, in either direction. ❌
5. **The fashionable representation was the lossy one**, and only the audit surfaced it. ✅
6. **A pipeline that cannot detect its own degeneracy is not an audit.** Four degeneracies (zero-variance truth, constant observer inputs, saturated threshold, knife-edge P1) each produced a confident, wrong answer before being caught. ✅
