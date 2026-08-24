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

**1. A source bath set and a leg bath set are two different quantities, and
the original table was carrying the first.**

Alpha decay is genuinely near-immune to substrate temperature and rail drift.
The nucleus does not care. The detector does — a PIN diode's leakage roughly
doubles every 7 °C, a PMT or Geiger tube needs a high-voltage rail, and both
sit on the board with everything else.

The first reading of `decay_alpha` at `baths={"COS"}` was that the readout
chain had been dropped. **That reading does not survive measurement.** The
readout baths are identical across all seven sources — TH, PWR and EM appear
in every one — so they are a constant, and a constant cannot separate pairs:

    distinct overlap sets, source baths only    2
    distinct overlap sets, source | readout     2      same partition

Adding the readout chain changes no pair ranking. A table built to rank pairs
by independence has a reason to carry the discriminating bath set and drop the
constant, and that reason was present in the original and not recovered on
first reading.

The readout chain does belong in the accounting — it was on the wrong object
twice. What discriminates is not which baths a source's readout touches, but
which readout elements two legs **share**, and sharing is a property of the
deployment:

    single board, one ADC              0 of 10 pairs clean
    split rail/clock/ADC, same board   0 of 10 pairs clean
    fully separate chains              7 of 10 pairs clean

`decay_alpha × rtd_tunnel` is source-disjoint and welds at the ADC. The
original `CLEAN` verdict is therefore recoverable rather than wrong: true for
a deployment nobody described, false for the compact one this folder is about.
Compactness forces the sharing, which is the squeeze — now priced rather than
asserted.

**2. The correlation rule is not where entropy hides — unless it carries key
material, which is a defined construction and was not recovered on first
reading.**

Read as a secret *algorithm*, "the correlation rule is where you can hide the
actual entropy" is security through obscurity: the rule is public under
Kerckhoffs, and hiding the combiner adds no min-entropy.

Read as a secret *seed*, it names a **seeded extractor** — a standard,
formally defined construction where the seed is key material and its secrecy
is priced as key, not as obscurity. That reading is legitimate and the first
audit of this folder did not recover it. Which reading applies is decided by
where the secret sits, and that is a design question the folder does not
settle.

What holds under both readings: the security is in the min-entropy, and the
independence measurement is what licenses the two-source construction that
needs no seed at all.

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
