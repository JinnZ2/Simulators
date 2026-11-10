# meander-ledger

Why does meander shape repeat from creek to large river? This folder applies the
forest ledger's METHOD BRIEF (`../forest-model-ledger/CLAUDE.md`) to that question.
It uses the same SCHEMA and checker. Work order verbatim in `WORK_ORDER.md`
(co-authored, Kavik + Claude, 2026-11-10).

**The main output is `QUESTIONS.md`.** It holds 20 mapped questions, none answered.
Each carries its layer, what raised it, the instrument that would answer it,
cross-domain shapes, and an OPEN status.

## What is here

```text
model/meander.py     bend growth + neck cutoff toy, mass-conserving sediment ledger  PROPOSED form
model/l0_audit.py    misclosure per budget + boundary audit line; forest verdict rule
runs/run_1.*         base, 3 seeds, depth/friction, bank strength, vegetation, supply, planted leak
runs/run_2.*         neck rule, node spacing, aspect 10 long run
runs/run_3.md        TOO-SMOOTH CHECK on DS_THAPA_2025 (tools/scatter.py)
tools/fetch_data.py  fetches the dataset pinned by commit + sha256 into data/raw/ (git-ignored)
ledger/              15 components, 8 assumption blocks, 5 branches, tests, regime map
                     (all cells void), data sources, 4 coincidence cards
tests/test_meander.py   10 tests, ids match ledger/tests.yaml
```

```sh
python3 meander-ledger/tests/test_meander.py
LEDGER_ROOT=$PWD/meander-ledger python3 forest-model-ledger/tools/check_ledger.py --tests
python3 meander-ledger/runs/run_1.py          # ~2.5 min, reproduces samples/run_1.sample.txt
python3 meander-ledger/tools/fetch_data.py && python3 meander-ledger/tools/scatter.py
```

## Scatter result (run_3, DERIVED from a third-party file, MIT)

```text
16951 meanders   lam/W median 15.81   IQR 7.23..29.27   p05..p95 1.68..63.02
in the recalled 10..14 band: 11.6%     below 5: 17.5%     above 30: 24.1%
linear R2 0.059     log-log slope 0.228, R2 0.116     shuffle-null R2 max 0.0005
sd log10(lam/W) 0.484  vs  sd log10(W) 0.486      Spearman(lam/W, W) -0.733
median lambda: 1562 m at W 30-60 m, 3186 m at W 1000-3000 m
```

Lambda is nearly flat across a 100-fold width range, so lam/W is mostly 1/W.
The band is crossed only at W 100-200 m. The result is not too smooth; it is too
rough, and the roughness points at the instrument:
- lambda has a floor at the DEM smoothing scale.
- W includes lakes.
- Two wavelength columns disagree.
- Slope carries nothing.

See `runs/run_3.md` and card MC_001.

## Toy result (run_1, run_2, DERIVED)

```text
lam/W 7.96..8.80 over 3 seeds    sinuosity ~2.0..2.45    7.5..8 cutoffs per 1000 steps
sediment CLOSED 13 of 13; planted leak caught (LEAK -1.213e+02)
water, energy CLOSED by IDENTITY (carry nothing); momentum VOID
```

What the toy shows:
- It sees depth and friction only through alpha (aspect 10 == Cf 0.005, byte-identical).
- Supply moves nothing in the planform.
- It is not grid-converged: ds 0.25 gives lam/W 2.62.

## Provenance

Recalled and not checked (egress allowlist):
- lambda ~ 10-14 W (Leopold and Wolman)
- helical flow
- the growth-cutoff steady state
- Ikeda-Parker-Sawai 1981 and the Howard-Knutson reduction

Nothing in this folder rests on any of them being right.

stdlib only, parses under Python 3.9, CC0.
