# CLAIM_TABLE — `transition-family-marker`

Claims about `RESULTS_RUN_1.md`, which is delivered verbatim and not
modified. `TFM_001`–`TFM_004` are computed by `check_run_1.py`; the rest are
read from the delivered text.

REFUTATION_PROTOCOL: the generators were not delivered. Every falsifier
below is either a re-derivation or a new run, and a claim that needs the
generators to settle is marked `UNVERIFIED` rather than assessed.

---

### TFM_001 — SIM-D's stated identity is false; the corrected form is `T/(1+s)`

> `temper(quench(p,s), T) == temper(p, T*(1+s))`

Holds in 24 of 120 tested cases — exactly the 24 where `s = 0`. The
corrected form holds in 120 of 120:

> `temper(quench(p,s), T) == temper(p, T/(1+s))`

Composing two temperings multiplies the temperatures, since
`(p^(1/T1))^(1/T2) = p^(1/(T1·T2))`. A quench by `s` **is** a tempering at
`1/(1+s)`, so the composite is `T/(1+s)`.

**Falsifier:** one distribution and one `s > 0` where the stated form holds.
`check_run_1.py --selftest` fails if any is found.

**Status: REFUTED as written.**

---

### TFM_002 — the argument survives the correction, and gains a number

The prose beside the formula says a sharpened distribution can be *"EXACTLY
UNDONE by raising temperature."* That is right. The corrected identity says
**which** temperature: `temper(quench(p,s), T) = p` exactly when
`T/(1+s) = 1`, so **`T = 1+s`**. Verified at `s = 0.25, 0.5, 1, 2, 4`.

Everything downstream is unaffected — the sim could not have shown a null,
the construction forbade it, and therefore alignment cannot be a pure
sharpening. The correction makes the argument sharper, not weaker: with the
stated formula the undo temperature is unrecoverable; with the corrected one
it is a named quantity a future run can set.

**Falsifier:** show the conclusion depends on the exponent's direction.

**Status: SUPPORTED.**

---

### TFM_003 — SIM-C returned the intact grid, not a nearly-intact one

A 5×5 grid graph has `V = 25`, `E = 2·5·4 = 40`, cycle rank
`E − V + 1 = 16`. The reported `loops=16, alive_edges=40` at every sigma are
**exactly those invariants**.

So the sim did not prune weakly or inconsistently. The pruning step had no
effect whatsoever, and the outputs are computable from the grid dimensions
without running anything. Sharper than "no variation at all", which is
compatible with a pruning step that removed a fixed subset.

**Falsifier:** a run at any sigma returning `alive_edges ≠ 40`.

**Status: SUPPORTED.**

---

### TFM_004 — the damping is algebraically cancelled, so `damp=0.85` does nothing

The stated cause is *"renormalized by max each iteration, and damped at
0.85, so nothing ever decays below the 1e-3 floor."*

Applied uniformly, the damping is removed exactly by the normalisation that
follows it: `(d·C)/max(d·C) ≡ C/max(C)`, identical in 200 of 200 random
vectors. `damp` is a free parameter with **zero** effect on the normalised
state.

That is a stronger diagnosis than the one delivered. There is no slow decay
that fails to reach the floor; there is no decay. Removing the
max-normalisation, as the NEXT line proposes, is therefore necessary and not
merely advisable — with it in place, no absolute decay constant can matter.

**Falsifier:** a non-uniform damping rule, under which the cancellation
fails.

**Status: SUPPORTED, and it extends the delivered diagnosis.**

---

### TFM_005 — SIM-B's tail inference does not follow from tail mass alone

The OPEN section reads a near-constant `tail_end` (0.400 → 0.459) against a
1.2-nat entropy drop as showing *"the entropy loss is happening INSIDE the
head."*

Constant tail **mass** does not locate the entropy loss. The tail's
**internal** entropy can collapse at fixed total mass — 1500 tail tokens
sharing 0.4 of the mass uniformly, versus 50 of them holding the same 0.4,
are very different entropies at identical tail mass.

The reading needs head entropy and tail entropy reported separately, and
neither is in the table. The drop is right to mark this UNRESOLVED; the
resolution is one more column, not a re-run.

**Falsifier:** report `H_head` and `H_tail` per row.

**Status: SUPPORTED — the inference is under-determined, not wrong.**

---

### TFM_006 — the "gradual, not steplike" negative is bounded by its grid

Seven anchor points, gaps from 0.010 to 0.200, a **20×** spread. A
transition narrower than the local spacing is invisible, and the spacing
where the curve is steepest (0.05 → 0.40) is the coarsest.

This does not overturn the negative. It bounds it: the response is gradual
*at the resolution sampled*, which is a `reasoning-gate` `G-RES` statement
and not a claim about the response.

**Falsifier:** a uniform fine grid over 0.00–0.10 showing the same
smoothness.

**Status: SUPPORTED as a bound on TFM's own negative.**

---

### TFM_007 — the entropy unit appears once, in prose, and never in the table

`H_start`, `H_end` and `dH` carry no unit. "nats" appears once, in the OPEN
paragraph. At `vocab=2000`, `ln 2000 = 7.60` and `log2 2000 = 10.97`, so
`5.625` is admissible in either and the column cannot be read without the
prose.

The CAUTION line already says not to quote the numbers, which makes this
small — but a table nobody may quote still needs a unit to be re-derived
from.

**Status: SUPPORTED, minor.**

---

### TFM_008 — the not-tuned discipline is the drop's strongest feature and is not checkable from here

*"NOT TUNED. Parameters were left as first written so the failure is on
record. Fixing this by searching parameters until loops appear would
manufacture the expected result."*

That is the discipline this repo's `REFUTATION_PROTOCOL` asks for, applied
to a sim that failed. It is also, without the generators and their history,
**unverifiable from outside**: a drop that had searched parameters and a
drop that had not produce identical results files.

Recorded as the honest counterweight to `TFM_001`–`TFM_004`, all of which
are objections. The confidence line — 0.40 before, 0.40 after, *"the marker
is not stronger. It is better specified"* — is the same discipline stated
about the whole run.

**Falsifier:** a commit history for the generators.

**Status: UNVERIFIED — a gap, not a defect.**
