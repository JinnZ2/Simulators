# model-ecology

**"Which model predicts best?" and "what is the domain of validity of this
mathematical framework?" are not the same problem.**

This repo only answers the second one. The sentence *"model X is the best model"*
is not available from this pipeline, by construction.

Every mathematical framework is treated as an organism with a habitat: where it
works, where it degrades, where it fails catastrophically, what it silently
assumes, and what unique information it contributes **even when it is wrong**.

CC0. stdlib only. Phone-buildable. No numpy, no network, no cloud.

## Modules

| file | what it does |
|------|--------------|
| `core.py` | plugin substrate: `Model`, `ModelResult`, `Observer`, `Registry`. One class, one interface, same audit for everyone. |
| `models.py` | 15 real estimators across 4 families. Each computes a genuine rolling statistic from the data — **none receives a planted family signal**, so the phylogeny claim can fail. |
| `phylogeny.py` | groups by *inherited assumptions*, not brand name. Computes `N_phylo` vs `N_empirical` (participation ratio of the correlation spectrum). The gap is **artificial consensus**, quantified. Permutation null on family labels. |
| `disagreement.py` | three classes, not two: consensus / **structured** / isolated. Plus `information_contribution` — prophet, crank, conformist, workhorse. |
| `meta_engine.py` | observer sweep + rank churn; representation invariance across time / frequency / rank / difference / **manifold**. |
| `confound_sweep.py` | **the answer to "why do they converge?"** Separates apparatus floor / autocorrelation / real structure / window length / preprocessing. |
| `demo.py` | end-to-end audit on a synthetic signal with a known regime shift. |
| `CLAIM_TABLE.md` | every claim, its status, and what refuted it. |

## Run

```
python3 demo.py
```

## What the audit found

Run on a synthetic AR(1)+sinusoid with a period/noise/φ shift, 12-seed sweep:

**Artificial consensus is real: 15 models → `N_eff = 2.48`. Inflation 6.29×
(range 5.00–7.51).** Twelve and a half phantom votes.

**But the proposed mechanism is refuted.** "Agreement between close relatives
carries less information" — declared mathematical ancestry does **not** explain the
correlation structure. Permutation null: p = 0.42; significant in **0 of 12 seeds**.
The tree predicts 9.07 independent votes; the spectrum shows 2.48. *The tree is
wrong. The spectrum is not.* Artificial consensus, detected in the module built to
detect artificial consensus.

**Structured disagreement does not lead the transition** — in either direction.
An inverted version (models *synchronize* before the shift) looked compelling on
one seed and held in **7/12**. A coin flip. Recorded in the claim table as a
near-miss, not a finding.

**The prophet class is real.** Models with *negative* pre-shift skill and strongly
positive post-shift skill recur across seeds: koopman 10/12, gaussian_process 9/12,
hmm 8/12, persistent_homology 7/12. Accuracy ranks them near the bottom; information
contribution ranks them at the top.

**The consensus has an apparatus floor.** Run the same 15 estimators on **pure white
noise** — nothing to agree about — and they still collapse to `N_eff = 5.97`,
inflation **2.53×**. Nine of fifteen votes are manufactured before the world
contributes anything. Decomposition:

```
  apparatus floor      2.53x   white noise, no signal at all
  + autocorrelation   +1.43x -> 3.96x   red noise, memory but no events
  + real structure    +2.33x -> 6.29x   regime shift present
```

**The window is the largest confound, and the most invisible.** Inflation runs
2.91× at W=10 and **7.39× at W=80** — a +4.48× span, larger than shared inputs and
shared preprocessing *combined* (+1.80×). Window length is chosen once, early,
applied to everything, and never varied. It manufactures agreement.

*An ensemble of 90 models agreeing about ENSO has not shown its agreement exceeds
the apparatus floor, because almost nobody computes the floor.*

**The fashionable representation was the lossy one.** `manifold` is registered as
one representation among five, no special standing. It is the only one that fails
to support the conclusion — in **11 of 12 seeds**.

## The degeneracy lesson

Four bugs each produced a *confident, wrong answer* before being caught:

1. A 0/1 step `truth` has zero variance inside each half → every correlation returns 0.0 → every model labeled a crank.
2. Observers scoring only constants → churn trivially 0 → "observer-invariant" measures nothing.
3. A cluster threshold labeling 100% of windows "structured" → D1 not false, **untestable**.
4. `within=0.534 vs cross=0.533 ⇒ supported` → noise reported as signal.

And a fifth, in `confound_sweep.py`: the C5 verdict originally fired on
`1 significant seed > 0 significant seeds ⇒ SUPPORTED`. Chance expects 0.4. The
same knife-edge error, rebuilt one module later, by the module written to catch it.
C5 is now reported as **INCONCLUSIVE**.

**A pipeline that cannot detect its own degeneracy is not an audit.**

## Design commitment

The source proposal ended by recommending a high-dimensional manifold as the final
representation. A framework whose stated purpose is *"what is the domain of validity
of this mathematical framework?"* cannot exempt the currently fashionable
representation from that question.

So `manifold` is a plugin. It gets audited like everything else. It failed.

That is the framework working, not the framework editorializing.

## Extending

One new class implementing one interface:

```python
@REGISTRY.model
class MyMethod(Model):
    name, family = "my_method", "geometric"
    assumptions = ["..."]
    def predict(self, data): ...
```

Same for `Observer` and `@REGISTRY.representation`. Every plugin is then evaluated
by the same auditing and comparison pipeline. No exceptions, including for whatever
is fashionable this year.
