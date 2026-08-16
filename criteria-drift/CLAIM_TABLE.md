# CLAIM_TABLE — criteria-drift

Seven claims, `CD_001..007`.

## REFUTATION_PROTOCOL

The kit is delivered verbatim and is not modified. Claims here are about
what it measures and what it can conclude, checked by running it.

Two of the seven are mechanical defects with a demonstrated repair; three
are structural and cannot be fixed by editing a function; two are about
what holds.

A failed check updates the claim. It does not edit the kit to protect one.

## Claims

| id | statement | status |
| --- | --- | --- |
| `CD_001` | The kit runs end to end on its own quick start, stdlib only, SQLite-backed, and is the **first real consumer of the declared-frame block** — `Frame` is a first-class dataclass, `unknown` is legal, omission is flagged, and drift is computed per frame field. | SUPPORTED |
| `CD_002` | **The drift metric is unsigned and the decision rule reads the sign.** Every primitive returns a non-negative distance, so widening and narrowing both push `composite_drift` up. | SUPPORTED |
| `CD_003` | `build_series()` **plants a `y = 0.0` at the head of every model's series** and pairs it with a real drift value. For Alpha-1B it replaces a measured `−0.04`. | SUPPORTED |
| `CD_004` | `version_order` is built from `to_version`, so the **first criteria version and every score attached to it is dropped.** Delta-350M holds the longest baseline in the dataset and contributes nothing. | SUPPORTED |
| `CD_005` | `CD_003` and `CD_004` together **flip the sign** of the only model with three real transitions — between the two opposite readings the README's decision rule offers. | SUPPORTED |
| `CD_006` | **The capability term is in the stated model and not in the code.** `Δscore = β₀ + β₁·drift + ε` drops the unobservable term, so the drift slope absorbs it. The repair is already expressible in the shipped schema. | SUPPORTED |
| `CD_007` | *"Significant"* appears twice in `README.md` and **zero times in `regress.py`.** No t-statistic, no p-value. The fits that exist have one degree of freedom, and `r_squared: 1.0` at n=2 is emitted as a field next to an interpretation string saying the data is insufficient. | SUPPORTED |

---

## CD_002 — the drift metric is unsigned

The README separates three verdicts by the sign of β₁:

```
β₁ > 0, significant   criteria inflation explains some reported gain
β₁ ≈ 0                improvement is orthogonal to criteria drift
β₁ < 0                stricter criteria are masking real gains
```

Every primitive in `DriftEngine` returns a non-negative distance:

```
_str_drift      1 - jaccard(tokens)        [0, 1]
_list_drift     1 - jaccard(sets)          [0, 1]
_dict_drift     fraction of keys changed   [0, 1]
_numeric_drift  abs(v2 - v1) / max(...)    [0, 1]
```

Measured on the delivered engine:

```
boundary widened   → 0.3636      both positive; the magnitude gap is a
boundary narrowed  → 0.5714      token-count artifact, not direction

exemplar_count  100 → 1000   0.9000
                1000 → 100   0.9000      byte-identical

observer_access  unknown  → verified   1.0
                 verified → unknown    1.0      an ordinal compared as a
                 partial  → verified   1.0      nominal; direction and
                                                step size both discarded
```

So the instrument cannot distinguish the two readings it exists to
distinguish. The honest reading of a positive β₁ is: **score changes are
larger when the criteria moved a lot, in either direction.** That is a real
finding and it is not the stated one.

**Four of nine fields are signable from data already in the schema**, three
of them as one-line changes (`exemplar_count`: drop `abs()`;
`observer_access`: rank 0/1/2; `rubric_dimensions`: `|added| − |removed|`).
Three need a declared `direction` field, because whether a free-text
boundary widened or narrowed is a judgement the text does not contain —
`../declared-frame/` `DF_007`'s shape, arriving in a metric instead of a
checker. Two (`sign_source`, `logic`) have no natural direction and should
stay unsigned.

**Falsifier:** a signed composite that reproduces the delivered `composite`
under `abs()`. Then the sign is recoverable post hoc and no schema change is
needed.

**Evidence:** `drift_sign.py` §1–§5.

---

## CD_003, CD_004, CD_005 — the series, and what it costs

```
model        scores on record              y as built            planted
Alpha-1B     v1.0,v2.0,v3.0,v3.1-hard      [0.0, -0.03, -0.07]   1 of 3
Beta-7B      v2.0,v3.0,v3.1-hard           [0.0,  0.07, -0.04]   1 of 3
Delta-350M   v1.0,v3.1-hard                (empty)               —
Gamma-70B    v3.0,v3.1-hard                [0.0,  0.03]          1 of 2
```

The head point is not padding. Alpha-1B has a real `v1.0 → v2.0` delta of
`−0.04` at drift `0.2971`, and the series records `+0.00` at that same x.

`version_order = [p["to_version"] for p in pairs]`, so `v1.0` is never in
the series and Delta-350M — scored at the **first and last** version, the
only pair spanning every criteria change — filters down to one score,
`len(ordered_scores) < 2`, and returns `([], [])`.

Corrected: every transition whose both endpoint scores exist, no planted
head, first version included.

```
model        as shipped              corrected
Alpha-1B     n=3 slope=-0.0782       n=3 slope=+0.0526      ← SIGN FLIP
Beta-7B      n=3 slope=+0.2835       n=2 slope=+0.6482
Delta-350M   n=0 (no fit)            n=0 (below 2)
Gamma-70B    n=2 slope=-0.1768       n=1 (below 2)
```

Alpha-1B is the only model with three real transitions, and shipped versus
corrected put it on **opposite sides of the README's own decision rule**.

After correction the demo supports one n=3 fit and one n=2. The shipped `n`
column is inflated by the planted head, not by having more data.

**Falsifier:** a reading of `build_series` under which the head `0.0` is
intended — a declared convention that the first observation is an origin.
Then it is a documentation gap rather than a defect, and the sign flip is
still real.

**Evidence:** `regression_audit.py` §1–§3.

---

## CD_006 — the term that is not there

The research program states:

```
reported = β₀ + β₁·actual_capability_gain + β₂·criteria_drift + ε
```

`regress.py` runs:

```
Δscore = β₀ + β₁·composite_drift + ε
```

The capability term is dropped because it is unobservable, and anything it
shares with drift loads onto the reported slope. The two are not plausibly
independent: **a benchmark is revised because models saturated it**, so
drift is downstream of capability — the reverse of the direction the slope
is read in.

`../anchor-interval/moving_reference.py` puts a number on the underlying
problem. Under `reported = a·c + b`, a capability rising 117% with a fixed
ruler and a capability that never moves under a ruler stretching 117%
produce the same published series to `5.6e-17`. One equation, two unknowns,
per release.

**The repair is already expressible in the shipped schema.** `ModelScore`
keys on `(model, artifact, version)`, so scoring every model on the **first**
version alongside its contemporary one is a legal ingest today. The
divergence between the two series isolates the criteria term — and
identifies capability only up to the fixed version's own unknown gain and
offset, so what it buys is a **share, not a capability**
(`../anchor-interval/` `ANC_006`).

Nothing in the CLI asks for it. In the example data, **0 of 4 models** carry
scores on more than one non-current version — the one design that cannot
separate the two terms.

**Falsifier:** an identifying restriction that does not require a fixed
benchmark — an item whose difficulty is fixed by construction, or an
external anchor with known gain. Then capability is recoverable without the
second series and the repair is unnecessary.

**Evidence:** `regression_audit.py` §5.

---

## CD_007 — the decision rule asks for a test the code does not run

`README.md` twice: *"If the slope is positive **and significant**"*,
*"β₁ > 0, **significant**"*.

`regress.py` contains no `signific`, no `p_value`, no `t_stat`. What the
demo produces:

```
model        n   slope      se        t       df
Alpha-1B     3   -0.0782    0.2363    -0.33   1
Beta-7B      3   +0.2835    0.2745    +1.03   1
Delta-350M   0   (no fit)
Gamma-70B    2   -0.1768    inf       n/a     0
```

One degree of freedom on the fits that have any, and no t near a
conventional threshold. The interpretation string reports the sign and R²
without either.

`R² = 1.000` at n=2 is arithmetic — two points define a line. `_interpret()`
guards it with *"Insufficient data for reliable inference"*, and `to_dict()`
emits `r_squared: 1.0` in the same object. **The guard is in the sentence,
not in the data**, so a consumer reading the field gets a perfect fit.

**Falsifier:** a use of the kit where the interpretation string is the only
consumed output. Then the guard is where it needs to be and the field is
internal.

**Evidence:** `regression_audit.py` §4.

## Related

- `../anchor-interval/` — `ANC_005` (capability and criteria not separable
  from a contemporary score), `ANC_006` (a fixed benchmark buys a share),
  `ANC_007` (seven co-moving terms, `N_eff` 1.22). `CD_006` is that argument
  arriving in a tool built to run it.
- `../declared-frame/` — the frame block this kit consumes; `DF_003`
  (free-text comparison) becomes the measurand here rather than the check,
  and `DF_007` (nothing in the block evaluates) is why three fields cannot
  be signed from text.
- `../uninstrumented/` — `AUTHORED REFERENCE` is this kit's whole subject;
  `SCALAR DEMAND` inverted is `CD_002`'s ordinal-as-nominal result.
- `../null-harness/` — `CD_007` is the missing gate: a statistic reported
  without the test that would let it fail.
