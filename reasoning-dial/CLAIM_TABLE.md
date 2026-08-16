# CLAIM_TABLE — reasoning-dial

Claims from [`SOURCE_DROP.md`](SOURCE_DROP.md) and from the audit here.

`who` follows the [`claim-audits/`](../claim-audits/) convention:
**D** = the drop's own claim, **A** = an audit claim added here.

## REFUTATION_PROTOCOL

1. A failed check updates the **claim**, not the model. `dial_response.py`'s
   constants are not retuned to preserve any entry here.
2. Absence of a verifiable source is logged `UNVERIFIED` — a gap, not a
   negative verdict. The drop's inline `cite web_search:NN#M` markers point
   at results not included in the delivery and cannot be resolved from what
   arrived.
3. Nothing in this folder is a claim about a deployed reasoning model. No
   reasoning model was run. Every quantity in `dial_response.py` is
   generator- or instrument-level, and `gate_dial.py` enforces that.

---

## RD_001 — the knee table contradicts its own prose

**who:** A · **status:** SUPPORTED

The delivered table gives knee locations 26 / 910 / 66 tokens for
D_r = 0.5 / 2.0 / 4.0, and gradients 0.21 / 0.06 / 0.12. The prose directly
above it says "For an easy problem, the knee is early and the gradient is
steep... For a hard problem, the knee is later and the gradient is
shallower."

Both columns are non-monotone. The hard problem's knee is 14× **earlier**
than the medium problem's, and its gradient is twice as **steep**. The table
and the sentence describe opposite behaviours.

This is the same shape as `AOS_005` one folder over: SIM-C's report block
contains "knee detected at f = 0.65" and "does not show a sharp threshold"
in the same section.

**Falsifier:** produce the generating code and show the table is monotone
under a stated ordering of the rows, or show the prose describes a different
quantity than the table's "Knee Location" column.

**Evidence:** `SOURCE_DROP.md` Part 3; `dial_response.py` §1.

---

## RD_002 — "maximum curvature" does not name one point

**who:** A · **status:** SUPPORTED

Any saturating response curve has **two** curvature extrema: one where
returns begin, one where they stop. On a logistic in log-budget they sit at
`z = ±ln(2+√3) ≈ ±1.3170` and are **exactly equal in magnitude**, opposite
in sign. A rule that maximises `|curvature|` is therefore choosing between
two tied candidates, and nothing in the data breaks the tie.

`dial_response.py` §3 measures the tie at `0.000e+00` and then reproduces the
delivered table's shape — small, large, small — on an independent
implementation with different constants, with the flip landing on the same
row.

The mechanism is compound. The tie means nothing in the curve prefers a
shoulder; the **sweep window** then decides which one is reachable. For the
hardest problem the saturation shoulder sits at ~14,000 tokens, outside a
10⁴-token window, so only the take-off shoulder survives and the reported
knee collapses by an order of magnitude exactly where the problem got harder.

A knee that moves when you change the plot range is a property of the plot
range. Convergent with `model-ecology/confound_sweep.py`, which finds the fit
window to be the largest and most invisible confound, on a different
substrate.

**Falsifier:** show the drop's knee finder maximises **signed** negative
curvature, or restricts to the saturation branch. Either would break the tie
and this claim with it — and would also make the delivered table monotone,
which it is not.

**Evidence:** `dial_response.py` §3;
`samples/dial_response.sample.txt`.

---

## RD_003 — declaring which shoulder makes the method work

**who:** A · **status:** SUPPORTED

With the knee defined as the **saturation** shoulder — the only one that is
a stopping rule — a logistic model with `μ` and `s` both increasing in `D_r`
gives knees of 76 / 716 / 14,170 tokens and gradients 0.247 / 0.124 / 0.074.
Monotone in both columns, matching the prose exactly.

The prose is implementable. The defect is in the knee rule, not the idea.

**Falsifier:** exhibit a monotone parameterisation whose saturation-shoulder
knee is non-monotone in `D_r`.

**Evidence:** `dial_response.py` §2.

---

## RD_004 — the cross-gradient claim survives

**who:** D · **status:** SUPPORTED (generator scope)

"At a fixed budget, the gradient is near-zero for trivial problems (already
saturated) and near-zero for extremely hard problems (the budget isn't enough
to matter). The peak is in the middle."

Reproduced: at B = 1000, `dQ/d(ln B)` rises from 0.0004 at `D_r = 0`, peaks
at `D_r = 3.0`, and falls to 0.053 by `D_r = 8`. The cross-gradient
`∂²Q/∂(ln B)∂D_r` changes sign at the peak, as an interior maximum requires.

This is the drop's most useful idea and the only part that does not depend on
locating a knee. **Scope is the limit**: it is a statement about the response
curve in `dial_response.py`, not about any reasoning model. `gate_dial.py`
records both versions of the claim on identical support and the gate
downgrades the physical one to `qualified`.

**Falsifier:** the same sweep on a response family where quality rises
monotonically in `D_r` at fixed budget. The interior peak requires
saturation at low `D_r`, which is an assumption, not a measurement.

**Evidence:** `dial_response.py` §4; `gate_dial.py` DIAL-GRAD.

---

## RD_005 — RND is described as the wrong algorithm

**who:** A · **status:** SUPPORTED

The drop states: *"The dominant theory in autonomous exploration is Random
Network Distillation (RND): the agent tries to predict the outcome of its
actions."*

That is not RND. RND (Burda et al., 2018) trains a predictor to match the
output of a **fixed, randomly-initialised target network** evaluated on the
observation. There is no action, no forward dynamics, and no outcome
prediction. The intrinsic reward is high on states the predictor has seen
little of — a novelty proxy, not a prediction-of-consequences signal.

Predicting the outcome of one's actions is the **Intrinsic Curiosity Module**
(Pathak et al., 2017), a different method.

The conflation is load-bearing rather than cosmetic. RND was designed
specifically to avoid the *noisy-TV problem*, in which a forward-dynamics
agent parks in front of a stochastic observation and farms unbounded
prediction error forever. Describing RND as forward-dynamics prediction
attributes to it the exact failure mode it exists to prevent, and erases the
reason to prefer it.

**Falsifier:** a definition of RND from the source in which the predictor
targets an action-conditioned outcome rather than a fixed random embedding of
the state.

**Evidence:** `SOURCE_DROP.md` Part 1 §III against Burda et al. 2018
("Exploration by Random Network Distillation") and Pathak et al. 2017
("Curiosity-driven Exploration by Self-supervised Prediction").

---

## RD_006 — the four domains are not four independent witnesses

**who:** A · **status:** SUPPORTED

"The convergence point is interior visibility" rests on four domains agreeing.
They are four sections of one survey, selected and framed together by one
author toward a thesis stated before the survey, and several cite the same
search results.

Naming the shared input does not refute the reading — interior visibility may
well be where the field is going. It downgrades "four domains converge" from
independent confirmation to a qualified claim about one survey. `gate_dial.py`
DIAL-SYNTH records exactly that, and G-IND is the guard that does it.

**Falsifier:** four surveys of the four domains written independently, by
authors not sharing a thesis, that reach the same synthesis.

**Evidence:** `gate_dial.py` DIAL-SYNTH.

---

## RD_007 — D_r is generator-level throughout

**who:** D · **status:** SUPPORTED, and stated by the drop itself

The drop concedes this: *"D_r is a phenomenological parameter fit from the
curve, not a fundamental property like fractal dimension"*, and *"The dial
dimension is similarly a property of the instrument, not the system under
study."* Then Part 3's "Fractal Connection" runs the analogy to `D_f` anyway.

Both halves of that are worth keeping. The concession is correct and unusually
explicit. The analogy is where it leaks — and `AOS_010` next door records the
identical move in the other direction, where a branching-walk parameter was
placed at the same epistemic level as a fact about aperiodic order.

**Falsifier:** fit `D_r` to measured quality-vs-budget curves from a real
model, with the budget controlled and quality scored by something that is not
the model. That single experiment promotes `D_r` from generator to physical
and is the missing piece for `RD_004`'s physical-scope claim.

**Evidence:** `SOURCE_DROP.md` Part 3; `gate_dial.py` DIAL-GRAD, where the
two claims split on identical support.

---

## RD_008 — the survey's specific attributions are unverified

**who:** A · **status:** UNVERIFIED

Several claims cannot be checked from what was delivered, because the
`cite web_search:NN#M` markers point at results not included:

- Zhu et al. 2026 on structural collapse and eRank
- "Adaptive Minds (Oct 2025)", "LoRA with Critical Parameter Constraints
  (Apr 2026)"
- The MIT TurtleBot4 result: 500 m², 40% faster than frontier exploration
- NARCBench and the Rose et al. AUROC figures
- MIT Technology Review's 2026 Breakthrough Technologies list
- WeightLens / CircuitLens (Golimblevskaia et al. 2026)

`UNVERIFIED` is a gap, not a negative verdict — the convention from
[`claim-audits/`](../claim-audits/). Several *other* claims in the same
survey do check out against established work: Snell et al. 2024 on test-time
compute, Titans and surprise-based memory, PRM800K, the min-form credit
assignment behind PURE, Anthropic's finding that Claude plans rhyme targets
backward, and the `circuit-tracer` library. The survey is not unreliable in
general; these particular entries are simply unresolvable as shipped.

**Falsifier:** supply the citations.

---

## RD_009 — G-STATE is a real gap in the gate, and it is not implementable there

**who:** D · **status:** PLAUSIBLE, NOT IMPLEMENTED

The drop proposes a guard the eight in
[`../reasoning-gate/guards.json`](../reasoning-gate/guards.json) do not have:
*"Am I cold? Am I time-pressured? Am I emotionally invested in a particular
diagnosis?"* — a declaration about the **observer's** state rather than the
instrument's.

The gap is real. Every existing guard constrains what the run declares about
the world; none constrains what the operator declares about themselves, and
the drop's own framing is right that the observer sits in the instrument
chain.

It is not implemented here, and the reason is the same one the drop names:
*"The hard part isn't the dial. It's knowing when your read on the dial is
itself miscalibrated."* A `G-STATE` field would record a self-report, and a
self-report from a miscalibrated observer is exactly the quantity in
question. The gate can record it; it cannot check it. That makes it a
different kind of guard from the eight, all of which compare two numbers or
check that a named thing exists.

Logged rather than built, because building it would imply a check that is not
there.

**Falsifier:** an operator-state declaration that can be validated against
something outside the operator's own report — timestamp, cabin temperature,
hours since sleep. Any of those would make `G-STATE` a two-number guard like
`G-RES`, and it should then be built.
