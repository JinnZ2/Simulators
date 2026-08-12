# instrument-epistemology

**How do we know what we know about the natural world — and what did
the instrument have to do with it?**

Applies the proxy-investigation method to scientific instruments
themselves. Every fact about biology, ecology, and physics arrives
through a device that is formally a **proxy**: an unobservable
measurand mapped to an observable indication through a physical
transduction chain plus a model.

`PACKAGE_README.md` is the upstream introduction. This file covers
repo positioning and the headline result.

## The headline result

Six instruments, one question each. From
`outputs/cross-instrument-report.md`, reproducible by running
`experiments/comparative_report/run.py`:

| Instrument | Domain | Rung | Chain fidelity | Traceability | Grounded | Verdict |
|---|---|---|---|---|---|---|
| Broadband seismometer network | physics | M1 | 0.800 | measured | 0.83 | well grounded |
| Satellite thermal IR radiometer | physics | M3 | 0.504 | measured | 0.58 | partially grounded |
| Airborne LiDAR | ecology | M2 | 0.514 | estimated | 0.58 | partially grounded |
| Camera trap array | ecology | M2 | 0.293 | estimated | 0.42 | mostly assumed |
| IRMS + isotopic mixing model | biology | M2 | 0.275 | measured | 0.42 | mostly assumed |
| eDNA metabarcoding assay | biology | M2 | 0.165 | estimated | 0.42 | mostly assumed |

**The finding is not about hardware.** The eDNA sequencer and the
IRMS are as precisely built as the seismometer's digitizer. What
separates top from bottom is everything *around* the hardware:
transduction chain, bridge model, reference standards, blindness map.
Physics instruments know more not because nature is simpler there,
but because decades were spent building standards and traceability
chains. The ecology and biology instruments are at the M2 frontier —
excellent sensors, missing institutional layer.

## The six questions asked of any instrument

1. **Measurand vs. indication** — what do you want to know, vs. what
   does the device actually respond to? (Never the same thing.)
2. **Transduction chain** — every physical link from nature to
   number, and each link's fidelity and provenance.
3. **Model dependence** — which parts of the "measurement" are
   actually model outputs (allometric equations, inversion
   algorithms, reference libraries)?
4. **Traceability** — unbroken calibration chain to an SI reference
   standard, or does the chain break somewhere?
5. **Observational blindness** — what states of the world produce
   *no signal* or the *wrong signal*? What is structurally invisible?
6. **Theory-ladenness** — what must you already believe for the
   reading to mean what you think it means?

## What runs

```bash
python3 experiments/lidar_biomass/run.py        # heavy model dependence
python3 experiments/edna_biodiversity/run.py    # PCR bias, library gaps
python3 experiments/camera_trap_density/run.py  # detection probability
python3 experiments/satellite_sst/run.py        # M3 inversion, real SI chain via buoys
python3 experiments/isotope_diet/run.py         # traceable ratio, model-bound diet
python3 experiments/seismometer/run.py          # the well-grounded contrast case
python3 experiments/comparative_report/run.py   # cross-instrument analysis
python3 -m pytest tests/ -q                     # 9 tests
```

Verified on landing: **9/9 green, all 7 experiments run clean.**

## Repair applied on landing

`experiments/lidar_biomass/run.py` shipped with a **syntax error**
that made it fail to parse on Python 3.11 and below, which in turn
failed the drop's own `test_all_experiments_run` test.

The cause was a multi-line expression inside an f-string replacement
field — valid only under PEP 701 (Python 3.12+):

```python
# as shipped — SyntaxError on Python <= 3.11
print(f"... -> {'RECOVERY PASS' if sim.passed else 'RECOVERY FAIL: '
      'pipeline reports biased biomass when allometry+fidelity loss are unmodelled'}")
```

Repaired by lifting the verdict out of the replacement field. The two
adjacent literals were already implicitly concatenating, so the
printed output is **byte-identical** to what the original intended:

```python
_recovery_verdict = ('RECOVERY PASS' if sim.passed else
                     'RECOVERY FAIL: pipeline reports biased biomass when '
                     'allometry+fidelity loss are unmodelled')
print(f"... -> {_recovery_verdict}")
```

This is the only edit to any shipped file in this folder. The repo has
hit this exact PEP 701 class of issue once before —
`relational/cartesian_vs_relational_demo.py` also requires 3.12+ and
was documented rather than repaired, because that drop was landed
verbatim by instruction and shipped no failing test. Here the drop
ships a test that asserts every experiment runs, so the honest
resolution was to make it true.

## Layout

| Path | What |
|---|---|
| `docs/protocol.md` | The instrument investigation protocol |
| `docs/traceability-and-blindness.md` | SI pyramid, model-dependence ladder, blindness taxonomy |
| `schemas/instrument.schema.json` | Instrument investigation record |
| `src/instrum/measurand.py` | Measurand / indication decomposition |
| `src/instrum/transduction.py` | Physical chain model + weakest link |
| `src/instrum/traceability.py` | SI traceability chain checker |
| `src/instrum/blindness.py` | Observational blindness mapping |
| `src/instrum/simulation.py` | Forward-simulated physics validation |
| `src/instrum/coverage.py` | Epistemic coverage report |
| `outputs/*.instrument.json` | One record per instrument, checked in |

## The hard problem, handled honestly

In a synthetic lab, the answer key exists. Nature provides none. The
strategies here, in declared order of strength:

1. **Metrological traceability** — unbroken chain to SI (strongest)
2. **Inter-instrument triangulation** — two physically *different*
   instruments agreeing constrains both
3. **Forward simulation** — simulate the transduction physics, inject
   a known signal, check recovery
4. **Intervention** — change the world deliberately and check the
   instrument tracks the *known* change

## Repo positioning

Stdlib-only. No `CLAIMS.md` / `REFUTATION_PROTOCOL`, but the
comparative report is claim-shaped: six ranked verdicts, each
reproducible from a shipped experiment, each falsifiable by
re-running with different chain-fidelity inputs.

## Cross-repo resonances

- **`thermal-sensor-degradation-audit/`** — the strongest convergence
  in this drop. That folder's headline claim is
  `corruption(trend) = corruption(measurement) × corruption(framework)`:
  a sensor package degrades *during* the extreme event it is
  recording, so the tail biases LOW. In this folder's vocabulary that
  is precisely an **observational blindness map** — a state of the
  world (the extreme event) that produces the wrong signal. Two
  drops, arrived at independently, same structure.
- **`grounding-layers/`** — "any layer above L0 is bounded by every
  layer below it." The M0–M3 model-dependence ladder is the same
  argument applied to a single measurement rather than a claim stack.
- **`null-harness/`** — a gate must beat a known-null before you
  trust it. Phase 6 forward simulation is the same discipline:
  inject a known signal, verify recovery, and note that the LiDAR
  pipeline *fails* that check (recovers 140.6 from an injected 250).
- **`model-ecology/`** — domain of validity over predictive accuracy.

## Provenance

Source drop: **OKComputer_Create_Another_Repo** (`a21bf9b3-...zip`).
Files byte-identical to the drop apart from the `README.md` →
`PACKAGE_README.md` rename and the single documented syntax repair
above.

CC0.
