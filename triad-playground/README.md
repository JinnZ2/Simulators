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
| [`SOURCE_DROP.md`](SOURCE_DROP.md) | The delivered proposal, **verbatim**. |
| [`triad.json`](triad.json) | The schema. Single source of truth: agents, dial vector, calibration checks, shadow protocol, pedigree fields. |
| [`CHECKLIST.md`](CHECKLIST.md) | Human-fillable pre-run checklist, **generated** from `triad.json`. |
| [`make_checklist.py`](make_checklist.py) | The generator. Regenerates byte-identically. |
| [`shadow_design.py`](shadow_design.py) | Does the shadow-sim pattern measure what it is for? Four checks. Stdlib only. |
| [`CLAIM_TABLE.md`](CLAIM_TABLE.md) | Seven claims (`TP_001..007`) under a REFUTATION_PROTOCOL. |
| [`samples/`](samples/) | Pinned output. |

```bash
python3 shadow_design.py     # the four checks
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

## License

CC0-1.0, matching the repository default.
