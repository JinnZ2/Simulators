# photon-upconversion

One toy simulation of triplet-triplet annihilation upconversion
(TTA-PUC) kinetics + the fractional efficiency boost when an
upconversion layer sits under a bandgap-limited solar cell.

| file | what it does |
|---|---|
| `tta_puc_solar_boost.py` | Sensitiser absorption → ISC to triplet → energy transfer to annihilator → T-T annihilation → singlet emission. Reports UC quantum yield vs excitation intensity and the efficiency gain for a Si-band-gap cell. |

Extracted verbatim from `../../Organize2.md`; source line range in the
docstring.

## For play

The kinetic coefficients here are illustrative. Real TTA-PUC
optimisation requires actual measured rate constants for the
sensitiser/annihilator pair.

## Running

```
pip install -r requirements.txt
```

## License

CC0. See the repo root `LICENSE`.
