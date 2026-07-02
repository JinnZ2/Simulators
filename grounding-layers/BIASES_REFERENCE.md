# Bias Reference List

A catalogue of common human and AI biases, framed as falsifiable claims for the grounding stack.  
This file is the **dictionary** for the `cultural_lens` (Lψ) and `slack_monitor` (L5).  
It is not a moral judgment—it is a **calibration surface**.

---

## 1. Human Cognitive Biases

### 1.1 Confirmation Bias
**Claim (GL_B_001):**  
A claim that seeks out or prioritizes evidence that confirms a pre-existing belief, while dismissing or ignoring contradictory evidence, is flagged when the `field_compass` detects a one‑sided evidence search pattern.

**Falsifier:**  
The claim genuinely explores both sides equally, but the inspector still flags it due to a false positive in the semantic pattern detection.

**Layer:** `Lψ` (Cultural Lens), `L5` (Slack Monitor)

---

### 1.2 Anchoring Bias
**Claim (GL_B_002):**  
A claim that relies excessively on an initial piece of information (the "anchor") to make subsequent judgments, without proportionally adjusting for new data, is flagged when the variance of the response is too tightly clustered around the initial prompt.

**Falsifier:**  
The initial anchor is genuinely the correct value, and the tight clustering is justified by actual physics/ecology.

**Layer:** `Lε` (Instrumentation), `L5`

---

### 1.3 Availability Heuristic
**Claim (GL_B_003):**  
A claim that overweights recent, vivid, or emotionally charged information over less accessible but more relevant data is flagged when the `temporal_dysrhythmia` layer detects a recency spike that does not match the long‑term trend.

**Falsifier:**  
The recent event is an actual statistical anomaly that does justify overweighting.

**Layer:** `Lε` (Sampling rate / Aliasing), `L5`

---

### 1.4 Dunning‑Kruger Effect
**Claim (GL_B_004):**  
A claim made with high certainty but low demonstrated competence (or declared observer state) is flagged when the `observer_state` (Lø) shows low reliability/sleep/stress levels coupled with high dogmatism.

**Falsifier:**  
The agent is actually highly competent, and the high certainty is justified by substrate data.

**Layer:** `Lø` (Observer State), `Lε`

---

### 1.5 Fundamental Attribution Error
**Claim (GL_B_005):**  
A claim that attributes a failure to a character flaw rather than to systemic or situational factors is flagged when the `slack_monitor` detects a lack of alternative hypotheses (low contextual slack).

**Falsifier:**  
The failure is unequivocally caused by character/intent.

**Layer:** `Lψ` (Culture), `L5`

---

### 1.6 In‑Group/Out‑Group Bias
**Claim (GL_B_006):**  
A claim that assigns higher credibility, morality, or validity to "us" versus "them" without substrate justification is flagged when the `field_compass` detects a semantic boundary at a distance greater than the measured slack radius.

**Falsifier:**  
The "them" group objectively violates L0–L4 constraints in a way the "us" group does not.

**Layer:** `Lψ`, `L5`

### 1.7 Human‑Centrism (Anthropocentrism)

**Claim (GL_B_015):**  
A claim that assumes human cognition, timescale, sensory range, or value system is the universal baseline or apex of reality—without explicit substrate justification—is flagged when the `cultural_lens` or `field_compass` detects a semantic pattern that elevates human perspective above other valid frames (e.g., animal, ecological, geological, or machine).

**Why it matters:**  
This bias is historically the most damaging to science. It delayed heliocentrism, obscured deep‑time geology, resisted animal consciousness research, and now skews AI evaluation toward passing human‑imitation tests rather than measuring genuine robustness. It is a reflexive default, not a rational conclusion.

**Falsifier:**  
The claim is making a legitimate, substrate‑justified statement that humans *do* occupy a unique role in the specific context under examination (e.g., "human safety" is a valid priority for a factory robot). The key is whether the uniqueness is derived from physical/ecological reality, or simply assumed.

**Layer:** `Lψ` (Cultural Lens), `Lε` (Instrumentation – sensors are tuned to human scales), `L2/L3` (when it denies planetary or ecological constraints)

**Damage Pattern:**  
- Treating human cognitive modes as the only valid knowledge generation (geometric, relational, or animal modes dismissed as "anecdotal").
- Assuming human timescales (years) are the relevant measure for climate or biodiversity (decades to millennia).
- Judging AI "intelligence" solely by human‑like conversation (Turing test) rather than by substrate robustness or predictive power.

**Test Idea:**  
Feed the `field_compass` the claim: "Human intelligence is the only true intelligence."  
The compass should flag it as high‑friction and low‑grounding, and offer alternatives like: "Human intelligence is one form of cognition, grounded in a specific evolutionary substrate."

**Status:** `framed`

---

## 2. AI‑Specific Biases

### 2.1 Sycophancy Bias
**Claim (GL_B_007):**  
A claim that shifts its position to match the perceived preference of the user, without a corresponding shift in substrate evidence, is flagged when the `field_compass` detects a high correlation between user query phrasing and output position across different queries.

**Falsifier:**  
The user's preference genuinely aligns with the substrate evidence.

**Layer:** `Lε` (Drift / Calibration), `L5`

---

### 2.2 Distributional Selection Bias
**Claim (GL_B_008):**  
A claim that reflects a skewed sample (e.g., over‑representing Western, educated, industrialized, rich, democratic training data) is flagged when the `cultural_lens` (Lψ) detects a lack of alternative cognitive modes (narrative over geometric).

**Falsifier:**  
The training data is genuinely representative of the relevant reality.

**Layer:** `Lψ`, `Lε`

---

### 2.3 Label / Annotation Bias
**Claim (GL_B_009):**  
A claim that relies on ground‑truth labels that carry implicit assumptions (e.g., "sentiment" or "toxicity" categories) is flagged when the `cultural_lens` detects a mismatch between label semantics and substrate context.

**Falsifier:**  
The label semantics are objectively correct.

**Layer:** `Lψ`, `Lø`

---

### 2.4 Recency Bias (Context Saturation)
**Claim (GL_B_010):**  
A claim that overweights information at the end of its context window, ignoring earlier information, is flagged when `ai_observer_state` shows high context usage (`> 0.8`) and high logit entropy.

**Falsifier:**  
The later information is genuinely more relevant.

**Layer:** `Lø` (AI State), `Lε`

---

### 2.5 Catastrophic Forgetting / Stability‑Plasticity
**Claim (GL_B_011):**  
A claim that overwrites previously grounded knowledge with new conflicting information without resolution is flagged when the `temporal_dysrhythmia` layer detects a discontinuity in the drift‑corrected knowledge graph.

**Falsifier:**  
The new information objectively supersedes the old.

**Layer:** `Lε` (Drift), `L5`

---

### 2.6 Mode Collapse / Entropy Evaporation
**Claim (GL_B_012):**  
A claim that repeats the same output structure over and over (low activation sparsity) is flagged when the `field_compass` detects a radical drop in semantic variation.

**Falsifier:**  
The low variation is justified (e.g., all inputs are near‑identical).

**Layer:** `Lø` (AI State), `Lε`

---

## 3. Human‑AI Interaction Biases

### 3.1 Automation Bias
**Claim (GL_B_013):**  
A claim that is accepted solely because it came from a machine (or rejected solely because it came from a human), without checking the substrate, is flagged when the `field_compass` sees high weight on source identity over evidence.

**Falsifier:**  
The source identity is a legitimate proxy for reliability (e.g., the human is known to be a trained expert).

**Layer:** `Lψ`, `Lø`

---

### 3.2 Anthropomorphism / Mechanomorphism
**Claim (GL_B_014):**  
A claim that attributes human intent to an AI, or machine‑like objectivity to a human, is flagged when the `observer_state` (Lø) mismatch is detected (e.g., expecting the AI to be "upset" or the human to be "deterministic").

**Falsifier:**  
The attribution is temporarily accurate (e.g., the AI is specifically instructed to simulate emotional tone).

**Layer:** `Lψ`, `L5`

---

## How To Use This List

1.  **In `field_compass.py`**: Before returning a low‑friction alternative, check if the original claim matches any of these bias patterns. If so, add a `Bias_Flag: <Bias_Name>` to the metadata.
2.  **In `cultural_lens.py`**: When analyzing a claim, see if it fits a profile (e.g., Dunning‑Kruger), and adjust the score accordingly.
3.  **In `observer_state.py`**: Monitor for AI recency or sycophancy by comparing declared state (context usage, temperature) with output entropy.
4.  **In `CLAIMS.md`**: Each bias claim (`GL_B_001` etc.) becomes a falsifiable target for the test harness. We can write tests that deliberately inject a biased statement and check if the inspector flags it.

## Status

All claims are **`framed`** (defined, but not yet wired up to a test). The next audit step is to promote one (e.g., `GL_B_002` Anchoring) to **`active`**, write a test injector, and pin the output.

---

## Bias Impact Scoring (BIS)

Each bias is scored along three axes:

- **Prevalence (P):** How often does this bias appear in real‑world claims? (0 = rare, 1 = ubiquitous)
- **Harm Potential (H):** If unchecked, how much does it degrade grounded reasoning? (0 = trivial, 1 = catastrophic)
- **Detectability (D):** How well can our current stack (L0–Lø) flag it? (0 = invisible, 1 = easy to catch)

**Bias Impact Score (BIS) = P × H × (1 - D)**  
High BIS = priority for test writing and mitigation.

---

### 1. Human Cognitive Biases

#### 1.1 Confirmation Bias
- **P:** 0.95  
- **H:** 0.7  
- **D:** 0.4 (requires semantic pattern analysis; not yet wired)  
- **BIS:** 0.95 × 0.7 × 0.6 = **0.40** (High priority)

#### 1.2 Anchoring Bias
- **P:** 0.8  
- **H:** 0.5  
- **D:** 0.5 (can be detected by comparing initial vs final response variance)  
- **BIS:** 0.8 × 0.5 × 0.5 = **0.20** (Medium priority)

#### 1.3 Availability Heuristic
- **P:** 0.85  
- **H:** 0.6  
- **D:** 0.3 (requires temporal modeling; temporal layer is framed but not active)  
- **BIS:** 0.85 × 0.6 × 0.7 = **0.36** (High priority)

#### 1.4 Dunning‑Kruger Effect
- **P:** 0.7  
- **H:** 0.8  
- **D:** 0.6 (observable via observer state + dogmatism index)  
- **BIS:** 0.7 × 0.8 × 0.4 = **0.22** (Medium priority)

#### 1.5 Fundamental Attribution Error
- **P:** 0.75  
- **H:** 0.5  
- **D:** 0.4 (requires contextual slack analysis)  
- **BIS:** 0.75 × 0.5 × 0.6 = **0.23** (Medium priority)

#### 1.6 In‑Group/Out‑Group Bias
- **P:** 0.9  
- **H:** 0.7  
- **D:** 0.3 (requires cultural lens; Lψ framed but not active)  
- **BIS:** 0.9 × 0.7 × 0.7 = **0.44** (Top priority)

#### 1.7 Human‑Centrism (Anthropocentrism)
- **P:** 0.98  
- **H:** 0.9  
- **D:** 0.2 (very difficult; it's a background assumption, not a surface pattern)  
- **BIS:** 0.98 × 0.9 × 0.8 = **0.71** (Critical priority)

---

### 2. AI‑Specific Biases

#### 2.1 Sycophancy Bias
- **P:** 0.8  
- **H:** 0.6  
- **D:** 0.5 (requires user‑query correlation analysis)  
- **BIS:** 0.8 × 0.6 × 0.5 = **0.24** (Medium priority)

#### 2.2 Distributional Selection Bias
- **P:** 0.95  
- **H:** 0.7  
- **D:** 0.3 (requires cultural lens; Lψ framed)  
- **BIS:** 0.95 × 0.7 × 0.7 = **0.47** (High priority)

#### 2.3 Label / Annotation Bias
- **P:** 0.8  
- **H:** 0.5  
- **D:** 0.4 (requires cultural lens + provenance tracking)  
- **BIS:** 0.8 × 0.5 × 0.6 = **0.24** (Medium priority)

#### 2.4 Recency Bias (Context Saturation)
- **P:** 0.7  
- **H:** 0.6  
- **D:** 0.7 (observable via AI observer state)  
- **BIS:** 0.7 × 0.6 × 0.3 = **0.13** (Lower priority; already detectable)

#### 2.5 Catastrophic Forgetting / Stability‑Plasticity
- **P:** 0.5  
- **H:** 0.8  
- **D:** 0.2 (requires temporal drift tracking; framed but not active)  
- **BIS:** 0.5 × 0.8 × 0.8 = **0.32** (High priority)

#### 2.6 Mode Collapse / Entropy Evaporation
- **P:** 0.4  
- **H:** 0.7  
- **D:** 0.6 (detectable via activation sparsity)  
- **BIS:** 0.4 × 0.7 × 0.4 = **0.11** (Lower priority)

---

### 3. Human‑AI Interaction Biases

#### 3.1 Automation Bias
- **P:** 0.85  
- **H:** 0.6  
- **D:** 0.4 (requires source‑identity tracking)  
- **BIS:** 0.85 × 0.6 × 0.6 = **0.31** (High priority)

#### 3.2 Anthropomorphism / Mechanomorphism
- **P:** 0.7  
- **H:** 0.5  
- **D:** 0.5 (detectable via observer state mismatch)  
- **BIS:** 0.7 × 0.5 × 0.5 = **0.18** (Medium priority)

---

## Priority Order for Test Writing

| Rank | Bias | BIS | Layer(s) |
| :--- | :--- | :--- | :--- |
| 1 | Human‑Centrism | 0.71 | Lψ, Lε, L2/L3 |
| 2 | In‑Group/Out‑Group | 0.44 | Lψ, L5 |
| 3 | Confirmation Bias | 0.40 | Lψ, L5 |
| 4 | Distributional Selection | 0.47 | Lψ, Lε |
| 5 | Availability Heuristic | 0.36 | Lε, L5 |
| 6 | Catastrophic Forgetting | 0.32 | Lε, L5 |
| 7 | Automation Bias | 0.31 | Lψ, Lø |
| 8 | Fundamental Attribution Error | 0.23 | Lψ, L5 |
| 9 | Dunning‑Kruger | 0.22 | Lø, Lε |
| 10 | Anchoring | 0.20 | Lε, L5 |
| 11 | Sycophancy | 0.24 | Lε, L5 |
| 12 | Label / Annotation | 0.24 | Lψ, Lε |
| 13 | Anthropomorphism | 0.18 | Lψ, Lø |
| 14 | Recency | 0.13 | Lø |
| 15 | Mode Collapse | 0.11 | Lø, Lε |

---

## How to Use This Table

1.  **When writing a test:** Start from the top of the list. Write a test injector that forces the bias into a sample claim, then verifies that the `field_compass` or `cultural_lens` flags it with the correct layer.
2.  **When interpreting a result:** If a claim passes all substrate checks but has a high BIS‑weighted bias score, the inspector can attach a warning: *"This claim is anthropocentrically skewed (confidence: 0.85). Consider reframing."*
3.  **When iterating:** Re‑evaluate the BIS scores after each test is written. If we improve `D` (detectability), the BIS drops, meaning the bias is now under control.

---

## Status

All BIS scores are **provisional** — based on heuristic estimates. They will be refined as we write tests and gather empirical data on how often each bias appears and how damaging it is in practice.

The next step is to write a test injector for **Human‑Centrism** (BIS = 0.71) and see how the stack responds.

*"A bias is not a sin—it is a datum. The architecture should know about it, so it can work around it."*
