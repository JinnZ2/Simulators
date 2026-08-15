# AUDIT_NOTES

Taking up the invitation in [`README.md`](README.md): *"Test fit, extend
it, or report where it breaks."*

**Status: all reported defects are fixed.** The delivered files were
checked in verbatim across three drops, audited here, and then repaired.
Sections 2, 3, 4 and 9 below describe defects that no longer exist —
kept, with what changed, because the repair is the record. Every one has
a test in [`tests/test_gate.py`](tests/test_gate.py) that asserted the
broken behaviour first and asserts the fix now, so a regression turns it
red. Section 1 is not a defect and was not "fixed": it is a limit on what
`G-RES` can promise.

The delivered files —
[`gate.py`](gate.py), [`guards.json`](guards.json),
[`make_docs.py`](make_docs.py), [`GUARDS.md`](GUARDS.md),
[`replay_sim_stack.py`](replay_sim_stack.py),
[`mine_logs.py`](mine_logs.py), [`explore.py`](explore.py),
[`SIM_STACK_BACKTRACE.md`](SIM_STACK_BACKTRACE.md) — arrived across three
drops and are now modified only by the repairs recorded here.
`SIM_STACK_BACKTRACE.md` is untouched. `GUARDS.md` regenerates
byte-identically from `make_docs.py`, asserted by a test.

Added alongside them:

| File | What it is |
| --- | --- |
| [`retro_sim_stack.py`](retro_sim_stack.py) | A second replay of the same three sims, declared differently. It disagrees with `replay_sim_stack.py` about SIM-B — see §1, the most useful thing in these notes. |
| [`../aperiodic-order-sim-stack/aperture_alias_demo.py`](../aperiodic-order-sim-stack/aperture_alias_demo.py) | The S(k) control the back-trace asks for, run on 1D probes with known spectra — see §7. |
| [`tests/test_gate.py`](tests/test_gate.py) | Guard behaviour, plus the shipped defects locked in as tests. |
| [`samples/`](samples/) | Pinned output of both replays. |

The subject of both replays is
[`../aperiodic-order-sim-stack/`](../aperiodic-order-sim-stack/).

---

## 1. G-RES is only as strong as the pair you declare — NOT A DEFECT

`replay_sim_stack.py` passes SIM-B. `retro_sim_stack.py` denies it at
`pre()`. Same guard, same sim, same gate, opposite verdicts — because
they declare different instrument/feature pairs:

| Declaration | instrument | feature | margin | verdict |
| --- | ---: | ---: | ---: | --- |
| smallest box vs mean nearest-neighbour spacing *(replay)* | 0.05 | 0.20 | 2.0 | **passes** |
| estimator artifact floor vs claimed separation *(retro)* | 0.252 | 0.334 | 2.0 | **denies** |

Both are honest. The first is the box-count's *geometric* resolution:
can the finest box see between neighbouring points? The second is its
*statistical* resolution: is the separation larger than the spread the
estimator produces on point sets whose true dimension is known? The
second number is measured in
[`../aperiodic-order-sim-stack/finite_n_control.py`](../aperiodic-order-sim-stack/finite_n_control.py)
— worst finite-N shift 0.137 across a 12× sample-size drop, plus 0.115
for box-ladder commensurability.

**Nothing in the gate requires the binding pair to be the declared one.**
An operator who declares the resolution that passes has satisfied G-RES,
and the log records a satisfied guard. This is not a bug in `gate.py` —
`Resolution` cannot know which of a measurement's many scales dominates.
It is a limit on what the guard can promise, and it belongs next to the
guard rather than discovered later.

Worth noting where the two declarations *agree*: SIM-A denies under both,
on the same numbers (k-grid 0.39 vs Bragg peak width 0.063). When the
binding constraint is obvious, G-RES is decisive.

The replay's error bar has a related gap. `cluster_spread = 0.075` is
declared as "spread across the three space-filling sets" — all three at
~12,000 points. The comparison it is used to license runs between AB at
12,000 points and the cascade at 1,024. The finite-N shift that spread
excludes is up to 0.137 on its own, larger than the error bar itself.

## 2. A generator-level quantity could support a physical claim — FIXED

The sharpest gap, and it showed up in the delivered replay's own output.

`replay_sim_stack.py` tags `Df_cascade` as `generator` with the note
*"set by E_split, E_min, branch rule - not a tungsten property"* — a
careful, correct tag. `summary()` then printed:

```
generator-level (no physical claim permitted): Df_cascade
claim    : [supported] the two sets do not share a fractal dimension
```

The claim was `supported_by=["Df_AB", "Df_cascade", "cluster_spread"]`,
its `support_layers` came out `["generator", "instrument", "physical"]`,
and `findings` was **empty**. The summary asserted "no physical claim
permitted" on the same page as a supported physical claim resting on that
quantity. G-LAYER guarded the *tagging* of quantities; nothing guarded
their *use*. `claim()` computed `support_layers` and never inspected it.

**Repair.** `claim()` now takes a `scope` — `"physical"` by default, or
`"generator"` for a claim explicitly about the code that produced the
data. A physical-scope claim resting on generator-level support is
recorded `qualified` rather than `supported`, carries a `layer_note`
naming the offending quantities, and emits a G-LAYER finding.

Downgraded, **not refused**, which is the same shape `G-IND` already uses
for convergence across shared inputs. The support is real; what it cannot
carry is a statement about the modelled system. SIM-B still passes — no
denial — but its claim now reads:

```
claim    : [qualified] the two sets do not share a fractal dimension
           ^ physical scope claim resting on generator-level support: Df_cascade
```

That is the substantive point from the back-trace's PATTERN 4 made
mechanical. By the replay's own tagging, "the two sets do not share a
fractal dimension" compares a physical property of the Ammann-Beenker
tiling against a parameter of the cascade generator. The gate now says so
in the report instead of leaving it to a reader.

`scope="generator"` is the escape hatch and it is deliberately narrow: a
claim about what the branching walk does at given parameters is fully
supported by generator quantities, and is not downgraded.

## 3. G-FIT was documented at the wrong stage — FIXED

`guards.json` gave G-FIT `"stage": "post"`, so `make_docs.py` rendered it
under **POST - at report assembly**. `gate.py` enforces it in `pre()` —
`discriminates` is one of four fields checked before anything runs, and
pre-stage guards deny regardless of `strict`. An operator reading
`GUARDS.md` would expect to supply the discrimination argument at report
assembly and would instead be denied before the sim executed.

**Repair.** `G-FIT` is now `"stage": "pre"`.

The related G-CTRL case is also fixed. It denies at `pre()` *and* fires at
`close()` for controls declared and never run, but `stage` carried one
value. It is now `["pre", "post"]`, and `make_docs.py` accepts a string or
a list — rendering such a guard under each stage it belongs to, with an
"Also fires at:" line. `GUARDS.md` regenerated.

## 4. Four defects in `gate.py` — ALL FIXED

Each has a test in `tests/test_gate.py::RepairedDefects` that asserted the
broken behaviour before the repair and asserts the fix now.

**D1 — the module docstring's usage example denied at `pre()`.** It
declared `Resolution(..., instrument=0.39, feature=0.063)` and then
continued through `record` / `claim` / `close`. It could not: 0.39 × 2.0 >
0.063.

*Fixed* by giving the Usage example a resolution that passes
(`instrument=0.020`) and moving the SIM-A numbers into an explicitly
labelled `DENIAL EXAMPLE` block that says what they are and why not to
copy them. The numbers are worth keeping — they are the real failure — but
not under a heading called "Usage".

**D2 — `promote()` and `ratio()` silently overwrote.** `record()` refuses
to overwrite a recorded name; neither of the other two writers checked, so
`promote("x", "y", ...)` replaced an existing `y` and its value was gone —
in the one operation G-LAYER exists to make explicit.

*Fixed* — both now deny on a name collision, matching `record()`. The
prior value is preserved.

**D3 — strict `close()` lost the report, and the retry misreported.** With
an unrun control, `_soft` raised before `self._closed = True` and before
the JSON was written, so the reason for the denial existed only in the
traceback. The gate was left open, so catching the error, answering the
control with a placeholder and closing again produced a clean report whose
`controls` block said `run: True` while a finding below said otherwise.

*Fixed* in two parts. The gate now closes **before** denying, so the retry
path is gone — a caller that catches the denial cannot call
`control_result()` or `close()` again. And every denial, at any stage,
writes `gate_<SIM>.denied.json` before raising, carrying the guard that
denied, the detail, the declaration and whatever had been recorded.
`control_result()` also now refuses an empty observation.

That denial record is the same change that fixes the mining blindness in
§9 — one repair, two defects.

**D4 — a malformed registry loaded, then crashed.** `_load_guards`
verified all eight ids were present but not that each carried a
`fail_message`. A registry missing one loaded fine and raised `KeyError` —
not `GateError` — at the moment that guard fired: open at load, crashing
at denial, the wrong order for a fail-closed tool.

*Fixed* — the loader now rejects any registry with a missing or blank
`fail_message`, naming the guards at fault.

## 5. What the gate catches on the audited stack

`retro_sim_stack.py` maps gate verdicts onto the four findings in
[`../aperiodic-order-sim-stack/README.md`](../aperiodic-order-sim-stack/README.md).
Every input is sourced — `[R]` report, `[F]` shipped figure, `[C]`
measured control, `[G]` `gate.py`'s docstring.

| Audit finding | Gate verdict |
| --- | --- |
| **1** — two estimators, opposite signs, one reported | **Partial.** G-CTRL gives the Line control one slot both results must occupy, so the disagreement lands beside the claim. The gate cannot compel an author to record a run. |
| **2** — decisive gap ~75% inside the artifact budget | **Caught at `pre()`** by G-RES under the retro declaration — but see §1, the replay's declaration passes. §2 catches it from the other side. |
| **3** — SIM-C's null entered as positive evidence | **Caught twice** — G-CTRL on the unrun positive control, G-SUP on the claim naming nothing. |
| **4** — no Bragg peaks in the S(k) figure | **Caught at `pre()`** by G-RES, under both declarations. SIM-A never runs. |

Two findings the audit missed, both from the delivered replay:

- **G-DIM voids the ratio 54.1.** SIM-C divides a band-edge splitting of
  the tight-binding model by a splitting of the cascade set. Both real,
  both dimensionless, division clean, quotient denoting nothing. The
  report reaches the same place in prose — "the two systems operate on
  very different normalized energy scales" — without noticing it has
  voided its own number.
- **G-IND downgrades the overall conclusion.** SIM-A and SIM-B are two
  statistics on the same pair of point sets, so "three independent
  simulations converge" is restatement, not corroboration.

### On SIM-A

The strongest single result, and it survives both declarations. The
k-grid is 0.39 against a finite-sample peak width of 2π/L = 0.063 — 6.2×
too coarse, 12.4× short of the 2× margin. The peaks fall between sample
points.

That is a quantitative account of the audit's Finding 4. The absence of
an eight-fold Bragg star in `sim_a_structure_factor.png` is not only the
linear colour scale: **SIM-A could not have resolved Bragg peaks whether
or not they were there**, so its null carries no information about
quasiperiodic order. The gate reaches that from two declared numbers,
before a figure is rendered.

## 6. On the n=1 caveat

The delivered README is explicit that these are candidate shapes
back-traced from one paired sample. These notes are a second pass over
the *same* artifact, so they do not raise n. §1 and §2 are the two places
a second sample would be most informative: whether operators reliably
declare the binding resolution pair, and how often claims rest on
generator-level quantities once tagging is enforced.

---

## 7. The back-trace's SIM-A diagnosis, checked

[`SIM_STACK_BACKTRACE.md`](SIM_STACK_BACKTRACE.md) reads SIM-A as an
artifact and names the control that would settle it: push the SIM-B
periodic lattice through the SIM-A `S(k)` code. That exact run is still
impossible here — the drop shipped results, not generators — but the
mechanism can be tested directly on 1D probes whose spectra are known
analytically.
[`../aperiodic-order-sim-stack/aperture_alias_demo.py`](../aperiodic-order-sim-stack/aperture_alias_demo.py)
does that. Both halves of the diagnosis hold, one more strongly than the
other.

**The floor tell is confirmed, and it is the strong half.** The
back-trace's sharpest observation is that AB's diffuse floor sitting
*above* the cascade's is backwards — a quasiperiodic set has a pure point
spectrum, so between its peaks there is almost nothing and its floor must
sit *below* the uncorrelated value of 1. A Fibonacci chain, the standard
1D analogue of an Ammann-Beenker tiling, returns a floor of **0.09**
against a Poisson floor of **0.99**. SIM-A reports AB at 2.08 and the
cascade at 0.96. The ordering is inverted, and this conclusion does not
depend on guessing the grid spacing.

**The aliasing mechanism is confirmed, with its magnitude
configuration-dependent.** A grid 86× the finite-sample peak width misses
25 of 34 Bragg peaks; on the Fibonacci probe exactly one of 400 samples
lands on a strong peak. The 9 hits on the periodic probe are a
commensurability accident — peak spacing over grid spacing near 35/3.
So the honest version is narrower than "only k=0 survives": a coarse grid
loses most of a point spectrum, loses all of it under small changes to
numbers nobody chose together, and always keeps k=0.

**This corrects an error in my own earlier audit.** The first pass over
this drop conceded that AB's oscillations out to |k| ≈ 20 were real
structure — "AB has more k-space structure than the Cascade, that much
the figure supports." That was wrong, and the refuting number (floor 2.08
vs 0.96) was already quoted in the same paragraph. `AOS_006` and
`AOS_007` in the sim-stack claim table are revised accordingly; `AOS_007`
moves from `UNVERIFIED` to `SUPPORTED`.

**One caveat that would reverse it**, stated because it turns on a label:
the plain *mean* of the same Fibonacci samples is 2.45, not 0.09, since a
single sampled peak dominates. If SIM-A's 2.08 were a mean rather than a
top-excluded floor, a genuine quasicrystal could produce it. The figure
panel reads "Diffuse Background (excl. top 1%)", so the comparison stands
— on that label.

## 8. The SIM-B error bar: two routes, one number

The back-trace identifies something the first audit missed. The report
justifies its separation as "~15× the AB–Poisson baseline (0.021)", and
0.021 is the **smallest** of three pairwise gaps inside the space-filling
cluster:

```
AB–Poisson       0.022   <- used as the noise floor
Poisson–Lattice  0.053
AB–Lattice       0.075
cluster spread   0.075
```

Three sets whose true dimension is 2 disagree by 0.075. The honest ratio
is `0.334 / 0.075 ≈ 4.5×`.

Worth recording that this converges with
[`finite_n_control.py`](../aperiodic-order-sim-stack/finite_n_control.py)
from the opposite direction. That control subtracts a measured worst-case
artifact budget (0.252) from the reported gap and leaves a residual of
0.082 as a lower bound on structure. The back-trace measures the
empirical spread among three sets that should agree and gets 0.075. Two
different routes, an effective error bar near 0.08, a separation near 4×.

The back-trace's framing is the better one to quote. My "magnitude does
not survive" was correct but under-specified; **"still decisive, still
separated, not 15×"** says the same thing with the number attached, and
identifies *which* step produced the inflation — picking the closest pair
in a cluster as the width of the cluster. Recorded as `AOS_009`.

## 9. Two defects in the new tools — FIXED

**`mine_logs.py` flagged every sound run as a divergence.** The
"divergences with no guard attached" section — labelled the growth edge —
tested `expected != observed` on two free-text strings. Those are never
equal, so any run that fired no guard landed in the list. On the delivered
corpus it flagged SIM-B, the one sound sim:

```
divergences with no guard attached  (the growth edge)
  SIM-B
    expected: AB near 2 (space-filling), cascade below 2 (clustered)
    observed: AB 1.889 / cascade 1.555, controls on target
```

Those agree. A section that fires on everything finds nothing.

*Fixed* on the gate side, where the information actually lives.
`close()` now takes `diverged=True | False | None` — the author's explicit
call, defaulting to `None` for not assessed. Divergence is not inferred
from prose, because two descriptions of one outcome never compare equal.
`mine_logs.py` reports the real growth edge (`diverged=True` with no guard
fired) and lists unassessed runs separately under "closed without a
divergence call (nobody has looked)" rather than guessing. `summary()`
shows the call as `YES` / `no` / `NOT ASSESSED`.

**`mine_logs.py` was blind to denials, which is the deeper one.** Hit
rates were computed over `gate_*.json` files, and a pre-stage deny wrote
no file — the run raised before `close()`. In the delivered corpus SIM-A
is denied by G-RES and left no log, so the report read:

```
  G-RES      0    0.0%   NEVER FIRED
```

G-RES was marked never-fired **because it worked**. An operator pruning
never-fired guards would have deleted the most effective ones first.

*Fixed* by the D3 denial records. `mine_logs.py` now reads both
`gate_<SIM>.json` and `gate_<SIM>.denied.json` and reports findings and
denials in separate columns. The same corpus now reads:

```
runs: 3   (closed 2, denied 1)   voided ratios: 1

guard activity
  guard    findings  denials    total
  G-RES           0        1        1
  ...
```

It also warns when a corpus contains no denial records at all, since that
is either a very clean corpus or a missing-log problem, and the two look
identical from the outside.

**`explore.py` read `sim` as `None` on a real gate report.** `__main__`
passed `d.get("declaration", d)` into `explore()`, which looked for
`sim_id` inside it — but `sim_id` is top-level in a gate report. The
output filename got it right; the `sim` field in the document did not.

*Fixed* — `explore()` accepts either a full report or a bare declaration
and finds `sim_id` in either position. Its output handle is also closed
properly now.

## 10. On the n=1 caveat, revisited

The delivered README and the back-trace are both explicit that these are
candidate shapes from one paired sample. Sections 7 and 8 above do raise
the evidence slightly, but not the sample count: they are independent
*checks* on the same artifact, using probes with analytically known
answers, not a second audited artifact.

What section 7 does establish is that the back-trace's PATTERN 2
("instrument resolution never enters as a precondition") has a
demonstrated mechanism behind it in at least one case, rather than only
a structural argument. The back-trace rates that pattern "moderate, but
contradicted by B". The aperture demo does not resolve the contradiction
— B genuinely did run its resolution check — but it does confirm that
where the check was skipped, the failure it would have caught is real and
reproducible.
