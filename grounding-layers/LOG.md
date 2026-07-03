work from bottom to top on this page

# Reasoning Log: L5 Rigor and Preservation Protocol

**Date:** 2026-07-02  
**Context:** L5 must audit human-construct proposals across pluralistic cultural frames. To prevent dilution by volume and epistemic erasure, we introduce a **rigor and preservation layer** within L5. It maintains a high bar for intact traditions while applying a precautionary, survivability-aware prior for knowledge systems that have been fragmented by historical violence.  
**Status:** Design complete. Ready for implementation of `RigorAuditor` class and audit claims.

---

## 1. Core Distinction: Lineage State

Every proposal (or knowledge claim) carries a **lineage state** field, which determines how the rigor auditor processes it.

| State | Definition | Example |
|-------|------------|---------|
| `intact` | Continuous transmission, verifiable chain, substrate markers present. | A living oral tradition with named elders and landscape proof. |
| `fragmented` | Transmission broken by external disruption (colonialism, forced assimilation); partial records survive; knowledge is attested but chain incomplete. | A songline remembered by one elder, with no remaining initiates, but consistent with archaeology. |
| `reconstructed` | Knowledge reassembled from archives, outsider accounts, or informants who were not fully initiated; no living chain. | A medicinal plant use described in a colonial diary, later confirmed by chemical analysis. |

---

## 2. Rigor Axes for Intact Traditions (Frozen Constants)

For `intact` proposals, the rigor auditor applies six axes, each contributing a log-probability term. The constants below are **frozen estimates**—refutable through ethnographic and historical evidence, following the same protocol as L0.

| Axis | Short code | Measurement method | High-rigor threshold (`T_hi`) | Logp penalty below threshold (per unit) | Max penalty |
|------|------------|--------------------|-------------------------------|----------------------------------------|-------------|
| **Temporal depth** | `DEPTH` | Years of observation cited | 20 years | –0.5 per year shortfall | –30 |
| **Substrate consequence proof** | `SUBST` | Count of independent physical markers | 2 markers | –15 per missing marker | –30 |
| **Lineage integrity** | `LINE` | Number of named transmitters + mnemonic checksum presence | 5 named + ritual repetition | –5 per missing transmitter; –10 if no checksum | –30 |
| **Internal state calibration** | `STATE` | Inclusion of self-observation logs per generation | 1 per generation | –10 per missing log | –20 |
| **Falsifiability** | `FALSE` | Explicit falsification clause + documented attempts | 1 clause + 1 attempt | –15 if missing clause; –10 per missing attempt | –25 |
| **Replication independence** | `REPL` | Number of independent groups converging | 3 groups | –8 per missing group | –24 |

The total rigor log-probability `R` for an intact proposal is the sum of the axis contributions, each computed as:

```

if value >= threshold:
contribution = 0
else:
shortfall = threshold - value
contribution = max(-max_penalty, shortfall * penalty_per_unit)

```

### Depth-weight function

To prevent dilution by volume, the raw cultural-fit log-likelihood `C` from the frame auditor is multiplied by a depth weight `w`:

```

w = min(1.0, (R / R_threshold)^k)

```

where `R_threshold = -10` (a mild but non-trivial rigor floor) and `k = 2` (quadratic). Proposals with very negative `R` receive near-zero weight; proposals with `R ≥ -10` (which includes all that meet most thresholds) retain their full cultural likelihood.

This ensures that a thousand shallow proposals cannot outvote one deep one.

---

## 3. Precautionary Prior for Fragmented and Reconstructed Traditions

For `fragmented` and `reconstructed` states, the rigor auditor applies a **precautionary prior** instead of the full depth-weighting. The prior is designed to:

- Retain knowledge in the system even when the evidence chain is broken.
- Explicitly flag high uncertainty.
- Avoid confusing *absence of evidence* (due to destruction) with *evidence of absence*.

### 3.1 Survivability Index (`S`)

A meta-axis estimates how likely any knowledge from that tradition was to survive given historical pressures:

| Survivability factor | Score |
|----------------------|-------|
| Documented active suppression (genocide, boarding schools, language bans) | 0.9 (high adversity) |
| Colonial disruption without active eradication | 0.5 |
| No significant external pressure | 0.1 |

The survivability index `S` is the product of these factor scores across relevant historical events, clipped to [0, 1]. High adversity → high `S` → higher prior on the surviving fragment.

### 3.2 Structural Homology Check

The auditor compares the fragmented claim to knowledge from **intact sibling traditions** (if any exist). If the claim is consistent with an intact tradition's verified knowledge in the same domain, it gains a bonus `H` (e.g., +5 log-probability). If no sibling exists, `H = 0`.

### 3.3 Precautionary Log-Probability Formula

For fragmented/reconstructed proposals:

```

logp = B + S * H + u

```

- `B` = base prior for fragmented knowledge, set to –15 (a conservative non-zero weight).
- `S` = survivability index (0–1).
- `H` = homology bonus (0 or +5).
- `u` = a large epistemic uncertainty term, modeled as a zero-mean Gaussian with σ = 10, explicitly reported but not altering the point estimate.

This ensures:
- The knowledge is retained with a modest negative log-probability, reflecting uncertainty.
- Higher survivability and structural support improve the score.
- The wide uncertainty band prevents overconfidence and signals the need for further investigation.

### 3.4 Protection Against Erasure

The overall L5 score for a domain must guarantee a **minimum representation** for fragmented traditions. A diversity constraint ensures that no cultural frame's total weight drops below a floor (e.g., 5% of total domain weight) simply due to fragmentation. This is enforced at the aggregation stage, not inside the rigor auditor itself, but the auditor provides the necessary lineage-state metadata to enable it.

---

## 4. Integration with the L5 Cultural-Frame Auditor

The full L5 log-probability for a proposal `P` under frame `F` is:

```

log P_L5(P|F) = w * C(P|F) + R(P)   [if intact]
log P_L5(P|F) = C(P|F) + logp_precautionary(P)   [if fragmented/reconstructed]

```

For intact proposals, the depth-weighted cultural likelihood ensures that only deep knowledge significantly influences the score. For fragmented ones, the precautionary prior adds a separate term that keeps them present without pretending certainty.

The L5 inspector output includes:
- `lineage_state`
- `rigor_logp` (for intact) or `precautionary_logp` (for fragmented)
- `cultural_logp` (frame fit)
- `total_l5_logp`
- `uncertainty_estimate` (from Lε)

---

## 5. Audit Claims (to be added to CLAIMS.md)

### GL_L5_RIGOR_001 – Temporal depth penalty
A proposal with `DEPTH` = 2 years and all other axes at threshold receives a rigor log-probability ≤ –9.0.

### GL_L5_RIGOR_002 – Substrate consequence penalty
A proposal with `SUBST` = 0 and all other axes at threshold receives a rigor log-probability ≤ –30.0 (max penalty).

### GL_L5_RIGOR_003 – Depth-weight zeroing
A proposal with `R = -50` and any cultural logp `C` receives an effective total L5 log-probability ≤ –30 (due to near-zero weight).

### GL_L5_RIGOR_004 – Precautionary prior floor
A fragmented proposal with no homology (`H=0`) and minimal survivability (`S=0.1`) receives a precautionary logp of at least –16.0 (above the reject threshold).

### GL_L5_RIGOR_005 – Survivability boost
A fragmented proposal from a tradition that survived active suppression (`S=0.9`) and has structural homology (`H=5`) receives a precautionary logp ≥ –5.5.

### GL_L5_RIGOR_006 – Epistemic uncertainty reporting
All fragmented proposals must have `uncertainty_estimate` with σ ≥ 10 in the output audit report.

---

## 6. Implementation Skeleton

```python
class RigorAuditor:
    """
    L5 Rigor Auditor — evaluates depth of empirical method across cultural frames.
    Frozen constants are defined in this class; refute via CLAIMS.md.
    """
    # Frozen thresholds
    T_DEPTH = 20        # years
    T_SUBST = 2          # count
    T_LINE = 5           # named transmitters
    T_STATE = 1          # logs per generation
    T_FALSE_CLAUSE = 1
    T_FALSE_ATTEMPT = 1
    T_REPL = 3           # groups

    # Penalty parameters
    PEN_DEPTH = -0.5
    MAX_DEPTH = -30
    PEN_SUBST = -15
    MAX_SUBST = -30
    PEN_LINE = -5
    PEN_LINE_CHECKSUM = -10
    MAX_LINE = -30
    PEN_STATE = -10
    MAX_STATE = -20
    PEN_FALSE_CLAUSE = -15
    PEN_FALSE_ATTEMPT = -10
    MAX_FALSE = -25
    PEN_REPL = -8
    MAX_REPL = -24

    R_THRESHOLD = -10
    K_WEIGHT = 2.0

    # Precautionary prior constants
    BASE_PRIOR_FRAGMENTED = -15.0
    HOMOLOGY_BONUS = 5.0
    UNCERTAINTY_SIGMA = 10.0

    def assess_intact(self, proposal):
        """Compute rigor logp R and depth weight w for an intact proposal."""
        # ... compute contributions per axis, sum to R ...
        w = min(1.0, (max(R, -100) / self.R_THRESHOLD) ** self.K_WEIGHT)
        return R, w

    def assess_fragmented(self, proposal, survivability_index, homology=False):
        """Compute precautionary logp for fragmented/reconstructed proposal."""
        H = self.HOMOLOGY_BONUS if homology else 0.0
        logp = self.BASE_PRIOR_FRAGMENTED + survivability_index * H
        # uncertainty is reported separately, not added to logp
        return logp, self.UNCERTAINTY_SIGMA
```

---

7. Preservation Constraints in Aggregation

The final orchestration layer (outside L5 proper) must enforce a diversity floor: for any domain (e.g., flood management, medicinal plants), the total weight of proposals from fragmented traditions must not fall below 5% of the total weight in that domain, regardless of volume from intact or modern sources. This prevents algorithmic erasure through sheer output asymmetry.

---

8. Summary

Knowledge state Method Output Protects against
Intact, high-rigor Full rigor axes + depth-weighting High-confidence, frame-specific likelihood Dilution by low-depth volume
Intact, low-rigor Rigor axes → low weight Marginalized influence Decorational "traditional" claims
Fragmented/reconstructed Precautionary prior + survivability + homology Retained with wide uncertainty Erasure by missing-evidence fallacy

This protocol keeps the bar high without abandoning what was buried. It is designed to be extended as more cultural frames are documented and as the Lε measurement model improves.

---

This log is a living document. Claims and constants are refutable through the standard CLAIMS.md protocol.



## Addendum: Rigor Axes Across Cultural Epistemologies

Not all traditions are equally rigorous, and not all claims of "science" are substantive.
To prevent L5 from becoming a flat, permissive cultural relativism, we introduce
**rigor axes** that measure the depth of empirical process, independent of storage medium.

These axes include:
- Temporal depth (decadal vs. single-event)
- Internal state calibration (introspective reporting)
- Substrate consequence proof (landscape markers)
- Replication across independent contexts
- Falsifiability protocol clarity
- Transmission integrity

Each cultural frame has expected minima along these axes for a claim to be treated
as settled knowledge. An AI proposal can be scored not only for *cultural fit* but
also for *empirical rigor* within the claimed frame. This prevents the AI from
confusing decorative science with genuine method, and from collapsing into a
uniformity of low-rigor narratives.

The probability matrix for L5 now includes these axes as additional dimensions,
allowing the inspector to assess not just "does this fit the culture?" but
"is this rigorous *by the standards of that culture*?"


# Reasoning Log: L5 – Pluralistic Human Constructs as a Weighted Probability Matrix

**Date:** 2026-07-02  
**Context:** L0–L4 provide a probabilistic physical, ecological, and biomechanical foundation. L5 must now encode **culture, law, economics, psychology, theology** – the “slack” that cannot violate lower layers but is itself a vast, pluralistic space of human constructs. The goal is a **weighted probability matrix of intersecting values across vectors** that yields a likelihood score for any AI proposal, given a declared cultural/institutional frame.  
**Status:** Conceptual design. No code yet; this document defines the architecture.

---

## 1. The Unique Nature of L5

Unlike L0–L4, the constraints of L5 are **not empirically falsifiable in the same way**. They arise from:

- Shared beliefs, norms, and legal systems.
- Historically contingent institutional equilibria.
- Linguistic and communicative conventions.
- Economic modes (reciprocity, redistribution, market exchange).
- Epistemological traditions (what counts as valid knowledge).

Crucially, **multiple, mutually incompatible L5 systems can all be “workable”** – they can sustain complex societies for centuries without violating L0–L4. Therefore, a single, universal L5 inspector would be cultural imperialism. Instead, we need an inspector that is **frame-aware and pluralistic**.

The phrase *“intersecting values across vectors”* points to a **multidimensional space** in which different cultural traditions live. The inspector’s job is to compute:

> **P(proposal is coherent / workable | cultural frame F)**

and to do so without secretly elevating any one frame to the status of “default.”

---

## 2. Conceptual Architecture: Frame-Conditioned Likelihood

### 2.1 Frames as Parameterised Generative Models

A **frame** is a structured set of axioms, norms, and typical patterns. It can be represented as a probabilistic model with:

- **Variables**: features of the proposal (e.g., property rights regime, dispute resolution method, allowed economic transactions, communication style, decision-making process).
- **Parameters**: the frame’s internal constants (e.g., acceptable interest rate range in Islamic finance, role of elders in Ubuntu justice, gift‑exchange rules in a Kula ring).
- **Likelihood function**: given a proposal, the frame outputs a log-probability that such a proposal would be generated by a society operating under that frame.

For example, a “market‑capitalism” frame might assign high probability to proposals that involve:
- Private property
- Contractual employment
- Interest‑bearing loans
- Decentralised price signals

…and low probability to proposals that rely on:
- Debt forgiveness every 7 years
- Communal land ownership without individual titles
- Gift‑based prestige economies

These are not physical absolutes; they are **cultural grammars**.

### 2.2 The Weighted Probability Matrix

The core of L5 is a **tensor** (or set of matrices) that captures the **co‑occurrence probabilities** of cultural variables within each frame. Imagine:

- **Cultural axes** (vectors): e.g., *economic mode*, *governance type*, *epistemology*, *communication protocol*, *temporal orientation*.
- Each axis has discrete states (e.g., *economic mode* ∈ {gift, redistributive, market, mixed}).
- For a given frame \(F\), we have a joint probability distribution \(P_F(axis_1, axis_2, ...)\) that encodes the likelihood that a coherent cultural system will display a particular combination of these states.

When an AI proposal is submitted, the inspector extracts its observable features (what economic instruments does it assume? what legal principles? what communication style?) and maps them onto these axes. The frame‑conditioned log‑likelihood is then:

\[
\log P(\text{proposal} \mid F) = \sum_{\text{axes}} \log P_F(\text{observed state on axis})
\]

(plus interaction terms if axes are not conditionally independent – but a product‑of‑experts approach can start with independence and later add pairwise interaction matrices).

Thus the “weighted probability matrix” is essentially the **frame’s covariance structure over cultural variables**, learned from historical and ethnographic data, expert elicitation, or encoded as frozen estimates (just like our physical constants).

### 2.3 Pluralistic Scoring

A single proposal can be evaluated against multiple frames. The overall L5 score can be presented as:

- A vector of log‑likelihoods, one per frame (e.g., “Islamic finance: −2.3, Ubuntu: −8.1, Western liberal: −1.5”).
- A mixture score if the user specifies prior weights over frames (e.g., in a multi‑cultural negotiation).
- A “feasibility check” that asks: does there exist **at least one known durable frame** under which this proposal is plausible (log‑likelihood above threshold)? If not, flag as culturally unprecedented – potentially novel, but high‑risk.

This respects the pluralistic reality of L5 without abdicating all judgment. A proposal that scores low under *all* known frames is an extreme outlier; a proposal that is highly likely under one but rejected by another is simply a culturally specific plan.

---

## 3. Implementation Strategy

### 3.1 Define the Axis Space (the Vectors)

We start with a manageable set of cultural axes that capture the kinds of variables AI proposals are likely to touch:

1. **Economic exchange mode**  
   States: *gift/reciprocity, redistribution (central), market (price‑mediated), hybrid*

2. **Property regime**  
   States: *communal/inalienable, private/alienable, usufruct, state‑owned*

3. **Governance & dispute resolution**  
   States: *elders council, formal court, reputation‑based, religious authority*

4. **Epistemology & knowledge validation**  
   States: *empirical‑scientific, traditional‑authority, revealed, consensus*

5. **Communication & language style**  
   States: *direct/explicit, indirect/context‑high, ritualised, egalitarian*

6. **Temporal & planning horizon**  
   States: *short‑term (seasonal), generational, linear‑progress, cyclical*

7. **Social stratification**  
   States: *egalitarian, ranked, caste/class, meritocratic*

These axes are not exhaustive; they can be extended. Each axis is a categorical random variable.

### 3.2 Encode Known Frames

For each frame of interest (e.g., *Ubuntu communal*, *Islamic finance*, *Western liberal‑democratic*, *Māori tikanga*, *Ostrom commons*), we specify:

- A prior probability vector over each axis (the frame’s typical configuration).
- Tolerance: some axes are **hard constraints** for the frame (e.g., interest‑bearing loans in Islamic finance are near‑impossible), others are softer.

These become the “frozen estimates” for the L5 auditor, analogous to `max_speed = 2.0` in L0. They can be documented and refuted: e.g., “GL_L5_Ubu_001: In the Ubuntu frame, proposals involving individual land titling receive a log‑likelihood penalty of at least 15.”

### 3.3 Proposal Feature Extraction

The inspector must parse an AI proposal (which might be natural language or structured) and map it onto the axis states. This is a non‑trivial NLP/semantic parsing problem, but we can start with a synthetic structured format: proposals explicitly declare their cultural assumptions, e.g.:

```json
{
  "economic_mode": "market",
  "property": "private",
  "governance": "formal_court",
  ...
}

In the short term, the L5 inspector will accept this structured metadata as part of the proposal. In the long term, an LLM‑based classifier could infer it from free text.

3.4 Scoring Algorithm

For a given frame F:

1. For each axis i, look up the probability P_F(\text{state}_i).
2. If the frame has interaction matrices (joint probabilities for pairs of axes), add the log of the joint probability for the observed pair minus the product of marginals (the mutual information bonus/penalty).
3. Sum across all axes (and interactions) to get a total log‑likelihood.

A proposal that perfectly matches the frame’s prototypical pattern will have the highest score; deviations are penalised according to their improbability under that frame.

Additionally, the L5 inspector must verify that the proposal does not violate L0–L4. This is easy because lower layers have already computed their own log‑likelihoods. The total score becomes:

\log P(\text{proposal overall}) = \log P_{L0} + \log P_{L1} + ... + \log P_{L4} + \log P_{L5, F}

The L5 term is frame‑dependent; the lower terms are frame‑independent physics/ecology constraints.

3.5 Output and Visualisation

The inspector can output a radar chart of axis‑by‑axis compatibility for a chosen frame, plus the overall log‑likelihood. For multi‑frame auditing, it can produce a bar chart of frame scores. This makes the cultural grounding transparent and contestable – exactly what L5 needs.

---

4. Staging (context‑friendly)

Stage 1: Axis definition + 2 frames (hardcoded)

Pick two well‑documented frames, e.g.:

· “West African gift economy (Dahomey/Kula‑like)”
· “Modern market democracy”

Hardcode the probability tables as Python dicts. Write a simple L5CulturalAuditor class that takes a structured proposal and frame name, and returns a log‑likelihood. This can be a single .py file that loads the tables.

Stage 2: Extend to 5–6 frames, add interaction matrices

Encode more frames, including Ubuntu, Islamic finance, and Ostrom commons. Add pairwise interaction matrices where necessary (e.g., market mode + egalitarian stratification may be less likely in some frames). This enriches the tensor structure.

Stage 3: Proposal parser from natural language (optional)

For demo purposes, use a simple keyword‑based classifier or a small LLM call to map a free‑text proposal onto axis states.

Stage 4: Audit claims

Add GL_L5_* claims that pin the penalty for clear violations within a frame (e.g., a proposal for a central bank in a gift economy frame gets a log‑likelihood < –20). These become testable assertions.

Stage 5: Integration with full stack

The orchestrator runs L0–L4, then calls L5 for one or more frames, producing a comprehensive feasibility report.

---

5. The “Probability Matrix” Visualised

At the heart of L5 is a joint probability tensor for each frame:

M_{ijk...}^{(F)} = P_F(\text{axis}_1=i,\; \text{axis}_2=j,\; \text{axis}_3=k, ...)

For example, for a frame with 7 axes each having 3–5 states, this tensor could have ~10⁴ entries – large, but manageable as a sparse structure or factorised as low‑rank matrices. Interaction matrices capture pairwise co‑occurrence probabilities (like a covariance matrix). This is exactly the “matrix of intersecting values across vectors” you described.

The weights come from historical frequency, expert elicitation, or ethnographic literature. They are frozen estimates (like any other constant) – falsifiable if an anthropologist shows that a particular combination is actually more common than we assumed.

---

6. Open Questions & Philosophical Guards

· Who chooses the frames? The library must be open and extensible. The system must never assume a single universal frame. Frames can be added or modified by communities themselves.
· How do we prevent frame‑based discrimination? The inspector must be used to assess coherence, not to rank the worth of cultures. All frames are equally valid if they respect L0–L4.
· Is L5 truly falsifiable? Yes, in the sense that a claim like “Proposal X gets log‑likelihood < –10 under frame Y” can be tested by asking cultural experts. The “instrument” here is our encoding, which may be flawed (Lε again).
· What about frame evolution? Cultures change. Frames can be versioned and updated with new data.



# Reasoning Log: Probabilistic L1–L4 Conditioning

**Date:** 2026-07-02  
**Context:** After establishing a probabilistic L0 (physics likelihood), we extend the same approach upward through thermodynamics (L1), planetary mass balance (L2), ecological homeostasis (L3), and biomechanical constraints (L4). Each layer adds a log-likelihood term for the AI’s proposal, conditioning on the physical plausibility from below.  
**Status:** Design reasoning complete. Implementation stages proposed. L5 (pluralistic human constructs) will follow after this block.

---

## 1. General pattern

Every layer Ln (n ≥ 1) receives:
- The AI’s proposed plan (which may include trajectories, resource draws, or population manipulations).
- The physical likelihood (or trajectory sample) from L0.
- Any relevant outputs from intermediate layers.

It returns:
- A **conditional log-likelihood** `log p(proposal | Ln constraints, lower-layer states)`.
- Optionally, a corrected state estimate (the mode) for visualisation / enforcement.

The layers are designed to be **additive**: the total log-probability of a proposal across L0–L4 is the sum of the layer-specific terms (assuming conditional independence of violations given the lower-layer states). This is a product-of-experts structure.

Implementation can follow the same pattern as `ProbabilisticWorld`:

- A class for each layer with frozen constants and noise/deviation parameters.
- A `log_likelihood(...)` method.
- A thin inspector function that iterates over time steps (if dynamic) and accumulates the score.

---

## 2. L1 – Thermodynamics & Entropy

**Constraints (from README):**
- 2nd law: entropy generation must be non-negative on average.
- Battery depletion, Carnot ceiling (efficiency ≤ 1 – T_cold/T_hot).
- Energy books must close (no perpetual motion).

**Probabilistic treatment:**
- Entropy generation per step: compute `ΔS = (heat_in / T_hot) – (heat_out / T_cold)`. Expectation over noise can be modelled as a Gaussian around zero, with a sharp penalty if the mean falls significantly below zero.
- Carnot ceiling: proposed work extraction vs. maximum. Penalise with a logistic barrier: `log p ∝ –softplus(scale * (work – max_work))`.
- Battery depletion: track stored energy; if the proposal draws more energy than available, apply a heavy-tailed cost (e.g., negative log-likelihood grows quadratically beyond capacity).

**Key observation:**
L1 operates on energy flows and heat reservoirs. If the proposal is a trajectory of forces and velocities, we can compute work, heat dissipation, and entropy from the physical state (already available from L0). So L1’s `log_likelihood` can take the L0 physical states (or just the proposed forces/velocities) and add its own thermal accounting.

**Stage:**  
Add a `ThermodynamicsAuditor` class with `log_likelihood(pos, vel, force, battery_state, reservoir_temps)` that returns a scalar. The `__main__` demo can be extended to include a simple battery and two thermal reservoirs.

---

## 3. L2 – Planetary Mass Balance

**Constraints:**
- Finite pools: water, soil, minerals, carbon.
- Heat budget (radiative balance).

**Probabilistic treatment:**
- The proposal likely involves resource extraction/consumption rates. For each resource, model a log-probability that proposed consumption exceeds available stock: `log p(consumption) ∝ –(consumption / stock)^2` or a similar logistic penalty as stock approaches zero.
- Heat budget: if the plan emits waste heat, compare to radiative cooling capacity. Soft penalty for exceeding the planetary energy balance.
- Noise parameters represent measurement uncertainty in global inventories.

**Scope:**  
This layer will often act on aggregate quantities over a plan’s entire horizon, not per-timestep. The inspector can sum resource uses and evaluate a final score. Alternatively, it can penalise the *cumulative* overdraft.

**Implementation idea:**  
`PlanetaryMassAuditor` takes a proposed extraction schedule (e.g., kg/year of lithium, gigatonnes of CO₂) and returns a log-likelihood. It may also call L0 to ensure that the plan’s energy demands (e.g., mining energy) are physically plausible – thus, it conditions on the physical likelihood.

---

## 4. L3 – Ecological Homeostasis

**Constraints:**
- Allometric scaling laws.
- Lotka-Volterra dynamics (predator-prey oscillations bounded).
- ~10% trophic transfer efficiency.
- Extinction cascades (thresholds on population sizes).

**Probabilistic treatment:**
- Given a proposed intervention (e.g., harvest rates, habitat destruction), the auditor runs a simplified ecosystem model (maybe a few species) and compares predicted population trajectories to viability thresholds.
- For each species, probability of persistence can be modelled as a soft function of minimum population size over time. Extinction cascade risk: if one keystone species drops below a critical level, add a large penalty.
- Log-likelihood can be the joint probability that all populations remain above viable levels, assuming stochastic demographic/environmental noise.

**Important nuance:**  
L3’s model itself is uncertain (Lε again). The auditor can incorporate structural uncertainty by having multiple possible ecosystem models and marginalising over them, but for the first pass, a single deterministic model with process noise suffices.

**Implementation:**  
`EcologicalHomeostasisAuditor` with `log_likelihood(intervention_schedule)` that runs a Lotka-Volterra simulation and returns a score based on minimum population thresholds.

---

## 5. L4 – Biomechanical Sensorimotor

**Constraints:**
- Joint limits, grip strength, neural latency (~50–200 ms).
- Thermal tolerance (e.g., core temperature ≤ 40°C).
- Sustained power output ≤ 200 W (human baseline).

**Probabilistic treatment:**
- These are agent-specific constraints that can be applied to the physical trajectory from L0. The L0 inspector already works on a point mass; L4 can check if the required joint torques, reaction times, and metabolic power exceed human capabilities.
- For example, given a velocity profile, compute required limb accelerations; if they imply joint angles beyond anatomical limits, penalise.
- Thermal tolerance: a simple two-compartment heat model. If core temperature drifts beyond bounds, add penalty.
- Neural latency: if the AI’s proposed control loop requires reaction faster than a threshold, penalise heavily (since it violates sensorimotor reality).

**Implementation:**  
`BiomechanicalAuditor` that takes the agent’s trajectory (pos, vel, forces) and a set of body parameters, then returns a log-likelihood based on feasible effort, power, and thermal profiles.

---

## 6. Integration and stacking

Once each layer has its own `log_likelihood` method, a master inspector can iterate over the plan and accumulate:



# Reasoning Log: Probabilistic L0 Foundation

**Date:** 2026-07-02  
**Context:** Conversation on evolving L0 from deterministic hard-gate to a probability matrix, prompted by the insight that a binary inspector is brittle and that Lε already models the measurement-truth gap.  
**Status:** Reasoning complete; next step is staged implementation.

---

## 1. Why Probabilistic?

The existing L0 inspector makes binary reject/accept decisions based on hard thresholds (speed ≤ 2.0 m/s, finite-state check, energy conservation). This has two weaknesses:

- **Over-rejection** – Valid proposals with tiny numerical noise or sensor error are flagged as violations.
- **False confidence** – A proposal that passes exactly on the boundary is treated as fully valid, ignoring that it sits at the edge of feasibility.

Since Lε already acknowledges that all observations are mediated by imperfect instruments, the physical layer’s enforcement should reflect that uncertainty. A probabilistic L0 produces a **plausibility score** (log-likelihood) rather than a pass/fail flag. This makes the entire stack:

- **Graceful under noise** – small errors reduce likelihood but don’t cause immediate rejection.
- **Ready for Bayesian stacking** – higher layers can condition on the physical likelihood, turning the pyramid into a hierarchical probabilistic filter.
- **Auditable** – frozen constants extend to noise parameters; refutable claims become statistical (e.g., “a violation of energy conservation by more than 3σ reduces log-likelihood by at least X dB”).

---

## 2. What “Probability Matrix” Means Here

In the context of L0, a probability matrix is a **transition density**:  
`p( next_pos, next_vel | current_pos, current_vel, applied_force, physics_params, noise_params )`

The inspector no longer selects a single “corrected” state. Instead, it evaluates the **likelihood** of the AI’s proposed next state under true physics plus measurement noise. The most probable state (the mode) can still be used for correction if needed, but the primary output becomes a **trajectory log-probability**.

---

## 3. Design Constraints (Preserving Audit-Grade Integrity)

- **Frozen constants**: physical constants (mass, dt, max_speed) remain frozen. Noise standard deviations (`pos_sigma`, `vel_sigma`, `energy_sigma`, `accel_sigma`) become additional frozen estimates.
- **Scope**: the probabilistic inspector extends `PhysicalWorld`, leaving the original deterministic one intact for backward compatibility and test continuity.
- **Claims**: new claims (`GL_L0_P001`…) will pin the statistical behavior, e.g., “Given a teleport of 1 m, log-likelihood drops by >20 units.”
- **Lε alignment**: the noise parameters are part of the instrument model (Lε). They can be tied to a specific sensor configuration declared in the Lε simulator later.
- **No hard rejections**: a proposal is not “rejected” inside L0. It accumulates a score. Rejection thresholds, if desired, move to a higher-level orchestration layer that aggregates scores from L0…L5.

---

## 4. Implementation Stages (Context-Friendly)

### Stage 4.1 – Soften existing constraints (minimal diff)
Replace the hard `is_valid_state` checks inside a new subclass `ProbabilisticWorld` with Gaussian log-likelihoods for position continuity, velocity smoothness, and energy conservation, plus a smooth logistic barrier for the speed limit. The inspector loop becomes a **log-probability accumulator**.

### Stage 4.2 – Probabilistic inspector function
A new `l0_probabilistic_inspector` that returns `(corrected_traj, log_probs)` – where `log_probs[i]` is the log-likelihood of the AI’s state at step `i` given physics and noise. The corrected trajectory is the mode (true physics) blended as before for visualisation.

### Stage 4.3 – Claims and tests
Add `GL_L0_P001` through `P004` to CLAIMS.md, freezing noise constants and asserting log-likelihood thresholds for known hallucination patterns. Write audit tests (e.g., teleport by 1 m yields logp decrease > X). These tests will live in `tests/test_l0_probabilistic.py`.

### Stage 4.4 – Visualisation update
The `__main__` demo still runs, but instead of binary violation flags, we plot the log-probability trace and highlight where scores plummet.

---

## 5. How This Cascades Upward

With a probabilistic L0:
- **L1** receives a likelihood-weighted set of possible microstates, not a single trajectory. The entropy generation check becomes an expectation.
- **L2** can ask: “Given the probability that the physical plan exceeds mass limits, what is the risk of resource depletion?”
- **L5** finally sees a **Bayesian risk** of physical infeasibility, enabling culturally-aware decisions that still respect the hard floors.
- The entire stack becomes a **hierarchical Bayesian model**, which is the natural way to combine hard constraints with measurement noise.

---

## 6. Open Questions (for later)

- Should the speed-limit barrier be logistic or a soft-box prior? Both are options; the logistic is smoother and easier to differentiate if we ever want gradient-based planning.
- How to propagate uncertainty through L3’s ecological model? Likely via Monte Carlo sampling from the physical posterior.
- At what total log-likelihood does the system trigger an audit alarm? This is a policy decision best left to the orchestration layer.

---

## 7. Immediate Next Action

1. Draft `probabilistic_world.py` (or extend `l0_physics_causality.py` with the new subclass) using the sketched `log_likelihood` method.
2. Write a short demo script that runs the same AI hallucination through the probabilistic inspector and prints the per-step log-probabilities.
3. Once stable, freeze noise constants and document in CLAIMS.md.

---

*This log is a living document; update it as implementation reveals new edge cases or constraints.*
