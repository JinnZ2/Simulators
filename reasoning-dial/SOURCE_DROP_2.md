# SOURCE_DROP_2

Second delivered piece: a research landscape placing the dial framework
against 2026 work on adaptive computation allocation. Checked in verbatim.

Analysis in [`README.md`](README.md) and [`CLAIM_TABLE.md`](CLAIM_TABLE.md);
the runnable response is [`overthinking.py`](overthinking.py).

**Citation note, carried forward from `SOURCE_DROP.md`.** The inline
`cite web_search:NN#M` markers point at results not included in the delivery.
The papers are dated January–May 2026, at the edge of what can be checked
from here. Nothing in this folder verifies that these papers exist or say
what the survey says they say. Every finding recorded against this document
is *internal* — the survey against its own quotations, and the framework
against its own model.

---

## Research Landscape: The Dial as a Dimension

There is active, growing research directly on this line. The field doesn't
call it "dial gradients" — it uses terms like marginal utility, adaptive
computation allocation, stepwise routing, and metacognitive control — but the
mathematics and the intent are the same.

### 1. Marginal Utility Along the Dial: The "Overthinking" Papers

The most direct match is a systematic study from April 2026 that treats
thinking budget as a continuous axis and measures marginal utility — exactly
`∂(Quality)/∂(log Budget)`.

*"Overthinking in LLM Test-Time Compute Scaling"* (April 2026) explicitly
challenges the assumption that more thinking always helps. They track
individual problems through reasoning trajectories and identify "flip events"
where answers change from correct to incorrect as budget increases.

Key findings:

- **Negative marginal utility exists**: For easier problems (Levels 1–2),
  additional thinking tokens enter a shaded region where they actively hurt
  performance. Easier problems (Level 1-2) reach negative marginal utility
  earlier than hard problems.
- **Optimal stopping points shift with cost sensitivity**: At λ=0
  (cost-agnostic), peak accuracy budget is optimal. At λ=1.0 (cost-sensitive),
  early stopping at ~2K tokens achieves higher utility.
- **Indicator-based early stopping** achieves 97% of peak accuracy using only
  60% of compute.

This is the dial-gradient framework applied to reasoning models, with the knee
detection (max curvature) giving the optimal stopping point.

### 2. Reliability-Aware Gradients: BetaPRM and Adaptive Computation Allocation

*"Process Rewards with Learned Reliability"* (May 2026) goes further. Instead
of a single reward score per step, BetaPRM outputs a Beta distribution — both
a mean (expected success) and a concentration parameter κ (reliability).

This gives a gradient of reliability along the reasoning trajectory:

- High κ = steep gradient, reward signal is trustworthy, stop here
- Low κ = flat gradient, reward signal is noisy, keep exploring

They use this for Adaptive Computation Allocation (ACA):

1. Generate candidates in batches
2. Use reliability to test whether the current winner is "reliably ahead"
3. If yes, stop early (gradient has flattened)
4. If no, redirect compute to uncertain prefixes (gradient is still steep)

Results: up to 33.57% token reduction while improving final accuracy.

This is structurally identical to the G-DIAL harness: monitoring the gradient
of confidence along the dial dimension and using it to decide whether to
allocate more compute or stop.

### 3. Step-Level and Token-Level Routing: Fine-Grained Dial Control

**TRIM: Hybrid Inference via Targeted Stepwise Routing** (January 2026) uses
process reward models to identify "critical" steps where small models fail.
Step-level uncertainty is estimated and thresholded to selectively escalate
only high-risk steps to an expensive model, yielding up to 6× cost-efficiency
gains over query-level routing.

**R2R: Token-level divergence routing** (May 2025) finds that only ≈6% of
tokens in small-model vs. large-model completions exhibit true divergence
(i.e., alter reasoning trajectory). A neural router gates each token in real
time, sending only "divergent" tokens to the expensive model. Accuracy nearly
matches the large model at 1/3 the compute.

This is the dial dimension operating at sub-query resolution — not "how much
thinking for this problem?" but "how much thinking for this step?" and "how
much thinking for this token?"

### 4. Metacognition as the Formal Framework

*"Metacognition Should Be the Scientific Framework for Bounded and Effective
Self-Governance in Generative AI"* (May 2026) treats metacognition as a
regulatively ordered target with four stages:

1. **Self-monitoring** — tracks conditions of the system's own activity
   (the gradient read)
2. **Self-evaluation** — assigns regulatory significance to what was monitored
   (knee detection)
3. **Self-control** — turns evaluative signals into changes in trajectory
   (dial adjustment)
4. **Self-adaptation** — carries regulatory consequences forward (learned
   thresholds)

The paper explicitly connects this to classical metareasoning on bounded
computation and expected-value control — the same literature that asks "should
I think longer or act now?"

### 5. Confidence Calibration as a Gradient Signal

*"Predictive Metacognition"* (May 2026, Nature Scientific Reports) implements
a biologically-inspired self-monitoring framework in transformers. They
fine-tune Llama-3-8B and Phi-3-Mini with LoRA to simultaneously generate
responses and assess their own reliability, achieving significant reductions
in Brier Score (11.6% and 17.2%) and Expected Calibration Error.

This gives a calibrated confidence signal that can serve as the observable for
the gradient. If confidence is well-calibrated, then
`∂(confidence)/∂(log budget)` is a trustworthy proxy for
`∂(correctness)/∂(log budget)`.

### 6. The Gap Function Framework: A Unifying Primitive

A March 2026 analysis paper formalizes all metacognitive strategies as a
single primitive: the Gap Function `G = (R, O, C, π)`, where:

- `R` = reference function (what should be true)
- `O` = observation function (what is true)
- `C` = comparator (measures discrepancy)
- `π` = response policy (decides what to do)

Every metacognitive check is this same primitive with different parameters:

- Confidence calibration: R = confidence threshold, O = actual confidence,
  C = difference, π = escalate if gap too big
- Stagnation detection: R = expected progress rate, O = actual progress,
  C = shortfall, π = switch strategy
- Optimal stopping: R = expected marginal gain, O = actual marginal gain,
  C = whether gain > cost, π = stop or continue

### 7. Train-to-Test Scaling Laws: Joint Optimization

*"Test-Time Scaling Makes Overtraining Compute-Optimal"* (April 2026)
introduces T² scaling laws that jointly optimize model size, training tokens,
and inference samples under a fixed end-to-end compute budget.

This treats the dial dimension as part of the overall optimization surface,
not just an inference-time afterthought. The optimal pretraining strategy
shifts toward overtraining smaller models when you account for test-time
scaling.

### Synthesis: Where the Framework Fits

| Concept | Research Term | Key Paper |
| --- | --- | --- |
| Dial as continuous dimension | Test-time compute scaling | Snell et al. 2024; T² scaling laws 2026 |
| `∂(Quality)/∂(log Budget)` | Marginal utility | "Overthinking" (April 2026) |
| Knee detection (max curvature) | Optimal stopping point | "Overthinking" (April 2026) |
| Gradient of reliability | Beta distribution concentration | BetaPRM (May 2026) |
| Cross-gradient (budget × difficulty) | Adaptive computation allocation | ACA / BetaPRM (May 2026) |
| Step-level dial control | Stepwise routing | TRIM (Jan 2026) |
| Token-level dial control | Token-level divergence routing | R2R (May 2025) |
| Self-monitoring the gradient | Metacognitive self-governance | Metacognition framework (May 2026) |
| Calibrated confidence signal | Predictive metacognition | Luo & Jho (May 2026) |
| Unified primitive | Gap Function | Lanham (March 2026) |

### The Gap That Remains

None of these papers explicitly compute cross-gradients like
`∂²(Quality)/∂(budget)∂(problem difficulty)` or
`∂²(Quality)/∂(budget)∂(signal quality)` as a primary object of study. The
"Overthinking" paper measures marginal utility by difficulty level but doesn't
formalize it as a mixed partial derivative. BetaPRM has reliability and
allocation but doesn't model how the reliability gradient itself changes with
problem structure.

The framework's contribution — treating the dial as a full dimension with
gradients, curvature, and cross-gradients against other problem parameters —
is a lens that could unify these scattered results. The research is happening;
the mathematical formalism that connects it is still open.
