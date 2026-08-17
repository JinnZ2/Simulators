# reasoning-dial

A drop about how reasoning models allocate thinking, put through the gate
that the last drop produced.

The delivered material is in two parts: a survey of 2026 work on reasoning,
learning, exploring and harnesses; and a proposal to treat the **thinking
budget as a measurable dimension** — an axis with gradients, cross-gradients
and a knee, read with the same machinery this repo uses for physical fields.

The proposal is good and it mostly works. One part of it does not, and the
part that fails is the same one that failed in
[`aperiodic-order-sim-stack/`](../aperiodic-order-sim-stack/) on a completely
unrelated substrate.

**A second drop then arrived** — a research landscape placing the framework
against 2026 work on adaptive computation allocation. It reports something
neither the first drop nor my model of it can represent: quality does not just
saturate with thinking budget, it *declines*. That refutes the response family
I chose, replaces the knee with a better primitive, and undercuts the
landscape's own novelty claim. See [Second drop](#second-drop).

## Contents

| File | What it is |
| --- | --- |
| [`SOURCE_DROP.md`](SOURCE_DROP.md) | First delivered piece — survey + the dial proposal, **verbatim**. |
| [`SOURCE_DROP_2.md`](SOURCE_DROP_2.md) | Second delivered piece — the research landscape, **verbatim**. |
| [`dial_response.py`](dial_response.py) | The dial as a dimension, implemented, and a check on the numbers the drop published. Stdlib only. |
| [`gate_dial.py`](gate_dial.py) | The drop's own claims run through [`../reasoning-gate/`](../reasoning-gate/). Cross-folder import, not a copy. |
| [`overthinking.py`](overthinking.py) | The declining branch the second drop reports, and what it costs the knee. Stdlib only. |
| [`CLAIM_TABLE.md`](CLAIM_TABLE.md) | Fifteen claims (`RD_001..015`) under a REFUTATION_PROTOCOL. |
| [`samples/`](samples/) | Pinned output of both scripts. |

```bash
python3 dial_response.py    # the model, and the table under test
python3 overthinking.py     # the declining branch, and what it costs the knee
python3 gate_dial.py        # the same claims, gated
```

Standard library only, deterministic. `gate_dial.py` imports the gate from
`../reasoning-gate/` so the two cannot drift; `GATE_SRC` overrides the path.
This is the repo's second cross-folder Python import, after
[`msiaf-gdprf-bridge/`](../msiaf-gdprf-bridge/).

## What holds

**The gradient transfers.** `dQ/d(log B)` is a well-defined marginal value of
one more thinking step, computable from any response curve you can measure.
Nothing about the dial being a control parameter rather than a field breaks
the calculus.

**The cross-gradient is the best idea in the drop.** `∂²Q/∂(log B)∂D_r`
answers the question that actually matters in the field: *given this problem
and this signal quality, is more thinking worth buying?* Reproduced here — at
a fixed 1000-token budget the gradient peaks at intermediate difficulty and
the cross-gradient changes sign there, exactly as claimed. It is also the one
part that does not depend on locating a knee.

**The drop is honest about its own limits**, more so than most: *"D_r is a
phenomenological parameter fit from the curve, not a fundamental property
like fractal dimension."* That concession is correct.

## What does not

### The knee table contradicts its own prose

| Problem | D_r | Knee | Gradient |
| --- | ---: | ---: | ---: |
| Easy | 0.5 | 26 tok | 0.21 |
| Medium | 2.0 | 910 tok | 0.06 |
| Hard | 4.0 | **66 tok** | **0.12** |

The sentence above that table reads: *"For an easy problem, the knee is early
and the gradient is steep... For a hard problem, the knee is later and the
gradient is shallower."*

The hard problem's knee is 14× **earlier** than the medium problem's, and its
gradient is twice as **steep**. Both columns run backwards from the claim
they illustrate.

### And the reason is that "maximum curvature" names two points

Any saturating curve has **two** curvature extrema — one where returns begin,
one where they stop. On a logistic in log-budget they sit at `z = ±1.3170`
and are **exactly equal in magnitude**. A rule that maximises `|curvature|`
is choosing between tied candidates, and nothing in the data breaks the tie.

`dial_response.py` measures the tie at `0.000e+00`, then reproduces the
delivered table's shape on an independent implementation with different
constants:

```
problem                     D_r   knee (tok)     shoulder  sat in win
Easy (pattern match)        0.5         76.3   saturation        True
Medium (multi-step)         2.0        715.7   saturation        True
Hard (novel mechanism)      4.0         37.8     take-off       False

Pattern:   ['76', '716', '38']
Delivered: ['26', '910', '66']
```

Small, large, small — non-monotone, and the flip lands on the same row.

The mechanism is compound. The tie means nothing in the curve prefers a
shoulder; the **sweep window** then decides which one is reachable. For the
hardest problem the saturation shoulder sits at ~14,000 tokens, outside a
10⁴-token window, so only the take-off shoulder survives — and the reported
knee collapses by an order of magnitude exactly where the problem got harder.

**A knee that moves when you change the plot range is a property of the plot
range.**

### The fix is one word

Say which shoulder. Define the knee as the **saturation** shoulder — the only
one that is a stopping rule — and the same model gives 76 / 716 / 14,170
tokens with gradients 0.247 / 0.124 / 0.074. Monotone in both columns,
matching the prose exactly. The idea is implementable; the rule was
under-specified.

### RND is described as the wrong algorithm

> "Random Network Distillation (RND): the agent tries to predict the outcome
> of its actions."

That is the **Intrinsic Curiosity Module** (Pathak et al. 2017). RND (Burda
et al. 2018) trains a predictor to match a **fixed, randomly-initialised
target network** on the observation — no action, no forward dynamics, no
outcome.

The conflation is load-bearing. RND exists specifically to avoid the
**noisy-TV problem**, where a forward-dynamics agent parks in front of a
stochastic observation and farms unbounded prediction error forever.
Describing RND as forward-dynamics prediction attributes to it the exact
failure it was built to prevent, and erases the reason to prefer it.

## Through the gate

`gate_dial.py` declares three of the drop's claims and closes them. Three
declarations, three different outcomes, none of them "bad drop":

| Run | Outcome |
| --- | --- |
| **DIAL-KNEE** | **Denied at `pre()`** on G-RES. The rule's positional ambiguity is 3.56 log-units — a 35× span in tokens — against a knee shift of 2.99 it is meant to detect. The table never gets recorded. |
| **DIAL-GRAD** | **Passes, and splits.** Two claims on identical support: the generator-scoped one is `supported`, the one about a deployed model is `qualified` by G-LAYER. |
| **DIAL-SYNTH** | **Passes, qualified.** G-IND requires the shared input named, so "four independent domains converge" becomes a claim about one survey. |

DIAL-GRAD is the useful one. The same two numbers support this:

> `dQ/d(log B)` at fixed budget peaks at intermediate difficulty  — **supported**

and fail to support this:

> a reasoning model gains most from extra thinking on intermediate-difficulty
> problems  — **qualified**

That gap is the whole finding, and it names the missing experiment exactly.
Not better maths: a **measured** quality-vs-budget curve from a real model,
with the budget under your control and quality scored by something that is
not the model. That single measurement promotes `D_r` from generator-level to
physical and lets the second claim stand. It is cheap, and nobody in this
chain has run it.

## Where the gate did not help

Worth recording, because it is a limit and not a success.

**G-FIT should have caught the knee ambiguity and could not.** Its rule is
"restate the question and name why the chosen statistic can discriminate it";
its implementation checks that a `discriminates` string is non-empty. "A knee
separates the paying region from the saturated one" satisfies it, and is
wrong in the specific way that matters. The ambiguity only became a denial
once it was rewritten as two numbers for G-RES.

This is [`../reasoning-gate/AUDIT_NOTES.md`](../reasoning-gate/AUDIT_NOTES.md)
§1 in a second instance: a guard is only as strong as what the operator
chooses to declare, and nothing makes them declare the binding thing. §1 found
it on G-RES. Here it is G-FIT, which is worse, because G-FIT's whole subject
is whether the statistic can answer the question — and it accepts prose.

**G-STATE is proposed by the drop and is not built here.** The drop asks for
an observer-state guard: *am I cold, time-pressured, invested in a
diagnosis?* The gap is real — every existing guard constrains what the run
declares about the world, none constrains what the operator declares about
themselves. It is not implemented because a self-report from a miscalibrated
observer is exactly the quantity in question; the gate could record it but
not check it. Logged as `RD_009` with the condition that would make it
buildable: tie it to something outside the operator's own report — cabin
temperature, hours since sleep, a timestamp — and it becomes a two-number
guard like G-RES.

## Second drop

A research landscape arrived placing the framework against 2026 work on
adaptive computation allocation — marginal utility, BetaPRM, stepwise and
token-level routing, metacognitive self-governance, the Gap Function, T²
scaling laws. It does three things to the first drop, and to my reading of it.

**None of it verifies the surveyed papers.** Their citation markers point
outside the delivery and they are dated January–May 2026. Every finding below
is internal: the survey against its own quotations, and the framework against
its own model.

### It refutes the response family — mine, not the drop's

The survey's central reported finding is *negative marginal utility*: past
some budget, additional thinking flips correct answers to incorrect ones.

`dial_response.py` models the response as a logistic. A logistic is monotone.
Its gradient is positive everywhere — measured at `1.0e-08` to `6.3e-03`
across the three difficulties — so it **cannot produce overthinking at any
parameter setting**. `RD_003` reported that the family behaves well, and it
does; it also rules out the effect by construction.

That is a correction to this folder's audit, not to the drop. Recorded as
`RD_010`.

### It replaces the knee with a better primitive

Rebuild the response as a rise minus drift accruing per log-token, and the
stopping point becomes `argmax Q` — the zero of `dQ/d(log B)` on the declining
side:

```
problem                     argmax Q    Q there   interior
Easy (pattern match)             444      0.914       True
Medium (multi-step)             8194      0.805       True
Hard (novel mechanism)        224214      0.675       True
```

Unique, interior, independent of the sweep window. Every objection `RD_002`
raised against `argmax |curvature|` dissolves — not because the objection was
wrong, but because **the rule is unnecessary**. The surveyed work's own
primitive is marginal utility crossing zero, which has no tie to break and no
shoulder to choose.

The `interior` column is a guard against precisely the failure `RD_002`
documented. It passes for all three.

**Keeping the knee would be expensive.** The survey's synthesis table maps
"knee detection (max curvature)" onto "optimal stopping point". On a curve
with a declining branch they are different points:

```
problem                     argmax Q    knee rule   knee/opt
Easy (pattern match)             444           76       0.17
Medium (multi-step)             8194          680       0.08
Hard (novel mechanism)        224214        14024       0.06
```

6–17% of the optimal budget, always early, and the error **grows with
difficulty** — worst exactly where the budget matters most. The knee is not a
conservative optimum; it is a different point on the curve. (`RD_012`)

### It undercuts its own novelty claim

The landscape closes: *"None of these papers explicitly compute
cross-gradients... The 'Overthinking' paper measures marginal utility by
difficulty level but doesn't formalize it as a mixed partial derivative."*

Six sections earlier the same document quotes that paper: *"easier problems
(Level 1-2) reach negative marginal utility earlier than hard problems."*

That sentence **is** the mixed partial — how the zero of the budget-gradient
moves with difficulty — measured, stratified, and reported. The quantity is
already an object of study. What is not standard is the notation.

Smaller than claimed, and still real. `overthinking.py` §4 is the argument
for it: with drift held problem-independent, the ordering 444 / 8194 / 224214
*falls out* rather than being put in. An easy problem finishes rising sooner,
so a fixed drift overtakes it sooner. Written as a derivative, the empirical
ordering stops being a fact to report and becomes a consequence to derive —
with a falsifier attached. Prose does not do that. (`RD_013`, `RD_014`)

### The measurement that would settle everything

`RD_014`'s falsifier is the most valuable experiment named anywhere in this
folder: **estimate the drift rate on problems of different difficulty.** Flat
drift explains the ordering for free. Difficulty-dependent drift refutes the
model and makes the ordering an independent fact needing its own account.

It requires exactly what `RD_007` and `gate_dial.py`'s DIAL-GRAD split are
already asking for — measured quality-vs-budget curves from a real model. One
experiment, three open claims closed.

## Cross-repo

- [`aperiodic-order-sim-stack/`](../aperiodic-order-sim-stack/) — `AOS_005`
  is the same knee defect: a detector fired on the largest of six comparable
  curvature peaks and landed on a local *minimum* of the curve it was meant
  to find the knee of. Here it fires on one of two exactly tied extrema. Two
  drops, two substrates, one under-specified rule.
- [`reasoning-gate/`](../reasoning-gate/) — the gate, imported not copied.
  Its README calls itself n=1 and asks to be tested against a second audit.
  This is that second audit, and the answer is that it transfers unmodified —
  with G-FIT's prose-only check as the new finding.
- [`model-ecology/`](../model-ecology/) — `confound_sweep.py` finds the fit
  window to be the largest and most invisible confound. §3 here is that
  result again: the window, not the curve, sets which knee you get.
- [`null-harness/`](../null-harness/) — the missing measurement in `RD_007`
  and `RD_014` is exactly its known-truth-first invariant applied one level
  up. You cannot grade an unknown response curve before recovering a known
  one.
- [`equivalence-field/`](../equivalence-field/) — `claim_lineage.py` treats a
  refuted claim as evidence the variable set was incomplete. `RD_010` is that
  shape: the logistic was not wrong arithmetic, it was a missing dimension
  (the declining branch), and `RD_011` is the child claim the break pointed
  at.

## License

CC0-1.0, matching the repository default.
