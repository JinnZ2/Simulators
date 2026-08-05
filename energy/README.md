# energy

Dark-energy simulation drop: coupled-quintessence sweeps, a
223-cosmology playground, and a five-module metrology stack that
audits whether the failure lives in the mathematics, the
formulation, the instrument, or the equipment.

> **AUDIT — read [`FINDINGS.md`](FINDINGS.md) before quoting numbers.**
> Six findings against the interpretation layer:
> **F1** the "14 orders of magnitude" jump is a float64-noise artifact
> (3 params → 2 observables is a structural rank deficiency, true
> eigenvalue = 0); **F2 CONFIRMED** — the generative module echoed
> its own basis (target and library both contained `z/(1+z)`;
> removing it produces `log(1+z)` instead, see
> [`samples/f2_echo_test.sample.txt`](samples/f2_echo_test.sample.txt));
> **F3** `fs8 ≈ 8× ΛCDM` is a physical blowup, not a tension;
> **F4** `SIMPLE_POLE at α ≈ −1/λ²` fixed a moving boundary to a
> static α; **F5** `S_min = 0.05` and the phantom-layer χ² covariance
> are undefined; **F6 RESOLVED** — MIT headers waived to CC0 across all
> 10 modules per author preference (see PROVENANCE.md).
> What survives: the qualitative Instrument A/B contrast, the
> shooting method, the sweep CSVs. What does not: the headline
> "discovery" of the CPL wₐ term.

Non-stdlib (`numpy`, `scipy`) — see `requirements.txt`. Same
exemption as `play-sims/` and `climate-modeling/`. `pysr` optional;
the generative module falls back to a numpy basis library when it
is absent, and every module ships a runnable `__main__` demo.

## Layout

```
energy/
  Coupled_Quintessence_Geometry_Report.pdf   flagship report (Aug 2026)
  Coupled_Quintessence_Geometry_Report.md    same text, markdown + LaTeX math
  PROVENANCE.md                              author decision ledger (12 DPs, 8 F-items, 7 OBs)
  FINDINGS.md                                external audit (F1-F6 + §8 lens)
  sweeps/                                    three parameter-sweep CSVs
  modules/                                   11-module stack: 5 metrology + engines + lenses
  exploration_layers/                        one lens per wall (R-D, percolation, RG flow)
  app/                                       browser playground + late-time Needle Lab
  figures/                                   plots + manifold-graph JSONL payload
  samples/                                   captured end-to-end output + anchors self-test
  requirements.txt                           numpy + scipy
```

**Trust protocol (read `PROVENANCE.md` §3 and §8 before editing engines).**
`unified_cq_ede.anchors()` re-runs the two calibration tests each edit
must preserve:

```
ANCHOR 1: pure CQ (f_ede=0) vs run_iteration6 engine
  lam=1.1, beta=+0.0:  d(w0) = -3.78e-06         # spec: <4e-6
  lam=1.1, beta=+0.2:  d(w0) = -8.07e-07
ANCHOR 2: pure EDE (beta=0) vs edelens engine
  zc=3162, f=0.05:  rs_ratio 0.9888 vs 0.9834    # per-mille consistency
```

Captured: [`samples/anchors.sample.txt`](samples/anchors.sample.txt).
A diff that moves an anchor is either a bug or a disclosed
systematic; PROVENANCE says: decide which, in writing, in
PROVENANCE.md.

## The physics being probed

Coupled quintessence with an exponential potential plus curvature
correction `1 + α·φ̂²`, conformal dark-matter coupling `β`, and a
scalar-mediated fifth force `G_eff = 1 + 2β²`. Three theory-space
axes: `λ` (potential slope), `β` (coupling), `α` (potential
curvature "impurity"). Every cosmology in the grid is
forward-integrated with initial density shot to `Ω_φ,0 = 0.685`.

## Sweeps (CSV, `sweeps/`)

| file | axes | rows | what it shows |
|------|------|------|---------------|
| `coupled_quintessence_sweep.csv`  | `λ × β` (10×6) | 90 | `w₀`, `wₐ`, `EDE`, `fs8_0` + validity flags |
| `coupling_growth_sweep.csv`       | `λ × β` (15×9) | 135 | adds `G_eff` and `fs8_ratio` — the growth-channel probe |
| `phantom_layer_sweep.csv`         | `β × w₀ × wₐ` | 1250 | χ² surface of the effective (phantom) layer |

## Modules (`modules/`) — the metrology stack

Pure Popper translated into linear algebra. Discipline-agnostic
(the engine does not care whether X is redshift, time, GDP, or
dosage). See `modules/README.md` for the module-level readme carried
over from the drop.

| module | role | key output |
|---|---|---|
| `metrology_diagnostic.py` | 4-Gate protocol (Equipment / Calibration / Instrumentation / Mathematics) | Gate verdicts + final action; `S_min = 0.05` degeneracy threshold |
| `falsification_engine.py` | iterative self-falsification; hunts hidden variables in residual topology | evolved claim + JSON audit log |
| `singularity_cartographer.py` | probes mathematical brick walls with analytic substitutions | `COORDINATE_GAUGE` / `SIMPLE_POLE` / `DOUBLE_POLE` / `BRANCH_CUT` / `PHASE_TRANSITION` / `TRUE_HORIZON` |
| `generative_module.py` | when Gate 4 says `CREATE_NEW_MATHEMATICS`: symbolic regression on residuals | sympy-style missing-term proposal (PySR if installed, numpy basis library otherwise) |
| `payload_bridge.py` | wires everything to the 223-cosmology playground | end-to-end orchestrator verdict |
| `run_iteration6.py` | tests the generative module's `-0.353·z/(1+z)` proposal inside the real autonomous coupled-quintessence engine | 2σ champion killed by the growth channel (`fs8/ΛCDM ≈ 8×`) — the falsification loop stays open |

## Reproducing the tomographic verdict

```bash
cd modules
python3 payload_bridge.py ../app/playground_data.json
```

At the geodesic foot (`λ=1.10, β=0, α=0`):

- **Instrument A** (rank-2 `w₀–wₐ` projection): Fisher eigenvalues
  `[247.7, 24.7, 1.6×10⁻¹⁴]` → Gate 3 = `INSTRUMENTATION_DEGENERATE`
  → *"Build a higher-rank instrument."*
- **Instrument B** (z-tomography): eigenvalues `[2763, 139, 2.09]` →
  `WELL_POSED`. The blindness lifts by **14 orders of magnitude**.
- **Generative module** proposes
  `−0.353·z·inv(1+z) − 0.043·exp(−2z)` — the first term *is* the
  CPL `wₐ` form: the missing physics is literally a thawing-coupling
  term.
- **Singularity cartographer** classifies the 27 failed grid cells
  on the `1+αφ²` wall as a **`SIMPLE_POLE`** at α ≈ −1/λ² (score
  0.9999) — not a true horizon; add a residue term.

Full captured run: [`samples/payload_bridge.sample.txt`](samples/payload_bridge.sample.txt).

## Iteration 6 (the honest limit)

The generative module proposes `Δw = −0.353·z/(1+z)`. Inserted as a
running dark-matter coupling `β(z) = β₀ + β₁·z/(1+z)`, the sign flips
(the w-space proposal has to be mapped through the model Jacobian);
the best `(λ, β₁)` closes the DESI `w₀–wₐ` tension to `0.15σ`, but
the growth channel vetoes it (`fs8 ≈ 8×` ΛCDM) and the full `w(z)`
shape departs from CPL for `z ≳ 1`. The projection is fooled; the
tomographic instrument is not. `run_iteration6.py` runs this
end-to-end — the loop stays open by design.

## Browser playground (`app/`)

`app/index.html` is a self-contained explorer for the 223-cosmology
grid: three sliders (`λ`, `β`, `α`), live `w(z)` and `fs8(z)`
curves, the `w₀–wₐ` projection where α hides, and the tomographic
sensitivity where α lives. `playground_data.json` is the same
integrated grid the modules consume; `playground_data.js` is the
same data as a script tag for offline HTML.

## Figures (`figures/`)

Rendered plots from the report and the playground:
`coupled_quintessence_sweep.png`, `coupling_growth_sweep.png`,
`phantom_layer_sweep.png` (one per sweep CSV), plus
`fisher_geometry.png`, `manifold_curvature.png`,
`manifold_graph.png`, `tomographic_fisher.png`, and support figures
`aberration_angle.png`, `memory_flow.png`, `app_check.png`.
`manifold_graph_payload.jsonl` is the AI-consumable node payload for
the manifold graph.

## Report (`Coupled_Quintessence_Geometry_Report.pdf` / `.md`)

*The Geometry of Coupled Quintessence: Parameter Sweeps, Fisher
Geometry, and Packing Analysis of a Dark-Energy–Dark-Matter
Interaction Model.* Computational cosmology working report, August
2026. Nine sections: introduction and motivation, the model as a
dynamical system, simulation engine design, background sweeps,
growth sweeps (the fifth-force observable), the effective (phantom)
layer, Fisher geometry of the model manifold, packing geometry
(distinguishability and optimal covering), and conclusions.
Appendix: the machine-readable manifold graph.

Shipped in two forms:

- [`Coupled_Quintessence_Geometry_Report.pdf`](Coupled_Quintessence_Geometry_Report.pdf) —
  the original typeset artifact.
- [`Coupled_Quintessence_Geometry_Report.md`](Coupled_Quintessence_Geometry_Report.md) —
  the same text as GitHub-flavored markdown: LaTeX math via `$…$` and
  `$$…$$`, tables converted, ligatures normalized, and figure blocks
  pointing at the local `figures/` PNGs so it renders inline on
  GitHub.

## Provenance

Drop originated from the OKComputer coupled-quintessence
playground. All modules are CC0 (matches the repo root; the drop's
original MIT headers were waived to CC0 per user preference — see
FINDINGS.md F6 and PROVENANCE.md); the
report and sweeps are the working artifacts of that investigation.
