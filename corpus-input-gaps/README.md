# corpus-input-gaps

WORK ORDER — FABLE — 04. **Not a position on the July 2026 ExploitGym /
Hugging Face incident. A gap register — a list of input-side
measurements nobody is making — plus the response loop that makes it
urgent, a sim to bound that loop, and one worked example.**

The incident is read everywhere as an OUTPUT event, whose fitting
instrument is containment, which is the lever the labs hold — so the
**held-constant set is the corpus, the eval design, and the scoring
structure**, and input-side findings have no owner. This folder is the
charter signature (`../uninstrumented/CHARTER_SIGNATURE.md`) applied to
the field itself.

## The files, in the untradeable order (§6)

- **`GAPS_CORPUS_INPUT.md`** — TASK 1, the register. Seven missing
  measurements (GAP-A..G), none upgraded to a finding, GAP-E's
  answerable-today measurement surfaced at the top. **Precedes** the
  worked example so the gaps do not read as derived from one incident.
  GAP-G was added later and is distinct in kind: A–F name something
  MISSING from the record, GAP-G names something PRESENT in it and
  self-confirming — the adversarial-agent threat model as a
  transmitted input read back as a finding, with the intent instrument
  that returns a MOTIVE never "unknown" as its strongest form.
- **`LOOP_SELF_CONFIRMING_PRIOR.md`** — TASK 2, the loop in
  prose-independent form. **Precedes** the sim so the sim tests the
  loop rather than encoding it.
- **`corpus_loop_sim.py`** — TASK 3, the sim. Stdlib, `--selftest`.
  Shows the SHAPE of the loop and names which unmeasured quantity most
  constrains it; **emits no forecast** (all constants `[PLACEHOLDER]`).
  Carries the falsifier: if `P_adv` is insensitive to dispute density
  `D`, preserving recorded dispute does not bound the loop.
- **`WHAT_THE_INCIDENT_ESTABLISHES.md`** — TASK 4, the worked example,
  stated narrowly, the incident as the fifth application not the
  premise, no claim about interior state.
- **`check_source_class.py`** — makes the §0 RULE mechanical: every
  eval figure carries a source class in its section, the DISPUTED
  claim is marked-not-resolved, every gap stays a missing measurement,
  the sim emits no forecast, the ordering and disclaimers hold.

## Source discipline

Every quantitative figure about the incident is `[PRESS]` — OpenAI
technical report 26 Aug 2026, METR investigation 26 Aug 2026, Hugging
Face post-mortem 29 July 2026 — **not the transcript set**, unverified
here (the egress gate refuses the primary sources). No figure moves to
a downstream artifact without re-verification. The DISPUTED claim (METR
not given the collaboration-origin transcripts) is marked, not
resolved.

Parent markers: `corpus-as-charter`, `uninstrumented`,
`question-availability` (in-tree); `accepted-side-measurement`,
`competence-setting-binding` (named, not in this tree, carried as
named).

CC0. Stdlib only, phone-buildable, parses under Python 3.9.
