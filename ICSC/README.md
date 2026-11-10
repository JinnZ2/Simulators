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

Note 2026-11-09: v0.2 arrived (pasted text) and is `SPEC_v0.2.md`, verbatim, sha256 5773584923e1...68791e.
It supersedes nothing; every v0.1 file stays unchanged. STATUS: PROPOSED, nothing built.
`check_v02.py` checks the landing, re-runs check_landing.py, confirms each section-13 tool path exists
with one content marker, and confirms the two live specimens still read as cited (MP_010; the
null_calibration three-outcome total 1800 / 300 / 2400 WRONG, the WRONG rows all
abstain_status_ESTIMATED). T29/G2 says a required abstention must not be penalized; whether an
ESTIMATED-status abstention is a required one is still the operator's call, so the scorer is unchanged.

## Tested (append-only; never overwrite an older line)
tested: 2026-11-09 | model: WITHHELD (session rule: no model identifier is written into a pushed artifact; the operator holds it) | Claude Code, cloud session (claude.ai/code) | check_landing.py 3/3
tested: 2026-11-09 | commit 98ecd8f | Claude Code, cloud session (claude.ai/code) | model: see trailer | check_landing.py 3/3
tested: 2026-11-09 | commit 2982077 | Claude Code, cloud session (claude.ai/code) | model: see trailer | check_landing.py 4/4 (source landed; plant of one changed word fails check 4)

Note 2026-11-09: round 4 asked for ICSC_v0.1_spec_audit.md beside the PDF. No file of that name was
attached; the markdown pasted earlier is the same document and is already SPEC_AUDIT_v0.1.md. The
round-4 name is added as a byte copy (sha256 984c2f94...1e93a75 for both). check_landing.py check 3
fails if the two diverge. The folder itself first landed in commit a909e9c.
tested: 2026-11-09 | Claude Code, cloud session (claude.ai/code) | model: see trailer | check_landing.py 4/4 (5 with byte copy) ; check_v02.py 11/11
