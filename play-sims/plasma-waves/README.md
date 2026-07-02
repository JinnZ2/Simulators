# plasma-waves

Four toy simulations that put dust into a wave field and watch what
falls out. All extracted verbatim from `../../legacy/Organize.md`; the source
line range is in each file's docstring.

| file | what it does |
|---|---|
| `wave_1d_fdtd_through_dust.py` | 1D FDTD of `u_tt + η(x)·u_t = c(x)²·u_xx`. Gaussian dust cloud slows and damps the wave. Reports fractional energy loss vs a clean control. |
| `wave_2d_fdtd_through_dust.py` | Same idea in 2D with a dust ring + core. Side-by-side animation of clean vs dusty wavefield. |
| `wave_field_dust_heating.py` | Wave field couples to charged dust grains. Wave damps near the dust; grain kinetic energy rises. Direct "wave → dust → heat" pathway. |
| `pic_plasma_dust_2d.py` | 2D Particle-in-Cell plasma with a fixed positive dust background. FFT Poisson solver, CIC deposition. Toy demo of dust-driven kinetic heating of the plasma population. |

## For play

These are exploratory sims — the physics is toy-scale, the parameters
are chosen for visualisation not calibration. Nothing here is audited
against experimental data. Read them the way you'd read a sketch.

## Running

Deps are `numpy` + `matplotlib`. `IPython.display` shows up in the
animation-emitting scripts so they render inline in a Jupyter notebook;
they'll still run at the CLI (the animation object goes unused).

```
pip install -r requirements.txt
python3 wave_1d_fdtd_through_dust.py
```

Note: `wave_2d_fdtd_through_dust.py`, `wave_field_dust_heating.py`, and
`pic_plasma_dust_2d.py` all `from IPython.display import HTML` at the
top. If you run outside a Jupyter environment, either install `ipython`
or comment that import.

## License

CC0. See the repo root `LICENSE`.
