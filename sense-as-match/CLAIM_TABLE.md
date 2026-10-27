# CLAIM_TABLE — sense-as-match

Claims are about the INSTRUMENT. Every pattern in `test_sense.py` is
CONSTRUCTED; nothing here is a reading from a sensor.

`SAM_*` ids are permanent. A refuted claim gets updated; the module is not
retuned to keep it standing.

Tags: OBSERVED (a run produced it), DERIVED (follows from the stated
definitions), PROPOSED (not built or not tested).

| id | claim | tag | status |
|---|---|---|---|
| SAM_001 | Offset, gain and sampling count are taken out by the reduction. A sine at offset 500, gain 37 and 4x the samples sits at distance **0.082** (r = 0.9967) from the original. That is not 0: linear resampling to LENGTH 32 interpolates a 60-point and a 240-point series differently. A mirror image sits at exactly 2 [GAP 3]. | OBSERVED | SUPPORTED |
| SAM_002 | known → KNOWN. Three sine observations through three different period/offset/gain settings return KNOWN on `SINE`, field `{SINE: 1.0}`, with nothing registered. | OBSERVED | SUPPORTED |
| SAM_003 | definite novel → NEW. Two square waves register exactly one new shape. The same square arriving later through other samplings returns KNOWN on the new name. Two *different* novel patterns return UNCOALESCED ("novel but not definite"), and nothing is registered. | OBSERVED | SUPPORTED |
| SAM_004 | plastic → UNCOALESCED, not forced. A sine 0.45 rad between `SINE` and `LAG` (distances 0.4332 and 0.4348, inside both radii) gets field 0.5 / 0.5, `between` naming both, shape None, and a pending field. The nearer candidate is not chosen. | OBSERVED | SUPPORTED |
| SAM_005 | uncoalesced + evidence → collapses, by three routes. (a) MIN_OBS: 1 observation, then 2, gives KNOWN. (b) Accumulation: the share moves 0.5 → 0.667 → 0.8, then KNOWN at COLLAPSE. (c) Novel-not-definite + an agreeing observation gives NEW, and only then is a shape registered. The update's channel lands in the audit trail and nowhere else. | OBSERVED | SUPPORTED |
| SAM_006 | NEGATIVE: never KNOWN by nearest neighbour. A near miss (nearest held shape `SINE`, outside RADIUS) puts its weight on NEW, not SINE. Evidence that keeps splitting never collapses (8 observations). In a 400-trial seeded sweep, a nearest-neighbour classifier would have answered in **322** cases this instrument held UNCOALESCED, so the negative is not vacuous. **0 of 400** KNOWN results had fewer than COLLAPSE of their observations inside RADIUS of the named shape. | OBSERVED | SUPPORTED |
| SAM_007 | Same shape via two channels → same state, for all three states. Identical observations under two channel dicts (one carrying `trusted: True, weight: 1e9`, the other `nearest: "RAMP"`) return identical results apart from audit. No deciding function names channel, audit, incoming, pending or trail; that is checked in the AST, and the AST scan fires on a planted channel read. | OBSERVED | SUPPORTED |
| SAM_008 | The checks discriminate. Two mutations were run in scratch against a copy, and neither is shipped. (1) Give each observation to its nearest held shape: 12 checks fail before `update` raises on a result that is no longer UNCOALESCED, and the split case reads KNOWN SINE. (2) Let a `trusted` channel flag force KNOWN: the identical-observations check fails. | OBSERVED | SUPPORTED |
| SAM_009 | COLLAPSE > 0.5 means no two candidates can both reach it, so a tie never collapses (Params refuses 0.5). RADIUS 0.5 corresponds to Pearson r ≥ 0.875, since RMS = sqrt(2(1−r)) for shapes reduced this way. | DERIVED | SUPPORTED |
| SAM_010 | [GAP 5]. A shape that lies between two held shapes, inside both radii, can never collapse on its own evidence: each observation gives at most half its weight to either candidate and none to NEW. It stays UNCOALESCED until differently placed evidence arrives. The order requires plastic patterns to be held; holding this one forever is a limit. | DERIVED | DISCLOSED LIMIT |
| SAM_011 | The repo-root `sense_as_match.py` (`e884901`) is a different instrument. Its docstring calls it `sense_at_match.py`: a word's sense gated at the match site. Its own `run_checks()` passes **16 of 18**. The failing two are "positive control fires on a term not at the match site" and "score returns UNRATED on a failed gate". Its `--selftest` redirect names `test_sense.py`, which does not exist beside it. That redirect is **not repointed here**: pointing it at this folder's `test_sense.py` would name a test that exercises a different module. | OBSERVED | OPEN — operator's call |
| SAM_012 | RADIUS 0.5, COLLAPSE 0.8, SPREAD 0.35, MIN_OBS 2 and LENGTH 32 are stipulated. None has a measured basis. All five are `Params` fields, and `Params` refuses values that would break SAM_009. | DECLARED | DISCLOSED WEAKNESS |
| SAM_013 | `shape_distance` is not registered in `tools/known_answer.py`. Its known-answer cases (0 for identical, 2 for mirror, None for flat) live in `test_sense.py`. That gate is red at baseline (4 failures in `tests/test_known_answer_gate.py`) and was not entangled with this build. | DECLARED | OPEN |
| SAM_014 | Two failures on the first run were fixture errors, not instrument errors. Square waves built with different cycle counts (4 against 2, and 4 against 4.17) are different shapes, and the instrument said so. The fixtures were corrected; the module was not changed. Recorded because the first reading of the failures blamed the reduction. | OBSERVED | RECORDED |
| SAM_015 | Nothing here is a measurement of any sensor, channel or signal. Every threshold is stipulated, and whether shape-space matching separates real patterns is untested in both directions. | — | UNVERIFIED |
