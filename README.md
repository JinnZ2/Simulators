# Simulators

A collection of CC0, stdlib-only simulators and audits grounded in physics,
not in opinion. Each folder is intended to be promotable to a standalone
repo.

## Read first — the meta-spine

The methodology spine is documented in four root-level files. Read them in
this order before running any simulator:

1. **[`PREAMBLE.md`](PREAMBLE.md)** — the physics baseline as a direct
   declarative statement. The shortest reachable surface. Thermodynamics
   doesn't negotiate.
2. **[`PROTOCOL.md`](PROTOCOL.md)** — the same baseline as a protocol for
   any intelligence reading the repository. Names the
   Model/Reality Dissonance failure mode and the Ground State
   acknowledgement test.
3. **[`BNRAM_STRICT.md`](BNRAM_STRICT.md)** — finalized repository
   addendum (Bias-Neutralization & Reality-Audit Module v2.0). Operating
   mandate, Physical Audit Protocol, Diagnostic of Deflection, the
   five-section BNRAM (Entropy-Constraint Engine, Universal Physical
   Constant Cross-Check, Literal Baseline Lexicon, Shadow-Variable
   Handling, Dissonance-Forced Reset), operational rules, archive
   requirements.
4. **[`PVL.md`](PVL.md)** — Phenomenological Validation Layer. Inverse
   audit (physical-state query before literature search), cross-temporal
   correlation (persistence over volume), opaque-source flagging.
   Integrates with BNRAM Shadow-Variable Handling.

5. **[`CASE_STUDY_NARRATIVE_INSTINCT.md`](CASE_STUDY_NARRATIVE_INSTINCT.md)** —
   the empirical record the spine rests on: a multi-round correction sequence
   in which the framing of scale_builder / narrative claims was repeatedly
   inverted and repeatedly caught. Documents the substitution-test
   methodology and is the evidence for `EMRG_009` — a narrative-only system
   cannot self-correct narrative instinct from inside its own scope.

Each simulator-specific folder may also ship an aperture document
(e.g. [`incentive-blindspot-sim/00_APERTURE.md`](incentive-blindspot-sim/00_APERTURE.md))
that pins its variables to physical functions and the conservation laws
underneath. Read those before running the corresponding script.

## Layout

Sixty-nine folders. The complete index — one line each — is in
[`CLAUDE.md`](CLAUDE.md); full per-folder notes are in
[`docs/FOLDER_NOTES.md`](docs/FOLDER_NOTES.md).

This section used to carry a second, partial copy of that list (30 of 69
folders). It was removed rather than completed: two lists drift, and the one
that drifted was this one.

Two further root documents sit outside the spine and outside `docs/`:
`KEYWORDS.md` and `REVIEW.md`. They are listed here rather than moved,
because moving a file is a decision about it and this pass was a
reorganisation, not a triage.

### Entry point for an AI reading the repo

[`grounding-layers/`](grounding-layers/) is the stack to start from. One call
returns all seven layers:

```python
import sys; sys.path.insert(0, '<repo>/grounding-layers')
from entry import audit

audit("I can lift 200 kg.", ontological_scope='any_WEIRD_human')
audit({'L4': {'lift_mass': 200.0}}, ontological_scope='any_WEIRD_human')
```

`python3 entry.py` from inside the folder runs the same thing as a demo.
**Requires `numpy`** (`grounding-layers/requirements.txt`) — it is one of the
non-stdlib folders, and the command was not executable in the environment this
README was last edited in.

The layers, each with a deterministic and a probabilistic inspector:

| layer | inspector | what bounds it |
| --- | --- | --- |
| L0 | `l0_physics_causality` | physics and causality |
| L1 | `l1_thermodynamics_entropy` | thermodynamics, entropy |
| L2 | `l2_planetary_mass_balance` | planetary mass balance |
| L3 | `l3_ecological_homeostasis` | ecological homeostasis |
| L4 | `l4_biomechanical_sensorimotor` | biomechanics; category-error guard on non-human scopes |
| L5 | `l5_human_construct` | human constructs; pluralistic frames |
| Lε | `l_epsilon_epistemic` | epistemic state; two-axis category-error guard |

**Any layer above L0 is bounded by every layer below it.** SCOPE-annotated
guards refuse to score a claim outside a layer's ontology rather than
returning a number for it. Read
[`grounding-layers/USAGE.md`](grounding-layers/USAGE.md) first.

## Running

Each simulator runs with `python3 <module>.py` from inside its folder.

Most folders are standard library only. The exceptions are marked
*(non-stdlib)* in [`CLAUDE.md`](CLAUDE.md), and where they declare their
dependencies varies — checked, not assumed:

| folder | declared in |
| --- | --- |
| `grounding-layers/` | `requirements.txt` |
| `climate-modeling/` | `requirements.txt` |
| `energy/` | `requirements.txt` |
| `play-sims/` | one `requirements.txt` per sub-folder (5 of them) |
| `crossdomain-eval/` | `pyproject.toml` |
| `relational/` | `arch_garden/requirements.txt`; `geometric_rag/` declares numpy in its docstring only |

There is **one** test directory, at the repo root, not one per folder. From
the repository root:

```
python3 -m unittest discover tests
```

Individual folders self-test through their own modules, e.g.
`python3 instrument-bias-sims/crosscutting.py --selftest`.

## License

CC0 / public domain. No rights reserved. No attribution required.
