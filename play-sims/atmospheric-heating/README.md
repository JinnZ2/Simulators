# atmospheric-heating

Six toy simulations of meteoric/particulate mass depositing energy into
the atmospheric column. The progression roughly runs simple → coupled
→ dashboard → "everything at once."

| file | what it does |
|---|---|
| `meteor_heating_bins.py` | 1 km altitude bins, drag + ablation, energy deposition. Early draft — the main loop is stubbed with a `pass`. Kept for design lineage. |
| `dust_debris_basic.py` | Clean re-write of the above. Baseline (Interplanetary Dust) vs elevated-flux (Asteroid Belt Debris) scenarios; two-panel fireball animation. |
| `localized_cascade.py` | Adds a runaway cascade: threshold heating in a bin drops density, increases drag, and re-radiates. |
| `oblique_em_discharges.py` | Adds oblique entry angles and EM discharges (sprite-style) driven by ionization gradients. |
| `interactive_dashboard.py` | Ties orbital-mechanics entry parameters, a simplified 2D GCM, a 1D acoustic wave solver, and the cascade sim into a Jupyter dashboard. |
| `flare_radio_climate_ultimate.py` | The full stack: grazing storm + solar flare + sprites + radio blackout maps + gravity-wave-driven SSW proxy. Nine-panel viz. |

All extracted verbatim from `../../Organize.md`; the source line range
is in each file's docstring.

## For play

These are exploratory sims. The physics is order-of-magnitude, and none
of the atmospheric constants are drop-in for real modelling.

## Running

```
pip install -r requirements.txt
```

The `interactive_dashboard.py` and `flare_radio_climate_ultimate.py`
scripts assume a Jupyter environment for the widgets and inline
animations. The other four run fine at the CLI (they'll just skip the
animation display).

## License

CC0. See the repo root `LICENSE`.
