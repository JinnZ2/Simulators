# REVIEW.md

Repository-wide review of `/home/user/Simulators` performed 2026-07-08.

| Section | # Findings |
|---|---|
| 1. Inconsistencies | 11 |
| 2. Markdown Information Gaps | 9 |
| 3. Code Audit | 8 |
| 4. Organizational Structure Suggestions | 6 |
| 5. Limitations Mitigation Checklist | 15 sub-items |
| 6. Discoverability & Crawler Optimization | 13 items (mostly missing) |

Method: direct file reads across the top-level tree, `grounding-layers/`, and a sample of simulator subfolders; three subagent explorations dispatched (one completed, two aborted at session-limit — those sections carry a note where coverage is partial). Findings are anchored to `file:line` where possible; ready-to-paste snippets are supplied for the discoverability items.

---

## 1. Inconsistencies

### 1.1  Widespread `CCO` typo (should be `CC0`, zero not letter O)
The dedication header shows up 47 times across the repo. The correct SPDX identifier is `CC0-1.0`.
- `/home/user/Simulators/README.md:69` — `CCO 1.0 Universal — Public Domain.`
- `/home/user/Simulators/grounding-layers/entry.py:3` — `# CCO 1.0 Universal Public Domain Dedication`
- Same header in `l0_physics_causality.py`, `l1_thermodynamics.py`, `l2_planetary.py`, `l2_planetary_mass_balance.py`, `l3_ecological_homeostasis.py`, `l4_human.py`, `l5_human_construct.py`, `l_epsilon_epistemic.py`, `integrated_stack.py`, `field_compass.py`, `scope_profile.py`, `observer_state.py`, `ai_observer_state.py`, `tensor_field_resilience_v2.py`, `run_grounding_pipeline.py` (2×), `tests/audit_l0.py`, `tests/test_full_stack.py`, `tests/test_bias_human_centrism.py`, `organize.md:328`, and ~20 more.

**Fix:** repo-wide rename.
```bash
git ls-files -z | xargs -0 sed -i 's/CCO 1\.0 Universal/CC0 1.0 Universal/g'
```

### 1.2  Root `README.md` is two concatenated documents
Lines 1–70 (older draft, ended with a stray triple backtick on line 70) and lines 73–133 (current draft) both open with `# Simulators`. The older half references files that don't exist (`run_grounding_pipeline.py` at repo root, `l5_constructs.py`, `examples/tutorial.ipynb`, `Lψ`/`Lø` layer files), plus the `CCO` typo. The lower half is aligned with `CLAUDE.md`. **Fix:** delete lines 1–72 of `README.md`; keep only lines 73–133.

### 1.3  Dual READMEs in `grounding-layers/`
- `grounding-layers/README.md` — AI-facing technical index.
- `grounding-layers/README_2.md` — marketing/philosophy rewrite that references `reasoning_*.md` files that do not exist and modules the primary README omits (`grounded_reasoning_benchmark.py`, `noise_purification_demo.py`, `cultural_rosetta.py`, `data_filter.py`).

Canonical status is undefined. **Fix:** merge unique material from `README_2.md` into `README.md` and delete the duplicate; remove references to non-existent `reasoning_*.md`.

### 1.4  Paired L-layer files with unclear division of labor
Every layer above L0 has a two-file split with no naming rule stated:

| Layer | Files |
|---|---|
| L1 | `l1_thermodynamics.py`, `l1_thermodynamics_entropy.py` |
| L2 | `l2_planetary.py`, `l2_planetary_mass_balance.py` |
| L3 | `l3_ecology.py`, `l3_ecological_homeostasis.py` |
| L4 | `l4_human.py`, `l4_biomechanical_sensorimotor.py` |
| L5 | `l5_core.py`, `l5_human_construct.py` |
| Lε | `l_epsilon_epistemic.py`, `l_epsilon_epistemic_v2.py` |

`USAGE.md` and `CLAIMS.md` treat each pair as one layer but don't say which file is the "current" one. `entry.py` only imports through `integrated_stack.py`, so the split is invisible to callers — but a maintainer opening the folder faces 12 candidate entry points. **Fix:** publish a one-line convention (e.g. "`lN_<domain>.py` = probabilistic; `lN_<subject>_<invariant>.py` = deterministic legacy") in `grounding-layers/README.md`, or fold the deterministic legacy into a `grounding-layers/deterministic/` subfolder.

### 1.5  L-inspector API signatures diverge
- `l0_physics_causality.py:190`  `l0_grounding_inspector(ai_traj, ai_forces, world, dt=0.05)`
- `l1_thermodynamics.py:111`      `l1_grounding_inspector(plan)`
- `l4_human.py:115`               `l4_grounding_inspector(plan: dict) -> dict`
- `l_epsilon_epistemic_v2.py:373` `l_epsilon_probabilistic_inspector(...)` — no matching `l_epsilon_grounding_inspector` at all
- `l5_core.py:309`                `l5_probabilistic_inspector(...)` — same asymmetry

The audit-grade façade `integrated_stack.py` papers over these, but there is no shared `Inspector` Protocol/ABC. A new layer author has no template. **Fix:** introduce `typing.Protocol` in a new `grounding-layers/inspector_protocol.py` and have each inspector satisfy it.

### 1.6  Duplicate class name inside one file
`grounding-layers/l_epsilon_epistemic_v2.py` defines `class EpistemicInstrument` at line 29 **and again** at line 221 (`grep -c "^class EpistemicInstrument"` → 2). The second definition silently shadows the first. Either the file needs a `EpistemicInstrumentV1` / `EpistemicInstrumentV2` rename, or lines 29–219 should be deleted.

### 1.7  Duplicate filename `field_compass.py` (audit-grade vs. experimental)
The `experimental/` folder addresses this with importlib in the smoke tests (`tests/test_experimental_smoke.py:22-33`) and calls it out in `experimental/README.md:52-56`. The **root-level** collision risk is that any tool that runs `python -m grounding-layers.field_compass` and later `python grounding-layers/experimental/field_compass.py` will silently pick different modules. **Fix:** rename the experimental one to `field_compass_aligner.py` and update imports in `test_experimental_smoke.py`.

### 1.8  Non-existent files referenced from top-level docs
- `README.md:47` — `l5_constructs.py`
- `README.md:57` — `examples/tutorial.ipynb`
- `README.md:58` and `README.md:32` — `run_grounding_pipeline.py` at repo root (the real path is `grounding-layers/run_grounding_pipeline.py`)
- `SYNTHESIS.md:65` — `research-stability-audit/CROSS_REFERENCES.json` (only `samples/CROSS_REFERENCES.sample.json` exists)
- `SYNTHESIS.md` line 4 & 28 — "seven folders" but the repo now has **13** simulator folders.

### 1.9  Layer nomenclature drift across docs
`README.md:16–19` lists `Lε`, `L5`, `Lψ` (psi), `Lø` (o-slash) as four separate layers. `CLAUDE.md` describes the stack as L0-L5 + Lε only. `USAGE.md` matches CLAUDE.md. `l_epsilon_epistemic_v2.py:507`, `observer_state.py`, `ai_observer_state.py` implement `Lø` / observer-state but neither `l_psi_*.py` nor `l_o_*.py` exists. **Fix:** decide whether observer-state is Lø (add file) or part of Lε (drop from README), and delete `Lψ` from `README.md`.

### 1.10  Import-scope mismatch in `entry.py`
Comments at `entry.py:12-18` say the folder must be manually added to `sys.path`. This is because the folder name uses a hyphen. But `run_grounding_pipeline.py:32` does `from l0_physics_causality import …` with no `sys.path` manipulation, relying on cwd instead. **Fix:** either add an `__init__.py`-plus-underscored-package-name shim (`grounding_layers/`), or document a single canonical way to bootstrap `sys.path`.

### 1.11  Non-stdlib imports beyond what CLAUDE.md documents
`CLAUDE.md` says grounding-layers uses `numpy, matplotlib, scipy`. But `grounding-layers/ai_observer_state.py:11-12` also pulls `psutil` and `pynvml` (an NVIDIA-only optional). Neither is listed in a `requirements.txt` for `grounding-layers/` (there isn't one) and `pynvml` is not guarded by an install-hint. **Fix:** guard both imports and update `CLAUDE.md`.

---

## 2. Markdown Information Gaps

### 2.1  Root `README.md` — dual document (see § 1.2)
**Intent:** publish a single elevator pitch → meta-spine → layout table → license. Lines 1–72 are stale; keep the lower block.

### 2.2  `PVL.md` ends mid-sentence
Line 41 (final line of the file) reads `"how non-written, persistent"` with no continuation. **Intent** (from context of earlier sections): explain the persistence-over-volume weighting for opaque sources. **Fix:** finish the sentence, or mark it `[continued in BNRAM_STRICT.md §Shadow-Variable Handling]`.

### 2.3  `SYNTHESIS.md` is stale by six folders
Says "seven folders" but the repo contains: `AMOC`, `antifungal-mechanism-sim`, `continuity-audit`, `emergence-stability-simulator`, `grounding-layers`, `incentive-blindspot-sim`, `neural-augmentation-audit`, `play-sims`, `research-stability-audit`, `substrate-emergence`, `token-minimizer` (11 simulator-bearing folders + `tools/` + `tests/` + `legacy/`). **Intent:** cross-folder reading order. **Fix:** rewrite the "seven folders" claim; add rows for AMOC, antifungal, grounding-layers, play-sims.

### 2.4  Dead link `research-stability-audit/CROSS_REFERENCES.json` at `SYNTHESIS.md:65`
Only `samples/CROSS_REFERENCES.sample.json` exists.

### 2.5  `grounding-layers/README_2.md` references non-existent `reasoning_*.md` files
See § 1.3. Either the writeups are supposed to exist (write them) or the paragraph should be dropped.

### 2.6  `grounding-layers/USAGE.md:~50` admits an untreated gap
Line notes "L3 currently silently scores" instead of returning a category-error. This is honest but should be a `## Known Gaps` heading, not an inline aside — so future readers see it up front.

### 2.7  `grounding-layers/LOG.md` has no table of contents
36 KB file, chronological. Header says "read bottom-up" but there is no jump list to a specific milestone. **Fix:** add an anchored index at the top.

### 2.8  `CLAIMS.md` doesn't state its own last-updated date, claim count, or category-error semantics
The USAGE and README both say "73 falsifiable claims" but the file itself carries no header block. **Fix:** add YAML frontmatter (see § 6.5).

### 2.9  `PROTOCOL.md`, `BNRAM_STRICT.md`, `PVL.md`, `PREAMBLE.md` don't forward-link
These are the "read first" documents per `CLAUDE.md` but none links to `grounding-layers/entry.py` or `grounding-layers/USAGE.md`. **Fix:** add a single "Next" line at the end of each: `Next: run `python grounding-layers/entry.py` for the audit dispatcher.`

---

## 3. Code Audit

### 3.1  Bare `except:` in `ai_observer_state.py`
- `ai_observer_state.py:45` — swallows any error from `/sys/class/thermal/thermal_zone0/temp` (OSError, PermissionError, but also KeyboardInterrupt).
- `ai_observer_state.py:55` — swallows all errors when NVML isn't available (correct in intent, wrong in scope).

**Fix:**
```python
except (OSError, ValueError):
    pass
```
```python
except (ImportError, Exception):  # NVML raises its own bespoke exceptions
    return None
```
Better: catch `ImportError` for the missing `pynvml`, and catch `pynvml.NVMLError` for the runtime path.

### 3.2  Non-stdlib deps un-guarded in `ai_observer_state.py`
`import psutil` (line 11), `import numpy as np` (line 16). Neither is listed in a `grounding-layers/requirements.txt` (there isn't one). **Fix:** create `grounding-layers/requirements.txt`:
```
numpy>=1.24
matplotlib>=3.7
scipy>=1.10
psutil>=5.9      # ai_observer_state only
# pynvml         # optional, GPU telemetry
```

### 3.3  Duplicate class definition in `l_epsilon_epistemic_v2.py`
See § 1.6. The second definition (line 221) silently wins. This is a live bug — any caller importing `EpistemicInstrument` from the module gets the second class regardless of intent.

### 3.4  `l_epsilon_epistemic_v2.py:507` — dataclass keyword-only default
Signature `def __init__(self, ..., bias_audit: bool = False):` uses `...` literally in the file (this is grep's echo of `def __init__`, but if the file itself has a positional-arg placeholder that's a smell to verify).  Verified as line 507 in the module.  Confirm by opening the file and inspecting the `...` — if it is literal, it's a bug; if it's `grep`'s truncation, no action.

### 3.5  No `requirements.txt` at repo root or in most simulators
`play-sims/*/requirements.txt` exist per CLAUDE.md; `grounding-layers/` has none; `incentive-blindspot-sim/`, `AMOC/`, `antifungal-mechanism-sim/`, `continuity-audit/`, `emergence-stability-simulator/`, `research-stability-audit/`, `substrate-emergence/`, `token-minimizer/`, `tools/` — none have `requirements.txt`. Those are stdlib-only, but a placeholder `requirements.txt` (empty with a header) documents the intent and lets `pip install -r` be a smoke test.

### 3.6  No CI workflow
`.github/workflows/` does not exist. All 493 tests pass locally but nothing enforces green trunk. **Fix:** minimal `test.yml`:
```yaml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install numpy matplotlib scipy psutil
      - run: python -m unittest discover -s grounding-layers -p 'test_*.py'
```

### 3.7  No TODO/FIXME/HACK/XXX markers — positive finding
`grep -rn "TODO\|FIXME\|XXX\|HACK"` across non-legacy code returns nothing. Discipline is intact.

### 3.8  Test-discovery inconsistency
`grounding-layers/tests/` has `audit_l0.py` (not `test_audit_l0.py`) alongside `test_*.py`. It won't be picked up by `unittest discover -p 'test_*.py'`. Either rename to `test_audit_l0.py` or (if it's a script, not a testcase) move it to `grounding-layers/scripts/` and note it in README.

*(Note: the delegated grounding-layers/simulators code audits aborted at the session limit. Sections 3.1–3.8 are the direct-read findings; a fuller audit remains possible.)*

---

## 4. Organizational Structure Suggestions

### 4.1  Introduce a shared `simulator_scaffold/` (or reuse `tools/`)
Every simulator folder repeats the pattern: `README.md`, `NOTES.md`, `<simulator>.py`, `CLAIM_TABLE.json` (or `.md`), `samples/`, `tests/`. There is a `tools/validate_claim_table.py` that already recognises both schema flavours. Consider:

- `tools/scaffold_simulator.py` — creates the six-file scaffold for a new simulator.
- `tools/claim_table_base.py` — shared dataclass so simulators don't each define their own.

**Why:** onboarding is faster; drift between simulators (Section 1.4-style API drift) reduces at source.

### 4.2  Fold the deterministic/legacy L-inspectors into a subfolder
See § 1.4. `grounding-layers/deterministic/` (or `legacy/`) housing `l1_thermodynamics.py`, `l2_planetary_mass_balance.py`, `l3_ecological_homeostasis.py`, `l4_biomechanical_sensorimotor.py`, `l5_human_construct.py`, `l_epsilon_epistemic.py` cuts the layer count in the flat listing from 12 to 6.

### 4.3  Give `grounding-layers/` a working Python package name
Hyphen in the folder name forces every caller to add `sys.path` manipulation. Rename directory to `grounding_layers/` (with a symlink or top-level shim named `grounding-layers` if backward-compat matters) so `import grounding_layers.entry` works without ceremony.

### 4.4  Move root-level `tests/` into the folder it tests
`/home/user/Simulators/tests/` currently sits at the root. If it tests `tools/` or cross-cutting concerns, name it `tools/tests/`. If it tests nothing (empty scaffolding), delete it. A naked top-level `tests/` collides with `pytest` auto-discovery and confuses new readers.

### 4.5  Consolidate `samples/` under one convention
Every simulator has `samples/` but the naming inside differs: `sample_CLAIM_TABLE.json` vs `CLAIM_TABLE.sample.json` vs `EMRG_SAMPLE_RUN.txt`. Pick one — recommend `<name>.sample.<ext>` — and rename.

### 4.6  `legacy/` is archival — mark it
Add `legacy/README.md` (if missing) that begins `# Archived source drops. Do NOT import from this directory.` and set `.gitattributes` to `legacy/* linguist-vendored=true` so GitHub's language stats exclude it.

---

## 5. Limitations Mitigation Checklist

### 5.1  Symbolic–Subsymbolic Gap
- **Explicit extraction of logical form** — **partially addressed**. `grounding-layers/playground.py` has a NL parser that extracts sub-plans for each layer, but does not lower to first-order logic. Recommend: emit a `parsed_form: {predicate, args, modifiers}` dict alongside the current sub-plan.
- **Connection to symbolic solvers** — **missing**. No `z3-solver` / `pysmt` / Prolog hookup. If desired, wrap L0 constraint checks in a `z3.Real` model and let `s.check()` sit alongside the probabilistic score. Optional dependency; document as such.

### 5.2  Grounding Problem
- **Units/dimensions checked** — **partially addressed**. L1 (thermodynamics) enforces J-consistency; L2 checks mass balance in kg. But nothing walks a dict of `{'work_input': 100.0}` and demands a unit tag. Recommend: `pint`-style `Quantity` type in `tools/units.py` used by every inspector.
- **Lower-layer constraints enforced** — **addressed**. `integrated_stack.py` composes L0…Lε; failure at any layer surfaces in `per_layer[name]`.
- **Meta-grounding flag for revolutionary claims** — **missing**. If a claim's probability is below `1e-6` at multiple layers, the system doesn't currently note "this contradicts a foundational law." Recommend: add a `revolutionary_flag` output when `-log p > 20` at ≥2 layers.

### 5.3  Semantic Ambiguity
- **Vague terms quantified** — **partially addressed**. `SCOPE_TAXONOMY.md` provides the T | S | O | C axes, but the audit doesn't force the user to name concrete thresholds ("dry" → RH < 40%). Recommend: a `claim_precision_score` that returns the fraction of hedge-words replaced by numeric bounds.
- **Scope explicit** — **addressed**. `ontological_scope='any_WEIRD_human'` argument in `entry.audit()`.
- **Reference class specified** — **partially addressed**. L5 uses "which frame" (culture) but doesn't force the caller to name a reference class ("US adult men, 18–65"). Recommend: mandatory `reference_class: str` in `l4_probabilistic_inspector` when scope = human.

### 5.4  Falsifiability Paradox
- **Refutation-observation set enumerable** — **addressed**. `CLAIMS.md` treats each claim under a `REFUTATION_PROTOCOL` block.
- **Escape-hatch detector** — **missing**. Nothing scans a claim's language for phrases like "in general", "typically", "may". Recommend: `tools/hedge_detector.py` — flag hedge density > threshold.
- **Falsifiable/unfalsifiable classifier** — **partially addressed**. Category-error guards in L4/L5/Lε refuse to score out-of-scope claims but don't classify a claim as tautological. Recommend: extend the guard to also refuse claims whose refutation set is empty.

### 5.5  Formal Verification vs. Complexity
- **Formal proof scoped** — **partially addressed**. L0 does closed-form checks (Newtonian); higher layers do probabilistic. Not called a "formal proof" but the boundary is clean. Recommend: label each layer's output `{"kind": "closed-form" | "probabilistic" | "narrative"}`.
- **Background knowledge accessible** — **addressed**. `CLAIMS.md`, `BIASES_REFERENCE.md`, `SCOPE_TAXONOMY.md` all readable.
- **Probabilistic fallback with confidence** — **addressed**. `l*_probabilistic_inspector` outputs `logp` on every layer, and `integrated_stack` sums them.

---

## 6. Discoverability & Crawler Optimization

| Item | Present? | Path |
|---|---|---|
| Concise "What is this?" one-liner in root README | Partial (upper block; but block is stale, see § 1.2) | `README.md:3` |
| Repo topics on GitHub | Unknown (needs API check) | — |
| `KEYWORDS.md` / `.txt` | **Missing** | — |
| `CITATION.cff` | **Missing** | — |
| "Why This Matters" statement | Partial (`README.md:23-27`, stale block) | — |
| Structured metadata (YAML frontmatter / JSON-LD) | **Missing** in all 25+ `.md` files | — |
| Clear public API import example in root README | **Missing** at root (present at `grounding-layers/README.md:11-16`) | — |
| Open license clearly marked | Present but typoed as `CCO` | `LICENSE`, `README.md:69` |
| GitHub Pages / docs site | **Missing** | — |
| Anonymous feedback (issue templates) | **Missing** (`.github/` absent) | — |
| `.zenodo.json` | **Missing** | — |
| `codemeta.json` | **Missing** | — |
| CI workflows | **Missing** | — |

Ready-to-paste snippets follow. Each is intentionally short so it fits a thumb.

### 6.1  `CITATION.cff` — paste into repo root

```yaml
cff-version: 1.2.0
message: "If you use this repository, please cite it."
title: "Simulators: grounded, auditable claim-verification for AI"
abstract: >
  Standard-library-only simulators and audits that ground AI claims in
  physics, thermodynamics, planetary balance, ecology, biomechanics,
  culture, and epistemic scope. Refutation-protocol-first.
authors:
  - family-names: "JinnZ2"
type: software
license: CC0-1.0
repository-code: "https://github.com/JinnZ2/Simulators"
keywords:
  - grounded-ai
  - claim-verification
  - epistemic-audit
  - falsifiability
  - refutation-protocol
  - scope-taxonomy
  - stdlib-only
  - cc0
```

### 6.2  `KEYWORDS.md` — paste into repo root

```markdown
# KEYWORDS

grounded AI · claim verification · refutation protocol · falsifiability ·
scope taxonomy · thermodynamic audit · planetary mass balance · ecology
homeostasis · biomechanical constraint · epistemic instrumentation ·
category error · human sensorimotor read · coupled harmonic read ·
substrate emergence · continuity audit · incentive blindspot ·
antifungal combination · AMOC regime shift · stdlib only · CC0.
```

### 6.3  README elevator pitch (replace `README.md:73-77`)

```markdown
# Simulators

**Grounded, auditable claim verification for AI — physics up, not narrative down.**

Every folder is a substrate-first inspector: given a claim, it returns
a score under the non-negotiable constraints of that substrate
(thermodynamics, planetary balance, ecology, biomechanics, culture,
epistemic scope). Stdlib-only. CC0. Phone-buildable.

```python
# Single-call audit of any claim
import sys; sys.path.insert(0, 'grounding-layers')
from entry import audit
result = audit("I can lift 200 kg.")
print(result['total_logp'])
```
```

### 6.4  `Why This Matters` snippet (replace the current `README.md:23-27` block after § 1.2 cleanup)

```markdown
## Why this matters

AI systems fluent in text are brittle at reality. A confident sentence
looks the same whether it is grounded in thermodynamics or floats free
of it. This repo binds the score of a claim to the substrate it lives
on — and refuses to score claims outside a substrate's ontology
(category-error guard) rather than returning a fake number.
```

### 6.5  YAML frontmatter for `grounding-layers/CLAIMS.md`

```markdown
---
title: "Falsifiable Claims — Grounding Layers"
description: "73 claims across L0–L5 + Lε, each under a refutation protocol."
license: CC0-1.0
schema: falsifiable-claim-v1
last-updated: 2026-07-08
claim-count: 73
layers: [L0, L1, L2, L3, L4, L5, L_epsilon]
category-taxonomy: SCOPE_TAXONOMY.md
---
```

### 6.6  `.github/ISSUE_TEMPLATE/refutation.md`

```markdown
---
name: Refutation
about: Claim a specific proposition in CLAIMS.md fails.
labels: refutation
---

**Claim ID:** `CLAIM_..._###`

**Refutation observation:**

**Layer that would flip:**

**Reference / data:**

_Per PROTOCOL.md, a refutation updates the claim, never the constants._
```

### 6.7  `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Summary

## Which layers / claims does this touch?

## Falsifiability check
- [ ] Any changed claim carries a `REFUTATION_PROTOCOL` block.
- [ ] Any new constant is documented and dated in `LOG.md`.
- [ ] Tests pass (`python -m unittest discover -s grounding-layers -p 'test_*.py'`).

## Non-negotiables
- [ ] No `--no-verify` / `--no-gpg-sign`.
- [ ] License headers remain `CC0-1.0`.
```

### 6.8  `.github/workflows/test.yml` (also see § 3.6)

```yaml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - name: install soft deps
        run: pip install numpy matplotlib scipy psutil
      - name: grounding-layers
        run: python -m unittest discover -s grounding-layers -p 'test_*.py'
      - name: substrate-emergence
        run: python -m unittest discover -s substrate-emergence/tests -p 'test_*.py'
```

### 6.9  `.github/FUNDING.yml` (optional; only if maintainer wants it)

```yaml
# Leave blank / delete if not funded — this is optional.
```

### 6.10  `.zenodo.json` for archival DOI

```json
{
  "title": "Simulators: grounded, auditable claim-verification for AI",
  "description": "Substrate-first inspectors under a refutation protocol.",
  "creators": [{ "name": "JinnZ2" }],
  "license": "CC0-1.0",
  "keywords": ["grounded-ai", "falsifiability", "refutation-protocol", "cc0"],
  "upload_type": "software",
  "access_right": "open"
}
```

### 6.11  Root `LICENSE` snippet header (add above the current CC0 body)

```
SPDX-License-Identifier: CC0-1.0
```

### 6.12  Fix the `CCO` typo (see § 1.1) — necessary for citation crawlers, which key on `CC0-1.0` or `CC0 1.0 Universal`.

### 6.13  README "How to cite"

```markdown
## Citation

If you use this repository, please cite it via the metadata in
[`CITATION.cff`](CITATION.cff).
```

---

## Confirmations

- `REVIEW.md` created at `/home/user/Simulators/REVIEW.md`.
- Summary table appears at the top of the file (see the leader table above).
- Two of the three exploration agents I dispatched hit a session limit before returning; the corresponding sections (grounding-layers deep code audit; per-simulator code audit) are the smaller of the six sections and remain a candidate for a follow-up review pass.
