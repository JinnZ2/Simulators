# triad-playground

Every experiment has three agents — the physical system, the measurement
instrument, and the reasoning agent reading the numbers. The claim is only as
strong as the weakest calibration in the chain.

That framing is the contribution, and it holds. The protocol built on top of
it, as specified, does not yet measure what it is for. Three design results
below, all with cheap fixes, none of which requires abandoning the idea.

## Contents

| File | What it is |
| --- | --- |
| [`SOURCE_DROP.md`](SOURCE_DROP.md) | The first delivered proposal, **verbatim**. |
| [`SPEC_V1.md`](SPEC_V1.md) / [`spec_v1.json`](spec_v1.json) | The generic v1 protocol delivered for reuse, **verbatim**. |
| [`triad.json`](triad.json) | The schema. Single source of truth: agents, dial vector, calibration checks, shadow protocol, pedigree fields. |
| [`CHECKLIST.md`](CHECKLIST.md) | Human-fillable pre-run checklist, **generated** from `triad.json`. |
| [`make_checklist.py`](make_checklist.py) | The generator. Regenerates byte-identically. |
| [`shadow_design.py`](shadow_design.py) | Does the shadow-sim pattern measure what it is for? Four checks. Stdlib only. |
| [`shadow_panel.py`](shadow_panel.py) | **With or without the human?** Panel composition vs `N_eff` and false-pass rate. Stdlib only. |
| [`CLAIM_TABLE.md`](CLAIM_TABLE.md) | Thirteen claims (`TP_001..013`) under a REFUTATION_PROTOCOL. |
| [`samples/`](samples/) | Pinned output. |

```bash
python3 shadow_design.py     # the four design checks
python3 shadow_panel.py      # with or without the human
python3 make_checklist.py    # regenerate CHECKLIST.md after editing triad.json
```

Standard library only, deterministic. Same `schema → generated doc`
arrangement as [`reasoning-gate/`](../reasoning-gate/)'s
`guards.json → GUARDS.md`.

## What holds

**The fourth layer.** [`reasoning-gate/`](../reasoning-gate/) tags every
quantity `generator` / `physical` / `instrument` and has no slot for the
observer. [`instrument-epistemology/`](../instrument-epistemology/) grades six
instruments on transduction chain and blindness map, and the reader is outside
the frame in all six. This drop supplies the missing layer and puts the
reasoning agent on the same footing as the other two.

`triad.json` records it as `layer = generator | physical | instrument |
reasoning`, with the rule that a physical-scope claim resting on
reasoning-level support is `qualified`, not `supported` — the same rule
`gate.py` already applies to generator-level support.

**The dial as a vector, not a scalar.** Three independent axes, and the point
is how errors in one propagate through the others. That is right, and it is
what makes §1 below matter.

## What does not

### Step 5 forbids the design step 6 requires

> **step 5** — "Never upgrade all three simultaneously (can't attribute
> variance)."
> **step 6** — "Cross-gradient: did conclusion change with dial setting?"

Step 5 is one-factor-at-a-time. Step 6 asks for an **interaction**. OFAT
cannot estimate an interaction at any number of runs, because no run in an
OFAT design varies two factors together.

On a response with a planted interaction (P = 1.0, I = 0.5, R = 2.0,
P×R = 3.0):

```
OFAT, 4 runs      P 1.00   I 0.50   R 2.00   P*R  n/a
                  predicts y(P=1,R=1) = 3.0, truth 6.0, error 3.0
                  — the entire interaction, invisible and unattributed

2^3 factorial     P 2.00   I 1.00   R 4.00   P*R 6.00   P*I 0.00
8 runs            every effect recovered exactly
```

The stated reason for OFAT — *"can't attribute variance"* — is backwards. A
factorial attributes variance to each factor **and** to their interactions.
OFAT attributes it only to factors, and silently loads any interaction onto
whichever main effect was varied last.

**Fix:** 2³ factorial at low/high over the three dials, then upgrade the axis
with the largest effect. Four extra runs. (`TP_002`)

### Consensus is blind to the error the shadows share

The shadow test is *"Do the three agree? If not, the axis is
underdetermined."* But the four shadows read the same physical declaration,
the same instrument output, and — for the AI shadows — the same prompt,
written by one of the human shadows.

Model each as `truth + shared_bias + individual_noise`:

```
 shared bias    mean shadow         spread   error vs truth
         0.0         100.01           2.04             0.01
         5.0         105.01           2.06             5.01
        20.0         120.00           2.02            20.00
```

Spread does not move. Error tracks the bias one-for-one. **Four shadows
agreeing tightly at 120 when the truth is 100 is exactly what this looks like
from inside** — and consensus reports it as a pass.

**Fix, and most of it is already built.**
[`divergence-playground/`](../divergence-playground/) is this protocol with
the null attached: readings hash-sealed before reveal so later readers cannot
anchor on earlier ones, spread on three declared axes rather than eyeballed,
and `null_ensemble.py` for shuffle and permutation nulls. Its
`agree_by_accident` flag is the cell the shadow protocol needs most —
shadows reaching the same verdict by different mechanisms. (`TP_003`)

### The first experiment cannot fail its own skip condition

> "If all four observers agree within instrument resolution, observer
> variance is negligible."

The expansion is easy to see: a 1 m aluminium bar over 60 K moves 1.386 mm
against a 0.01 mm division — a factor of 139. But the experiment is about
observer variance, and there the numbers invert:

```
observer reading spread   ~0.005 mm   (half a division)
instrument resolution      0.010 mm
ratio                      0.50
```

Four people reading one mechanical dial agree to within a division because a
division is the quantum of what the dial can say. The condition fires
whatever the truth is, so "negligible" is a statement about the dial. That is
[`null-harness/`](../null-harness/)'s `CONSTANT_SILENT`, and `G-RES`: a null
from an instrument that could not have seen the feature.

**Fix, cheap, no better bar needed.** The instrument must record
*independently of the observer reading it* — a digital indicator with a data
log, or a timestamped photograph of the dial. The observer writes a value
without seeing the log. Observer error becomes `|observer − logged|`,
measured directly instead of inferred from consensus, and the skip condition
can now fail. (`TP_004`)

### The worked example shows a different failure than claimed

The aluminium run goes "crack at 200 cycles" → "1,800 ± 400" → "no crack;
this is wrought, not cast", and the drop reads the sign change as a
reasoning-dial cross-gradient.

Run 3 says something else: runs 1 and 2 were answering a question about *cast*
aluminium while the specimen is *wrought*. That is the physical declaration
being wrong and the high-dial observer catching it.

The distinction is load-bearing. If a mis-specified physical system is scored
as reasoning-dial variance, then **every physical error the reasoning agent
catches inflates the measured observer variance** — and the playground
concludes the observer is unreliable when what happened is that the observer
was right.

**Fix:** `triad.json` check `P4` records `state_revised_during_run` separately
from `state_declared`. A run that revises the physical declaration reports a
*physical* finding, not a reasoning gradient. (`TP_005`)

## On the reasoning checks

Of the four reasoning-agent checks, only the AI one — model version, thinking
budget, temperature, context window — is readable from outside the observer.
Fatigue, emotional investment and conflict of interest are declarations, and
a declaration from a miscalibrated observer is the quantity in question.

That is [`reasoning-dial/`](../reasoning-dial/)'s `RD_009` at system scale,
and the same reason `G-STATE` was logged there rather than built. `triad.json`
marks each check's `readable` field and `CHECKLIST.md` renders `[DECLARED]`
against the three that are not measurements — the distinction is carried in
the pedigree rather than hidden. (`TP_006`)

## What is still unrun

Everything above is a design result — a property of the experimental design
and the consensus rule, provable without data. The load-bearing empirical
question is untouched:

**does observer variance matter at any scale worth measuring?**

`TP_004`'s fix makes it measurable. Nobody has measured it. The first real
result is one bar, one indicator with a data log, and one afternoon.
(`TP_007`)

## With or without the human?

The question the v1 spec came with. v1 requires `human_baseline`, `ai_low`,
`ai_high`, with `human_degraded` optional.

Model each shadow as `truth + b_shared + b_family + e_ind` and read the panel
two ways — `N_eff`, the participation ratio of the shadow correlation
spectrum, and the false-pass rate, `P(shadows agree | panel mean wrong by
more than tolerance)`:

```
panel                                      k   N_eff    spread  false-pass
v1 required: human + AI-low + AI-high      3    1.61     1.346       38.2%
v1 full: + human_degraded                  4    1.72     1.577       25.1%
v1 minus the human                         2    1.14     0.565       84.2%
no human, 4 shadows, one model             4    1.22     1.027       50.2%
no human, 3 model families                 3    1.93     1.596       26.8%
no human, 4 model families                 4    2.18     1.938       12.4%
human + 3 model families                   4    2.16     1.929       12.7%
```

**Yes, it works without the human — but the human's decorrelation has to be
replaced, not just removed.**

Four model families with no human reach `N_eff` 2.18 and false-pass 12.4%,
**stronger than v1's required panel with a human** (1.61, 38.2%). Adding the
human back on top of that moves `N_eff` by −0.02, inside the noise.

Drop the human from v1's panel without substituting and it collapses:
`N_eff` 1.61 → 1.14, false-pass 38% → **84%**. A panel that returns a
confident wrong answer 84 times in a hundred is not a check.

The reason is that `ai_low` and `ai_high` **on one model** share a family
bias — they are close to one shadow at two dial settings, so the human is the
only decorrelated element v1's required panel has. The design variable is not
human-vs-AI. It is how many independent failure modes the panel contains.

Three consequences for the spec:

1. **`ai_low` and `ai_high` are not two shadows.** On one model they are one
   shadow at two budgets, which is a reasoning-*dial* measurement. Both are
   worth doing; they answer different questions.
2. **Require a minimum `N_eff`, not a minimum count.** A four-shadow panel
   can carry `N_eff` = 1.22. Counting shadows measures effort.
   [`model-ecology/phylogeny.py`](../model-ecology/phylogeny.py) already
   computes this statistic — fifteen estimators there turn out to carry
   `N_eff` = 2.48. (`TP_009`)
3. **The substitution for a human is three model families, not three
   budgets.** That is a procurement fact rather than an epistemics problem:
   three vendors, not three prompts.

What a human still uniquely supplies is **embodied context** — cold-stiffened
proprioception is not a failure mode any model has. That argues for a human
shadow on *physical* measurements specifically, and it is a different
argument from the decorrelation one. (`TP_008`)

The ranking survives a five-point sweep of the variance components; the
absolute rates do not and are illustrative. (`TP_013`)

## What v1 changed, and what it did not

v1 is a real improvement on the first drop in one place and unchanged in
three.

**Improved:** `"Variance must be compared against instrument resolution, not
against zero."` That addresses half of `TP_004`. It is still the wrong
denominator — instrument resolution bounds what the *instrument* can say,
while shadow spread is bounded by what an *observer* can repeat. The correct
reference is same-observer repeat variance, which is also the null `TP_003`
says is missing. (`TP_010`)

**Sharpened, not fixed:** v1 §5 now names `∂²/∂(physical)∂(reasoning)` and
`∂²/∂(instrument)∂(reasoning)` explicitly, while §2 rule 3 still says
"upgrade ONE dial at a time". Rule 3 is the binding one; rule 4 ("never
upgrade all three") would happily permit a 2² factorial over a pair. So the
fix is now one line: replace rule 3 with *"vary dials in a 2² factorial over
the pair whose interaction is being tested"* and keep rule 4. Four runs per
pair. (`TP_011`)

**New problem:** §6 maps `G-DIM` to *"checks that dial settings are actually
different compute levels"*. `G-DIM` voids ratios across unlike objects and
does not do this. The job named is real and unassigned — **nothing verifies
that `ai_low` and `ai_high` actually produced different reasoning effort**,
and a model ignoring its budget parameter would collapse two declared shadows
into one silently, which is `TP_008`'s failure mode arriving undeclared. The
check reads like a `G-RES` pair: declared budget separation versus observed
reasoning-token separation, with a margin. (`TP_012`)

## Cross-repo

- [`reasoning-gate/`](../reasoning-gate/) — the epistemics this applies at
  system level. `G-RES`, `G-CTRL` and `G-LAYER` all fire on the protocol as
  specified; `triad.json` extends its three layers with a fourth.
- [`divergence-playground/`](../divergence-playground/) — the shadow protocol
  with the null already attached. The overlap is close enough that the shadow
  pattern is best read as a special case: readers replaced by observers, one
  fork point replaced by one measurement.
- [`null-harness/`](../null-harness/) — `TP_004` is its invariant exactly. A
  skip condition that cannot fire has not been shown to work.
- [`instrument-epistemology/`](../instrument-epistemology/) — grades
  instruments and leaves the reader outside the frame. This is the folder that
  puts the reader in it.
- [`reasoning-dial/`](../reasoning-dial/) — `RD_009`'s `G-STATE` gap is
  `TP_006` here, unchanged by the change of scale.
- [`model-ecology/`](../model-ecology/) — `phylogeny.py` computes the same
  participation ratio `TP_009` asks the spec to require, on a family of
  estimators rather than a panel of observers. Fifteen estimators, `N_eff` =
  2.48. The shadow panel is that question with the estimators replaced by
  readers.

## License

CC0-1.0, matching the repository default.
