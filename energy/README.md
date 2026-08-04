# energy

Dark-energy simulation drop: coupled-quintessence sweeps, a
223-cosmology playground, and a five-module metrology stack that
audits whether the failure lives in the mathematics, the
formulation, the instrument, or the equipment.

Non-stdlib (`numpy`, `scipy`) — see `requirements.txt`. Same
exemption as `play-sims/` and `climate-modeling/`. `pysr` optional;
the generative module falls back to a numpy basis library when it
is absent, and every module ships a runnable `__main__` demo.

## Layout

```
energy/
  Coupled_Quintessence_Geometry_Report.pdf   flagship report (v2, Aug 2026)
  sweeps/                                    three parameter-sweep CSVs
  modules/                                   five-module metrology stack + iter-6 driver
  app/                                       browser playground (index.html + JSON payload)
  figures/                                   plots + manifold-graph JSONL payload
  samples/                                   captured end-to-end output
  requirements.txt                           numpy + scipy
```

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
playground. Modules are MIT-licensed (see per-file headers); the
report and sweeps are the working artifacts of that investigation.
