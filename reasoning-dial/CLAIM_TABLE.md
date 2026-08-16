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

**who:** A · **status:** SUPPORTED, and superseded in remedy by `RD_011`

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

**who:** A · **status:** SUPPORTED on its own terms, **response family REFUTED** by `RD_010`

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

---

# Second drop

Claims arising from [`SOURCE_DROP_2.md`](SOURCE_DROP_2.md), the research
landscape. **Nothing below verifies that the surveyed papers exist or say what
the survey says they say** — their citation markers point outside the delivery
and the dates sit at the edge of what is checkable from here. Every finding is
internal: the survey against its own quotations, the framework against its own
model.

---

## RD_010 — the response family in `dial_response.py` forbids the phenomenon

**who:** A · **status:** SUPPORTED. Refutes this folder's own prior model.

`SOURCE_DROP_2` reports negative marginal utility as the central empirical
finding of the work it surveys: past some budget, additional thinking flips
correct answers to incorrect ones.

A logistic is monotone. Its gradient is positive everywhere, measured at
`1.0e-08` to `6.3e-03` across the three difficulties over 2 to 10⁷ tokens.
`dial_response.py` therefore cannot represent overthinking at any parameter
setting, and `RD_003` reported that the family "behaves well" while that
family ruled out the effect by construction.

This is a correction to the audit, not to the drop. The saturating model was
chosen to match the *first* drop's prose, which described saturation; the
second drop says the prose was describing the wrong shape.

**Falsifier:** a monotone response family exhibiting negative marginal
utility. There is none — monotone means the gradient does not change sign.
The claim is refutable only by showing that real quality-vs-budget curves do
not decline, which is a measurement, not an argument.

**Evidence:** `overthinking.py` §1; `samples/overthinking.sample.txt`.

---

## RD_011 — with a declining branch the stopping rule becomes well-posed

**who:** A · **status:** SUPPORTED

Model the response as a logistic rise minus drift accruing per log-token.
`argmax Q` — equivalently the zero of `dQ/d(log B)` on the declining side —
is then unique, interior, and independent of the sweep window:

```
problem                     argmax Q    Q there   interior
Easy (pattern match)             444      0.914       True
Medium (multi-step)             8194      0.805       True
Hard (novel mechanism)        224214      0.675       True
```

Every objection `RD_002` raised against `argmax |curvature|` dissolves — not
because the objection was wrong, but because the rule is **unnecessary**. The
surveyed work's own primitive is marginal utility crossing zero, which has no
tie to break and no shoulder to choose.

The `interior` column is a guard against exactly the failure `RD_002`
documented: an extremum reported at the edge of a sweep is a property of the
sweep. It passes for all three.

**Falsifier:** a plausible response shape on which `dQ/d(log B) = 0` has
multiple interior solutions. Multi-modal quality curves would do it, and
nothing here rules them out — the model has one rise and one drift by
construction.

**Evidence:** `overthinking.py` §2.

---

## RD_012 — on this shape the knee rule stops far too early

**who:** A · **status:** SUPPORTED

`SOURCE_DROP_2`'s synthesis table maps "knee detection (max curvature)" onto
"optimal stopping point". On a curve with a declining branch these are not the
same point, and the gap is large:

```
problem                     argmax Q    knee rule   knee/opt
Easy (pattern match)             444           76       0.17
Medium (multi-step)             8194          680       0.08
Hard (novel mechanism)        224214        14024       0.06
```

The knee lands at 6–17% of the optimal budget, always early, and the error
**grows with difficulty** — worst exactly where the budget matters most. It
is not a conservative version of the optimum; it is a different point on the
curve.

**Falsifier:** show the surveyed paper's stopping rule is curvature-based
rather than marginal-utility-based. The survey's own summary says otherwise —
it describes tracking where marginal utility goes negative — so the synthesis
table's mapping appears to be the survey's, not the paper's.

**Evidence:** `overthinking.py` §3.

---

## RD_013 — the novelty claim is undercut by the survey's own quotation

**who:** A · **status:** SUPPORTED

`SOURCE_DROP_2` closes: *"None of these papers explicitly compute
cross-gradients... The 'Overthinking' paper measures marginal utility by
difficulty level but doesn't formalize it as a mixed partial derivative."*

Six sections earlier the same document quotes that paper: *"easier problems
(Level 1-2) reach negative marginal utility earlier than hard problems."*

That sentence is a statement about how the zero of the budget-gradient moves
with problem difficulty — the mixed partial, measured, stratified by
difficulty, and reported. The quantity is already an object of study. What is
not standard is the notation.

The contribution is real and smaller than claimed: writing the ordering as a
derivative turns a fact to be reported into a consequence to be derived, with
a falsifier attached (`RD_014`). Prose does not do that. But "no paper
computes this" and "the paper measures this by difficulty level" cannot both
stand, and the second is the survey's own quotation of the source.

**Falsifier:** show the quoted sentence reports something other than the
difficulty-dependence of the optimal stopping budget.

**Evidence:** `SOURCE_DROP_2.md` §1 against its closing section;
`overthinking.py` §4.

---

## RD_014 — "easier problems flip earlier" follows from problem-independent drift

**who:** A · **status:** SUPPORTED (generator scope), with a cheap falsifier

In `overthinking.py` the drift rate is identical across difficulties — damage
from overthinking is modelled as a property of the reasoning system, not of
the problem. Only the rise moves with `D_r`. The optimal stop then comes out
monotone increasing (444 / 8194 / 224214) without that ordering being put in.

An easy problem finishes rising sooner, so a fixed drift overtakes it sooner.
The empirical ordering needs no separate explanation.

**Falsifier, and it is the most valuable measurement named anywhere in this
folder:** estimate the drift rate on problems of different difficulty. If it
is flat, the ordering is explained. If drift varies systematically with
difficulty, this model is wrong and the ordering is an independent empirical
fact requiring its own account.

That measurement also settles `RD_007`: it requires exactly the
quality-vs-budget curves whose absence keeps every quantity in this folder at
generator level.

**Evidence:** `overthinking.py` §4.

---

## RD_015 — the second drop's citations are unverifiable, as the first drop's were

**who:** A · **status:** UNVERIFIED

Extends `RD_008`. The surveyed papers — "Overthinking in LLM Test-Time Compute
Scaling", BetaPRM, TRIM, R2R, the metacognition framework, "Predictive
Metacognition", the Gap Function paper, T² scaling laws — carry
`cite web_search:NN#M` markers pointing at results not included in the
delivery, and are dated January–May 2026.

`UNVERIFIED` is a gap, not a negative verdict. The specific numbers quoted
(97% of peak accuracy at 60% of compute; 33.57% token reduction; ≈6% divergent
tokens; 6× cost-efficiency; Brier reductions of 11.6% and 17.2%) are
internally plausible and mutually consistent, and nothing here suggests
otherwise. They simply cannot be checked from what arrived, and no claim in
this folder rests on them.

**Falsifier:** supply the citations.
