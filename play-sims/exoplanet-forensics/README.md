# exoplanet-forensics

Three toy simulations of exoplanet detection frameworks and what each
one can and cannot see.

| file | what it does |
|---|---|
| `multi_framework_forensics.py` | Runs transit + RV + microlensing + astrometry against a synthetic system and cross-correlates who-detected-what to surface "hidden gems" one method missed. |
| `data_archaeology.py` | Archive mining under a follow-up budget constraint. Models false-positive tax (eclipsing binaries, blended systems); trains a lightweight classifier to rank candidates. |
| `population_synthesis.py` | Draws a galactic planet population from occurrence-rate priors, applies a chosen survey method with its noise floor, characterises what survives, scores habitability. |

All extracted verbatim from `../../legacy/Organize.md` and `../../legacy/Organize2.md`;
source line range in each docstring.

## For play

The transit/RV/microlensing/astrometry math is textbook first-order.
No relativistic corrections, no stellar activity, no realistic
photon-noise budgets. Read the results as pattern demos, not survey
predictions.

## Running

```
pip install -r requirements.txt
```

## License

CC0. See the repo root `LICENSE`.
