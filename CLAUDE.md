# Simulators

Repository for different simulations and supporting tooling.

## Layout

- `token-minimizer/` — Token compression tool design notes and a working
  `compress.py` implementation (Python stdlib only). Built around the
  "energy_english" compressed query format, local geometry references, and
  output-side delta compression.
- `emergence-stability-simulator/` — Notes and specification for a Monte
  Carlo test of stable vs. parasitic agent dynamics in multi-model
  emergence. Hypotheses, parameters, metrics, outputs, and a target repo
  structure live here.

## Working branch

Active development happens on `claude/token-minimizer-emergence-sim-T4pjn`.
All changes for the token minimizer + emergence simulator scaffolding land
on that branch.

## Conventions

- Python files target the standard library only unless a note says
  otherwise.
- Notes files (`NOTES.md`) preserve design thinking as written so the
  reasoning is traceable; implementation files keep to what the notes
  specify.
- Each simulator subfolder is intended to be promotable to its own repo
  later (e.g. `emergence-stability-simulator` is sketched as a standalone
  CC0 repo in its notes).
