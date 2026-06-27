# REGIME_SHIFT — AMOC regime-shift trajectory framework

CC0. stdlib-only. Anti-freeze. A fork-able skeleton for asking *what does my
specific patch of ground do when Atlantic overturning flips*, without
swallowing an institutional point-forecast built on linear assumptions.

This is scaffolding, not authority. It returns response surfaces and honest
gaps, never a verdict. Fill the gaps with your own ground-truth and the bands
narrow. Where it can't know, it says so.

---

## What it is / is not

IS: a way to sweep a freshwater-loading control parameter, see where the
overturning loses its stable branch (spinodal), borrow the *pattern* of past
shutdown events, strip the parts of those events that depended on a world we no
longer live in (continental ice, meltwater buffer, permafrost cycle), and read
the corrected response as a band for a user-supplied site.

IS NOT: a GCM, a forecast, or a claim about *when*. It deliberately refuses to
emit "your region will be X in year Y." Timing is a coupled-systems question
this skeleton does not pretend to close.

---

## Modules

| file | role |
|---|---|
| `forcing.py` | two instruments on the same transition: `StommelBox` (two-box thermohaline, readable, hysteresis visible) and `KramersWell` (tilted double-well escape-rate, continuous with `field_collapse.py`) |
| `baseline.py` | paleo analogs (Younger Dryas, 8.2ka, Heinrich 1) as PATTERN sources, each tagged with provenance + confidence |
| `divergence.py` | strips analog terms that needed ice / meltwater buffer / permafrost; flags what can't be inherited; **discounts analog recovery** because present loading is ocean-sourced and not finite |
| `sitespec.py` | user's substrate, with chain-of-custody per datum; owns the declared Sv→F calibration |
| `response.py` | couples forcing+analog+site into BANDS, widening where site data is missing |
| `trajectory.py` | anti-freeze ensemble core; surfaces cliff zones and model-disagreement bands |
| `carlton_county.py` | the worked slice to fork |

---

## Honest-gap protocol (inherited from CONVERGENCE_TABLE_2026)

1. No AI-filled cells for ground truth. A missing site datum stays `None` and is
   reported as a gap. It is never silently interpolated into false precision.
2. Every datum carries provenance: `field_measured` / `public_dataset` /
   `estimate` / `keeper`, plus who and when and a confidence.
3. Analog numbers are order-of-magnitude scaffolding from the published
   paleoclimate literature, marked `proxy_reconstruction`. Replace them.
4. Species/biome tolerances are keeper-supplied only. The framework will not
   invent them.

---

## Claims (falsifiable; refute the claim, not the model)

**RGS_001** — *A no-glacier start makes the transition faster and choppier than
any glacial-era analog.* Mechanism: loss of meltwater-buffer and permafrost
thermal inertia removes damping. Refutation: show a damping term, present in the
current Upper-Midwest/Shield system, that replaces glacial buffering at
comparable magnitude. If found, `divergence.rate_adjustment` is wrong.

**RGS_002** — *Analog recovery should be discounted.* The 8.2ka system recovered
because its freshwater pulse was finite (a draining lake). Present loading is
Antarctic+Greenland sourced and sustained. Refutation: demonstrate a sink that
makes present ocean freshwater loading self-limiting on a decadal scale.

**RGS_003** — *The collapse zone is under-determined between the two forcing
models* (Stommel spinodal ≈ 0.22, Kramers spinodal ≈ 0.39 on the nondim axis).
This Consensus-Fault band is itself the finding: any single-model timing inside
it is overconfident. Refutation: a physical argument selecting one model's
spinodal as correct for this basin would collapse the band.

**RGS_004** — *Heinrich-class (ENSO-coupled) forcing yields a deeper, higher-
variance cold band than 8.2ka-class for the same site*, because it carries the
amplified-variability signal. This is the super-El-Niño-during-loading case.
Refutation: site data showing variance does not amplify under combined Pacific
thermal forcing + Atlantic loading.

---

## The one mapping we refuse to hide

`sitespec.ForcingCalibration` converts real sverdrups to the nondimensional F
axis. It is the most assumption-laden step in the whole framework, so it lives
in the open with its anchors and its source note. Do not read a nondimensional
spinodal as a measured sverdrup value without going through it — and replace its
anchors with your own literature read.

---

## Fork it

1. Copy `carlton_county.py` → `my_land.py`.
2. Replace every `Datum` with your own measurement + provenance. Leave true
   unknowns as `None`; they'll be reported as gaps.
3. Set `now_state` for your latitude.
4. Adjust `ForcingCalibration` anchors to your own reading of the AMOC
   freshwater-hosing literature.
5. Run. Read the surface. Close the keeper gaps. Re-run.

The bands are wide on purpose. Wide-and-honest beats narrow-and-wrong.

---

## Note on filenames

The collaborator's drop contained one file named `site.py` whose first-line
docstring also referred to it as the substrate module. The README table above
and every importing module (`carlton_county.py`, `response.py`,
`trajectory.py`) reference it as `sitespec`. Saved as `sitespec.py` here so the
import chain resolves; the content is the operator's verbatim text.
