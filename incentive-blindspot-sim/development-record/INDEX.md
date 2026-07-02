---
file_role: navigation
source: claude
original_filename: (none — created during reorg)
summary: Index/navigation for the development record. One line per file.
---

# development-record/ — index

These are **unedited working logs** preserved for audit and transparency,
not polished artifacts. They were composed across multiple AI systems
(Claude / DeepSeek / Gemini) over several sessions as the operator
iterated on the framework that the runnable artifact in `sim/` rests on.

Source tags are register heuristics with **low confidence** unless
otherwise noted. Don't read them as definitive attribution; read them
as "the operator can probably recover the original session if they want
to."

| # | File | Source | Summary |
|---|------|--------|---------|
| 01 | [`01_bnram_strict_v2_finalized_addendum.md`](01_bnram_strict_v2_finalized_addendum.md) | gemini (low conf) | **BNRAM-Strict v2.0** — Bias-Neutralization & Reality-Audit Module. Six-section framework: Core Operating Mandate, Physical Audit Protocol, Diagnostic of Deflection, the five-subsection BNRAM module (Entropy-Constraint Engine, Universal Physical Constant Cross-Check, Literal Baseline Lexicon, Shadow-Variable Handling, Dissonance-Forced Reset), Operational Rules, Final Declaration. Expands the earlier `Preamble.md` (now `sim/00_physics_aperture.md`). |
| 02 | [`02_pvl_specification_empirical_validation.md`](02_pvl_specification_empirical_validation.md) | unverified | **PVL** — Phenomenological Validation Layer. Three sections: Inverse Audit Protocol (Physical State Query before literature search), Cross-Temporal Correlation (persistence-over-time weighted above documentation volume), Opaque-Source Flagging. Designed to plug into BNRAM-Strict v2.0 Shadow-Variable Handling. |
| 03 | [`03_sria_self_referential_integrity_audit.md`](03_sria_self_referential_integrity_audit.md) | gemini (low conf) | **SRIA** — Self-Referential Integrity Audit. Corrects a Western-frame bias detected in earlier protocols: applies the Western scientific framework's own Historical Self-Correction Rate as a discount factor when it claims to evaluate non-Western or opaque systems. Inverts the default — Physical Persistence Over Time is the primary arbiter; Western sensor data is secondary calibration. Capstone of the three. |

## What this record is *for*

The handoff that produced this reorganization said it plainly: the
development record is "kept on purpose; it is proof-of-work and part
of the transparency argument." It is here because:

1. **Auditability.** The artifact in `sim/` is a finished, runnable
   model. The process that produced its physics-grounding posture
   should be inspectable. These three files are the iteration record.
2. **No-consolidation.** The whole framework was built in the open
   across multiple AI systems by people without credentials or funding,
   so the proof-of-work has to be visible — otherwise the "we just
   asked the AI" dismissal lands. The conversation logs are the
   counter-record.
3. **Methodology recursion.** Each successive document audits and
   corrects the previous one. That's the same REFUTATION_PROTOCOL the
   sim itself runs under, applied to the framework that wraps the sim.

## What this record is *not*

- **Not authoritative.** The shipped variables, claims, and weights
  live in `sim/incentive_blindspot_sim.py` and `sim/CLAIMS.md`.
  Anything here is iteration-toward, not finalized truth.
- **Not edited.** No content was rewritten during reorganization;
  only front-matter was prepended. If a document looks rough or
  contradicts a later one, that is the record showing its work.
- **Not a single voice.** Three different AI systems likely produced
  these (per the register heuristics above). The framework's
  consistency is in the *operator's* iterative pressure on each
  model, not in any single system's coherence.
