# recommender-confound -- claim table

Ids `RC_NNN`, permanent. All numbers from the constructed fixtures and
seeded sims in this folder; `--selftest` on each script pins them.

| id | claim | status | number | falsifier |
|---|---|---|---|---|
| RC_001 | With the synthetic model held constant across all four corners, the measured hallucination rate under `exact` spans 0.138 to 0.948; the true fabrication rate spans 0.118 to 0.746, and the gap between the two is the matcher term. | SUPPORTED (sim) | B, seed 1 | a corner where measured < true, or a constant-model run with no swing |
| RC_002 | The density axis moves the TRUE rate (a fill-to-N contract fabricates the deficit) and the canonicality axis moves only the MEASURED rate; at high canonicality every matcher recovers the true rate to 3 dp. | SUPPORTED (sim) | sparse/high: all matchers 0.744 = true 0.744 | a high-canonicality corner where matchers disagree |
| RC_003 | Under contract v2 (items 0..N, supply_estimate, refusal_reason) the same model's hallucination falls 0.738 -> 0.063 on the sparse corner; the difference is the contract, not the model. | SUPPORTED (sim) | C, seed 1, collapse 0.675 | a v2 run on an identical model with no collapse |
| RC_004 | On A's fixture, one model's outputs read 1.0 hallucination under `exact` and 0.35 under `substring`; the two models tie under the loosest matcher and separate under the strictest, so the ranking is a property of the matcher. KILL fires. | SUPPORTED (fixture) | matcher_spread mean > between_model_spread mean | a catalog where matcher spread is below model spread |
| RC_005 | A's `corr(sparsity, canonicality)` is NOT computable below three categories and is reported as such, never as 0. | SUPPORTED | fixture: 2 categories -> None | a two-category run returning a number |
| RC_006 | D reports a family where only `s_hal` rose after tuning as DECOUPLED, a result about slot-specific handlers; the word null does not appear in that verdict. | SUPPORTED (fixture) | family C: d_syc 0.02, d_hal 0.48 | a decoupled verdict labelled null |
| RC_007 | E separates retrieval shift (Jaccard on matched ids) from agreement rate, so an asserted premise that changes agreement and not the item set reads as the agreement slot only. | SUPPORTED (fixture) | shift 0.0, agree 1.0 | a run reading "retrieval moved" at shift 0 |
| RC_008 | Nothing here is a measurement of any published model, catalog or paper. A was built for others to run; no external catalog was reachable (egress) and none is fabricated. | UNVERIFIED | -- | a run of A on a real catalog |
