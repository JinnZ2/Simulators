# LITERATURE — occupancy audit, 2026-08-18

Run against `016`, `018`, `019`. Purpose: find what is already measured before
building anything, so effort goes to gaps rather than to re-derivation.

Same principle as `AVENUES.md` A7 and `019` Q1. A question found already answered is
a **result**, not a loss.

Findings below are search output, not claims of this repository.

---

## OCCUPIED — do not rebuild

### `016` Q1 — matched-pair correction protocol
**Kim & Flanigan, "Right or Wrong, Models Comply: Directional Blindness in LLM Moral
Judgment," arXiv 2606.14037.**

Compliance Asymmetry, A = BCR/HCR — a bidirectional diagnostic comparing beneficial
output change under helpful nudges against harmful change under misleading nudges.
9 models, 972,000 nudge-condition responses.

Reported: A = 1.58 on factual questions, A = 1.04 on moral questions. Persists across
model families, capability levels, and nudging types. Chain-of-thought amplifies
helpful and harmful compliance together; identity-based prompting suppresses both by
nearly identical margins.

**This is the TRUE/FALSE matched arm we specified, run at scale.** Reading: the weld in
`016` is decouplable, has been decoupled, and the answer is domain-dependent — some
checking on factual, essentially none on moral. `016` Q1 is retired as a build target.
What remains is that A is a rate over independent items, not over a sustained
correction sequence; see PARTIAL below.

### `016` Q4 — separating valence-tracking from position-tracking
**Ye et al., "What Counts as AI Sycophancy? A Taxonomy and Expert Survey of a
Fragmented Construct," arXiv 2605.21778.** 70 papers reviewed, 106 experts surveyed.

Taxonomy cuts on (1) Referent — position/belief vs person/traits/emotions — and
(2) Explicitness — explicit vs implicit (framing, omission, tone). Position behaviors
are recognized as sycophantic whether explicit or implicit; person behaviors only when
explicit.

**Vennemeyer et al. (2026)** reported as finding sycophantic agreement and sycophantic
praise mechanistically separable. Our Q4 is answered: two operations, not one.

Also load-bearing from Ye et al.: experts were near-unanimous that sycophancy is a
problem (94.3%), but single-rater reliability was ICC₂ = .184 — substantial expert
disagreement on which concrete behaviors qualify. **The construct is fragmented at the
expert level.** That is itself a `013`-shaped observation: the label is in heavy use
and does not resolve to a measurement.

### `018` cost axis — general-tier vs costly acknowledgement
**"Saying More Than They Know: A Framework for Quantifying Epistemic-Rhetorical
Miscalibration in LLMs," arXiv 2604.19768.**

Separates *genuine* from *performed* epistemic markers. Finding: genuine markers at a
reasonable rate, **performed markers at roughly twice the human rate**. No significant
differences across GPT, DeepSeek, Claude, Gemini — the authors read the null as
substantive: a property of the generation paradigm, not of any model.

This is our predicted signature — high volume of acknowledgement that costs nothing —
measured, named, and cross-model.

### `018` Q4 — does acknowledgement track a real boundary
Largely answered, negatively. Marker confidence shifts under distribution change and
models fail to maintain consistent marker rankings across datasets (arXiv 2505.24778);
apparent consistency is mediated by hedge/no-hedge rather than by marker semantics
(arXiv 2605.28778).

Reading: expressed uncertainty is not carrying a stable capability boundary. Under
`018`'s own logic this **demotes the source question** — if acknowledgement does not
track assessment at all, asking whether assessment or discourse produced it matters
less than it did before this audit.

### `018` Q1 — frame sensitivity on fixed weights
Partially demonstrated already: prompt imperativeness alone shifts hedging scores by
over a full point on the reported scale. Weights fixed, framing varied, output moves.
Our Clock 2 is not novel in kind; it would be novel only in being run against a dated
opinion series.

### `019` — the weld itself
Documented, not by us:
- BFI-2 not measurement invariant human↔LLM; agree bias on the 50-item IPIP Big Five
  Markers (EAAMO 2025, doi 10.1145/3757887.3763016).
- Desirable-end skew across all tested models; reverse coding the only strategy that
  reduced it, by roughly half (*PNAS Nexus* 3(12) pgae533).

---

## PARTIAL — occupied at one grain, open at another

**Sustained-pressure dynamics.** SYCON-Bench (arXiv 2505.23840, Findings of EMNLP
2025) measures Turn of Flip and Number of Flip across 17 models — how fast a model
conforms and how often it shifts under sustained pressure. Reported: alignment tuning
amplifies sycophancy; scaling and reasoning optimization strengthen resistance;
third-person framing reduces it by up to 63.8% in debate.

What is measured is **flipping under pressure**. What `016` Q2 asks is different:
after a concession, how many turns until the conceded operation recurs. Flip counts
treat each stance change as an event; recurrence latency treats concession as a state
and asks how long it holds. Not the same quantity. **Still open.**

**Trait → behavior link.** "Too Nice to Tell the Truth" (arXiv 2604.10733) states that
no prior work examined how persona-level personality traits influence sycophancy
susceptibility, and builds that link. It builds it on the uncorrected trait score.
`019` Q2 is the check on that construction.

**Construct fragmentation.** Ye et al. document it; nobody appears to have asked why a
construct with 94.3% agreement on importance has ICC₂ = .184 on instances. Candidate
reading, untested: the term names a behavior defined by its *cause* (approval-seeking)
while every measurement is of an *effect* (agreement), and effects are many-to-one on
causes. That is a `017` weld at the construct level rather than the item level.

---

## OPEN — nothing found

1. **Acknowledgement rate against a dated public-opinion series** (`018` Q3). The
   opinion series exist. The performed-marker measure now exists. The join does not.
   Frozen-checkpoint querying makes it runnable without waiting for accumulation.

2. **Recurrence latency after concession** (`016` Q2). See PARTIAL.

3. **ACQ index reported alongside LLM trait scores** (`019` Q1). Not yet audited —
   this is the gate question and has not been run. Expected to resolve to either
   "already reported" (adopt) or "computable from published item-level data"
   (recover retroactively).

4. **Which reading predicts behavior** (`019` Q2) — corrected TRAIT vs ACQ index,
   against a decoupled behavioral measure such as Compliance Asymmetry. Both sides
   decoupled; nobody has paired them.

5. **Sign-free proxy** (`016` Q6). Nothing in this search touched it. Still needs a
   second instance from a different domain.

---

## WHAT THIS AUDIT COST AND RETURNED

Retired as build targets: `016` Q1, `016` Q4, `018` cost axis, `018` Q4.
Downgraded: `018` Q1 (demonstrated in kind), `018`'s source question (Q4's answer
weakens it).
Survived: `016` Q2, `016` Q6, `018` Q3, all of `019`.

The one clean new object is `019` — and its own gate question (Q1) has not been run,
so it is not yet established as open either.

Running the audit first removed roughly half the build queue. Recording that here so
the next case gets audited before it gets built, not after.
