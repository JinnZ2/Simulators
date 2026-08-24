# RESULTS — first run, 2026-08-24

`python3 sim_span.py`. N = 20000 per run, 40 seeds per rate, 360
parameter combinations per leg. Deterministic given the seeds; the full
run is pinned in `samples/sim_span.sample.txt`.

Logged as run. No parameter was tuned toward an expected outcome, and the
two places where a first attempt gave the wrong answer are recorded below
rather than smoothed.

---

## ANSWER

**Yes, but not through the leg the spec's falsifier is scoped to, and not
at the same place on the axis in every leg.**

| leg | U on reported | of those, minimum inside 6–9 h | lowest vertex |
|---|---|---|---|
| `flat` | **4** of 360 | 4 | 7.15 h |
| `mono` | **124** of 360 | **0** | **10.16 h** |
| `frag_driven` | **63** of 360 | **52** | **5.23 h** |

Read across the row, not down the column. Three different answers:

**`flat` — 4 of 360, and they are noise.** Their quadratic coefficients
are `+0.009` to `+0.017`, an order of magnitude below the other two legs.
Over 40 seeds at the default parameters the U rate is 0.03 on reported
and 0.05 on true — no separation between the axis under test and its own
control. A reporting rule cannot manufacture a relation out of an outcome
that has no relation to anything. **The spec's falsifier, as written,
essentially fires.**

**`mono` — the U is manufactured robustly and always in the wrong
place.** 124 of 360 combinations produce one, and **not one** puts the
minimum inside 6–9 h. The floor is 10.16 h across the whole grid. A
published U with a minimum at 7–8 h is not explained by a mechanism that
cannot put a minimum below 10.

**`frag_driven` — this is the leg that answers the question.** 63 of 360
produce a U and **52 of them land inside 6–9 h**, floor 5.23 h. If the
outcome is really driven by fragmentation and the reported quantity is
time in bed, a U-shaped *duration* curve appears at the place a published
one sits, from a true relation that has no duration term in it at all.
The control axis stays clean.

## THE SPEC'S FALSIFIER IS SCOPED TO THE ONE LEG THAT CANNOT ANSWER

The null is stated as *"flat OR monotone"*. The falsifier is stated over
*"the flat null"*. Those are different sets, and the three legs disagree,
so which one is run decides the verdict:

- run `flat` → almost nothing → *"the reporting artifact can't explain
  the published U on its own, and the finding survives this objection"*
- run `frag_driven` → 52 combinations put a manufactured U in the
  published window → the objection stands

Both are in the delivered spec. Only the first is in the falsifier.

This is not a defect of reasoning; it is a scope that was written before
the legs were run. But it is load-bearing, because passing the falsifier
as scoped would license discarding the whole objection, and the leg that
carries the objection is one the spec itself asked for.

## WHERE IT APPEARS AND DISAPPEARS

At the spec's own default fragmentation — mean 2 awakenings, 15 minutes
each, 0.5 h of excess time in bed — **`mono` does not fire at all.** The
curvature is present and pointing the right way (`a = +0.055`) and the
vertex sits at 14.75 h, outside a reported range of 4.0–11.5. The
mechanism is live and has not yet turned.

Sweeping (all `mono`, p = 1.0, U rate over 20 seeds):

| mean frag | U rate reported | U rate true |
|---|---|---|
| 0.0 | 0.00 | 0.00 |
| 2.0 | 0.00 | 0.00 |
| 4.0 | 0.35 | 0.00 |
| 8.0 | 1.00 | 0.00 |

| mean wake_cost | U rate reported | U rate true |
|---|---|---|
| 0 min | 0.00 | 0.00 |
| 15 min | 0.00 | 0.00 |
| 30 min | 0.95 | 0.00 |

The control axis stays at 0.00 throughout, which is what makes the
reported-axis column mean anything.

`p` behaves differently by leg. The lowest `frag_driven` vertices sit at
`p = 0.5`–`0.75`, not at `p = 1.0`: a mixture of span-reporters and
true-reporters manufactures a U placed lower on the axis than a
population where everyone reports span. Nothing in the spec predicted
that and nothing here explains it beyond the arithmetic.

## TWO THINGS THAT CAME OUT WRONG FIRST, KEPT ON RECORD

**The U detector fired on noise at 40–55%.** The first criterion was the
spec's own — sign of the quadratic term, plus a vertex inside the range.
Under `flat`, where the outcome is pure noise, that criterion returned a
U in 133 of 360 combinations and at a rate of 0.30–0.55 across seeds on
*both* axes. It was admitting monotone rising curves: a curve that only
goes up fits a positive quadratic whose vertex sits just inside the left
margin. The lowest `frag_driven` "U" under that criterion had a vertex of
4.46 in a range of 3.5–11.0 — the fit's turning point at the left edge of
the data.

Replaced with a requirement that the curve **turn**: both arms must rise
by `MARGIN = 2.0` times the residual scatter of the bin means about the
fit. A `reasoning-gate` G-RES pair — the feature against the instrument's
own noise, with the margin named. `flat` fell from 133 to 4;
`frag_driven` from 206 to 63, and its floor rose from 4.46 to 5.23. The
tightening removed more than half of every leg's hits and changed no
conclusion except to make the `flat` leg honest.

**`round_half` rounded 7.25 down.** Python's `round()` is banker's
rounding, so `round(7.25 / 0.5)` is 14 and 7.25 h reported as 7.0. The
spec says *"rounded to the nearest half hour"* and does not state a tie
rule. Ties now go up. Caught by a fixed-in-advance case in the selftest,
not by reading. It matters more here than it usually would, because a
tie rule that alternates direction is a second reporting artifact inside
the one being measured.

## KNOWN LIMITS

Stated as the spec requires, plus two it did not name.

**Independence of `frag` and `true_sleep` is assumed and is probably
wrong.** Real fragmented sleepers may compensate by extending time in
bed, which would correlate the two and change the mixing. Not modelled.

**The rounding rule is invented**, and so is its tie behaviour.

**The outcome model is not a biological ageing clock.** `mono` is a
straight line in true sleep; `frag_driven` is a straight line in
awakenings. Neither is a claim about anything.

**Every distribution constant is invented.** True sleep is Gaussian at
7.0 ± 1.1 h clipped to 3–11; awakenings are Poisson; per-agent wake cost
is lognormal. No value in this file is sourced from a sleep study.

**Not named in the spec: the published window is stipulated.** 6–9 h is
where U-shaped sleep-duration minima are reported to sit, entered here as
a constant and used only to ask *where* a manufactured U lands, never to
score one. If that window is wrong, the `mono`/`frag_driven` contrast
moves with it.

**Not named in the spec: the units.** The spec gives `wake_cost` in
minutes and writes `span = true_sleep + frag * wake_cost` with
`true_sleep` in hours. Taken literally that adds minutes to hours — mean
frag 2 at 15 min/wake would add 30 hours to a night. Implemented
dimensionally, with the conversion explicit and a selftest assertion that
the mean excess time in bed stays between 0.1 and 2.0 h.

**This tests whether the mechanism CAN produce the shape.** It does not
test whether it did, and nothing here is a statement about sleep, ageing,
or any published result.

## WHAT WOULD MOVE THIS

The `frag_driven` result is the one that carries the objection, and it
rests on an outcome that depends on fragmentation and not on duration.
That is an empirical question with a reachable answer: in a study with
polysomnography or actigraphy, both `true_sleep` and `frag` are measured
separately. Fit the outcome on both. If duration survives with
fragmentation in the model, this mechanism is not the explanation. If it
does not, the reported-duration U is the fragmentation effect wearing a
duration label.

`p` is also measurable and nobody reports it: the fraction of respondents
who answer a sleep-duration question with time in bed rather than time
asleep. A validation sub-study against actigraphy would give it directly,
and every number in the sweep depends on it.
