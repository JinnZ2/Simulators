OPEN_RESEARCH.md

---

## CLAIM_TABLE_v2.md

Claims about the delivered category-weld/ folder, about what a Python stdlib environment can establish concerning it, and about the measurement‑gap protocol it inherits.

This is a detection scaffold, not a measurement. No real‑world readings populate any weld term. Every case in welds/ is currently unquantified: named, with no paired before/after readings attached. n_cases is live. max_spread and bias are implemented and verified against synthetic fixtures, and return -- until real paired readings exist. That is the honest state. The gap is in the data, and it is marked rather than filled.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A break is a measurement — update the claim, never retune the scorer to preserve a claim.

| id | claim | status |
|---|---|---|
| `CW_001` | CATEGORY WELD is distinct from the existing eight mechanisms. Those exclude a quantity from being measured; this one prevents two measurable quantities from being separated. | SUPPORTED (by mechanism definition) |
| `CW_002` | A term is welded iff at least one divergence case can be named AND the language has no separate handle for the diverged components. | SUPPORTED (by definition) |
| `CW_003` | n_cases alone is insufficient. Rare‑but‑enormous divergence and frequent‑but‑small divergence are different, and case count cannot tell them apart. | SUPPORTED (by scorer design) |
| `CW_004` | bias separates directional welds from imprecise ones without any input about intent. | SUPPORTED (by scorer design) |
| `CW_004a` | bias is a continuous measure from 0 to 1. Bias near 0 means divergence in random directions — the term is imprecise. Bias near 1 means divergence always in the same direction — one component systematically stands behind another. | SUPPORTED (by scorer design) |
| `CW_005` | Language models are more prone to welds than to retrieval errors. Co‑occurrence training provides no gradient that would separate components a corpus never separates. | SUPPORTED (by mechanism logic) |
| `CW_006` | "rural" is welded: density diverges from ownership distribution and functional diversity. | UNVERIFIED — cases named, no paired readings yet |
| `CW_007` | "capital" is welded: title diverges from decision authority, risk bearing and revenue claim. | UNVERIFIED — cases named, partial readings (risk_bearing) exist |
| `CW_008` | "hierarchy" is welded: nested containment diverges from imposed ordering, ordering origin, and cut rate. | UNVERIFIED — cases named, no readings yet |
| `CW_009` | Divergence in the seed terms runs in a consistent direction rather than randomly. | UNTESTED — no term quantified yet |
| `CW_010` | The delivered code is stdlib‑only. weld.py and test_weld.py import only from the Python standard library. | SUPPORTED |
| `CW_011` | The delivered code is runnable. Both .py files execute and provide interactive CLIs. | SUPPORTED |
| `CW_012` | The scorer's arithmetic is verified against synthetic fixtures. test_weld.py exercises n_cases, n_quantified, n_unquantified, max_spread, and bias with invented numbers. | SUPPORTED |
| `CW_013` | Every case in welds/ is currently unquantified. Named, with no paired before/after readings attached. | SUPPORTED (by file inspection) |
| `CW_014` | Cases without paired readings still count toward n_cases and are reported separately as n_unquantified. They do not contribute to max_spread or bias. An unquantified case is a gap marker, not a smaller case. | SUPPORTED (by scorer design) |
| `CW_015` | The repository contains no real‑world measurements. All readings are either null or, in one case, a single‑sided point estimate with no paired before/after. | SUPPORTED |
| `CW_016` | The folder is phone‑buildable. stdlib‑only, no dependencies, parses under Python 3.9. | SUPPORTED |
| `CW_017` | The repository produces no policy recommendation. It is a marker for a sensed shape that needs more exploration — not a thesis and not a position under defense. | SUPPORTED |
| `CW_018` | The "generation rule" — that models are structurally prone to welds — is a hypothesis, not a demonstrated claim. It requires empirical testing across corpora. | UNVERIFIED |

---

## OPEN_QUESTIONS.md

Open questions in the category‑weld framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. DATA POPULATION — Rural Weld Quantification

**Gap:** rural.json names four divergence cases — industrial consolidation, no‑alternate‑check, employment concentration, service withdrawal — but all readings are null or endpoint‑only.

**Knowledge state:** UNKNOWN_ATM

**Research question:** Do the components of "rural" (density, ownership distribution, functional diversity, self‑supporting capacity) actually diverge in the field? If so, by how much, and in what direction?

**Disciplines:** Agricultural economics, rural sociology, demography

**Data sources:**

- USDA Census of Agriculture (farm size, operator count, land ownership)
- USDA Economic Research Service (rural‑urban continuum codes, county typology)
- Bureau of Labor Statistics (employment concentration, industry diversity)
- Health Resources & Services Administration (rural hospital closures)
- County‑level time series (2000–present)

**Method:**

1. For each divergence case, identify measurable proxies:
- Industrial consolidation: operators per 1000 acres over time
- No‑alternate‑check: number of independent operations per county over time
- Employment concentration: Herfindahl index of regional employment
- Service withdrawal: hospital and clinic presence over time
2. Collect paired before/after readings for each case
3. Compute relative changes for each component
4. Feed readings into weld.py to generate n_cases, max_spread, bias
5. Document which components diverged and in what direction

**Expected deliverable:** A populated rural.json with quantified readings and a computed scorer output.

**Falsifier:** All components move together (then "rural" is not welded — it is a genuine summary).

---

### 2. DATA POPULATION — Capital Weld Quantification

**Gap:** capital.json names four divergence cases — intermediated‑title, socialized‑downside, subsidy‑without‑behaviour‑change, input‑supply‑uncompensated. One case has a partial reading (risk_bearing: 14.1 → 2.5). The rest are unquantified.

**Knowledge state:** UNKNOWN_ATM

**Research question:** Do the components of "capital" (ownership title, decision authority, risk bearing, revenue claim, input supply) actually diverge? If so, by how much, and in what direction?

**Disciplines:** Corporate finance, public economics, political economy

**Data sources:**

- Bloomberg Tax, SEC EDGAR (corporate ownership, tax expenditures)
- Federal Reserve Flow of Funds (risk bearing, public subsidy)
- Bureau of Economic Analysis (returns, revenue claims)
- Corporate governance datasets (ISS, Proxy Insight)
- State‑level subsidy databases (Good Jobs First, Subsidy Tracker)

**Method:**

1. For each divergence case, identify measurable proxies
2. Collect paired before/after readings
3. Compute relative changes
4. Feed readings into weld.py
5. Document which components diverged and in what direction

**Expected deliverable:** A populated capital.json with quantified readings and a computed scorer output.

**Falsifier:** All components move together (then "capital" is not welded).

---

### 3. DATA POPULATION — Hierarchy Weld Quantification

**Gap:** hierarchy.json names five divergence cases — environment‑ordered‑dominance, volunteer‑fire‑crew, credentialed‑fire‑service, surgical‑team‑drift, naturalness‑argument. All readings are null. The file also notes two open methodological issues.

**Knowledge state:** NOT_STUDIED

**Research question:** Do the components of "hierarchy" (nested containment, imposed ordering, ordering origin, cut rate) actually diverge? If so, by how much, and in what direction?

**Disciplines:** Organizational theory, sociology, anthropology, history of medicine

**Data sources:**

- Fire service records (volunteer → credentialed transition, documented and dated)
- Surgical team literature (1900s → present hierarchy evolution)
- Organizational ethnographies
- Military and corporate hierarchy studies

**Method:**

1. For each divergence case, identify measurable proxies:
- Volunteer vs. credentialed fire service: credentialing interval over time
- Surgical team drift: number of distinct credential tiers over time
- Naturalness argument: semantic analysis of "hierarchy" usage across corpora
2. Collect paired before/after readings
3. Compute relative changes
4. Feed readings into weld.py
5. Document which components diverged and in what direction

**Expected deliverable:** A populated hierarchy.json with quantified readings and a computed scorer output.

**Falsifier:** All components move together (then "hierarchy" is not welded — it is a genuine summary).

---

### 4. METHODOLOGICAL — The Read‑vs‑Imposed Criterion Fix

**Gap:** The hierarchy file notes: "The read‑vs‑imposed criterion must be fixed BEFORE any series is run. Sorting cases into 'not really hierarchy' after seeing the cut rate makes the finding true by construction."

**Knowledge state:** UNDEFINED

**Research question:** What is the operational definition of "read‑vs‑imposed" that can be applied before data collection? How do we distinguish a hierarchy that is read off the environment from one that is imposed on it?

**Disciplines:** Philosophy of science, organizational theory, methodology

**Data sources:**

- The hierarchy weld definition itself
- Published literature on hierarchy in organizational theory
- Case studies of volunteer → credentialed transitions

**Method:**

1. Define the distinction operationally: what measurable criteria separate "read" from "imposed"?
2. Test the criteria against known cases (volunteer fire crew vs. credentialed fire service)
3. Document the criteria in the hierarchy file
4. Apply criteria before collecting any series
5. Verify that the criteria are stable across cases

**Expected deliverable:** An operational definition of "read‑vs‑imposed" with test cases, added to hierarchy.json as a methodological note.

**Falsifier:** The distinction cannot be operationalized (then it must be dropped from the weld definition).

---

### 5. EMPIRICAL — Language Model Weld Proneness

**Gap:** The generation rule states: "Models are structurally prone to this one... when a corpus never separates the components, nothing in training provides a gradient that would pull them apart." This is a hypothesis, not a demonstrated claim.

**Knowledge state:** UNDER_STUDY

**Research question:** Are language models more prone to category welds than to other types of error? Can we measure weld proneness across model families and training corpora?

**Disciplines:** NLP, AI safety, computational linguistics

**Data sources:**

- Multiple language model families (GPT, Claude, LLaMA, etc.)
- Training corpus documentation (The Pile, C4, Common Crawl)
- Published benchmarks for compositional generalization
- The category‑weld definitions themselves

**Method:**

1. Design a probe: present models with components that diverge in a text, ask them to report on the category
2. Test across model families and sizes
3. Measure how often models fail to separate welded components
4. Compare to retrieval‑error rates on the same inputs
5. Correlate weld proneness with training corpus properties

**Expected deliverable:** An empirical study of language model weld proneness, with per‑model and per‑corpus measurements.

**Falsifier:** Models separate welded components as often as they retrieve facts correctly (then the generation rule is false).

---

### 6. EMPIRICAL — Category Weld Prevalence in Policy Language

**Gap:** The repository seeds three welds (rural, capital, hierarchy). Many more likely exist in policy and administrative language.

**Knowledge state:** NOT_STUDIED

**Research question:** What other categories in policy, law, and administration are welded? How prevalent is the category‑weld pattern in regulatory language?

**Disciplines:** Public policy, legal studies, linguistics

**Data sources:**

- Federal and state regulatory codes
- Policy documents (Congressional Research Service, GAO, OMB)
- Administrative law casebooks
- Published policy analysis

**Method:**

1. Develop a method for detecting welds in text: identify terms where multiple components are fused
2. Scan policy corpora for candidate welds
3. For each candidate, name divergence cases and components
4. Add new weld terms to the repository
5. Document the prevalence of the pattern

**Expected deliverable:** An expanded set of weld terms (10+), with documented divergence cases and components, added to welds/.

**Falsifier:** Fewer than three additional welds can be found (then the pattern is not prevalent).

---

### 7. EMPIRICAL — Welds in Environmental and Resource Management

**Gap:** The repository does not yet include environmental or natural resource categories, where the field‑desk gap is most acute.

**Knowledge state:** NOT_STUDIED

**Research question:** What categories in environmental management, forestry, water, and land use are welded? How do these welds affect resource decisions?

**Disciplines:** Environmental science, natural resource management, hydrology

**Data sources:**

- USDA Forest Service documents
- Bureau of Land Management land use plans
- EPA water quality regulations
- State natural resource agency documents
- Published environmental policy analysis

**Method:**

1. Identify candidate welds in environmental management (e.g., "forest health," "water quality," "sustainable yield")
2. For each candidate, name components and divergence cases
3. Collect paired readings where available
4. Add new weld terms to the repository
5. Document the implications for resource decisions

**Expected deliverable:** Environmental weld terms (3+), with documented components, divergence cases, and where possible, readings.

**Falsifier:** Environmental categories are not welded (then the pattern does not extend to this domain).

---

### 8. THEORETICAL — Weld vs. Summary Distinction

**Gap:** The definition states: "Failing (1): the components may genuinely be one quantity. Failing (2): the term is a summary, not a weld — the handles exist." The distinction between a "weld" and a "summary" is theoretically clear but operationally underdeveloped.

**Knowledge state:** UNDEFINED

**Research question:** What is the operational distinction between a category that is welded and one that is merely summarized? How do we distinguish them in practice?

**Disciplines:** Philosophy of language, measurement theory, epistemology

**Data sources:**

- The category‑weld definition
- Published literature on measurement and construct validity
- Examples of summaries and welds from multiple domains

**Method:**

1. Define operational criteria for "handles exist" (condition 2)
2. Define operational criteria for "components genuinely one quantity" (condition 1 failing)
3. Test criteria against known summaries (e.g., GDP, BMI) and candidate welds
4. Document the distinction
5. Update the mechanism definition with the operational criteria

**Expected deliverable:** An operational guide for distinguishing welds from summaries, added to the mechanism documentation.

**Falsifier:** The distinction cannot be operationalized (then the definition is unfalsifiable).

---

### 9. BIAS INTERPRETATION — What Bias Values Mean

**Gap:** The scorer computes bias as a continuous 0‑1 measure, but the interpretation of intermediate values is underdeveloped.

**Knowledge state:** UNDEFINED

**Research question:** What do different bias values tell us about a weld? Is there a threshold above which a weld is "directional" versus "imprecise"?

**Disciplines:** Statistics, measurement theory, epistemology

**Data sources:**

- The scorer's arithmetic
- Synthetic and real data from populated welds
- Published literature on bias and systematic error

**Method:**

1. Generate synthetic data with known bias properties
2. Map bias values to weld behavior
3. Identify natural thresholds (if any)
4. Test against populated welds
5. Document bias interpretation guidelines

**Expected deliverable:** A bias interpretation guide, with thresholds and examples, added to the mechanism documentation.

**Falsifier:** Bias values are uniformly distributed and show no natural thresholds (then interpretation is case‑specific).

---

### 10. MAX_SPREAD INTERPRETATION — What Spread Values Mean

**Gap:** The scorer computes max_spread as the largest ratio between component relative‑changes. The interpretation of different spread magnitudes is underdeveloped.

**Knowledge state:** UNDEFINED

**Research question:** What do different max_spread values tell us about a weld? Is there a threshold above which a weld is "severe"?

**Disciplines:** Statistics, measurement theory, risk analysis

**Data sources:**

- The scorer's arithmetic
- Synthetic and real data from populated welds
- Published literature on divergence and measurement error

**Method:**

1. Generate synthetic data with known spread properties
2. Map spread values to weld severity
3. Identify natural thresholds (if any)
4. Test against populated welds
5. Document spread interpretation guidelines

**Expected deliverable:** A spread interpretation guide, with thresholds and examples, added to the mechanism documentation.

**Falsifier:** Spread values are uniformly distributed and show no natural thresholds (then interpretation is case‑specific).

---

### 11. USER GUIDE — Non‑Specialist Translation

**Gap:** The repository is documented for researchers and developers but not for non‑specialists (policymakers, journalists, general public).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the category‑weld framework's insights be communicated to non‑specialists in a way that changes how they think about categories and measurement?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The framework itself
- Published science communication research
- Policy documents on measurement and indicators

**Method:**

1. Translate each weld concept into plain language with concrete examples
2. Develop case studies for each seed term (rural, capital, hierarchy)
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the category‑weld framework, with case studies and plain‑language explanations.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard measurement practice

---

### The Problem

In measurement and policy, categories like "rural," "capital," and "hierarchy" are treated as stable, unproblematic handles. If a statistic says "rural population is X," that is treated as a fact about the world. If a policy says "invest in rural communities," that is treated as a coherent action.

But the category is welded: two or more independent quantities are fused into a single handle. The components can move to opposite extremes without the record moving at all, because the language admits one value where the world has several.

When we treat a welded category as a stable handle, we are not simplifying reality — we are modeling a different system than the one that actually exists. And then we are surprised when policies based on that category fail.

---

### Six Ways the Connection Gets Lost

#### 1. The "Category as Fact" Fallacy

Many policy analysts treat categories as facts about the world. If the category says "rural," that is treated as a description of a place.

But "rural" is welded: density, ownership distribution, functional diversity, and self‑supporting capacity are fused into one label. A place can have low density (so it reads as "rural") while ownership has consolidated to a few operators, functional diversity has collapsed, and self‑supporting capacity has vanished. The category stays the same while the components diverge. If the policy says "rural," it is not false for the label, but it may be false for the system. The weld was causal — just not represented.

So "category as fact" often means "We treated the label as the thing." That is a measurement error, not evidence that the components don't matter.

#### 2. The "Title as Control" Fallacy

Many economic analyses treat ownership title as a proxy for control. If the title says "owned by X," that is treated as a description of who decides.

But "capital" is welded: title, decision authority, risk bearing, revenue claim, and input supply are fused into one label. Title can be maximally diffuse (index funds, pension accounts) while decision authority is concentrated. Risk bearing can run through public subsidy while revenue claim stays private. The category stays the same while the components diverge. If the analysis says "owned by X," it is not false for the title, but it may be false for the control. The weld was causal — just not represented.

So "title as control" often means "We treated the label as the thing." That is a measurement error, not evidence that title and control move together.

#### 3. The "Hierarchy as Natural" Fallacy

Many organizational theories treat hierarchy as natural — a stable feature of human organization.

But "hierarchy" is welded: nested containment, imposed ordering, ordering origin, and cut rate are fused into one label. A volunteer fire crew has nested containment (roles) but ordering established at the point of use and cut rate near zero. A credentialed fire service has the same nested containment but ordering established off‑site and cut rate unbounded. The category stays the same while the components diverge. If the theory says "hierarchy is natural," it is not false for nested containment, but it may be false for imposed ordering. The weld was causal — just not represented.

So "hierarchy as natural" often means "We treated the label as the thing." That is a category error, not evidence that all hierarchy components move together.

#### 4. The "Language Model as Neutral" Fallacy

Many AI practitioners treat language models as neutral retrievers of facts. If the model says "rural," that is treated as a description.

But language models are structurally prone to welds. A word's representation is a summary of the contexts it occurs in. When a corpus never separates the components, nothing in training provides a gradient that would pull them apart. The weld is not learned — it is the absence of anything that would break it. If the model says "rural," it is not retrieving a fact about the world; it is reproducing a weld from its training corpus. The weld was causal — just not represented.

So "language model as neutral" often means "We treated the model's output as a fact." That is an AI safety error, not evidence that the model has separated the components.

#### 5. The "Single Number as Complete" Fallacy

Many policy analyses reduce complex phenomena to a single number. If the number moves, that is treated as a signal.

But a welded category can stay flat while components diverge. The number is not a signal; it is a silence. If the analysis treats the flat number as evidence of stability, it will miss the divergence. The weld was causal — just not represented.

So "single number as complete" often means "We treated the summary as the thing." That is a measurement error, not evidence that the components don't matter.

#### 6. The "Intent as Input" Fallacy

Many analyses of bias treat intent as relevant. If no one intended the bias, that is treated as mitigation.

But a weld's bias does not depend on intent. A term with high bias behaves the same way regardless of who is using it or why. Dropping intent is what makes the thing testable on the data alone — and it means decomposing the category works without anyone's cooperation. If the analysis says "no intent, no bias," it is not false for intent, but it may be false for the system. The bias was causal — just not dependent on intent.

So "intent as input" often means "We treated intent as relevant to measurement." That is a methodological error, not evidence that bias disappears without intent.

---

### What This Framework Does Differently

This framework treats categories as potentially welded — fusions of independent quantities that can diverge without the record moving. The following components document mechanisms that standard measurement practice typically drops:

- weld.py — The scorer: three readouts per term (n_cases, max_spread, bias). Three numbers rather than one, because case count alone cannot separate rare‑but‑enormous divergence from frequent‑but‑small divergence, and cannot separate imprecision (bias near 0) from a term that systematically hides one component behind another (bias near 1).
- The weld definition — A term is welded if: (1) at least one divergence case can be named — the components moved independently in the field — and (2) the language provides no separate handle for the components that diverged.
- The gap protocol — Cases without paired readings still count toward n_cases and are reported separately as n_unquantified. A gap is marked, not filled.
- The seed terms — "rural," "capital," and "hierarchy" — each with named divergence cases and components, awaiting quantification.

---

### The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. Whether "rural" components actually diverge in the field.
UNDER_STUDY Data collection is in progress; value is provisional. Language model weld proneness.
NOT_STUDIED The mechanism is recognized, but no measurement has ever been attempted. Environmental category welds.
UNDEFINED The variable has no agreed definition or measurement protocol. The read‑vs‑imposed criterion.

---

### What Is NOT a Valid Epistemic State

CATEGORY_AS_FACT is not a valid knowledge state. If a category fuses independent quantities, treating it as a stable handle is a measurement error, not an epistemic one. The physics does not respect our category boundaries.

The framework refuses to record a category as stable because of convention. Instead, it records the category as a candidate weld — named divergence cases, components identified, awaiting quantification — and names what would be needed to move it to a measured state.

---

### The Standard

The question should not be:

"What does the category say?"

But rather:

"What components are welded into this category, and how do they move independently in the field?"

If the answer is that components can diverge while the category stays flat, the category is welded. End of story.

The world is already interconnected. Our categories are the only things pretending otherwise. And that pretense has cost lives, money, and ecosystems on a scale that we are only beginning to understand.

This framework does not pretend otherwise.
