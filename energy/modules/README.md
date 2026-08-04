# Metrology Add-On Modules

A minimal, discipline-agnostic audit stack for any AI — and for the
coupled-quintessence playground it grew out of. Pure Popper, translated
into linear algebra. Runs on a phone (Termux): only numpy + scipy required.

## The stack

| Module | Role | Key output |
|---|---|---|
| `metrology_diagnostic.py` | 4-Gate protocol: Equipment / Calibration / Instrumentation / Mathematics | Gate verdicts + final action; the S_min degeneracy threshold (0.05) |
| `falsification_engine.py` | Iterative self-falsification of a claim; hunts hidden variables in residual topology | Evolved claim + JSON audit log |
| `singularity_cartographer.py` | Probes mathematical brick walls with analytic substitutions | COORDINATE_GAUGE / SIMPLE_POLE / DOUBLE_POLE / BRANCH_CUT / PHASE_TRANSITION / TRUE_HORIZON |
| `generative_module.py` | When Gate 4 says CREATE_NEW_MATHEMATICS: symbolic regression on residuals | Sympy-style missing-term proposal (PySR if installed, numpy basis-library fallback otherwise) |
| `payload_bridge.py` | Wires everything to the playground's 223 integrated cosmologies | End-to-end orchestrator verdict |
| `run_iteration6.py` | Real-engine test of the generative proposal: running coupling β(z)=β₀+β₁·z/(1+z) | Projection closes (0.15σ) but growth vetoes (fσ₈ ≈ 8×ΛCDM) — instrument A fooled, tomography not |
| `theory_space_lenses.py` | Three-lens scan of the (β₀,β₁) plane: R-D dynamics / percolation topology / Fisher curvature | UNIVERSAL PATHOLOGY: growth kink, graph fragmentation peak (8.75σ) and rank collapse all at β₁≈0.2–0.3 |
| `edelens.py` | Early Dark Energy polarity-flip control: KG thawing + w=1/3 fluid, shot to f_EDE | No universal pathology — smooth growth crater, healthy Fisher rank; data-space bottleneck, not theory-space |
| `overlap_lens.py` | Bridge between CQ and EDE manifolds in the common (σ₈, H₀) plane | Closest pair 0.46σ at the ΛCDM anchor; ambiguity band (5/40 EDE points within 1σ); holographic-cancellation pair finder |
| `late_trigger_lens.py` | Free w_DE(a) = CPL + smooth kink at (a_t, δw, Δa); closure-scheme background, full 4-gate output | The needle CAN be threaded: kink at a_t=0.92–0.95, δw=+0.1 → DESI 1.1–1.8σ, σ₈ in band, θ* at calibration floor — but w(z) departs from DESI-CPL at z≳0.3 (shape RMS 0.157): the z>0.3 tomography bins are the deciding instrument |
| `unified_cq_ede.py` | True unified CQ+EDE integration: one ODE system, both fields sharing Hubble friction + closure + growth (no multiplicative composition); running coupling β(z)=β₀+β₁z/(1+z) supported | Anchors: CQ matches iteration-6 to 1e-6 (incl. β₁ landmark w₀=−0.86324), EDE matches edelens. σ₈/H₀ corridor: β≈0.09–0.11 × f≈0.12–0.17. Three-channel verdict: closure EXISTS at (λ=1.1, β₁=0.2, f=0.35) → DESI 1.35σ, σ₈=0.810, H₀=72.95. CMB channel (100θ*, Planck 1.04109±0.0003, pinned-background): vetoes everything interesting — closure 837σ, corridor 283σ, champion 1872σ; survivable frontier (mechanism strength ≲0.05) buys only DESI ~1.7σ, σ₈≈0.80, H₀≈68.2. Quantum-gravity gates (npl power-law coupling + Δφ excursion): late-trigger β(a)=β₀aⁿ dodges θ* but buys nothing (no-go in miniature: the coupling's usefulness IS its early action); distance conjecture independently kills constant β≳0.15 (Δφ=2.66 Mpl); de Sitter conjecture forbids λ<1 |

## End-to-end test (reproduces the tomographic verdict)

```bash
python payload_bridge.py /path/to/playground_data.json
```

At the geodesic foot (λ=1.10, β=0, α=0):

- **Instrument A** (rank-2 w₀–wₐ projection): Fisher eigenvalues
  [247.7, 24.7, **1.6×10⁻¹⁴**] → Gate 3 = INSTRUMENTATION_DEGENERATE →
  *"Build a higher-rank instrument."*
- **Instrument B** (z-tomography): eigenvalues [2763, 139, **2.09**] →
  WELL_POSED. The blindness lifts by 14 orders of magnitude.
- **Generative module** on the canonical-track residuals proposes
  `−0.353·z·inv(1+z) − 0.043·exp(−2z)` — the first term *is* the CPL wₐ
  form: the missing physics is literally a thawing-coupling term.
- **Singularity cartographer** on the 27 failed grid cells classifies the
  1+αφ̂² wall as a **SIMPLE_POLE** at α = −1/λ² (score 0.9999): add a
  residue term — it is not a true horizon.

## Usage (any discipline)

```python
from falsification_engine import FalsifiableClaim
claim = FalsifiableClaim(X, y_obs, y_pred, claim_description="My model")
final, log = claim.iterative_falsification(max_rounds=5)
print(final.claim)
```

X can be redshift, time, GDP, temperature, dosage — the engine doesn't care.

## Origin

Inspired by off-grid metrology: constraints are a bandpass filter that
strips away computational theater and leaves only irreducible physical truth.
The 27 failed cells are not errors — they are where the universe reveals
its true geometry.

License: CC0 1.0 Universal (public domain) — matches the repo root.
Modules were originally MIT-headered; the author waived to CC0 to keep
the ecosystem coherent (see PROVENANCE.md and F6 in FINDINGS.md).
