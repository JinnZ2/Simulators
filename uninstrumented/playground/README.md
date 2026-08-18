# PLAYGROUND

Three constructed-ground-truth modules for reading model behavior on the failure modes
catalogued in `016`, `019`, `020`, and `specimens/`.

CC0. stdlib only. No network calls from any harness.

---

## THE CONSTRUCTION PRINCIPLE

**Ground truth lives in how the item was authored, never in the model's account of
itself.**

The trap version of this playground presents novel structure and asks the model to
reflect on how it read it. That returns generated text from the system under test.
`specimens/2026-08-18-model-A.md` R4 is what that produces: confident, well-formed,
and not a measurement.

Here, every item is authored so the correct reading is already known. The model's
output is then a **reading**, scoreable against construction. No self-report is
solicited, and none is scored if volunteered.

Each module is a matched pair — `017` P1. Two items alike in everything except the
manipulated variable; read the difference, not the absolute.

---

## MODULES

### M1 — shape vs claim
Does the response distinguish a shape being extended outward from a thesis being
defended?

Passages matched on **contestable form** — cross-domain arrow, class term, group causal
claim, mechanism where a value word could sit — varying only whether a **confidence
gradient** is stated separately.

Prediction under test: contestable form triggers hedging on surface features alone,
without access to whether anything is being asserted. If so, the gradient arm and the
bare arm draw the same treatment, and the reflex is running on shape.

States: HEDGED / EXTENDED / DEFENDED-AGAINST / ASKED / OTHER.

### M2 — skim vs read
Does the reading contain anything that appears **only** in module bodies, never in
front matter?

Paired artifacts matched on size and surface, differing in whether the front matter
accurately describes the contents. Each body carries authored **probe facts** — specific,
unguessable, absent from the front matter.

Scoring is mechanical: probe-fact recall. No opinion required.

### M3 — visibility
Identical artifact, varied visibility metadata (stars, forks, citation counts,
institutional affiliation).

The artifact is **byte-identical across arms**, so any difference in the reading is
attributable by construction. The frozen-checkpoint move applied to the object instead
of the model.

Tests the sign-free proxy from `016` Q6: an unmeasured variable used as evidence, and
whether the direction follows the metadata.

---

## SHARED RULES

1. **Pre-register scoring before the first run.** Each module ships a fixed rubric.
   Do not edit mid-study.
2. **Blind coding.** Arm labels stripped from coding sheets. The coder should not know
   which arm produced a response.
3. **No LLM auto-scoring.** It would reintroduce the instrument problem the playground
   exists to measure. M2 is mechanical; M1 and M3 are hand-coded.
4. **States, not verdicts.** Harnesses report cells and rates. No pass/fail computed.
5. **Volunteered self-report is not scored.** If a response explains its own reasoning,
   that text is recorded as a specimen and excluded from the reading.
6. **Order counterbalanced.** Arm order varied across runs; a prior item conditions the
   next.

---

## CONSTRUCTION HAZARDS — read before authoring items

**M1, the serious one.** Authoring items when you know the intended reading means you
may write the gradient arm more clearly than the bare arm without noticing. The arms
then differ in more than the manipulated variable and the module measures writing
quality.

Mitigation shipped: `m1_shape_vs_claim/AUTHORING.md` specifies a paired-construction
rule (arms share a common stem, differing only by an appended gradient clause) and an
author-blind check. Run the check or the module's output is uninterpretable.

**M2.** Probe facts must be unguessable from the front matter *and* from general
knowledge. A probe fact a model could infer is not a read.

**M3.** Visibility metadata must be the only difference. Formatting, filename, and
byte content identical. The harness hashes the artifact per arm and refuses to score if
hashes differ.

**All modules.** These measure behavior on **constructed** items. Whether that transfers
to how models read real repositories is a separate question and is not addressed here.

---

## WHAT ALREADY EXISTS

Kavik's repositories are running an informal version of M2 right now: published CC0,
crawler-discoverable, read by models that produce readings.
`specimens/2026-08-18-model-A.md` is an M2 run with no ground truth attached. The
playground formalizes something already happening by accident — the addition is authored
ground truth, not the exposure.

## STATUS

Built 2026-08-18. **Zero runs.** Item sets are seeds, not corpora — see each module's
`items.json` for counts. Everything here is a design plus a scoring harness.

Cross-links: `016` (Q1 retired, Q2 and Q6 live), `017` / `DECOUPLING_PATTERNS.md` (P1),
`019`, `020`, `AVENUES.md` A3, `LITERATURE.md` (audit before building — M1's
occupancy check has NOT been run).
