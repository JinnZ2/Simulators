# CLAIM TABLE — residual-direction

Claims from building work order 3. `WORK_ORDER.md` is untouched.

**REFUTATION PROTOCOL.** The fixtures are the claim. A check that fails
updates the claim or the fixture, never the tool's output to suit it.

---

### RDD_001 — the pooled sign test misses F1, exactly as the order says

| | |
|---|---|
| pooled sign, fraction positive | **0.5083**, no lean at 2 standard errors |
| S2(a), residual vs predicted magnitude | standardized **0.868**, lean |

F1 overpredicts below the midpoint and underpredicts above it. Pooled,
that is symmetric. The order's PASS condition for F1 is *pooled sign
returns no-lean AND S2(a) fires*, and both hold — which is what makes
the conditional test more than a preference.

Pooled sign is retained as one row, printed with the note that it is not
the verdict.

**Falsifier:** a conditional lean the slope misses that the sign test
catches.

**Status: SUPPORTED.**

---

### RDD_002 — the ranked list has to be standardized, or it ranks units

S2 asks for a ranked list of slopes against magnitude, each predictor,
and time. Those predictors carry **different units**, so their raw
slopes are not on one scale and sorting them is a comparison across
unlike objects.

The list ranks on the **standardized** slope, which is dimensionless and
equals the correlation for a simple regression; the raw slope and its
standard error are printed beside it and not sorted on.

This is `reasoning-gate`'s `G-DIM` in the one place a ranked list makes
it easy to miss: a table sorted by a column looks like one quantity.

**Falsifier:** two predictors whose standardized ranking a reader judges
wrong where the raw ranking is right.

**Status: SUPPORTED.**

---

### RDD_003 — F1 cannot separate magnitude from time, and naming one would be picking

In F1 the predicted values rise with the time index. That is the common
real shape, and it makes S2(a) and S2(c) carry **identical** standardized
slopes (0.8681 both).

A ranked list cannot separate two axes that move together: the residual
leans with both by the same amount. S2 asks for the folded term to be
**named directly rather than inferred from the existence of a lean**, and
naming one of a collinear pair is inference of the worst kind — a
specific wrong answer rather than an absent one.

So the report emits `NOT SEPARABLE` with the group, states the
correlation threshold it used, and says what would separate them: a
series in which the two axes move independently.

Found by reading the F1 output, not by design.

**Falsifier:** a pair above the threshold that a reader can separate
from the ranked list alone.

**Status: SUPPORTED.**

---

### RDD_004 — all four cells of the 2x2 are reachable, and a missing coupling is a fifth state

| lean | coupling | cell |
|---|---|---|
| present | strong | `RECOVER`, term named |
| present | weak | `LOG_AND_LEAVE` |
| absent | strong | `CHECK_S2A` |
| absent | weak | `NO_ACTION` |
| any | **not supplied** | **`COUPLING_UNKNOWN`** |

The fifth row is not in the order and is forced by it: a coupling nobody
supplied is not weak coupling, and treating it as weak routes a case to
`LOG AND LEAVE` on an absence. The state names the order's own fallback
chain instead — claim record, then perturbation, then dependent count,
with the last named as a fallback wherever it is used.

`LOG_AND_LEAVE` on F2 names **no term**, because no conditional row
leans there: the lean is a pooled offset. A cell that produced a name
anyway would be inventing one.

**Falsifier:** a case the five states cannot hold.

**Status: SUPPORTED.**

---

### RDD_005 — stable and growing are different findings and different outputs

S4 regresses the per-window S2(a) slope on the window index.

| fixture | rate check |
|---|---|
| F1 | `STABLE` — missing term, claim inside its domain |
| F2 | `STABLE` |
| F3 | `GROWING` — background moved past the rate ceiling, claim has left its domain |

The three reports are distinct strings, which the selftest asserts
rather than trusting: the order says *do not report as the same
finding*, and two findings that print the same are the same finding.

`NOT_COMPUTABLE` is kept apart from both, for a series too short to
window.

**Falsifier:** a growing lean the windowed regression reads as stable.

**Status: SUPPORTED.**

---

### RDD_006 — F4 emits uninterpretable, and the same series with a known history does not

A symmetric residual set whose adjustment history is `unknown` is not a
clean score. A claim that left no lean and a claim whose lean was
removed are **the same artifact from here**.

The selftest checks both directions: F4 returns `UNINTERPRETABLE`, and
the identical series with `correction_status` set to `unadjusted`
returns a readable cell. The difference is entirely in the record, which
is the point.

**Falsifier:** a way to tell the two apart from the series alone.

**Status: SUPPORTED. A clean score here would be a false negative on the
instrument's own record, as the order says.**

---

### RDD_007 — S5 and S6 name field 8's values differently, and S6 governs

S5 gives `raw | corrected | unknown`. S6 says use `adjusted / unadjusted`
for the state.

Both are in the same order. S6 is the naming constraint and is the
later, more specific instruction, so the vocabulary is
`unadjusted | adjusted | unknown` and **S5's two spellings load as
aliases** — a series written to the letter of S5 still validates, and
nothing is silently renamed underneath its author.

Recorded rather than resolved by choosing quietly: an internal tension
in a delivered order is a fact about the order.

**Falsifier:** a reading under which S5's spellings and S6's are not the
same states.

**Status: SUPPORTED. Aliases accepted, canonical form is S6's.**

---

### RDD_008 — the naming screen scans itself, because the phrase is never written

A screen that stored the banned phrase as a literal would put the phrase
in the file it screens, and the file would then have to skip a region of
itself — the hand-broken loop this repository recorded as `UNI_010`.

The patterns are composed from tokens, so the literal never appears in
`naming.py` at all and `--source .` scans the whole folder **including
that file**, with nothing excluded on its own account.

**One file is exempt: the delivered order**, which has to name the
phrase in order to ban it. The exemption is measured, not assumed — the
selftest checks that the tool is clean with the specification excluded
*and* that the specification is the **only** file that fires without the
exclusion.

Not banned: the bare word `correction`. S5 names three fields with it.
The order bans a two-word phrase and its close forms, not the vocabulary
of adjustment.

**Falsifier:** a form of the phrase the five patterns do not hold —
open, as every lexical screen here is.

**Status: SUPPORTED.**

---

### RDD_009 — field 8 is the first non-uniform field in the claim registry

`CR_007` and `CR_017` recorded that every sentinel-bearing column came
back single-valued: `outside_this` `UNTESTED` 9 of 9, `rate_ceiling`
`UNMEASURED` 8 of 9, `error.kind` `systematic` 6 of 6.

Field 8 does not:

| value | records |
|---|---|
| `unadjusted` | **6** — counts produced in this session, nothing subtracted |
| `unknown` | **3** — values read from published sources that say nothing about it |

The split is not a formatting choice. The six `SSS_*` records are counts
this session computed from a file; the three `UNF_*` records are numbers
read from a dataset and an index whose own production the workbook does
not describe, which is `COLLAPSED_UPSTREAM` seen from a second side.

Field 10 splits with it: depth `0` on six, `UNKNOWN` with a reason on
three.

**Falsifier:** a record whose status a reader would assign differently.

**Status: SUPPORTED. The first field in this registry that carries
information about the corpus rather than about the schema.**

---

### RDD_010 — the coupling is imported from the claim record, not reimplemented

S3 says the coupling comes from the claim record. It does:

```
coupling  0.8815  (claim record UNF_GRID_IRAQ, clock.coupling,
                   basis: measured by perturbation, +0.1% on the cell)
```

Three folders in one line. The number the discriminator responds to is
the same object the clock divides a time constant by, and it was
produced by perturbing a cell in a real workbook — not stipulated
anywhere in the chain.

An unknown claim returns a state with a reason rather than a zero, and a
claim whose coupling is `UNMEASURED` returns the record's own stated
reason.

**Falsifier:** a divergence between the coupling the discriminator uses
and the one the clock uses for the same claim, which the shared import
is what prevents.

**Status: SUPPORTED.**
