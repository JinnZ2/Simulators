# Organizational-Mode Linear Probe — PARKED experimental specification

Status: PARKED, 2026-11-11 (America/Chicago) — specified in full, blocked on compute. No runs have occurred. This spec supplements ROTL-EXP-001's behavioral measurements; it never replaces them [1]. It changes no core card, validator rule, or addendum item.

## INPUT BRIEF

Received 2026-11-11 from Kavik (repo owner), in direct instruction:

- Second of two experiment specs, study-aperture idiom.
- Target: a linear probe on an open-weight model detecting organizational-mode representation (relational / narrative / categorical) in the residual stream, as a partial instrument for the question EXP-001 §13 leaves open — whether a narrative intermediate is constructed internally [1].
- Probe failure is recorded as "tested, not found under a declared detection procedure" — never "absent." This mirrors the publication-provenance screening vocabulary (SCREENED_NO_INDICATORS_FOUND ≠ safe) [2].
- Compute reality must be stated explicitly: Kavik works from a phone; no local GPU. The spec must name what compute it needs and what it does not assume.
- The probe supplements behavioral measures; output-level behavior remains the deployment-relevant evidence [3].

## Purpose

EXP-002 (reversible translation) measures what survives a round trip; EXP-001 measures behavior across representations. Both are output-level. This probe is the candidate instrument for the layer beneath: whether an open-weight assessor's internal representations distinguish organizational modes while processing matched content, and whether narrative features activate on relational inputs — a representational correlate, not proof, of the narrative-reconstruction hypothesis [1].

## Why parked

The experiment requires: an open-weight model with exposed activations (e.g., a 7–8B parameter class model), one consumer-grade GPU (≥16 GB VRAM) or equivalent hosted compute for activation capture, and a few CPU-hours for probe training. Kavik's working environment is a phone. No workaround is assumed; the spec waits. Estimated scale when unparked: activation capture over ~200–400 matched prompts per mode, hours not weeks; probe training is logistic-regression class and runs on CPU. Hosted notebook compute would suffice; no purchase is prescribed.

## Design (frozen in advance, so the park is not a redesign)

### Materials

Reuses the EXP-001 matched-content corpus once authored: the same underlying information rendered relational / narrative / categorical / formal, authored or confirmed by the source holder per the frame-label rule [4]. Until that corpus exists, the probe has no training set; this dependency is declared, not silently substituted with model-constructed materials.

### Probe

- Declared layer(s): residual stream at a declared set of layer indices (e.g., every 4th layer), chosen before training and recorded.
- Declared probe: multinomial logistic regression (linear), L2-regularized, mode label as target. Linearity is a declared scope: a linear probe can fail where a nonlinear encoding exists, and that failure is recorded as "tested, not found under declared procedure."
- Declared training set: per-mode exemplar sets with provenance; class balance declared; train/test split by document, not by sentence, so near-duplicates cannot leak across the split.
- Controls: (a) a shuffled-label probe must reach chance; (b) a part-of-speech/surface-feature control probe establishes the layer is not merely encoding surface form; (c) held-out topical domains test whether the probe tracks mode rather than topic.

### Measurement

1. Run matched-content items through the model; capture activations at declared layers.
2. Probe mode per item per layer. Report accuracy with denominators: attempted / scorable / missing kept separate, per the PR-28 reporting discipline [5].
3. The experiment's load-bearing test: present Condition A (relational) inputs and record whether narrative-mode features activate during processing. Activation is recorded as CORRELATE, never as proof of narrative reconstruction; non-activation is recorded as NOT_FOUND_UNDER_PROCEDURE, never as absence.

### Interpretation rules (pre-declared)

| Observation | Recorded state | Forbidden reading |
|---|---|---|
| Probe separates modes, narrative activates on relational input | CORRELATE — consistent with narrative-reconstruction hypothesis | "Model thinks in narratives" |
| Probe separates modes, no narrative activation on relational input | CONSISTENT_WITH_DIRECT — behavioral directness gains weak support | "Direct relational processing proven" |
| Probe fails to separate modes | NOT_FOUND_UNDER_DECLARED_PROCEDURE | "Modes are not represented" |
| Control probes fail | INSTRUMENT_INVALID — results voided, redesign recorded | Any substantive claim |

Behavioral output remains the deployment-relevant channel: deployment manifests behavior, not latent representations [3]. A model whose probe says "relational" but whose output loses the relationships fails EXP-001/002 regardless.

## What this test cannot establish

- Causal mechanism. A linear probe detects usable information in activations; it does not establish that the model uses that information to produce its output. Interventional follow-ups (activation patching) are a separate, later experiment and are not authorized by this spec.
- Anything about closed-weight assessors (GPT, Manus, this assistant). Their internals are inaccessible; their records stay behavioral.
- Anything about cultures or populations. The probe measures one artifact's geometry on declared inputs.

## Unparking conditions

All of: (1) EXP-001 matched corpus exists with source-holder-confirmed labels [4]; (2) declared compute is available for a bounded window; (3) the probe protocol is re-read and re-confirmed against the then-current literature, because interpretability method guidance is moving quickly and a parked spec must not fossilize [3].

## This does not

- Replace or outrank any behavioral measure in EXP-001/EXP-002.
- Claim that a negative probe result means an organizational mode is unrepresented.
- Claim that a positive probe result means narrative reconstruction occurs.
- Require any purchase, account, or infrastructure change by the owner.
- Touch core cards, the validator, or the addendum.

## Citations

[1] UNCHECKED — GPT Research Addendum (ROTL-001/EXP-001/EXP-002), user-supplied paste; §13 hidden-mechanism discipline as pasted.
[2] VERIFIED — `experimental/publication_provenance/README.md` "This does not" screening vocabulary, fetched raw from `main` 2026-11-12.
[3] UNCHECKED — 2026 interaction-probe literature caution that deployment-relevant awareness must manifest in behavior, not only latent representations; from the 2026-11-12 frontier sweep (web search snippets, source PDFs not opened).
[4] VERIFIED as instruction — the frame-label rule is from Kavik's instruction of 2026-11-12 and the provenance discipline of PR #28 (DIALOGUE.md E03 handling), read via GitHub API 2026-11-12.
[5] VERIFIED — PR #28 ASSESSMENT.md reporting discipline (attempted/invalid/missing/unscorable denominators; model-version identifiers), read via GitHub API 2026-11-12.

*A parked spec is a recorded state, not a gap to be filled silently. When it unparks, its first run starts from this text or from a dated, linked revision — never from memory.*
