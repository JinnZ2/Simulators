# ICSC

ICSC: Implicit Communication and Substrate Coupling. This folder holds the v0.1 specification audit,
landed verbatim under FINDER FOLLOW-UP item B, 2026-11-09. STATUS: PROPOSED. Nothing is built.

- `SPEC_AUDIT_v0.1.pdf` -- the delivered bytes.
- `SPEC_AUDIT_v0.1.md` -- the markdown source, verbatim as delivered (arrived after the PDF).
- `SPEC_AUDIT_v0.1.pdftotext.md` -- `pdftotext -layout` text of the PDF in one fence, with sha256 and
  provenance in the header; the stand-in used before the source arrived.
- `check_landing.py` -- re-extracts the PDF, confirms the fenced text is unchanged, and confirms the
  source and the PDF carry the same 2612-word sequence.

Note 2026-11-09: the source arrived; the stand-in moved from `SPEC_AUDIT_v0.1.md` to
`SPEC_AUDIT_v0.1.pdftotext.md`, content unchanged.

The audit's own sections are F (nine specification defects), A (corrected architecture),
B (acceptance tests T01-T20), C (confounders), D (assumptions), E (indistinguishable cases),
G (proposed acceptance contract) and an Open list. None of that content is restated here.

Cross-references, recorded and not built:
- Amendment A2 names Cross-Domain-Toolkit `falsification_ledger/` as the lock layer for the ICSC manifest
  (the audit's "lock + hash manifest before first run", section G, and T15 epoch lock).
- TOOL_FINDER NAME_COLLISION: ICSC's `functional_selection` axis vs Simulators `encoding-selection/`.

## Tested (append-only; never overwrite an older line)
tested: 2026-11-09 | model: WITHHELD (session rule: no model identifier is written into a pushed artifact; the operator holds it) | Claude Code, cloud session (claude.ai/code) | check_landing.py 3/3
tested: 2026-11-09 | commit 98ecd8f | Claude Code, cloud session (claude.ai/code) | model: see trailer | check_landing.py 3/3
tested: 2026-11-09 | commit 2982077 | Claude Code, cloud session (claude.ai/code) | model: see trailer | check_landing.py 4/4 (source landed; plant of one changed word fails check 4)
