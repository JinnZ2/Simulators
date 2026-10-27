# Scope Audit Lab — Prototype 0.5

A preference-free, standard-library Python instrument for recording mathematical models,
their declared scope, controlled experiments, discrepancies, and unresolved questions.

**Design constraint:** this tool records evidence and relationships. It does not decide
that a model is correct, incorrect, universally valid, or invalid. A discrepancy is a
recorded observation requiring characterization, not an automatic conclusion.

## Requirements
- Python 3.10+
- Standard library only
- No network access
- No external solver required

## Quick start
```bash
python -m unittest discover -s tests -v
python -m scope_audit_lab demo --out demo_output.jsonl
python -m scope_audit_lab transitions-demo --out transitions_demo.jsonl
python -m scope_audit_lab experiments-demo --out experiments_demo.jsonl
python -m scope_audit_lab physics-demo --out physics_demo.jsonl
python -m scope_audit_lab waves-demo --out waves_demo.jsonl
python -m scope_audit_lab validate experiments_demo.jsonl
```

The demos create synthetic illustrative data, not empirical findings.

## Record types
- `model`: purpose, target quantity, declared scope, assumptions, dependencies, units, unknowns, representation, provenance.
- `experiment`: question, conditions, changed factors, control, planned comparisons, status. In 0.3 this type also carries the four instrument-level experiment payloads below.
- `observation`: predicted and observed values, uncertainty, method, conditions, residuals when calculable.
- `audit_event`: recorded evidence, unresolved questions, proposed next tests; no automatic verdict.
- `transition_scan`: one factor-variation scan — ordered cases, adjacent
  deltas, candidate transition regions, unresolved items. No boundary verdict.

Records are appended as JSON Lines. Model revisions should receive new IDs; prior observations are not overwritten. Streams written by 0.1 remain valid (schema versions 0.1 and 0.2 are both accepted; 0.3 adds no new record structure, so the schema version remains 0.2).

## Scope-transition engine (0.2)

`scope_audit_lab/transitions.py` implements the experiment engine specified at the end of
the 0.1 cycle:

1. Vary a recorded factor across cases **in the order given** — the engine never sorts.
2. Compare adjacent cases and calculate output changes (absolute and relative).
3. Record changes that exceed a declared threshold (`strictly greater than`) as
   **candidate transition regions**, with direction and factor interval.
4. Preserve missing inputs: a missing or non-finite factor/output is recorded with a
   reason — never dropped, interpolated, or replaced.
5. Zero-valued outputs: absolute change is still computed; relative change is recorded
   as undefined with the reason retained.

The engine does **not** declare that a scope boundary exists, that a model failed, or
that a transition is significant. Candidate regions are inputs to follow-up experiments.

## Experiment procedures (new in 0.3)

`scope_audit_lab/experiments.py` wraps the transition engine in four controlled,
instrument-level experiments. Each returns a payload recorded as an `experiment` record.
All use seeded generators (deterministic given the seed) and label synthetic data as
synthetic in every payload. None assigns stability, robustness, significance, or cause —
appearance counts and lists are recorded, characterization is left to separately
recorded human judgment.

1. **Null-baseline scan** (`null_baseline_scan`) — scan seeded synthetic noise with no
   planted structure; record how many candidate regions the engine reports per
   replication, and where. A null-baseline record that future real-data scans can be
   recorded alongside.
2. **Threshold sweep** (`threshold_sweep`) — scan one case set at several thresholds
   (in the order given, never sorted); record the region set per threshold and, for
   each distinct between-pair, the thresholds at which it appeared.
3. **Order-permutation probe** (`order_permutation_probe`) — scan the given order plus
   seeded permutations; record candidate-region appearances across orders. The engine's
   no-sorting contract makes order load-bearing; this probe records how much.
4. **Two-factor coupling scan** (`coupling_scan`) — scan one case set against two
   recorded factors; record coincident, factor-A-only, and factor-B-only region pairs,
   with an explicit note that coincidence does not establish a shared cause or confound.

CLI (all commands print the record JSON; `--out` also appends it to a stream):
```bash
python -m scope_audit_lab null-scan --threshold 10 --seed 7 --n-cases 12 --replications 25
python -m scope_audit_lab sweep cases.json --thresholds 1 5 10 20
python -m scope_audit_lab permute cases.json --threshold 10 --seed 3 --permutations 25
python -m scope_audit_lab couple cases2f.json --threshold 10 \
    --factor-a-label visibility --factor-b-label tide_height
python -m scope_audit_lab transitions cases.json --threshold 5 --kind absolute
```
`cases.json` is a list of `{"case_id", "factor", "output", "notes?"}`;
`cases2f.json` is a list of `{"case_id", "factor_a", "factor_b", "output", "notes?"}`.
Missing (`null`) values are recorded with reasons, never dropped.

## Law-driven physics domains (new in 0.4)

`scope_audit_lab/physics_demos.py` adds a third data category to the lab: **law-driven
simulation** — outputs computed from a stated physical law with stated parameters,
labeled in every case and payload as "law-driven simulation; synthetic, not a
measurement." Five domains, one per requested phenomenon:

| Domain | Law | Factor → output | Planted structure |
|---|---|---|---|
| `stopped_light` | EIT phenomenology v_g = cΩ²/(Ω²+Ω_K²), calibrated to 17 m/s at 1 MHz (Hau 1999; Liu 2001) | coupling Ω → group velocity | none |
| `polarized_light` | Malus: I = I₀cos²θ | analyzer angle → intensity | none |
| `em_resonance` | series RLC: I = V₀/√(R²+X(f)²) | drive frequency → current | none |
| `gravity_transect` | buried point mass: Δg = GMz/(x²+z²)^{3/2} + seeded noise | position → gravity anomaly | buried mass, declared |
| `doppler_passby` | moving source: f_obs = f₀c/(c−v_r(t)) | time → observed frequency | none |

`run_physics_demo_suite()` scans all five with the v0.2 engine, then applies four
v0.3 procedures: a Malus threshold sweep (32→24→8→0 regions as the threshold rises
10→150 — thresholds carve a smooth law, they do not find boundaries), a Doppler
order-permutation probe (given-order pairs survive at most 5 of 26 scans), a gravity
null baseline matched to the survey's noise (mean 9.6 flagged pairs on pure noise at
the survey's own threshold), and an RLC two-knob coupling scan (4 coincident pairs,
0 factor-only — coincidence recorded, cause unassigned). The EIT scan also exhibits
the metric contrast exactly: relative deltas are constant at 0.3842 across all pairs
while absolute deltas span 0.03–163 m/s.

```bash
python -m scope_audit_lab physics-demo --out physics_demo.jsonl
python -m scope_audit_lab waves-demo --out waves_demo.jsonl
```

## Waves: light as electromagnetism, sound as contrast (new in 0.5)

`scope_audit_lab/waves.py` organizes the wave domains around one recorded fact:
light's phenomena live inside electromagnetism; sound's do not. Terminology
correction carried from 0.4: the EIT phenomenon is **slow light**; "stopped
light" denotes its storage limit (Liu et al. 2001).

| Record | Law | What the engine/lab records |
|---|---|---|
| `em_unification` | c = 1/√(μ₀ε₀) (Maxwell) vs exact SI c | compare_numeric: residual −6.5×10⁻⁶ m/s, u = ±0.032 m/s, \|z\| = 2×10⁻⁴; no verdict (agreement is partly definitional structure post-2019 SI) |
| `em_spectrum` | λ = c/f, one law radio→gamma (72 pts, band labels as notes) | 23 flagged pairs at 1 m threshold — recorded as a metric artifact of absolute deltas on a geometric grid |
| `longitudinal_contrast` | I(θ) = I₀ constant (no transverse mode) | **0 flagged pairs** at the same threshold where Malus flags 24 — polarization recorded as the transverse-wave signature |
| `sound_speed` | c = √(γRT/M), ideal gas | 12 flagged pairs; medium-dependence (molar mass) noted vs light's medium-free law |

```bash
python -m scope_audit_lab waves-demo --out waves_demo.jsonl
```

## Interpretation boundary
The tool does not automatically attribute a discrepancy or a candidate transition region
to scope mismatch, measurement error, numerical error, implementation defect, omitted
dependency, invalid assumption, stochastic variation, or an unmodeled process. Those
remain candidate explanations to be tested. The 0.3 procedures extend the same boundary
to the instrument itself: what the engine flags on noise, across thresholds, and across
orderings is recorded, not judged.

## Verification status
- 90 unit tests pass (11 core + 20 transition engine + 25 experiment procedures + 21 physics domains + 13 waves).
- Test coverage includes the four behaviors mandated by the 0.2 specification:
  threshold behavior (strict `>`, absolute and relative kinds), input-order
  preservation, missing measurements, and zero-valued outputs.
- Procedure tests pin: determinism given a seed, summary/replication consistency,
  non-increasing sweep counts under sorted thresholds, threshold-order preservation,
  exact coincidence partitioning, membership preservation under permutation, and
  synthetic-data labeling.
- 0.1 record streams still validate.

## Not implemented in 0.3
Automatic transition *detection* (statistical change-point estimation), missingness-
injection stress runs, a dedicated `confound_record` type, dimensional-analysis
plugins, dependency graph algorithms, compression adapters, statistical diagnostics,
uncertainty propagation, domain-specific solvers, and cryptographic log chaining.
