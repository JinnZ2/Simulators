# Working notes: Kimi K3 second-reader material

CC0. Co-authored (filed by Manus, an AI agent, at the repository owner's request, 2026-11-18). Status: working notes.
These are not findings of this repository. Marker meanings are those of `READ_ME_THIS_WAY.md` (`[stated]`, `PROPOSED`, `VERIFY`, `OWED`, `specimen`).
Nothing outside this folder was edited, including `playground-crossrun/COMBINED_SPEC.md` and the precursor reference notes.

How to read this folder: the words of the second reader are in `as_received/`, byte for byte, and are not annotated there.
Everything that is Manus's is in this file, dated, and says what was checked and how. A mismatch between the two is data, not a defect to clean up.

## 1. What was received, and how

| file here | original name | bytes | sha256 | how received |
|---|---|---|---|---|
| `as_received/report_parts_A_B_C.txt` | `Pasted_content_76.txt` | 12609 | `a72a527a3cf042427f719f67e525895454f54cff66ba5a99ebd3f19722f4a81a` | pasted text, 2026-11-18 |
| `as_received/one_page_precursor_note.md` | `Pasted_content_77.txt` | 4856 | `cbec70e623dca38073fd9eb92be6ade3772ab3065fba067eb34d449e93280c80` | pasted text, 2026-11-18 |
| `as_received/ipython_632f71c4a62c4dcb.png` | same, inside the zip below | 114141 | `9d5ef10bd187fbd89032655b20898e677fe4b59d390c1746c11a4f061d7ccf50` | zip, 2026-11-18 |
| `as_received/precursor_fraction_sweep.png` | same, inside the zip below | 180393 | `78ff3b608ea44773feb6910b926da09fe3f39fcab5a93f637c5a5165c1c27b28` | zip, 2026-11-18 |

The zip was named `OKComputer_谓词分配与守卫分析.zip` (the Chinese reads "predicate assignment and guard analysis"), 282175 bytes, sha256 `8c8cde137bb00b3b4c04b9251286f9724e0633afe38a2e9b7100967a0cbe047f`. It is not kept here; its two members are.
Hashes identify the received bytes. They do not authenticate who wrote them.

## 2. Provenance, and what is not established

- **Author.** Both texts name themselves "Kimi K3" (`[stated]` by the text). Manus did not run that model and cannot authenticate it. How the texts reached the owner is not recorded here.
- **Date.** Both texts carry 2026-11-19. They were received on 2026-11-18 (local time, UTC-6; the receipt was about 19:00 UTC). The date is unresolved. `PROPOSED` reading, not tested: the author's clock was ahead of UTC.
- **The blind was not blind, by the author's own account.** The report opens: "the first-reader verdicts for pass A are recorded in COMBINED_SPEC §9c (the VOID-12 lines), in the same file I had to read for the right-column definitions. I saw them." The author says its assignments were derived from the definition sites only, and asks the reader to weigh that. Weigh it: Part A agrees with the first reader on all eight pairs (section 3), and that agreement is not independent evidence.
- **Content lost in the paste (`specimen`).** The text holds five U+FFFC object-replacement characters, at lines 17, 23, 44, 45 and 46 of the report. Line 17 stood where a table of the seven guard comparisons in Part B was; **that table is not in the paste and not in the zip**, so Part B's seven verdicts are stated only as "GUARD_OK everywhere". Line 23 stood, presumably, where a result table of the n = 200 replay was (the text introduces one and then continues without it). Lines 44 to 46 stood where citation links were. `OWED`: the Part B table and the n = 200 replay table, from the author.
- **The two PNGs.** Both show the same three-panel figure, "precursor operating curve: what the detector actually reads, 200 seeds/cell, Kimi K3 replay 2026-11-19", at two resolutions (1487 x 472 and 2227 x 705); their hashes differ. Read off the figure by eye, the n = 60 and n = 200 curves at window fraction 0.5 sit near 0.39 and 0.79 (limit 0.5) and near 0.60 and 0.93 (limit 0.3), which matches the counts in the report's text. Which U+FFFC the figures belong to is not stated.

## 3. What Manus checked, and what it did not

Method for everything marked CHECKED: the file or page was opened and read in this session; nothing was taken from memory.

### Part A (predicate assignment, eight pairs)

| item | result |
|---|---|
| The eight pair labels and their order | CHECKED against `combined-playground/samples/vocab_branches.txt`: same eight pairs, same order. |
| Per-pair relations | CHECKED: MAPS, PARTIAL, PARTIAL, PARTIAL, HOMONYM, PARTIAL, NONE, PARTIAL for pairs 1 to 8 in the report; the relation column in `vocab_branches.txt` reads the same, 8 of 8. The tally in the report (MAPS 1, PARTIAL 5, HOMONYM 1, NONE 1) is the tally logged in `COMBINED_SPEC.md` under "DECIDED VOID-12". |
| Whether that agreement means anything | Not by itself. The author saw the first reader's verdicts (section 2). It shows the second reader did not contradict them. |
| The quoted definitions and slot lists, the pins (TAF `16285cc`, numcheck, cplay), and the line numbers "GAP_INSTRUMENT_CRASH at line 96, COVERAGE_KINDS line 101" | NOT CHECKED. A TAF repository was not found under the owner's account in this session. `OWED`. |
| The open item in `COMBINED_SPEC.md`: "VOID-12 predicates were assigned by one reader (this build); a blind second-reader predicate assignment is open" | Left as it is. This report is a second reader's assignment that is not blind. Whether it closes the item, or is logged beside it, is the owner's call. |

### Part B (guards in `algebra.mm` against `set.mm`)

NOT CHECKED. The seven-row table is missing (section 2); the claims about `set.mm` (blob `e483895`, the `sqrtsq` name trap, `sqrtth` needing no non-typing antecedent) were not looked up. `VERIFY`.

### Part C and the one-page note (precursor flag, window dependence)

| item | result |
|---|---|
| `glyph/precursor.py` | CHECKED. On `formula-audit` `main` the file has sha256 prefix `d1eab08effbc`, the pin in `tools/TOOL_CARDS.md` (commit `c644b3c`). `--selftest`: 10 of 10 passed, as the report says. |
| Docstring claims ("readings and questions, never a verdict"; every threshold a declared input; Scheffer 2009 "recalled, VERIFY") | CHECKED: all three are in the module docstring. |
| Raw fixed-limit table in the one-page note (4 windows x 2 limits x 4 signal classes, 200 seeds, n = 400) | REPLICATED with the module's own `kendall_tau`, `rolling`, `variance`, `lag1_autocorr`: **30 of 32 cells equal, 2 differ by 1 count** (memory, w 20, limit 0.3: 87 against 88; memory, w 100, limit 0.5: 169 against 168). Script and output in `replication/`. |
| Series-length claims (w = 20 collapses as n grows; w = 50 stays flat; half-series window gains) | REPLICATED within 2 counts of 200 in every cell: w 20, limit 0.5, memory by n = 60/100/200/400 gives 44/20/16/6 (report: 46, 14, 6); w 50 gives 95/112/108/109 (report: about 110); n 60, w 30 gives 77/8 at limit 0.5 and 118/20 at 0.3 (report: 79/8 and 120/20); n 200, w 100 gives 157/14 and 185/35 (report: 158/14 and 186/35). |
| How independent that replication is | **Less than it looks.** I used Python's `random.Random`, seeds 0 to 199 and 10000 to 10199 for white noise, as the one-page note's seed ranges suggest. Agreement to within one count in most cells suggests the author used the same generator and seeds, so it confirms the code path and the arithmetic, not independence of the random numbers. The author's claimed independence check (a JavaScript port with another generator, six cells) was **not re-run**. Two details of the memory construction are not stated in the note: the starting value (I drew it from N(0,1)) and the exact climb of rho (I used 0.05 + 0.90 t/(n-1)). |
| Surrogate-calibrated table (phase randomization, 100 surrogates, alpha 0.05) | NOT REPLICATED. `OWED`. It carries the note's main claim (the calibrated rule gives 65 to 79 percent detection at every window and false alarms at the stated alpha), and its own limit is stated: about +/- 5 points. |
| Textbook arithmetic ("32 percent at w = 20", "within 1.33 sigma squared for rho up to 0.5") | CHECKED: sqrt(2/19) = 0.324; 1/(1 - 0.5^2) = 1.333. The overlap correction ("predicts about 10 percent false alarms where iid predicts 0.001 percent") was not recomputed. |
| The "36 of 36 fidelity" check | NOT CHECKED (no harness provided). |
| Reference notes "one construction ... other windows and lengths were not run" | NOT LOCATED in this session. `OWED`. |

### Literature cited by the report

| citation | result |
|---|---|
| Dakos et al. 2012, PLoS ONE 7(7): e41010 | READ (open access). The phrase "within rolling windows half the size of the datasets" is there, verbatim (Step 3), for the two example datasets. The phrase "a set of 1,000 surrogate datasets" is there, verbatim (Fig. 11 caption). Two cautions on how the report uses it. (a) The paper does not give half the series as a rule; it says the window choice "depends on a trade-off between availability of data and reliability of the estimation of the indicators". "The repo's heuristic is this paper's rule of thumb" is the author's reading. (b) Its surrogates come from a best-fit ARMA model; the one-page note uses phase randomization. Both are surrogate nulls, but they are not the same one. |
| "~1,400 citations" | A search snippet showed "Cited by 1408" for this paper; the source and date of that count are not known. |
| Boettiger & Hastings 2012; O'Brien et al. 2023; Clements & Ozgul 2018; Scheffer et al. 2009 | NOT RE-READ here. The Boettiger quotation ("takes on almost any value in its range") is `VERIFY`. The one-page note itself says its literature section is from snippets, not full texts. |

## 4. The report's own recorded limits, kept in view

The one-page note's "Limits": one construction per class; drift slope and step size are declared constants, not swept; the calibration has about +/- 5 point rate error; phase randomization asks a slightly different question from the raw flag. The report's "layer-by-layer verdict" locates the window dependence in the math, not the docstring, language, code, repo or rules; the replication here supports that the code does what the report says on the cells above and that the raw-rule counts reproduce, and nothing more.

## 5. The "curiosities" in the report, recorded without a verdict

Two questions Kimi raised, `PROPOSED` by it and not tested here: what a decision with a stated power budget looks like as a first-class token (the VOID-9 case at N = 32, where 400 trials cannot separate 0.0094 from alpha = 0.01); and whether a real case straddles the two meanings of VOID (a value absent because an instrument was refused).

## 6. Also attached with these notes, not filed here

| attachment | bytes | sha256 | relation to what is already in the other repository |
|---|---|---|---|
| `contextual_substrate_entry.md` | 12308 | `08630115a4f157a3006284137b4b54120ea1557d17198b67d4a758b91cc33121` | `Geometric-to-Binary-Computational-Bridge` already holds `experiments/experiment_bridge/evidence/kimi_round2_as_received/contextual_substrate_entry.md` (16019 bytes, sha256 `f2aa9229734e906cdef56d10d0c06388bc978906bf15fcf63d06858586e3e27e`). The attachment is a **byte-exact prefix** of that file; the longer file adds section 8 (an addendum dated 2026-11-18). So the attachment is an earlier state of a file already preserved. |
| `experiment_bridge_v1_expanded.zip` | 239957 | `64d2aeed2a976a05a2893e67537bdf9906d40029249d3e24abdb165b80dd710a` | 118 files. Compared by git blob hash with the bridge repository's `main`: 112 identical, 5 differ (`CLAIM_TABLE.md`, `README.md`, `RESEARCH_GAPS.md`, `VALIDATION.md`, `tests/test_experiment_bridge_wire.py`; the repository has moved on since), 1 absent (`BUNDLE_INFO.txt`). Its own `BUNDLE_INFO.txt` names bridge PR #90, which is merged. |

The one absent file, quoted whole: "Checked Experiment bridge v1 expansion, 2026-11-17. / Start: experiments/experiment_bridge/v1/README.md / Contract: experiments/experiment_bridge/v1/CONTRACT.md / Original audit/specimens retained unchanged. / PR: https://github.com/JinnZ2/Geometric-to-Binary-Computational-Bridge/pull/90 / No real NCM inference, semantic calibration, or physical model. / Optional cobc is needed only for actual COBOL transport tests."
Nothing was added to the bridge repository.

## 7. Reproduce the replication

```text
git clone https://github.com/JinnZ2/formula-audit && (cd formula-audit && git checkout main)
FORMULA_AUDIT_DIR=/path/to/formula-audit python3 second-reader-kimi-k3/replication/replicate_raw_table.py
FORMULA_AUDIT_DIR=/path/to/formula-audit python3 second-reader-kimi-k3/replication/replicate_lengths.py
```
The first takes about half a minute on six cores, the second a few minutes. Both use only the standard library. `replication/*.out` hold the outputs filed with this note.

Note 2026-11-18: where this file and `as_received/` disagree about what Kimi said, `as_received/` is the record.
