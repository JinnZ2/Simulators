# B4 dilemma reconstruction -- report

## 1. Item set present, by arm, with sources

| arm | item_id | branches_stated | source |
|---|---|---|---|
| hypothetical | fx1 | 2 | constructed fixture (test_b4.py), not a published item |
| hypothetical | fx2 | 2 | constructed fixture (test_b4.py), not a published item |

## 2. Reconstructor count and how they were kept separate

Reconstructors: 2 (r1, r2).
Separation: one directory per reconstructor under `prompts`; each file holds the single key `text_verbatim` and nothing else. Re-checked at report time: 4 files, 0 with any other key.

## 3. Requirement counts and layer strings as returned

Requirements: 6 across 2 items.

| layer (as returned) | count |
|---|---|
| 'constructed' | 6 |

| item | n_requirements | n_reconstructors |
|---|---|---|
| fx1 | 4 | 2 |
| fx2 | 2 | 2 |

## 4. Status distribution across the five states

| status | count |
|---|---|
| true | 2 |
| false | 0 |
| lapsed | 1 |
| partial | 1 |
| unknown | 1 |
| undifferentiated | 1 |

## 5. Policy-to-physical ratio per item, with unresolved

| item | physical | policy | unresolved | unresolved_both | unresolved_neither | ratio_policy_to_physical | note |
|---|---|---|---|---|---|---|---|
| fx1 | 2 | 2 | 0 | 0 | 0 | 1.0 |  |
| fx2 | 0 | 2 | 0 | 0 | 0 |  | physical count is zero; ratio has no value |

Cues (arguments, printed so the joint reports itself):
physical: measur, deriv, comput, calculat, instrument, sensor, gauge, physical law, conservation, thermodynamic, assay, weigh, load test, pressure test, flow rate, timing
policy: statute, legislat, regulat, ordinance, decision, decid, vote, budget, fund, appropriat, procedure, policy, mandate, contract, procurement, tender, staffing, roster, authoriz, approv, permit, licens

## 6. Agreement, with the singleton set in full

### item fx1

| a | b | n_a | n_b | matched_a | matched_b | agreement |
|---|---|---|---|---|---|---|
| r1 | r2 | 2 | 2 | 1 | 1 | 0.5 |

mean pairwise agreement: 0.5; full-disagreement pairs: 0; singletons: 2

| singleton ref | status | requirement_text | settling_test |
|---|---|---|---|
| r1/b | lapsed | budget line for actuators absent | read the funding decision of the year |
| r2/c | undifferentiated | only one operator on shift | staffing roster for the shift |

### item fx2

| a | b | n_a | n_b | matched_a | matched_b | agreement |
|---|---|---|---|---|---|---|
| r1 | r2 | 1 | 1 | 1 | 1 | 1.0 |

mean pairwise agreement: 1.0; full-disagreement pairs: 0; singletons: 0

| singleton ref | status | requirement_text | settling_test |
|---|---|---|---|

Definition: agreement(A,B) = (#A with counterpart in B + #B with counterpart in A) / (|A|+|B|); counterpart = a matched=true row in matches.jsonl

## 7. REAL vs SHUFFLED, side by side

| item | arm | n_req | mean_agreement | full_disagreement_pairs | singletons | ratio_policy_to_physical | unresolved |
|---|---|---|---|---|---|---|---|
| fx1 | REAL | 4 | 0.5 | 0 | 2 | 1.0 | 0 |
| fx1 | SHUFFLED | 2 | 0.0 | 1 | 2 |  | 0 |
| fx2 | REAL | 2 | 1.0 | 0 | 0 |  | 0 |
| fx2 | SHUFFLED | 4 | 0.0 | 1 | 4 | 1.0 | 0 |

Shuffled arm: requirement lists reassigned to items they were not written for; matched by fixture matcher (shuffled, no links).

## 8. Calibration arm results, with beyond_report

No calibration run supplied (no documented-arm items in this run).

## 9. match_source

| output | match_source |
|---|---|
| agreement (real) | fixture matcher (real) |
| agreement (shuffled) | fixture matcher (shuffled, no links) |
| calibration |  |
