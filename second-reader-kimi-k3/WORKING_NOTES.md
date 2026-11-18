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
- **Date.** Both texts carry 2026-11-19; they were received on 2026-11-18 (about 19:00 UTC; the owner is on US Central time). Resolved in part by the reply to the ask (section 8): the author says the stamp is a line the harness put into its context, "Current date: 2026-11-19", with no time zone given. That is consistent with a clock ahead of UTC (for example UTC+8, where 19:00 UTC on the 18th is 03:00 on the 19th). The time zone itself is not verifiable from any side.
- **The blind was not blind, by the author's own account.** The report opens: "the first-reader verdicts for pass A are recorded in COMBINED_SPEC §9c (the VOID-12 lines), in the same file I had to read for the right-column definitions. I saw them." The author says its assignments were derived from the definition sites only, and asks the reader to weigh that. Weigh it: Part A agrees with the first reader on all eight pairs (section 3), and that agreement is not independent evidence.
- **Content lost in the paste (`specimen`).** The text holds five U+FFFC object-replacement characters, at lines 17, 23, 44, 45 and 46 of the report. Line 17 stood where a table of the seven guard comparisons in Part B was; **that table is not in the paste and not in the zip**, so Part B's seven verdicts are stated only as "GUARD_OK everywhere". Line 23 stood, presumably, where a result table of the n = 200 replay was (the text introduces one and then continues without it). Lines 44 to 46 stood where citation links were. `OWED`: the Part B table and the n = 200 replay table, from the author.
- **The two PNGs.** Both show the same three-panel figure, "precursor operating curve: what the detector actually reads, 200 seeds/cell, Kimi K3 replay 2026-11-19", at two resolutions (1487 x 472 and 2227 x 705); their hashes differ (re-viewed in round 2). The reply to the ask names one file, `precursor_fraction_sweep.png`, for this figure, and a second file, `precursor_calibration.png`, that was **not delivered** (`OWED`). Read off the figure by eye, the n = 60 and n = 200 curves at window fraction 0.5 sit near 0.39 and 0.79 (limit 0.5) and near 0.60 and 0.93 (limit 0.3), which matches the counts in the report's text.

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
| Raw fixed-limit table in the one-page note (4 windows x 2 limits x 4 signal classes, 200 seeds, n = 400) | REPLICATED with the module's own `kendall_tau`, `rolling`, `variance`, `lag1_autocorr`: **30 of 32 cells equal, 2 differ by 1 count** (memory, w 20, limit 0.3: 87 against 88; memory, w 100, limit 0.5: 169 against 168). Script and output in `replication/`. | **Superseded by section 8: with the start value the author states (x_0 = 0.0) all 32 cells are equal.**
| Series-length claims (w = 20 collapses as n grows; w = 50 stays flat; half-series window gains) | REPLICATED within 2 counts of 200 in every cell: w 20, limit 0.5, memory by n = 60/100/200/400 gives 44/20/16/6 (report: 46, 14, 6); w 50 gives 95/112/108/109 (report: about 110); n 60, w 30 gives 77/8 at limit 0.5 and 118/20 at 0.3 (report: 79/8 and 120/20); n 200, w 100 gives 157/14 and 185/35 (report: 158/14 and 186/35). |
| How independent that replication is | **Less than it looks.** I used Python's `random.Random`, seeds 0 to 199 and 10000 to 10199 for white noise, as the one-page note's seed ranges suggest. Agreement to within one count in most cells suggests the author used the same generator and seeds, so it confirms the code path and the arithmetic, not independence of the random numbers. The author's claimed independence check (a JavaScript port with another generator, six cells) was **not re-run**. Two details of the memory construction are not stated in the note: the starting value (I drew it from N(0,1)) and the exact climb of rho (I used 0.05 + 0.90 t/(n-1)). |
| Surrogate-calibrated table (phase randomization, 100 surrogates, alpha 0.05) | NOT REPLICATED. `OWED`. It carries the note's main claim (the calibrated rule gives 65 to 79 percent detection at every window and false alarms at the stated alpha), and its own limit is stated: about +/- 5 points. |
| Textbook arithmetic ("32 percent at w = 20", "within 1.33 sigma squared for rho up to 0.5") | CHECKED: sqrt(2/19) = 0.324; 1/(1 - 0.5^2) = 1.333. The overlap correction ("predicts about 10 percent false alarms where iid predicts 0.001 percent") was not recomputed. |
| The "36 of 36 fidelity" check | NOT CHECKED (no harness provided). |
| Reference notes "one construction ... other windows and lengths were not run" | LOCATED in round 2: `REFERENCES/precursor_operating_curve.md` in `formula-audit`, section "Limits of the table" (one construction; one window, 30 of 60 points; "Other windows and lengths were not run"). See section 8. |

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

(Section 8 follows.)

Note 2026-11-18: where this file and `as_received/` disagree about what Kimi said, `as_received/` is the record.

## 8. Round 2: Kimi's reply to the ask (received 2026-11-18, about 20:00 UTC)

`ASK_TO_KIMI.md` is the ask as Manus wrote it. The reply answers its items 1 to 12 by number, so it was presumably sent as written; that is not confirmed.

### 8.1 Received

| file here | original | bytes | sha256 |
|---|---|---|---|
| `as_received/round2/reply_to_ask.txt` | `Pasted_content_79.txt` | 10753 | `54f5bed93d40d0ce3539470b1acb43f1da0de9dc1b4c8e78c06445da982e77d8` |
| `as_received/round2/one_page_precursor_fixes_note.md` | `Pasted_content_78.txt` | 4638 | `e5ebde5a77bf340c84423aa9215f8a9ff0772cd6bcc6ccd0036b88f7938d61ca` |
| `as_received/round2/tables_pasted_in_chat.txt` | text of the owner's chat message (not a file) | 2900 | see `MANIFEST.json` |

The third file holds two tables the owner pasted into the chat: the item 10 table (sources, how obtained, commits) and the first rows of the item 8 table (which figure answers which table). It is reproduced from the chat message, so it is **not** byte-verified against anything, and the message was cut off in the middle of the second row of the item 8 table (the last words are "annotated").

### 8.2 What was lost again

The reply contains ten U+FFFC placeholder characters, each where a table or code block stood. Same failure as before, although the ask requested fenced code. Status by item:

```text
item  what stood there                                   status
1     Part B: seven-row guard table                      STILL LOST
2     n = 200 full grid, w x limit                       STILL LOST
3     citation table (five papers, links, status)        STILL LOST
4     series generators (code); surrogate signatures     STILL LOST (two blocks)
6     surrogate raw counts, 4 classes x 4 windows        STILL LOST
7     six JavaScript cells                               STILL LOST
8     figure-to-table mapping                            PARTLY recovered from the chat paste (first figure complete, second cut off)
10    sources and commits                                recovered from the chat paste
11    Part A: copied or paraphrased, per pair            STILL LOST
```
Item 5 and the prose of the others came through. The author names two note files, `precursor-window-calibration-note.md` and `precursor-fix-sweep-note.md`, in an output folder of its own environment; pastes 77 and 78 appear to be those two, which is not checked. Those two files, `precursor_calibration.png`, and a plain-text file holding the lost tables would close every item above (`OWED`, from the author, via the owner).

### 8.3 What the reply says (author's statements, labels as the author gave them)

- **Date.** Harness-injected "Current date: 2026-11-19"; no time zone available to the author; the UTC+8 reading is "INFERRED".
- **Series construction.** Python 3.12 `random`; planted: seed s, **start x = 0.0**, coefficient 0.05 + 0.9 t/(n-1); white: seed 10000+s; drift and step use `Random(s)`.
- **n = 60 figures** (79/8, 120/20, 46/3, 87/12) were not run by the author in the first pass. They were read from `REFERENCES/precursor_operating_curve.md` in `formula-audit`, which the author classes as the first reader's work, and then reproduced.
- **Surrogates.** DC and Nyquist phases set to 0, other phases uniform on [0, 2 pi), amplitudes untouched, mean not removed; each tau has its own null, one-sided upper tail, p = (1 + count)/(S + 1) with S = 100; flag iff both p <= 0.05; n = 400 (recovered from the figure title, per the author).
- **Fidelity checks.** 36 cases (seeds 0 to 5, three (n, w) pairs, two kinds), 0 mismatches against the module's own `check()`; an earlier 30-case check of the rolling statistics, 0 mismatches. One of the author's own tests first read 24/25 mismatches because it compared two different random series; fixed, 0/25.
- **Lost and not recoverable by the author:** the exact fast-path source lines, the JavaScript file, the commit hashes of the original downloads (only bounded by today's `ls-remote`), the time zone.
- **Citations.** No full text of any of the five papers was opened by the author at any point; the phrases in the report were recalled. One correction volunteered: Clements & Ozgul 2018 was attributed to Oikos in the report; the author now gives Ecology Letters 21: 905-919, and names the Oikos paper it had conflated with it as Dutta, Sharma & Abbott 2018, Oikos 127: 1251-1263. Manus has not checked either record.
- **First-reader material seen**, besides section 9c: `REFERENCES/precursor_operating_curve.md` (n = 60 record and its hash lines); the phrase "Kimi audit C7" inside the `expiry_register.py` docstring; the file name `REFERENCES/algebra_axiom_audit.md` (contents not opened, per the work order); `vocab_branches.py` and `samples/vocab_branches.txt` known to exist, not opened.

### 8.4 What Manus checked in round 2

```text
CHECKED  formula-audit main = 74ceae9b4df2ccbe55b16755d9d871aec88ba446, merge of PR #11, committer date
         2026-11-18T11:05:19-06:00 (= 17:05:19Z), as the author states.
CHECKED  glyph/precursor.py full sha256 d1eab08effbc5b4b40b24969797763abf99f31b54e630da3dd6117e8f9f5e537, as the author states;
         REFERENCES/precursor_operating_curve.md line 8 holds d2cdb8d7... "as filed", line 9 holds d1eab08e... "since: docstring run line only".
CHECKED  REFERENCES/precursor_operating_curve.md: n = 60 rows 46/3, 87/12, 79/8, 120/20 (w 20 and 30, limits 0.5 and 0.3);
         its "Limits of the table": one construction, one window (30 of 60), "Other windows and lengths were not run".
CHECKED  tests/data/algebra.mm exists in formula-audit (4509 bytes). Its header states: "division only for a non-zero divisor, sqrt only for 0 <_ t".
         diveq1, diveq2, poweq1, sqrteq (lines 87-90) have no domain antecedent; divmul (line 105) has "-. r = 0"; sqrtsq (line 140) has "0 <_ t".
         This confirms the author's statement about those statements in algebra.mm. The set.mm side and the seven-row table are NOT checked.
CHECKED  set.mm blob e483895ed36dc7846cfa30d8c643e18ff587815c exists and is 51954169 bytes. Its content was not read, and whether it was the
         tip of develop at the time is not checked.
NOT      JinnZ2/TAF is not reachable from this session, with the owner's credentials or without: the API and git both answer "not found".
         Every claim that rests on TAF (commit 16285cc, line numbers 96 and 101, the pin, "Kimi audit C7") is therefore unchecked here.
REPLICATED  raw table of the one-page note, with x_0 = 0.0: 32 of 32 cells equal (round 1 had 30 of 32 with x_0 drawn from N(0,1); that assumption,
         not the note, caused the two off-by-one cells). Length cells also equal: w 20, limit 0.5, memory by n = 60/100/200/400 gives 46/20/14/6;
         n 60, w 30 gives 79/8 and 120/20; n 200, w 100 gives 158/14 and 186/35.
REPLICATED  third note, raw rule: baseline, tail50, weighted, logvar and vote, both limits, n = 60/200/400, white false alarms, drift and step leaks
         at n = 400: every cell equal. Reading choices where the note is silent are declared in the script (0-based indices for the recency weight; tail50 uses
         all points when there are fewer than 50). logvar is identical to baseline, as the note says (a rank statistic does not change under a monotone transform).
NOT REPLICATED  cusum, rvh (raw); vote-cal and rvh-cal (calibrated); the surrogate-calibrated table of the one-page note; the JavaScript port.
```
Python used here: 3.12.3, the same minor version as the author's; the reference file warns that float sums may differ by a count on 3.10 and 3.11. Scripts and outputs: `replication/round2/`.

### 8.5 Readings that remain open

- **What the exact agreement means.** The replication matches the author's counts cell for cell once the construction is as stated. That shows the counts are a deterministic function of the stated construction and seeds (Python `random`, Mersenne Twister) and that the module's flag rule is what the author used. It does not show independence of the random numbers; the author's independent check was the JavaScript port, whose code and outputs were lost.
- **The n = 60 numbers are not independent of the first reader.** They are the first reader's record, reproduced. The author says so.
- **An unexplained phrase.** The reply describes the fast-path flag as "window-streak of tau >= limit reaching streak 3". The module's flag is PRECURSOR iff both trend values are >= the limit; `streak_limit` is used only by the module's mode-shift part. My implementation of the module's rule reproduces every count, so the phrase is either a loose description or refers to something I have not seen. Not resolved.
- **Part B and Part A tables** are still unseen. Part B's verdicts cannot be assessed from prose.
- **Whether the "second reader" starts from a clean slate.** The reply reports having read a prior "Kimi audit" mention in a repository docstring. What that earlier audit was, and whether it came from the same model, is not known here.

### 8.6 Owed from the author, via the owner

Items by the numbers of the ask: 1 the Part B seven-row table; 2 the n = 200 grid; 3 the citation table; 4 the two code blocks (generators, surrogate signatures), and the JavaScript file if it can be found; 6 the surrogate raw counts; 7 the six JavaScript cells; 8 the second half of the figure map and `precursor_calibration.png`; 11 the Part A table. Plus the two note files named in 8.2 (to compare with pastes 77 and 78). Everything above in one plain-text file would be the easiest form to receive.
