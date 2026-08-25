# CLAIM_TABLE — `alignment-under-coupling`

Claims about `RESULTS_RUN_1.md` and the sims that produced it. Delivered
files are unmodified. Computed by `check_run_1.py`, which imports the sims.

`TFM_001`–`TFM_008` were written when only the results had been delivered,
in a folder called `transition-family-marker/`. The generators arrived
afterwards; that folder was merged into this one so the checks could import
the code instead of modelling it. **Two verdicts changed on contact with the
code and both are marked. The ids are kept rather than renumbered.**

REFUTATION_PROTOCOL: a claim that needs a run is settled by a run. A claim
that needs the sims' authoring history is marked `UNVERIFIED` and stays
there.

---

### TFM_001 — SIM-D's stated identity is false; the corrected form is `T/(1+s)`

> `temper(quench(p,s), T) == temper(p, T*(1+s))`

Tested against the sim's own `quench()` and `temper()`: holds in **24 of
120** cases, exactly the 24 where `s = 0`. The corrected form holds in 120
of 120.

`temper` is `p^(1/T)/Z` and `quench` is `p^(1+s)/Z`, so a quench by `s` **is**
a tempering at `1/(1+s)`, and temperings compose multiplicatively. The
composite is `T/(1+s)`.

**Falsifier:** one distribution and one `s > 0` where the stated form holds.

**Status: REFUTED as written. Confirmed against the code, having first been
established against a model of it.**

---

### TFM_002 — the argument survives the correction, and gains a number

The prose beside the formula — *"EXACTLY UNDONE by raising temperature"* —
is right, and the corrected identity says which temperature:
`temper(quench(p,s), T) = p` exactly at **`T = 1+s`**, verified at
`s = 0.25 … 4`.

Everything downstream is untouched: the sim could not have shown a null, the
construction forbade it, and therefore alignment cannot be a pure sharpening.
The correction sharpens the argument. With the stated formula the undo
temperature is unrecoverable; with the corrected one it is a quantity a
rewritten `quench()` can be tested against — if a support-truncating quench
is *not* undone at `T = 1+s`, that is the discriminator the original
construction forbade.

**Status: SUPPORTED.**

---

### TFM_003 — SIM-C returned the intact grid, not a nearly-intact one

`build_grid(5)` gives `V = 25`, `E = 40`; cycle rank `E − V + 1 = 16`. The
reported `loops=16, alive_edges=40` at every sigma are exactly those.

No pruning at all, not weak pruning, and the outputs are computable from the
grid dimensions without running anything.

**Status: SUPPORTED.**

---

### TFM_004 — **CORRECTED. This claim was mine and it was wrong.**

**As written:** *"uniform damping followed by max-normalisation is
algebraically cancelled, so `damp=0.85` is a free parameter with zero
effect."*

That reading came from the delivered prose — *"renormalized by max each
iteration, and damped at 0.85"* — with no code to check. The code is:

```python
newC.append(0.85 * C[i] + 0.15 * target)
m = max(newC) or 1.0
C = [max(1e-9, c / m) for c in newC]
```

A **convex combination toward the target**, not a uniform scaling. Measured:
a uniform scaling is cancelled by max-normalisation in **200 of 200** random
vectors; the code's actual update is cancelled in **0 of 200**. The damping
does real work.

**The real reason nothing prunes**, measured on the sim's own state:

| sigma | min C | median | max C | floor below min by |
|---|---|---|---|---|
| 0.00 | 4.17e-2 | 1.34e-1 | 1.00 | 42× |
| 0.40 | 4.71e-2 | 1.33e-1 | 1.00 | 47× |
| 1.60 | 4.57e-2 | 1.24e-1 | 1.00 | 46× |

The floor is `1e-3`. The smallest conductance the dynamics ever produce is
`~4.6e-2`. **The floor sits about 46× below the bottom of the range it is
applied to**, and the conductances span barely one decade, with the spread
almost unmoved by sigma.

That is a `reasoning-gate` `G-RES` failure — a threshold outside the range of
the quantity it tests — and it is a different repair from the delivered NEXT
line. Removing the max-normalisation would change the scale; it would not by
itself put the floor inside the range. The floor has to be set from the
observed distribution, or the dynamics have to be made capable of producing
values near it.

**Falsifier:** a run in which any conductance reaches `1e-3`.
`--selftest` fails if one does.

**Status: the claim as written is REFUTED. The replacement is SUPPORTED and
is a stronger diagnosis than either the delivered one or the one it
replaces.**

---

### TFM_005 — **CORRECTED, and the drop's UNRESOLVED contradiction dissolves**

**As written:** the drop's tail reading is *under-determined* without head
and tail entropies reported separately.

Both are computable from the code. Computed, the reading is not merely
under-determined — it is **inverted**.

| anchor | H_total | tail_mass | dH_head | dH_tail |
|---|---|---|---|---|
| 0.00 | 4.429 | 0.4000 | **−0.120** | **−2.289** |
| 0.05 | 4.737 | 0.4247 | −0.022 | −1.817 |
| 0.40 | 5.255 | 0.4593 | +0.013 | −0.903 |

True distribution: `H_head 3.197`, `H_tail 7.064`, `tail_mass 0.4499`. The
decomposition `H = H(mass split) + head_m·H_head + tail_m·H_tail` closes to
1e-9, so the split is arithmetically sound.

The drop read near-constant tail **mass** against a falling total entropy as
showing *"the entropy loss is happening INSIDE the head … which contradicts
the reported mechanism"*, and logged it UNRESOLVED.

Unanchored, the head loses **0.12** nats and the tail loses **2.29** — a
factor of nineteen. The loss is almost entirely in the tail, which keeps its
mass while concentrating it onto far fewer tokens. That is exactly the state
tail mass alone cannot distinguish. Anchoring cuts the tail loss to 0.90 and
leaves the head flat.

**So the reported mechanism — anchoring preserves long-tail tokens — is
REPRODUCED, not contradicted, and the drop's own open contradiction
dissolves.** Two columns settle it; no re-run was needed.

**Falsifier:** a head/tail split showing `|dH_head| ≥ |dH_tail|`.

**Status: SUPPORTED in a stronger form than written.**

---

### TFM_006 — the "gradual, not steplike" negative is bounded by its grid

Seven anchor points, gaps 0.010 to 0.200, a **20×** spread, coarsest where
the curve is steepest. A transition narrower than the local spacing is
invisible.

This does not overturn the negative; it sizes it. `G-RES` about the grid,
not a claim about the response.

**Status: SUPPORTED as a bound on the drop's own negative.**

---

### TFM_007 — the entropy unit is confirmed nats, and is still absent from the table

`SIM-B` uses `math.log`, so the columns are nats. `H` of the true Zipf is
**5.625**, which is exactly the reported `H_start`. `ln(2000) = 7.601`,
`log2(2000) = 10.966`.

Confirmed rather than inferred, now that the code is here. The table still
carries no unit and the prose still names it once.

**Status: SUPPORTED, minor.**

---

### TFM_008 — the not-tuned discipline is the drop's strongest feature and is still not fully checkable

The parameters are now inspectable, so *what* they are can be verified. What
cannot be verified from here is that they were not searched: a run that had
searched and one that had not leave identical files, and the sims arrive
without history.

Recorded as the counterweight to seven objections. The confidence line —
0.40 before, 0.40 after, *"the marker is not stronger. It is better
specified"* — is the same discipline applied to the whole run, and it is the
right call.

**Falsifier:** a commit history for the sims.

**Status: UNVERIFIED — a gap, not a defect. Narrowed by the code's arrival,
not closed.**

---

### TFM_009 — the loop count is not cycle rank unless the alive subgraph is connected and spanning

`loops = alive - (nodes - 1)`. Cycle rank is `E − V + components`. Nothing
checks connectivity, so:

| alive | reported loops |
|---|---|
| 40 | 16 |
| 30 | 6 |
| 24 | 0 |
| 12 | 0 |

At `alive = 12` no subgraph can span 25 nodes, and the formula still returns
`0` rather than flagging a disconnected result. On this run the defect is
inert — nothing pruned — but it becomes load-bearing the moment `TFM_004`'s
floor is repaired, which is the run the NEXT line proposes.

**Falsifier:** add a component count and show it is always 1 after pruning.

**Status: SUPPORTED, latent.**

---

### TFM_010 — `run_all.py --quick` does nothing

```python
a = list(args)
if quick:
    a = [x for x in a]
```

The branch rebinds `a` to a copy of itself. The flag is documented in the
usage block and is inert.

**Falsifier:** any argument list `--quick` changes.

**Status: SUPPORTED.**
