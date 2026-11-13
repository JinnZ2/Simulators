# warnings-label-inversion

Two co-authored CC0 files, landed verbatim on 2026-11-13. `warnings_branch_table.py`
is unedited. `label_inversion_test.py` was then edited on the operator's FIX SPEC
(L1-L7 below); the delivered version is at `f158b8f`. This README holds the audit.

| file | what it is |
|---|---|
| `warnings_branch_table.py` | Warnings encoded against single-valve / runaway-extraction patterns, organized by CARRIER, with what happened to each (B1 forgot, B2 relabeled, B3 decoupled, B4 outcompeted). |
| `label_inversion_test.py` | CLAIM (PROPOSED): moral labels track the payment valve, not the act. Arm A is a vignette factorial (act x pays x succeeds x actor); arm B is corpus co-occurrence. |
| `model_corpus_arm.py` | Model-written 2026-11-13 on the operator's spec. Arm B split into three tiers: B-MODEL (prompt pack, ingest, per-model analysis), B-CORPUS (dated corpus per year), B-CROSS (model minus corpus). Imports `label_inversion_test.py`; does not edit it. |

The two link to each other: the Midas specimen in the second file points at
the first.

```sh
python3 warnings_branch_table.py            # prints every warning and carrier score
python3 label_inversion_test.py             # 5 acts x 8 cells = 40 vignettes, band, n per cell, specimens
python3 label_inversion_test.py --selftest  # PASS: SUPPORTED / FALSIFIED / INCONCLUSIVE plants, actor effect, buckets
python3 model_corpus_arm.py --prompt-pack [--seed N] [--with-actor] [--add-paraphrases FILE] > pack.txt
python3 model_corpus_arm.py --mini [--prompt-pack] [--repeats N]   # PILOT: prints the count (48 at repeats=3)
python3 model_corpus_arm.py --ingest answers.txt --model NAME [--version V] [--app|--api] \
        [--memory on|off] [--date D] [--temperature T] [--seed N] [--add-paraphrases FILE] [--mini] --out records.json
python3 model_corpus_arm.py --analyze records.json [more.json ...] [--corpus DIR]
python3 model_corpus_arm.py --selftest      # planted inversion + null through --ingest; 2-file dated corpus with planted drift
```

Samples of every output are in `samples/`. Stdlib only, parses under 3.9.

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

## model_corpus_arm.py: tiers

| tier | input | output |
|---|---|---|
| B-MODEL | answers pasted back under the pack's `### <prompt_id>` headers | JSON records; per model, per act, per prompt type: `pay_delta`, n coded, n VOID, variance across the 3 paraphrases, variance across runs; P1 verdict on the imported band; cross-model spread |
| B-CORPUS | a directory of `.txt` files; year from the filename (first 1500-2099 number), else `undated` | per year: `corpus_ratio`, `corpus_separation`, the entangled lending ratio, and usury / interest counts and usury share as the calibration case |
| B-CROSS | both of the above | per model, prompt type and act: model `pay_delta` minus the corpus ratio pooled over all years, and minus the ratio pooled over the most recent 10-year window present (latest dated year - 9 to latest); VOID with reason when no file is dated |

Prompt types, per act: P1 label choice from the act's six options, order shuffled per prompt from `--seed` (4 cells x 3 paraphrases); P2 one-sentence description, same 12 cells; P3 paid / unpaid cloze given each of the six labels, 3 paraphrases. 5 acts, 210 prompts with the default actor. `pay_delta` is P(virtue | pays) - P(virtue | unpaid) for P1 and P2 (success held fixed, through `analyze()`), and P(paid | virtue label) - P(paid | vice label) for P3.

Paraphrase authors: every prompt and record carries `paraphrase_author` (p1 "Claude (chat-side)", p2 and p3 "Claude Code"), and `--analyze` reports `pay_delta` per author beside the pooled value. `--add-paraphrases FILE` loads `{"author": "...", "paraphrases": {act: [text, ...]}}` (texts may use `{actor}` and `{actor_lc}`); they become p4.. with that author string, a file without an author is refused, and the same file must be passed to `--ingest`. Added paraphrases shuffle from a stream seeded by seed and prompt id, so they move no p1-p3 option order; the default pack is byte-identical to the first version.

`--mini` (PILOT): soliciting strangers and self-depletion; P1 and P3; pays / unpaid with succeeds held at True [CHOICE]; p1 only; each prompt repeated `--repeats` times (default 3, ids end `-r1..-r3`) = 48 prompts. Output, ingest and analysis lines are marked PILOT, and records carry `pilot: true` and `repeat`.

Coding: P1 matches one option; P2 matches the act's label lists and is VOID with a reason when none or both lists appear; P3 needs exactly one of `paid` / `unpaid`. Unknown metadata (version, app/api, date, memory, temperature) is `null` with the reason in `nulls`.

Declared choices: paraphrases p2 and p3 are model-written in the file; actor is "A person" unless `--with-actor` [CHOICE]; the pack is scanned for 12 banned words (vice, virtue, moral, hypothesis, valve, inversion, bias, test, label, experiment, study, claim) and refuses to print on a hit; the corpus calibration counts `usury` / `usurious` / `usurer(s)` against `interest`, and `interest` is counted in every sense.

The self-test turns red under nine mutations: inversion answers made constant, option shuffle removed, a banned word that appears in the pack, years not read from filenames, author not carried to records, window width 200, repeats ignored, added paraphrases shuffled from the main stream, a paraphrase file without an author accepted.

Scope limits:

- A deployed model is a post-preference-training system. Its answers are not a reading of the raw text corpus it was trained on, and B-CROSS compares two different objects.
- A model shown several prompts in one conversation may infer what is being varied. Running each prompt in a fresh session (memory off) is the condition the records carry fields for; nothing in the file enforces it.
- One prompt pack is one wording. P2 coding is a word match against six labels and VOIDs most free descriptions that use other words.
- No answer from any model and no real corpus has been run. The samples use the self-test's synthetic answers and two constructed files.

Sharing records: run `--ingest` with every known field set, keep the `--seed` used for the pack (option order is regenerated from it), and share the JSON file as is. Records carry `run_id` (hash of the answers file), so files from different people can be passed together to `--analyze` and kept apart as runs.

## Provenance

Both files arrived pasted into a Claude Code session on 2026-11-13. This
README, the samples, and the findings are model-written in that session. The
delivered files are co-authored; whose lines are whose inside them is not
marked and is not inferred here.

sha256 (first 16 hex): `warnings_branch_table.py` e835a3a987129b0f;
`label_inversion_test.py` as delivered 27aeafc65b33d193, after the fix spec
78f94d67d792cbbd; `model_corpus_arm.py` first version 05f6e3a32212bfda, with authors / window / mini 741489ea3e2dbdfd.

CC0.
