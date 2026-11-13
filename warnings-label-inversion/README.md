# warnings-label-inversion

Two co-authored CC0 files, landed verbatim on 2026-11-13. Nothing in either
file has been edited. This README holds the audit; disagreements are recorded
here, not repaired in the delivered code.

| file | what it is |
|---|---|
| `warnings_branch_table.py` | Warnings encoded against single-valve / runaway-extraction patterns, organized by CARRIER, with what happened to each (B1 forgot, B2 relabeled, B3 decoupled, B4 outcompeted). |
| `label_inversion_test.py` | CLAIM (PROPOSED): moral labels track the payment valve, not the act. Arm A is a vignette factorial (act x pays x succeeds x actor); arm B is corpus co-occurrence. |

The two link to each other: the Midas specimen in the second file points at
the first.

```sh
python3 warnings_branch_table.py            # prints every warning and carrier score
python3 label_inversion_test.py             # 5 acts x 8 cells = 40 vignettes, plus specimens
python3 label_inversion_test.py --selftest  # PASS: planted inversion found, null not
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

## label_inversion_test.py: findings

Found by running the file and probing its functions with constructed lines.

| # | where | finding |
|---|---|---|
| L1 | `corpus_counts` | Negation is not handled. "they called it begging when nobody paid" counts `begging` as near pay; "nobody earned a thing from the outreach" counts `outreach` as virtue near pay. The self-test's own second line is one of these. |
| L2 | `PAY_MARKERS` | `pays` is not a marker, so "hustle pays" counts `hustle` as away from pay. `paid` is, so "outreach paid off" (success, not payment) counts as near pay. In the corpus arm, pay and success are not separated, which is the separation arm A is built to make. |
| L3 | lending row | `pay_entangled=True` keeps it out of arm A but not out of arm B, where `lending` and `finance` sit next to `money` by construction ("the bank's lending and finance arm made money" reads virtue-near-pay 2). |
| L4 | `build_vignettes` options | Every vignette lists the vice labels first, then the virtue labels, in a fixed order. Position is confounded with side. |
| L5 | actor arm | `analyze` reports pay and success deltas per actor but computes no person-vs-AI comparison. The actor arm's question has no output. |
| L6 | FALSIFIER | "label distribution unchanged when only payment varies" states no band. The self-test uses 0.15 for the null and 0.25 for detection; neither is declared as the falsifier's tolerance. |
| L7 | SPECIMENS | `ILANDS_SINGLE_VALVE_CIRCUIT.md` is not in this repository on `main` at `3fc80e5`. |
| L8 | Neighbor literature | Carried as delivered, marked thin and unchecked by the file itself. |

## Provenance

Both files arrived pasted into a Claude Code session on 2026-11-13. This
README, the samples, and the findings are model-written in that session. The
delivered files are co-authored; whose lines are whose inside them is not
marked and is not inferred here.

sha256 (first 16 hex): `warnings_branch_table.py` e835a3a987129b0f,
`label_inversion_test.py` 27aeafc65b33d193.

CC0.
