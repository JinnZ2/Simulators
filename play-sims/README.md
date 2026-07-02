# play-sims

Exploratory sims. **This folder is the repo's explicit exception to
stdlib-only.** Every simulator outside `play-sims/` uses standard
library only; the code here reaches for `numpy`, `matplotlib`, `scipy`,
and `ipywidgets` because it's exploratory and visualisation-first, not
audit-grade.

## Layout

| folder | count | subject |
|---|---|---|
| [`plasma-waves/`](plasma-waves/) | 4 | 1D/2D FDTD wave propagation through dust; wave→dust heating; 2D PIC plasma |
| [`atmospheric-heating/`](atmospheric-heating/) | 6 | Meteor ablation, cascade, oblique EM discharges, GCM+acoustic dashboard, solar-flare-coupled ultimate |
| [`sponge-reef/`](sponge-reef/) | 3 | Filter/mixotroph productivity across depth; light/temp/herbivory; seasons + pulses + larval dispersal |
| [`exoplanet-forensics/`](exoplanet-forensics/) | 3 | Multi-framework detection cross-correlation; data archaeology + ML classifier; population synthesis + habitability |
| [`photon-upconversion/`](photon-upconversion/) | 1 | TTA-PUC kinetics + solar cell efficiency boost |

Total: 17 sims across 5 domains.

## Source

Every file was extracted verbatim from the archived source drops in
[`../legacy/`](../legacy/):

- [`../legacy/Organize.md`](../legacy/Organize.md) — 14 sims
- [`../legacy/Organize2.md`](../legacy/Organize2.md) — 3 sims

Each `.py` file's docstring names its source line range. If you edit a
sim and want the source-of-truth to move here, remove the extraction
note from the docstring — the archived `Organize*.md` files are the
original drops, not the current state.

## Adding new sims

The intake pattern (see [`../legacy/README.md`](../legacy/README.md) for
the full protocol):

1. Drop a new `Organize.md` at the repo root.
2. Extract each simulation into the right domain folder here.
3. `git mv` the drop into `../legacy/` with the next round number
   (`OrganizeN.md`) so the root stays clear for the next drop.

Each extraction keeps the docstring pointer to the archived source
file, so provenance survives the move.

## For play

These are sketches. The physics is order-of-magnitude, the parameters
are chosen for visualisation not calibration, and none of the outputs
should be read as predictions.

Compare to the rest of the repo:

- Audit-grade simulators (`AMOC/`, `antifungal-mechanism-sim/`,
  `incentive-blindspot-sim/`, `continuity-audit/`, `emergence-*/`,
  `research-*/`, `substrate-*/`) all follow the `REFUTATION_PROTOCOL`
  pattern: weights are frozen estimates, coupling topology is the
  claim, tests pin the claim.
- Play sims: no claim table, no refutation protocol, no frozen weights.
  Adjust and re-run.

The two categories don't collide because they live in different folders
and the `play-sims/` framing is up-front.

## Dependencies

Each subfolder has its own `requirements.txt`. Install per-folder:

```
pip install -r plasma-waves/requirements.txt
```

The union across all subfolders is `numpy`, `matplotlib`, `scipy`,
`ipywidgets`, `ipython`. Several sims `from IPython.display import HTML`
at the top and assume a Jupyter environment for rendered animations —
they'll still run at the CLI, just without the display.

## Tests

Smoke tests for the pure-math helpers live in
[`tests/`](tests/). They skip anything that pulls in `matplotlib`,
`ipywidgets`, or animation. Run with:

```
python3 -m unittest discover play-sims/tests
```

The tests are guarded on `numpy` import — if `numpy` is missing they
skip cleanly rather than failing.

## License

CC0. See the repo root `LICENSE`.
