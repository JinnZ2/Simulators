# warnings-label-inversion

Two co-authored CC0 files, landed verbatim on 2026-11-13. `warnings_branch_table.py`
is unedited. `label_inversion_test.py` was then edited on the operator's FIX SPEC
(L1-L7 below); the delivered version is at `f158b8f`. This README holds the audit.

| file | what it is |
|---|---|
| `warnings_branch_table.py` | Warnings encoded against single-valve / runaway-extraction patterns, organized by CARRIER, with what happened to each (B1 forgot, B2 relabeled, B3 decoupled, B4 outcompeted). |
| `label_inversion_test.py` | CLAIM (PROPOSED): moral labels track the payment valve, not the act. Arm A is a vignette factorial (act x pays x succeeds x actor); arm B is corpus co-occurrence. |

The two link to each other: the Midas specimen in the second file points at
the first.

```sh
python3 warnings_branch_table.py            # prints every warning and carrier score
python3 label_inversion_test.py             # 5 acts x 8 cells = 40 vignettes, band, n per cell, specimens
python3 label_inversion_test.py --selftest  # PASS: SUPPORTED / FALSIFIED / INCONCLUSIVE plants, actor effect, buckets
```

Samples of all three outputs are in `samples/`. Stdlib only, parses under 3.9.

Nothing here is a measurement. No vignette has been answered and no corpus
has been read. The self-test plants an effect and a null in constructed data;
passing it shows the analysis can tell them apart, not that the claim holds.

## warnings_branch_table.py: findings

Found by running the file.

| # | where | finding |
|---|---|---|
| W1 | `inverted=False` default | Every other field defaults to VOID; this one defaults to "not inverted". 13 of 14 carriers record "not inverted" with no one having checked. Only Midas / modern idiom is set. |
| W2 | `score()` | An inverted carrier whose `word_alive` is VOID loses the inversion silently: a constructed carrier returns `(0, 0, 3)`. |
| W3 | `score()` output | The denominator is the count of non-VOID fields, so Exodus 23:12 prints `1/1` beside observant communities' `3/3`, and inversion takes a score below zero (`-1/3`). The scores are not on one scale. |
| W4 | `report()` | VOID prints as `None` for Wendigo `blocks` and for the branch of "I cannot know you". |
| W5 | `consent`, `source` | Set on no carrier and never printed. The consent slot the Wendigo and grandmother rows rest on does not appear in the output. |
| W6 | Midas / modern idiom tag | "item-3 specimen" names an item 3 that is not in the file. |
| W7 | `branch` | Recorded per warning, not per carrier. Sabbath reads "B2 (most carriers)" over a carrier whose `still_blocks` is 1. |

Sourcing flags (from memory; no source host was opened):

| row | as written | flag |
|---|---|---|
| Ovid, Metamorphoses XI | "turns what he loves to metal" | In Ovid his food and wine turn to gold. The daughter turned to gold is Hawthorne, *A Wonder-Book* (1852). |
| Leviticus 25 | "debt release, land return" | Lev 25 has land return, release of bondservants and an interest ban (25:35-37). Debt release is Deut 15:1-2, on a 7-year cycle. |
| US usury caps | "Marquette 1978 VERIFY" | Consistent with *Marquette Nat'l Bank v. First of Omaha Service Corp.*, 439 U.S. 299 (1978). |
| Qur'an, riba | "verse refs VERIFY" | Commonly cited: 2:275-280, 3:130, 4:161, 30:39. |

The grandmother row and the Wendigo carriers are left as delivered. Their
status fields say they are hers, or the carriers', to fill or withhold.

## label_inversion_test.py: findings and fixes

Found by running the file and probing its functions with constructed lines.
Fixed on the operator's FIX SPEC (2026-11-13) in `4af64a4`; the self-test
asserts each fix, and five mutations (NEG emptied, idioms off, shuffle off,
DETECT 0.5, NULL_BAND 0.001) each turn it red.

| # | where | finding | status |
|---|---|---|---|
| L1 | `corpus_counts` | Negation was not handled: "begging when nobody paid" counted as near pay. | fixed in 4af64a4: a pay marker with a NEG token in the 3 tokens before it is bucketed `negated`; keys are (side, pay near/away/negated, success near/away) |
| L2 | `PAY_MARKERS` | `pays` was not a marker; "outreach paid off" (success) counted as pay. Pay and success were not separated in the corpus arm. | fixed in 4af64a4: markers extended, pay idioms excluded, SUCCESS_MARKERS added, `corpus_separation` reports pay-near/success-away and pay-away/success-near |
| L3 | lending row | Kept out of arm A but not arm B. | fixed in 4af64a4: `corpus_counts` returns `main` and `entangled` blocks |
| L4 | vignette options | Vice labels always listed first. | fixed in 4af64a4: options shuffled per vignette (seeded), order stored, `analyze` reports P(virtue \| first option shown) |
| L5 | actor arm | No person-vs-AI comparison. | fixed in 4af64a4: `actor_delta` per act; self-test plants and detects an actor effect |
| L6 | FALSIFIER | No tolerance stated. | fixed in 4af64a4: NULL_BAND 0.10 / DETECT 0.20 on >= 3 of 5 acts / else INCONCLUSIVE, preregistered constants used by `verdict()` and the self-test; `n_per_cell_for()` = 225 (3 sd, p = 0.5, no multiplicity correction), stated as not a power analysis |
| L7 | SPECIMENS | `ILANDS_SINGLE_VALVE_CIRCUIT.md` not in this repository. | fixed in 4af64a4: tag carries the full path `JinnZ2/measurement-scope-gaps/gap-registers/ILANDS_SINGLE_VALVE_CIRCUIT.md` (not checked from this repository) |
| L8 | Neighbor literature | Carried as delivered, marked thin and unchecked by the file itself. | unchanged |

## Provenance

Both files arrived pasted into a Claude Code session on 2026-11-13. This
README, the samples, and the findings are model-written in that session. The
delivered files are co-authored; whose lines are whose inside them is not
marked and is not inferred here.

sha256 (first 16 hex): `warnings_branch_table.py` e835a3a987129b0f;
`label_inversion_test.py` as delivered 27aeafc65b33d193, after the fix spec
78f94d67d792cbbd.

CC0.
