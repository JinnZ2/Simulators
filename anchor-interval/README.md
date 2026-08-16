# anchor-interval

A system fitted to a corpus it also writes into. Its internal checks
improve while its coupling to anything unauthored falls, and the check that
would catch it is computed inside the layer it would be checking.

Delivered notes in [`SOURCE_DROP.md`](SOURCE_DROP.md), verbatim. Three of
the structures in them are runnable; this folder runs them.

```
corpus_loop.py        the loop, two detectors, the anchor interval
moving_reference.py   "the model drifted" as a difference between two
                      moving things
recoverability.py     provenance decides; timing only gets to matter
                      afterwards
CLAIM_TABLE.md        ANC_001..011 with falsifiers
```

Stdlib only, deterministic, seed 20260816. Sample runs in `samples/`.

---

## corpus_loop.py

```
corpus -> model -> outputs -> corpus
```

No adversary and no bad actor. The only ingredient is that a fit is not an
identity map — any shrinkage toward a prior, `lam` in the code — and a path
from output back to input.

| reading | needs | run |
| --- | --- | --- |
| coherence, model vs the corpus it was fitted to | nothing outside the loop | 0.0677 → 0.0481 **better** |
| corpus shift, corpus now vs corpus then | nothing outside the loop | 0.0520 → 0.0035 **quieter** |
| coupling, model vs a substrate the system did not author | a reference no actor inside wrote | 0.3604 → 0.4141 **worse** |

At `lam = 0` the loop is a fixed point and coupling drift falls from
`+0.0537` to `+0.0063`. The effect is carried by the shrinkage, not by
feedback alone.

**D1 — model against its own corpus — is `CONSTANT_SILENT`, and it gets
quieter as the drift proceeds.** It fell 29.0% while coupling error rose
14.9%, monotonically. It is not measuring drift; it is measuring how much
of the corpus the model has yet to write.

**D2 — corpus now against corpus then — is a real detector, and it does not
discriminate.** Run as a `../null-harness/` sweep: the degrading arm is the
known signal, the improving arm is the known null, and the two differ in
exactly one branch, the provenance of what gets injected.

```
threshold      TP         FP         TP - FP
0.00292        0.994      1.000      -0.006
0.03784        0.060      0.083      -0.024
0.07277        0.012      0.042      -0.030
0.14261        0.000      0.042      -0.042
0.17753        0.000      0.000       0.000

FP >= TP at EVERY threshold on the sweep: True
verdict: NO_DISCRIMINATION
```

Worse than undiscriminating — **anti-correlated**. Correcting a 0.35 bias
displaces the corpus more than shrinking toward a pooled mean does, so a
monitor tuned to fire on real degradation fires harder on real repair. The
only threshold with `TP − FP = 0` is the one that fires on nothing.

So the anchor interval has to be **scheduled**:

| anchoring | final coupling err |
| --- | --- |
| none | 0.4141 |
| every 12 | 0.3867 |
| every 4 | 0.2747 |
| every 2 | 0.1629 |
| triggered by internal confidence | 0.4141 — never fires, 0 of 24 generations |

Not a convenience. It is the only form the interval can take, because the
statistic that would trigger it is computed inside the layer it would be
detecting.

---

## moving_reference.py

Drift measurement assumes a fixed reference the model moved against. What
is there is a benchmark, a rater pool, an annotation guideline and a
curation criterion, each versioned, each set by a cohort with its own
formation.

```
reported_k = a_k * c_k + b_k
```

**Not separable.** A capability rising 117% with a fixed ruler, and a
capability that never moves at all under a ruler stretching 117%, produce
the same published number to `5.6e-17`. One equation, two unknowns per
release. A rank problem, not a precision problem — no amount of data fixes
it.

**A held-fixed benchmark is the right measurement and buys a share, not a
capability.** Scoring every generation on `B_0` identifies capability only
up to `B_0`'s own unknown gain and offset, so ratios of differences are
identified (`0.428571` recovered exactly) and levels are not. The
divergence between the contemporary and fixed curves *is* the criteria-drift
term.

And if the old benchmark reads as obsolete rather than as a control, that
judgment came from inside the thing being measured.

**Seven terms moved, one number reported.**

```
co-movement    N_eff     reading
0.00           6.409     terms separable      <- apparatus floor, not 7
0.50           5.500     terms separable
0.70           3.239     partly confounded
0.95           1.216     one direction
```

`N_eff` is the participation ratio of the correlation spectrum — the
statistic `../model-ecology/phylogeny.py` already computes, on a different
substrate.

What makes the co-movement non-removable by a better ablation: the
architectural term was **selected against** the corpus. Attention shapes
fitted to language statistics, tokenizers to the writing system, context
lengths to document lengths, objectives to what the corpus can score. The
covariance was built in before any experiment started. Small-scale ablations
do isolate, and small-scale results are known not to transfer reliably
upward, so the isolated result is not the one that ships.

Falsifier: an architectural term chosen without reference to the corpus
should decorrelate the pair.

---

## recoverability.py

Two positions that cannot both hold in the same conditions:

```
drift-literature remedy   detect drift -> retrain on recent data
                          presupposes a clean reference obtainable on demand

irrecoverability claim    a baseline is only acquirable during a stable
                          interval; once the system is deviating there is
                          no clean reference to acquire
```

They are not two opinions about one regime. They are two regimes, and one
measurable quantity separates them: **`f`, the fraction of the
re-acquisition pool that is downstream of the system being corrected.**

**Regime I, independent provenance.** Timing decides. Sampling longer buys
precision and costs survival probability, so the optimum is interior,
finite, and moves with the shift interval — `t_acq = 6, 12, 25` at
`t_shift = 20, 60, 200`. Everything here is an argument about scheduling.

**Regime II, downstream provenance.** Averaging kills the variance and does
not touch the bias.

```
n         f=0.00   f=0.10   f=0.30   f=0.60   f=1.00
100       0.0470   0.0260   0.0510   0.1595   0.3030
100000    0.0009   0.0359   0.1062   0.2105   0.3509
floor     0.0000   0.0350   0.1050   0.2100   0.3500
```

A 10,000× increase in sample count buys nothing once the floor is reached.
At bias 0.35 and a stated tolerance of 0.05, above `f = 0.143` the target is
not slow to reach — it is outside the reachable set at any `n`, and no
schedule changes that.

`f` is a provenance audit, answered by labelling the pool, not by analysing
it. Both positions have something to lose depending on how it comes back:
`f ≈ 0` collapses `K15` in `../measurement-fork/` into an ops step and fails
the mediation prediction resting on it; `f` above the floor means the
retraining remedy has a precondition it does not ask anyone to report.

---

## What is not checked here

`SOURCE_DROP.md` says of itself that its citation markers are mangled and
unresolvable and that one venue attribution is unconfirmed. No claim in
`CLAIM_TABLE.md` rests on a literature fact. `ANC_010` records the coverage
reading and the three pieces of named prior art as **UNVERIFIED** — a gap,
not a negative verdict.

`ANC_011` — the creek-crossing case, and "literature contains what survives
removal of the body" — is **OPEN** with a named instrument: `../inverseminar/`'s
`CANNOT DERIVE` channel. No round has been run.

## Related

- `../null-harness/` — `CONSTANT_SILENT` and the known-null/known-signal
  sweep. Both detectors here are graded by that invariant.
- `../model-ecology/` — `N_eff`; and `confound_sweep.py`'s window result is
  the same shape as the moving-benchmark result on a different substrate.
- `../measurement-fork/` — `f` decides `K15`'s status; the coverage reading
  is a second instrument on that folder's empty `SAME QUANTITY` cell.
- `../declared-frame/layer_zero.py` — the layer-0 / layer-1 split from this
  drop, applied to that folder's tool.
- `../instrument-epistemology/` — a benchmark with unknown gain and offset
  is an instrument without reference standards.
- `../inverseminar/` — named in `ANC_011`.

CC0.
