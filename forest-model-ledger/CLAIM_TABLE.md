# forest-model-ledger -- claim table

Claims about this folder's instruments and about the work order's first three
tasks. Status: SUPPORTED / REFUTED / UNVERIFIED. Ids are permanent. No claim
here is about a forest: every number is model output at one hand-set
parameter point, and runs 1-8 are carried as reported.

| id | claim | status | rests on | falsifier |
|---|---|---|---|---|
| FML_001 | The rebuilt base model closes its N and water budgets: N misclosure -5.062e-11 on gross throughput 576.35 over 300 yr (seed 0), water -3.426e-13; 10 of 10 seeds PASS. | SUPPORTED | `runs/run_9.py`, `T_L0_N_CLOSURE`, `T_L0_WATER_CLOSURE` | a seed, dt or parameter point where the audit reads LEAK with `leak=0` |
| FML_002 | Closure is by construction for transfers routed through the flux table. The audit detects mass moved outside the table; it does not test whether any flux has the right size. | SUPPORTED | `model/base.py` `deriv()`, `model/l0_audit.py` | a wrong-sized flux the audit flags |
| FML_003 | The audit fires on a leak: a planted loss of 0.3 of the fungal payment reads N LEAK, misclosure -72.64, water still CLOSED. | SUPPORTED | `T_L0_LEAK_DETECTED` | a planted off-table path that reads CLOSED |
| FML_004 | The work order's "old model leaked ~24 N units" is not verified here. The pre-run-6 code is not in this tree; FML_003 tests the instrument and reconstructs nothing. | UNVERIFIED (carried) | `runs/run_6.md` | the original code, run under `l0_audit` |
| FML_005 | Three of five L0 budgets (C, P, energy) are VOID and print as VOID, never CLOSED or 0. The multi-budget guard therefore has two live budgets and has not caught anything a single budget missed. | SUPPORTED | `T_L0_VOID_NEVER_CLOSED`, `L0_MULTI_BUDGET_GUARD` | a run report showing a void budget as closed |
| FML_006 | Five of eight N boundary terms are void (fixation, dust, groundwater, animal in/out) and print as void. | SUPPORTED | `T_L0_VOID_TERMS_PRINTED` | a void term printed as a number |
| FML_007 | Grass extinction (run 6's open issue) reproduces in the rebuild, 10 of 10 seeds by year 18.96-20.52, and also occurs with fire switched off (year 20.50). In this rebuild it is competitive, not fire-driven. | SUPPORTED (one parameter point) | `runs/run_9.py` case `no_fire` | a sweep showing persistence over most of the plausible range, which would make this a property of the point |
| FML_008 | Run 9's 80 fires and run 6's reported 47 are not comparable: different parameters, and run 6's length and parameters are not on record. | SUPPORTED | `runs/run_6.md`, `runs/run_9.md` | run 6's parameters, rerun here |
| FML_009 | Runs 1-8 are logged as reported. No number in `runs/run_1.md`..`run_8.md` was recomputed; `code`, `seed` and `params` are void in all eight. | SUPPORTED | `runs/`, `tools/check_ledger.py` | -- |
| FML_010 | Every ledger entry carries every schema field (void when unfilled), status `admitted` occurs only with a named test that passes when run, and assumption-block links resolve in both directions. Six planted violations each fire. | SUPPORTED | `tools/check_ledger.py --tests`, `--selftest` | a schema violation the checker passes |
| FML_011 | The trajectory is not dt-converged: halving dt moves the fire count 80 -> 79 and final tree N by 1.8%. Closure is unaffected. | SUPPORTED | `runs/run_9.py` case `base_dt_half` | -- |
| FML_012 | No entry has provenance class OBSERVED. Agreement between runs is model-to-model consistency. The two data sources in the order are listed and not retrieved. | SUPPORTED | `ledger/data_sources.yaml`, `AB_SYNTHETIC_ONLY` | -- |
