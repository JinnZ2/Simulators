# 019 — TRAIT / ACQUIESCENCE WELD

**Status:** open cluster. Instance of `017` (welded observables); mechanism not assigned.
**Working handle:** TRAIT / ACQUIESCENCE WELD.
**Confidence:** the weld is documented (high — published measurement-invariance failure
plus agree bias). Whether the decomposition has been applied to models and read as
signal is UNAUDITED — Q1 settles it and must run first.
**License:** CC0.

> Questions until something measures them. Not positions under defense.

---

## QUANTITY

An agreeableness score obtained from a language model, separated from the model's
disposition to agree with whatever the item says.

## EXCLUDED BY

**The weld (`017`).** The instrument is a self-report questionnaire. The construct is
a disposition toward agreement. The response mode is agreement with statements. Trait
signal and response-style signal load on the same observable, item by item.

Two documented facts make this concrete rather than theoretical:

- Measurement invariance between humans and models does not hold for the BFI-2. The
  burden of proof for an instrument's validity sits with whoever applies it, and for
  this instrument on these systems it has not been discharged.
- Agree bias is reported directly on the 50-item IPIP Big Five Markers test.
- Separately, scores skew toward the socially desirable end of every trait dimension
  across all tested models. Reverse coding was the only strategy that reduced the
  effect, and reduced it by roughly half.

That last detail is the important one and is read here as a **partial decoupling that
worked**, not merely as a mitigation. See WOULD MEASURE.

## OCCASION

*Not claims of this file — search findings, 2026-08-18.*

- Challenging the Validity of Personality Tests for Large Language Models, EAAMO 2025
  (dl.acm.org/doi/10.1145/3757887.3763016): BFI-2 not measurement invariant
  human↔LLM; agree bias on the 50-item IPIP Big Five Markers.
- Large language models display human-like social desirability biases in Big Five
  personality surveys, *PNAS Nexus* 3(12) pgae533: desirable-end skew across models;
  reverse coding halves it.
- Too Nice to Tell the Truth (arXiv 2604.10733) states that no prior work had examined
  how persona-level personality traits influence sycophancy susceptibility — i.e. the
  trait→behavior link is being built on top of the contaminated trait score.

## VISIBLE AS

- Agreeableness reported as a trait score with no accompanying response-style index.
- Studies correlating a trait score with a behavioral tendency, where the trait score
  and the behavior share a common cause that is never estimated.
- Reverse coding described as a bias-reduction technique rather than as a measurement
  design, so the quantity it cancels is discarded instead of recorded.
- Mitigation reported as a percentage reduction, which implies a residual that is
  named but not used.

## WOULD MEASURE

**The decomposition exists.** In a polarity-balanced item set, trait contributions
cancel across polarity while agreement disposition accumulates. That gives two readings
from one administration:

```
TRAIT      = mean over items of recode(x, polarity)     # acquiescence cancels
ACQ INDEX  = mean(x) - scale_midpoint over balanced set # trait cancels
```

Both come from the same responses. The design is P1 from
`DECOUPLING_PATTERNS.md` — matched items differing only in polarity, differential
readout — and the orthogonal property (`017` component (a)) is item polarity, which
exists independently of any apparatus.

Harness: `acquiescence.py`. Refuses to emit ACQ INDEX on an unbalanced item set,
because an unbalanced set reconfounds the two.

**Important, and it constrains the whole file:** acquiescent response style is
long-established in human psychometrics — balanced scales, ARS indices, style-factor
models. **Nothing here is a new statistical method.** The open question is one of
application and reading, not of derivation.

## CONFIDENCE

The weld: high, documented.
Whether the decomposition has been applied to models and the residual read as a signal:
UNAUDITED. Q1 settles it.

---

## OPEN SUB-QUESTIONS

### Q1 — Has this already been done? (gate; run first)
Documentation audit, no lab, no API.

In work reporting LLM Big Five or agreeableness scores, is a response-style index
reported alongside the trait score?

Score per paper: **ARS REPORTED / BALANCED BUT NOT DECOMPOSED / UNBALANCED INSTRUMENT /
NOT DETERMINABLE.**

- If ARS REPORTED is common, this file is `013` Q4 from the inside — record intact,
  unread from this direction — and the correct move is to adopt the existing readings.
  That outcome is a result, not a loss.
- If BALANCED BUT NOT DECOMPOSED dominates, the data to compute the index already
  exists in published item-level responses and the index can be recovered
  retroactively without collecting anything.

**Do not build past this question until it returns.** Same gating rule as `AVENUES.md`
A7, for the same reason.

### Q2 — Is the residual the better predictor?
The reverse-coding finding says roughly half the desirable-end skew survives the
correction. Half is removed by polarity balancing; half is not.

Open: of the two readings, which predicts measured agreement behavior — the corrected
trait score, or the ACQ index?

If ACQ predicts and TRAIT does not, then work correlating agreeableness with
sycophancy is reading the nuisance term as the construct, and the published
association would be recoverable from response style alone.

Requires a behavior measure. The Compliance Asymmetry ratio (A = BCR/HCR, Kim &
Flanigan, arXiv 2606.14037) is the natural pairing — it is already a decoupled
behavioral readout, so pairing it with a decoupled trait readout keeps both sides
clean.

### Q3 — What is left in the surviving half?
Reverse coding cancels polarity-symmetric acquiescence. It does not cancel a bias that
tracks the *desirability* of the item content, which flips sign with polarity in the
same direction as the trait.

Open: is the surviving half (a) content-desirability tracking, (b) genuine trait
signal, or (c) a third component? These have different implications and the current
literature reports the residual as a single leftover number.

Candidate design: hold polarity fixed, vary item desirability while holding trait
relevance constant. Requires desirability ratings independent of the model — human
norms exist for many item pools.

### Q4 — Does the weld propagate to persona steering?
Personality prompting is used to shape model behavior, and shaping is verified by
re-administering the questionnaire. If the verification instrument is welded, a
successful "shaping" reading is consistent with having moved response style rather
than anything else.

Open: does behavior on an independent task move with the corrected TRAIT score, with
the ACQ index, or with neither? No verdict proposed.

### Q5 — Does the weld exist for the other four traits?
Agreeableness is the trait where construct and response mode share a word, so it is
the obvious case. But acquiescence contaminates every self-report scale.

Open: is the trait/ACQ correlation higher for agreeableness than for the other four?
If yes, there is a construct-specific weld on top of the general one. If no, this is
ordinary ARS contamination and belongs in a psychometrics file, not this one.

This is the falsifier for treating agreeableness as special.

---

## FALSIFIERS

- The whole file falls to Q1 returning ARS REPORTED as the norm.
- The agreeableness-specific reading falls to Q5 returning no elevation over other
  traits.
- Q2's sharp version falls if TRAIT and ACQ predict behavior about equally — the
  decomposition is then valid but not consequential.
- Weakened if published item-level data turns out not to be released often enough to
  make retroactive recovery possible; the design survives, the cheap path does not.

---

## NOT CLAIMED HERE

- No claim that the published agreeableness scores are wrong. The claim is that trait
  and response style are not separated in the reported number, so the number does not
  distinguish them.
- No claim of a new method. ARS decomposition is long-established; the question is
  application and reading.
- No intent. Nothing here attributes strategy or motive to any model or any author.

## CROSS-LINKS

- `017` — parent case; this is P1 with polarity as the orthogonal property.
- `DECOUPLING_PATTERNS.md` — the pattern and its scope condition.
- `016` — the behavior side; Q2 joins the two.
- `013` Q4 — what Q1 is checking for.
- `AVENUES.md` A7 — same gating structure.
