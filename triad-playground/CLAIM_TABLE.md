# CLAIM_TABLE — triad-playground

Claims from [`SOURCE_DROP.md`](SOURCE_DROP.md) and from the audit here.

`who` follows the [`claim-audits/`](../claim-audits/) convention:
**D** = the drop's own claim, **A** = an audit claim added here.

## REFUTATION_PROTOCOL

1. A failed check updates the **claim**, not the schema. `triad.json` is not
   retuned to preserve any entry here.
2. No triad experiment has been run. Every quantity in `shadow_design.py` is
   generator- or instrument-level except the two handbook values in §3
   (aluminium CTE, dial-indicator division), which are marked `[physical]`
   inline.
3. The three corrections below are corrections to the **protocol**, not to
   the framing. `TP_001` records that the framing is the load-bearing part
   and that it survives.

---

## TP_001 — the triad framing is the contribution and it holds

**who:** D · **status:** SUPPORTED

Naming the reasoning agent as an instrument with its own calibration, on
equal footing with the physical system and the measuring device, is a move
the rest of this repo has been circling without making.
[`reasoning-gate/`](../reasoning-gate/) tags every quantity `generator` /
`physical` / `instrument` and has no slot for the observer.
[`instrument-epistemology/`](../instrument-epistemology/) grades six
instruments on transduction chain and blindness map, and the reader is
outside the frame in all six.

The drop supplies the missing fourth layer. `triad.json` records it as
`pedigree_fields.layer = generator | physical | instrument | reasoning`,
with the rule that a physical-scope claim resting on reasoning-level support
is `qualified` rather than `supported` — the same rule `gate.py` already
applies to generator-level support.

**Falsifier:** show that observer variance is always below instrument
resolution in practice, making the fourth layer inert. `TP_004`'s fix is
what would let anyone measure that; nobody has.

---

## TP_002 — step 5 forbids the design step 6 requires

**who:** A · **status:** SUPPORTED

The workflow says *"Never upgrade all three simultaneously (can't attribute
variance)"* (step 5) and then *"Cross-gradient: did conclusion change with
dial setting?"* (step 6).

Step 5 is one-factor-at-a-time. Step 6 asks for an interaction. **OFAT cannot
estimate an interaction at any number of runs**, because no run in an OFAT
design varies two factors together.

Demonstrated on a response with a planted interaction (main effects
P = 1.0, I = 0.5, R = 2.0; interaction P×R = 3.0):

```
OFAT, 4 runs      P 1.00   I 0.50   R 2.00   P*R  n/a
                  predicts y(P=1,R=1) = 3.0, truth 6.0, error 3.0
                  -- the entire interaction, invisible and unattributed

2^3 factorial     P 2.00   I 1.00   R 4.00   P*R 6.00   P*I 0.00
8 runs            every effect recovered exactly (2x coefficients,
                  the standard +/-1 contrast scaling)
```

The stated reason for OFAT — "can't attribute variance" — is backwards. A
factorial attributes variance to each factor *and* to their interactions;
OFAT attributes it only to factors, and silently loads any interaction onto
whichever main effect was varied last.

**Fix:** replace step 5 with a 2³ factorial over the three dials at low/high,
then upgrade the axis with the largest effect. Four extra runs.

**Falsifier:** an OFAT design that recovers a two-factor interaction. There
is none; this is a property of the design matrix, not of the response.

**Evidence:** `shadow_design.py` §1.

---

## TP_003 — consensus among shadows is blind to the error shadows share

**who:** A · **status:** SUPPORTED

The shadow pattern's test is *"Do the three agree? If not, the axis is
underdetermined."*

The four shadows are not independent. They read the same physical
declaration, the same instrument output, and — for the AI shadows — the same
prompt, written by one of the human shadows. Model each as
`truth + shared_bias + individual_noise`:

```
 shared bias    mean shadow         spread   error vs truth
         0.0         100.01           2.04             0.01
         2.0         102.00           2.04             2.00
         5.0         105.01           2.06             5.01
        20.0         120.00           2.02            20.00
```

Spread does not move. Error tracks the bias one-for-one. **Four shadows
agreeing tightly at 120 when the truth is 100 is exactly what this looks like
from inside**, and the consensus test reports it as a pass.

So "do the shadows agree?" has no null. Agreement means nothing until you
have the disagreement between two runs of the *same* observer at the *same*
dial, and the shared term is invisible to consensus at any sample size.

**Fix, and most of it is already built:**
[`divergence-playground/`](../divergence-playground/) is this protocol with
the null attached — readings hash-sealed before reveal so later readers
cannot anchor on earlier ones, spread computed on three declared axes rather
than eyeballed, and `null_ensemble.py` supplying shuffle and permutation
nulls. Its `agree_by_accident` flag is the cell the shadow protocol needs
most: shadows reaching the same verdict by different mechanisms.

**Falsifier:** show the shadows are independent — that no shadow's input
depends on another's output and none share a framing. For a human writing
the AI prompts, that is hard to arrange and worth arranging.

**Evidence:** `shadow_design.py` §2.

---

## TP_004 — the first experiment cannot fail its own skip condition

**who:** A · **status:** SUPPORTED

Proposed skip condition: *"If all four observers agree within instrument
resolution, observer variance is negligible."*

The expansion itself is easy to see — a 1 m aluminium bar over a 60 K swing
moves 1.386 mm against a 0.01 mm dial division, a factor of 139. But the
experiment is about observer variance, not expansion, and there the numbers
run the other way:

```
observer reading spread   ~0.005 mm   (half a division)
instrument resolution      0.010 mm
ratio                      0.50
```

Four people reading one mechanical dial agree to within a division because a
division is the quantum of what the dial can say. The skip condition fires
whether or not observer variance exists, so "negligible" is a statement about
the dial.

This is [`null-harness/`](../null-harness/)'s `CONSTANT_SILENT` — a gate that
cannot fire has not been shown to work — and `G-RES` in
[`reasoning-gate/`](../reasoning-gate/): a null from an instrument that could
not have seen the feature.

**Fix, cheap, no better bar required.** The instrument must record
independently of the observer reading it: a digital indicator with a data
log, or a timestamped photograph of the dial. The observer writes a value
without seeing the log, and observer error is `|observer − logged|`,
measured directly rather than inferred from consensus. Recorded in
`triad.json` as check `I4`.

**Falsifier:** a mechanical-dial protocol in which observer disagreement can
exceed instrument resolution — e.g. observers reading at different times
during a transient, where reaction lag is the quantity. That is a different
experiment and a better one.

**Evidence:** `shadow_design.py` §3.

---

## TP_005 — the worked example shows physical mis-specification, not observer variance

**who:** A · **status:** SUPPORTED

The aluminium example runs one physical dial setting past three reasoning
dials and gets "crack at 200 cycles" → "1,800 ± 400" → "no crack; this is
wrought, not cast". The drop reads the sign change as a reasoning-dial
cross-gradient and a G-LAYER violation.

Run 3 says something else. It reports that runs 1 and 2 were answering a
question about *cast* aluminium while the specimen is *wrought*. That is the
physical declaration being wrong and the high-dial observer catching it —
not the observer's gain varying against a fixed system.

The distinction is load-bearing. If a mis-specified physical system is scored
as reasoning-dial variance, then every physical error the reasoning agent
catches inflates the measured observer variance, and the playground concludes
the observer is unreliable when what happened is that the observer was right.

**Fix:** `triad.json` check `P4` records `state_revised_during_run`
separately from `state_declared`. A run that revises the physical declaration
reports a **physical** finding, not a reasoning gradient.

**Falsifier:** an example where the conclusion changes with the reasoning
dial while the physical declaration survives the run unrevised. That would be
a genuine reasoning-dial cross-gradient, and it is the example the protocol
needs.

**Evidence:** `shadow_design.py` §4.

---

## TP_006 — three of four reasoning checks are self-report only

**who:** A · **status:** SUPPORTED, and it is a limit rather than a defect

Of the four reasoning-agent checks, only the AI one (`R3`: model version,
thinking budget, temperature, context window) is readable from outside the
observer. Fatigue, emotional investment and conflict of interest are
declarations, and a declaration from a miscalibrated observer is the quantity
in question.

This is [`reasoning-dial/`](../reasoning-dial/) `RD_009` restated at system
scale — the same reason `G-STATE` was logged there rather than built.
`triad.json` marks each check's `readable` field so the pedigree carries the
distinction rather than hiding it, and `CHECKLIST.md` renders `[DECLARED]`
against the three that are not measurements.

**Falsifier, and it is the same one as `RD_009`:** tie a reasoning check to
something outside the observer's own report — cabin temperature, hours since
sleep, a timestamp, a keystroke-latency measure. Any of those makes it a
two-number check like `G-RES`, and it should then be enforced rather than
declared.

---

## TP_007 — no triad experiment has been run

**who:** A · **status:** UNVERIFIED

Everything in this folder is a study of a proposed protocol. The corrections
in `TP_002` through `TP_005` are design results — properties of the
experimental design and of the consensus rule, provable without data — but
the load-bearing empirical question is untouched:

**does observer variance matter at any scale worth measuring?**

`TP_004`'s fix makes it measurable. Nobody has measured it. The first real
result is still unrun, and it is one bar, one indicator with a data log, and
one afternoon.

**Falsifier:** run it.

---

# Spec v1

Claims arising from [`SPEC_V1.md`](SPEC_V1.md) / [`spec_v1.json`](spec_v1.json),
the generic protocol delivered for reuse. Both are checked in verbatim.
[`triad.json`](triad.json) is v1 plus the corrections below; where the two
differ, the difference is a finding.

---

## TP_008 — the pattern works without the human; it does not work without decorrelation

**who:** A · **status:** SUPPORTED (generator scope)

The question attached to the drop. Modelling each shadow as
`truth + b_shared + b_family + e_ind` and reading the panel two ways —
`N_eff` (participation ratio of the shadow correlation spectrum) and
false-pass rate (P(shadows agree | panel mean wrong by more than tolerance)):

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

**Answer: yes, without the human — provided the human's decorrelation is
replaced.** Four model families with no human reach `N_eff` 2.18 and
false-pass 12.4%, *stronger* than v1's required panel with a human (1.61,
38.2%). Adding the human back on top changes `N_eff` by −0.02, inside the
noise.

Drop the human from v1's panel without substituting and it collapses:
`N_eff` 1.61 → 1.14, false-pass 38% → **84%**. A panel that returns a
confident wrong answer 84 times in a hundred is not a check.

The reason is `TP_003`: `ai_low` and `ai_high` on one model share a family
bias, so v1's required panel has one decorrelated element and it is the
human. The design variable is independent failure modes, not human-vs-AI.

**What a human still uniquely supplies** is embodied context — cold-stiffened
proprioception is not a failure mode any model has. That argues for a human
shadow on *physical* measurements specifically, and it is a different
argument from the decorrelation one.

**Falsifier:** measure the correlation between two model families on a real
shadow task. If cross-family correlation is as high as within-family, model
diversity buys nothing and the human is not substitutable.

**Evidence:** `shadow_panel.py` §1–2; ranking survives a 5-point sweep of the
variance components in §3.

---

## TP_009 — the spec should require a minimum N_eff, not a minimum shadow count

**who:** A · **status:** SUPPORTED

v1 requires `human_baseline`, `ai_low`, `ai_high`, and a minimum of two
controls. Counting shadows measures effort; it does not measure independence.
A four-shadow panel can carry `N_eff` = 1.22.

The spec already requires a minimum *number* of controls for exactly this
kind of reason. `N_eff` is the same kind of number for the shadow panel, and
[`model-ecology/phylogeny.py`](../model-ecology/phylogeny.py) already computes
it for a family of estimators — fifteen of which turned out to carry
`N_eff` = 2.48.

Recorded in `triad.json` under `shadow_protocol.panel_independence`.

**Falsifier:** a panel-quality statistic that predicts false-pass rate better
than `N_eff` does. This is a modelling choice, not a theorem.

---

## TP_010 — v1 improved the consensus denominator and it is still the wrong one

**who:** A · **status:** SUPPORTED

v1 adds `"threshold_rule": "Variance must be compared against instrument
resolution, not against zero."` That is a real improvement over the first
drop and it addresses half of `TP_004`.

It is still the wrong denominator. Instrument resolution bounds what the
**instrument** can say. Shadow spread is bounded by what an **observer** can
repeat. The correct reference is the same-observer repeat variance — one
observer measuring twice at one dial — which is also the null `TP_003` says
is missing.

If observer repeat variance exceeds instrument resolution, every panel reads
`exceeds_resolution` and the verdict is a statement about observer
repeatability, not about underdetermination.

**Falsifier:** a measurement regime where observer repeat variance is
reliably below instrument resolution. Then the two denominators coincide and
v1's rule is sufficient — and `TP_004`'s independent-log fix is what would
establish it.

---

## TP_011 — v1 states the mixed partials explicitly and still forbids the design

**who:** A · **status:** SUPPORTED. Sharpens `TP_002`.

v1 §5 now names the interactions directly: `∂²/∂(physical)∂(reasoning)` and
`∂²/∂(instrument)∂(reasoning)`. v1 §2 execution rule 3 still says *"upgrade
ONE dial at a time, re-shadow"*.

Rule 3 is the binding one. Rule 4 — *"never upgrade all three
simultaneously"* — would permit a 2² factorial over any pair, which is
exactly what a two-factor interaction needs. So the contradiction is now
sharper than in the first drop and the fix is smaller:

> replace rule 3 with *"vary dials in a 2² factorial over the pair whose
> interaction is being tested"*, and keep rule 4 unchanged.

Four runs per pair, three pairs, and every mixed partial in §5 becomes
estimable while rule 4's prohibition survives intact.

**Falsifier:** as `TP_002` — an OFAT design that recovers a two-factor
interaction. There is none.

---

## TP_012 — v1 assigns G-DIM a job it does not do, and the job is real

**who:** A · **status:** SUPPORTED

v1 §6 maps `G-DIM` to *"checks that dial settings are actually different
compute levels"*. `G-DIM` in
[`reasoning-gate/guards.json`](../reasoning-gate/guards.json) voids ratios
whose operands are properties of different objects. It does not check dial
distinctness and cannot be made to without becoming a different guard.

The job named is genuine and currently unassigned: **nothing verifies that
`ai_low` and `ai_high` actually produced different reasoning effort.** A model
that ignores its budget parameter, or a task below the budget's effect
threshold, silently collapses two declared shadows into one — which is
`TP_008`'s failure mode arriving without anyone declaring it.

The check is cheap and reads like a `G-RES` pair: declared budget separation
versus observed reasoning-token separation, with a margin.

**Falsifier:** show `G-DIM` as implemented rejects a run whose two dial
settings produced identical output. It does not — it never inspects dial
settings at all.

---

## TP_013 — none of this has been measured on a real panel

**who:** A · **status:** UNVERIFIED. Extends `TP_007`.

`shadow_panel.py`'s three variance components are chosen, not fitted. What
survives the sweep is the **ranking** of panel compositions, which follows
from which shadows share which bias term; the absolute rates do not and
should be read as illustrative.

Fitting them needs one measurement: several observers, including at least two
model families, reading one instrument against an independently logged
reference. That is the same experiment `TP_004` and `TP_007` already name.

**Falsifier:** run it.
