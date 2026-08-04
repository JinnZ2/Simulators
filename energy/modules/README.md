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

License: MIT — use freely, let the machines think critically.
