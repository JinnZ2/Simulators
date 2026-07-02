# sponge-reef

Three toy simulations of sponge-reef productivity, filter-feeders vs
photosynthetic mixotrophs, progressively adding axes.

| file | what it adds |
|---|---|
| `reef_basic.py` | 2D reef grid, depth-attenuated light, mixo/filter split by depth. Interactive over size, depth, attenuation, mixo fraction, and per-mode efficiency. |
| `reef_light_temp_herbivory.py` | Spectral attenuation (blue + red), oblique solar angle, temperature-driven metabolism, herbivory pressure, competition between morphs. |
| `reef_seasons_pulses_larvae.py` | Latitude-driven seasonal light/temperature cycles, discrete nutrient pulses (upwelling/runoff), larval production + advective dispersal. |

All extracted verbatim from `../../Organize.md`; source line range in
each docstring.

## For play

Exploratory. Everything is coarse — sponge growth rates, larval mortality,
herbivory, and nutrient uptake are all toy parameters, not experimental
values.

## Running

```
pip install -r requirements.txt
```

All three sims are Jupyter-oriented (interactive widgets). At the CLI
they'll still run to completion but you won't see the sliders.

## License

CC0. See the repo root `LICENSE`.
