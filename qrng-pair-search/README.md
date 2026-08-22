# QRNG PAIR SEARCH

Marker under exploration. Not a position under defence.

Candidate axes for two-source joint keying, where the unit of search is
`(source, bath_set)` and not `(source, name)`. Two sources coupled to
different baths beats two sources with different names.

CC0. Stdlib only.

```
python3 qrng_pair_search.py             # source table, pair verdicts, budgets
python3 qrng_pair_search.py --protocol  # the independence measurement
python3 qrng_pair_search.py --selftest  # 33/33
```

## THE SQUEEZE

Randomness wants real quantum indeterminacy. Independence wants sources whose
noise floors do not share a bath — different mechanism, ideally different
energy scale, no common thermal or EM path. Instrumentability wants both
readable at a rate and package size you can field.

The sources easiest to instrument in a small footprint are the ones most
likely to share an environment. Independence and compactness fight directly,
and that is the axis this table is organised along.

## THIS IS `category-weld/` RUN BACKWARDS

A category weld fuses quantities that are independent in the world into one
handle. Here the shared bath is the welder: two legs that are nominally
independent become one quantity when the environment moves them together. The
audit is the same instrument pointed the other way — there to expose an
assumed independence that is not there, here to establish one you need.

## THREE CORRECTIONS TO THE DELIVERED TABLE

**1. A bath set assigned to the source is not the bath set of the leg.**

Alpha decay is genuinely near-immune to substrate temperature and rail drift.
The nucleus does not care. **The detector cares.** A PIN diode's leakage
roughly doubles every 7 °C, a PMT or Geiger tube needs a high-voltage rail,
and both sit on the board with everything else. Pricing `decay_alpha` at
`baths={"COS"}` prices the physics and drops the readout chain.

So the delivered verdict —

    decay_alpha x rtd_tunnel   overlap {}   CLEAN

— is **false as fielded**. Every source here carries `source_baths` and
`readout_baths` separately, and pair verdicts use the union. Under that
accounting **no admissible pair is clean**: all ten are welded at TH/PWR/EM
through their readouts.

The source material names this failure mode in its own prose — "if both are on
the same board, same temperature, same power rail, the environment couples
them" — and the table beside it exempts `decay_alpha` from exactly those
baths. The prose and the table disagree. No authorship is assigned to either:
the material is co-produced and the layers are not separable from here. What
is audited is the table, because the table is what a pair verdict is computed
from.

**2. The correlation rule is not where entropy hides.**

"The correlation rule is where you can hide the actual entropy" is security
through obscurity. The rule is an algorithm; Kerckhoffs says price it as
public. Hiding the combiner adds no min-entropy, and an attacker who
compromises both legs is not additionally slowed by not knowing the XOR.

What the two-source structure actually buys is better than what it was being
credited with: **a two-source extractor needs no seed and no secrecy — it
needs independence**, which is the measurable thing. The security sits in the
min-entropy of the legs. The independence is what has to be established, and
it is establishable.

**3. Min-entropy, not Shannon.**

Correlated drift attacks min-entropy far harder than it attacks the average. A
pair whose Shannon entropy is barely dented can have its min-entropy halved by
a bath excursion pushing both legs the same way at the same time. The module
reports an XOR floor (guaranteed, survives one leg being fully compromised)
and a two-source target (a budget, requiring a named extractor), and subtracts
measured coupling from the second rather than assuming zero.

## THE VERDICT THAT REPLACES "CLEAN"

Three states, not two:

    structural weld   the SOURCES share a bath. Irreducible without changing
                      the physics of a leg. Shared pump laser is this.
    separable         sources share nothing; the LEGS share a bath through
                      their readouts. Reducible by engineering — and then it
                      must be MEASURED, not asserted.
    clean             neither. No pair in this table reaches it.

Seven of ten admissible pairs are separable. Those are the ones worth
building, because for them the weld is an engineering fact rather than a
physics one. `decay_alpha × rtd_tunnel` is the best of them on independence
and the worst on rate — the decay leg caps the pair at ~10^5 Hz, which is what
the namespace/payload split in `--protocol` exists to absorb.

## WHAT A CORRELATION SWEEP CAN ACTUALLY RESOLVE

Under the null the standard error of Pearson *r* is ~1/√N, so detecting *r* at
5σ needs N ≥ (5/r)². Scanning many lags is a multiple-comparison problem and
raises the count further.

    r >= 5e-3   1.0e6 samples    (100 lags: 1.4e6)
    r >= 1e-3   2.5e7 samples    (100 lags: 3.5e7)
    r >= 1e-4   2.5e9 samples    (100 lags: 3.5e9)

The delivered protocol says "over ≥1e6 samples". That resolves *r* ≥ 5×10⁻³
and is blind to anything smaller. Whether 5×10⁻³ is small enough is a
key-lifetime question this folder does not answer — but the count should be
set by the smallest correlation that would matter, not by a round number.

## THE VERDICT LINE THAT MATTERS

Coupling shows up under perturbation that is invisible at rest. **A
quiet-bench cross-correlation of zero is not evidence of independence; it is
evidence the bath was not moving.** The sweeps in `--protocol` are the
measurement; the resting XCF is only a precondition.

## WHAT WOULD BREAK IT

See `CLAIM_TABLE.md`. The load-bearing one: if a fielded pair with empty
structural overlap shows correlated drift that survives rail, thermal and EM
separation, then `separable` is not a real category and the three-state
verdict collapses back to two.
