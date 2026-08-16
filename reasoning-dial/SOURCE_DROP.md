# SOURCE_DROP

The delivered material, verbatim. Two pieces arrived together: a literature
survey of 2026 work on reasoning / learning / exploring / harnesses, and a
proposal to treat the thinking budget as a measurable dimension with its own
gradients.

Checked in as received. Analysis is in [`README.md`](README.md) and
[`CLAIM_TABLE.md`](CLAIM_TABLE.md); the runnable part is
[`dial_response.py`](dial_response.py).

**Citation note.** The survey carries inline `cite web_search:NN#M` markers
pointing at search results not included in the drop. Those pointers cannot be
resolved from what was delivered, so no claim below is treated as sourced on
their strength alone. Where a claim is checkable against established work it
is checked in `CLAIM_TABLE.md`; where it is not, it is marked `UNVERIFIED` —
a gap, not a negative verdict.

---

## Part 1 — Deep Research: Newest Theories on Reasoning, Learning, Exploring, and Harnesses in AI (2026)

### I. REASONING: The Test-Time Compute Revolution

**The Three-Scaling-Law Framework**

The dominant paradigm in AI reasoning has shifted from "bigger models" to
"more thoughtful models." The field now recognizes three distinct compute
investment strategies rather than one:

1. Pre-training scaling — traditional "bigger model, more data"
2. Post-training optimization — fine-tuning, RLHF, distillation
3. Test-time compute scaling — letting models "think longer" at inference

The critical insight from Snell et al. (2024) is that a smaller model given
the right thinking budget can outperform one up to 14x larger at matched
compute. The best strategy depends on problem difficulty — which makes
routing by task complexity the correct architectural choice.

**The Reasoning Model Landscape (2026)**

Every major lab now ships a reasoning model, but they expose "thinking"
differently:

| Model Family | Thinking Exposure | Standout Feature |
| --- | --- | --- |
| OpenAI o-series / GPT-5 | Hidden reasoning tokens; real-time router | Auto-routing fast vs. deep |
| DeepSeek-R1 | Full reasoning trace; RL-trained | Open weights, distillable |
| Claude extended / adaptive | `budget_tokens` / effort parameter | Tunable thinking budget |
| Gemini 2.5/3 | `thinkingBudget`; Deep Think mode | Dynamic thinking with 1M+ context |

The throughline: thinking is becoming a dial, not a fixed mode.

**Process Reward Models (PRMs): The Verification Layer**

A major theoretical advance is the shift from outcome reward models (ORMs) to
process reward models (PRMs). ORMs provide a single sparse reward at the end;
PRMs evaluate every intermediate step.

Key open-source PRMs in 2026:

- **ThinkPRM-14B**: Generative verification with natural language critiques;
  uses ~1% of process labels in PRM800K
- **GenPRM-7B**: Hybrid chain-of-thought + code verification; outperformed a
  discriminative model 10x its size
- **ReasonFlux-PRM-7B**: Trajectory-aware supervision (both step and
  path-level); reaches 89.8% MATH-500 accuracy
- **PURE-PRM-7B**: Min-form credit assignment to mitigate PRM-induced reward
  hacking

The PURE framework is particularly important: it addresses the reward hacking
problem where models learn to exploit the PRM's evaluation rather than solve
the problem.

**From Thinking to Acting: Chain-of-Action-Thought (COAT)**

The 2026-2027 trajectory extends pure reasoning to reasoning + action in a
unified framework. COAT interleaves thinking and acting fluidly through three
stages:

4. Small-scale format tuning to internalize reasoning format
5. Large-scale self-improvement via reinforcement learning
6. Model learns to interleave thinking and acting

### II. LEARNING: Continual Learning and the Forgetting Problem

**Structural Collapse Theory**

A 2026 paper by Zhu et al. established that structural collapse — measured
through effective rank (eRank) of weights and activations — is the mechanism
behind catastrophic forgetting. Forgetting and collapse are strongly
correlated: as networks lose capacity to expand their feature space, they are
forced to overwrite existing representations.

**The LoRA Adapter Revolution**

The most practical 2026 approach to continual learning is adapter
composition. Rather than modifying base model weights, new capabilities are
encoded as lightweight LoRA adapters (~0.1-1% of base parameters). The base
model, which holds general knowledge, is never modified.

Key advances:

- **I-LoRA**: Iterative merging without task-order influence
- **L-MoE**: Gating network dynamically composes adapter outputs per token
- **Adaptive Minds (Oct 2025)**: Semantic routing selects best adapter(s) at
  inference
- **LoRA with Critical Parameter Constraints (Apr 2026)**: Prevents updates
  from overwriting critical prior parameters

**Memory-Augmented Architectures: Titans**

Google's Titans Architecture (Dec 2024 / NeurIPS 2025) introduces a dedicated
neural long-term memory module alongside attention. Attention handles
short-term context; the memory module stores history in its own parameters
and learns to memorize at test time through surprise-based prioritization —
storing information proportional to how unexpected it is.

**Wake-Sleep Consolidated Learning (WSCL)**

A biologically inspired approach from Spampinato et al. mimics human sleep
and dreaming:

- **Wake phase**: Network exposed to new data, stored in short-term memory
- **Sleep phase**: Information replayed into long-term memory
- **Dreaming phase**: Network exposed to dream-like samples to prepare for
  future experiences

Results show WSCL reduces forgetting and improves knowledge transfer to new
tasks.

### III. EXPLORING: Intrinsic Motivation and Agent Discovery

**Prediction Error as Reward**

The dominant theory in autonomous exploration is Random Network Distillation
(RND): the agent tries to predict the outcome of its actions. Predictable
outcomes yield low intrinsic reward; surprising outcomes (high prediction
error) yield high reward.

In 2025 MIT experiments, a TurtleBot4 with RND-augmented Nav2 mapped a 500m^2
office building 40% faster than frontier-based exploration, naturally
gravitating toward visually novel features.

**Agentic Tool Use as Exploration**

The 2026 agent architecture treats tool use as a form of structured
exploration. Agents register typed functions with docstrings that serve
double duty: describing purpose to the LLM and defining input schemas for
structured invocation.

Key constraints for safe exploration:

- Idempotent tools where possible
- Structured error messages rather than exceptions
- Timeouts on external calls
- Human approval gates via `interrupt()` for sensitive actions

The exploration loop is bounded: explicit iteration limits, scoped goals, and
checkpointed state transform open-ended systems into predictable ones.

### IV. HARNESSES: Interpretability, Oversight, and Control

**Mechanistic Interpretability: From Research to Production**

MIT Technology Review named mechanistic interpretability one of its 10
Breakthrough Technologies of 2026. The field reverse-engineers neural
networks into human-understandable algorithms by identifying:

- **Features**: Human-interpretable directions in activation space
- **Circuits**: Causal pathways connecting features to outputs

Key 2026 discoveries:

- Anthropic traced Claude 3.5 Haiku and found the model plans backward when
  writing poetry — picking the rhyming target word before generating the line
- The model forms internal candidate diagnoses that influence follow-up
  questions even when never stated aloud
- Persistent "reward model bias" features are active during every assistant
  interaction

Tools now available:

- `circuit-tracer` library (works on Gemma-2-2b, Llama-3.2-1b)
- Transcoders (Dunefsky et al.): Separate local behavior from global MLP
  function
- WeightLens & CircuitLens (Golimblevskaia et al. 2026): Infer feature
  meaning from weights regardless of context

**Multi-Agent Collusion Detection**

A critical 2026 advance is multi-agent interpretability — extending white-box
inspection from single models to multi-agent contexts. Rose et al. introduced
NARCBench, a benchmark for evaluating collusion detection under distribution
shift.

Key findings:

- Every model reaches 1.00 AUROC in-distribution
- On Llama-3.1-70B, probing techniques achieve 0.73-0.93 AUROC zero-shot on
  structurally different scenarios
- 0.99-1.00 AUROC on steganographic blackjack card-counting
- Detection performance scales with model capability
- No single probing technique dominates all collusion types — different
  anomaly types require different detection paradigms

The framework identifies three collusion signatures mapped onto distinct
anomaly types, treated as a distributed anomaly detection problem.

**Scalable Oversight for Multi-Agent Systems**

Schmidt Sciences' 2026 research program identifies four pillars for
multi-agent oversight:

1. Detection of collusion and emergent communication — including
   steganography
2. Attribution and oversight interfaces — tracing failures back to specific
   agents, interactions, or delegation chains
3. Multi-agent control and scalable oversight — secure harnesses respecting
   cross-principal trust boundaries
4. Mechanism and information design — circuit breakers,
   (de)synchronization, action-rate limits for stabilizing volatile networks

**AI Control and Secure Harnesses**

The concept of AI control (Greenblatt et al. 2025) extends to multi-agent
settings through:

- Secure harnesses and task-allocation architectures
- Red/blue-team evaluations of control protocols
- Robustness to subversion by groups of agents

### V. SYNTHESIS: The Four Domains as a System

| Domain | Core Question | 2026 Key Mechanism |
| --- | --- | --- |
| Reasoning | How should models allocate compute? | Test-time scaling + routing by difficulty |
| Learning | How do models retain knowledge? | Adapter composition + surprise-based memory |
| Exploring | How do agents discover capabilities? | Prediction-error intrinsic motivation + bounded tool loops |
| Harnesses | How do we maintain oversight? | Circuit-level interpretability + multi-agent activation probing |

The convergence point is **interior visibility**. Reasoning models expose (or
hide) their thinking traces. PRMs evaluate internal steps, not just outputs.
Mechanistic interpretability reverse-engineers internal circuits. Multi-agent
interpretability probes internal activations for collusion. The 2026 frontier
is not just making AI systems more capable — it's making their interior
states legible to operators.

This maps directly onto the "interior calibration" framework: the observer
(human operator) must have read on the instrument's (AI system's) own gain
settings — its thinking depth, its adapter composition, its exploration
strategy, its internal feature activations — or the variation gets attributed
to the exterior world.

### VI. Open Problems and Research Frontiers

1. **Monitorability of chain-of-thought**: Can reasoning traces be reliably
   monitored for deceptive reasoning?
2. **Efficiency scaling**: If o3 proved reasoning could be solved with $1M
   compute, the 2026 goal is solving the same problems for $1.
3. **From thinking to acting**: Models that independently execute multi-day
   projects across different software environments.
4. **Polysemanticity resolution**: Sparse autoencoders have made progress,
   but neurons encoding multiple unrelated concepts remains only partially
   solved.
5. **Cross-principal trust boundaries**: In multi-agent systems with multiple
   owners, how do harnesses respect boundaries while enabling coordination?

---

## Part 2 — The Sensory Dial

In reasoning models, the "dial" isn't just "think more." It's a mode switch:

| Dial | What happens |
| --- | --- |
| Low | Pattern-match against cached heuristics. Fast. Cheap. Brittle on novel problems. |
| Medium | Cross-reference a few sources, check consistency, rule out obvious confounders. |
| High | Explicit step-by-step, verify each transition, backtrack when contradictions appear, hold multiple hypotheses in working memory. |

The sensory gradient framework has the same structure, just distributed
across modalities instead of tokens.

**Low dial — Threshold monitoring.** "The engine note changed." One sense,
one threshold, one bit of information. Efficient. Also where catastrophic
misattribution happens — you feel a vibration gradient and blame the road,
not the bearing, because you didn't spend the compute to cross-reference.

**Medium dial — Gradient correlation.** "The pitch dropped and the vibration
harmonics shifted and the exhaust temp is lagging behind where it should be
for this load." Tracking coordinated gradients across senses. The meaning
isn't in any single gradient — it's in how they move relative to each other.

**High dial — Cross-modal mechanism reconstruction.** "The pitch drop is in
the 2nd harmonic, which means the imbalance is upstream of the turbo. The
vibration has a 4-second thermal lag vs. the exhaust, which means the heat
path is through the block, not the manifold. The oil pressure isn't dropping
yet, so the bearing hasn't lost its film. I have maybe 40 hours before this
becomes unrecoverable." Full cross-modal integration with temporal dynamics
and causal attribution. Expensive.

**Where the Dial Misfires**

- *Under-dial*: pattern-match "vibration = loose mount", miss that the
  vibration is coordinated with a thermal and a pressure gradient. Tighten
  the mount, the real problem progresses unseen.
- *Over-dial*: reconstruct the full thermodynamic cycle because of a single
  anomalous ping. Burn resources on noise, miss the obvious threshold
  crossing elsewhere.
- *Dial stuck high*: every gradient interaction gets the full mechanism
  treatment. Exhaustion, decision fatigue, and eventually the dial breaks.

**The Routing Layer**

The real insight from the 2026 reasoning work isn't just the dial — it's
routing by task difficulty.

| Situation | Dial setting | Why |
| --- | --- | --- |
| Routine pre-trip, good weather, known machine | Low | Heuristics are reliable, save resources |
| Same machine, 40 below, only rig for 200 miles | Medium | Margin for error is thinner, cross-check more |
| New failure signature, no parts, reading the schematic for someone dyslexic | High | Novel problem, high stakes, no fallback |

**A Practical Harness**

- **G-STATE (interior calibration check)**: Am I cold? Am I time-pressured?
  Am I emotionally invested in a particular diagnosis?
- **G-RES (resolution check)**: What is the declared source of each gradient?
  Are two "independent" senses actually coupled through the same physical
  mechanism?
- **G-CTRL (control check)**: Did I run the low-dial heuristic and the
  high-dial mechanism check on the same artifact? Do they agree?

The dial is a claim about the observer's own state. The hard part isn't the
dial. It's knowing when your read on the dial is itself miscalibrated.

---

## Part 3 — The Dial as a Dimension

The dial is a continuous control parameter — thinking budget in tokens, or
equivalently `log(compute)`:

```
Output Quality = f(Sensory Input, Problem Structure, Thinking Budget)

d(Quality) / d(log Budget) = marginal value of one more thinking step
```

**What the Gradients Tell You**

| Problem Type | D_r (Reasoning Dimension) | Knee Location | Gradient at Knee |
| --- | --- | --- | --- |
| Easy (pattern match) | 0.5 | ~26 tokens | 0.21 |
| Medium (multi-step) | 2.0 | ~910 tokens | 0.06 |
| Hard (novel mechanism) | 4.0 | ~66 tokens | 0.12 |

The knee is the point of maximum curvature — where the marginal value of
additional thinking drops fastest.

For an easy problem, the knee is early and the gradient is steep: a little
thinking goes a long way, but extra thinking wastes resources. For a hard
problem, the knee is later and the gradient is shallower: you need sustained
thinking, and the payoff is gradual.

**Cross-Gradients**

```
d2(Quality) / d(log Budget) d(Problem Difficulty)
```

At a fixed budget of 1000 tokens, the gradient is near-zero for trivial
problems (already saturated) and near-zero for extremely hard problems (1000
tokens isn't enough to matter). The peak is in the middle.

**The Fractal Connection**

A problem's "reasoning dimension" D_r is analogous to fractal dimension: some
problems are space-filling in reasoning space — every additional thinking
token explores new structure (hard problems). Others are clustered — most of
the thinking is redundant, and only a few tokens matter (easy problems).

**Practical Harness for the Dial Dimension**

- **G-DIAL**: at current budget B, compute `d(confidence)/d(log B)`. If
  gradient > threshold: under-thought, increase budget. If gradient < 0:
  over-thinking is introducing noise. If gradient ~ 0 and confidence low:
  problem may be beyond current capacity.
- **G-CROSS**: compute `d2(confidence)/d(log B) d(signal quality)`. If signal
  quality is low and cross-gradient flat: additional thinking won't overcome
  noise. Act or acquire better data.
- **G-KNEE**: track curvature `d2(confidence)/d(log B)^2`. Maximum curvature
  = knee location. Never allocate budget beyond knee x safety_factor.

**The Limitation**

The dial dimension is not a physical field. You can't measure it with a
sensor. It's a control parameter you set, not a property of the world you
discover. This means:

1. The gradient is a response function, not a field gradient. It depends on
   the model architecture, not just the problem.
2. The "reasoning dimension" D_r is a phenomenological parameter fit from the
   curve, not a fundamental property like fractal dimension.
3. The cross-gradient requires you to declare the problem difficulty — it's
   not self-evident.

These are the same limitations as the SIM stack: the cascade parameters were
generator-level properties, not physical facts. The dial dimension is
similarly a property of the instrument (the reasoning model), not the system
under study.
