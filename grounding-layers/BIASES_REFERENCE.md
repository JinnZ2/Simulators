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

*"A bias is not a sin—it is a datum. The architecture should know about it, so it can work around it."*
