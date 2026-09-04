# removal-closure — claim table

Claims are about the instrument, the order's own arithmetic and
schema, and — for the attached gaps — about one named file under this
module's operations. None is a claim about any constant, any coupling,
any language, speaker or species.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph.

| id | claim | status |
|---|---|---|
| RMC_001 | derivations and the three rules reproduce fixed-in-advance answers and fire in both directions on constructed worlds | SUPPORTED |
| RMC_002 | 0 of 5 seed rows count by the order's own rule; three step cells are ranges and two year cells are decades where the schema wants one value | SUPPORTED |
| RMC_003 | the seed table's years-to-closure column is consistent with its own year cells to within the `~` it carries | SUPPORTED |
| RMC_004 | H2's closed-only reading drops every open row, and open rows are exactly where H2 predicts the low-removability constants sit; a censored reading is printed beside it | SUPPORTED |
| RMC_005 | P2's pre-registration is a hash over the removability coding, publishable before any closure year is filled; the seed table itself carries both columns in one row | SUPPORTED |
| RMC_006 | the attached dataset is reachable from here — the first in this drop family — and the two gaps that need only its intermediate table run | SUPPORTED |
| RMC_007 | G2: the upstream split applies no lower pause threshold; re-merged at 0.50 s the analysed unit's mean moves 2.257 → 3.531 s, and the direction is fixed by construction | SUPPORTED |
| RMC_008 | G3: right-tail ratio exceeds 1 in 49 of 49 languages on both the analysed unit and the speech run | SUPPORTED |
| RMC_009 | G4 and G5 do not run from the repository, for reasons in its own scripts; G1, G6, G7 are reading questions | SUPPORTED |
| RMC_010 | two numbers the upstream script states in comments reproduce from the table | SUPPORTED |
| RMC_011 | nothing here bears on H1, H2 or H3, and nothing here is a statement about coupling | UNVERIFIED |

## RMC_001 — known answers first

`years_to_closure` is `closure_year − first_correlation_year` and None
on an open row. H1 fires on one closed row without a removal
demonstration and not otherwise; `partial` is counted under the strict
reading and not under `[CHOICE 2]`, both printed. H2 returns rho < 0 on
a world where closure time rises as removability falls and rho > 0 on
its reverse, using the Spearman imported from `readout-count`. H3
fires on a low-removability row at step 4 and not on one at step 3.
Every rule returns `undetermined` where its input is empty. A first
draft of the constructed world put a closed low-removability row at
step 5 and the H3 check failed — correctly, since that is H3's own
falsifier; the world was corrected, not the rule.

## RMC_002 — the seed rows do not count, by the order's own rule

*"Each cell needs a citation before it counts."* None carries one.
Read back from the order: step cells `5`, `5`, `4-5`, `4-5`, `1-2`
against a schema field of one value in 1–5; year cells `2000s` and
`1930s` against a schema wanting a year. The validator refuses a step
range and a decade year, so a seed row typed in as written does not
load. Nothing is filled in.

## RMC_003 — the seed table checked against itself

The years-to-closure column is recomputable from the two year cells
beside it, with a decade read as a range. Gravity 1806 → 2000s gives
194..203 against a stated ~200 (inside); day/night 242 against ~245;
tidal/lunar 68..77 against ~80; geomagnetic 162 against ~160; ELF
cavity 133 open-years against 130. Every stated figure sits within
three years of its computed range, which is what the tilde is
carrying. A check that came back clean, recorded because the order's
own numbers are the only numbers in the folder that can be checked
without a literature.

## RMC_004 — informative censoring in H2

H2's rule ranks time-to-closure, which exists only for closed rows.
Open rows have no value and drop out of the closed-only reading — and
the order's own thesis is that the low-removability constants are the
open ones. Dropping them removes the rows the hypothesis is about and
leaves a comparison among constants that all closed. The instrument
prints a second reading with open rows entered at
`CURRENT_YEAR − first_correlation_year`, a lower bound on their
time-to-closure `[CHOICE 4]`, and names the open low-removability rows.
Neither reading is picked.

## RMC_005 — pre-registration as a hash

P2 says code removability before looking at closure year.
`precode_hash()` is sha256 over sorted (constant, organism,
removability) triples; it is stable when closure years change and moves
when a removability is recoded, so a coder can publish the digest
before filling the table and anyone can check the filled CSV against
it. The seed table carries removability and closure in the same row,
so for those five rows the ordering P2 asks for cannot be shown from
the file.

## RMC_006 — a reachable dataset

Every prior drop in this family named literature or data behind hosts
the egress allowlist refuses. The repository this order attaches is on
`github.com`, which answers, and it was cloned (commit
`b174bd64afba`). Its intermediate table is one row per pause-bounded
unit with onset, offset, trailing pause, unit duration and speech
duration per language. The file is not checked in (third-party, 16 MB);
its size and sha256 are printed on every render so a re-obtained copy
can be checked, and the selftest pins the headline numbers when the
file is present and reports its absence rather than failing.

## RMC_007 — G2, run

The order asks whether the ~2 s figure moves with the pause threshold.
From the repository's own scripts: the unit is opened at the first
non-pause word after a pause label and closed at the next, and no
minimum pause length is applied — the shortest trailing pause in the
table is 0.001 s. Re-merged so that a unit whose trailing pause is
shorter than t joins the next unit in the same file, speaker and part:

| t | units | unit mean | unit median | speech mean |
|---|---|---|---|---|
| 0.00 | 105687 | 2.257 | 2.020 | 1.430 |
| 0.15 | 96086 | 2.483 | 2.219 | 1.582 |
| 0.25 | 87791 | 2.717 | 2.427 | 1.751 |
| 0.35 | 79762 | 2.991 | 2.652 | 1.957 |
| 0.50 | 67567 | 3.531 | 3.019 | 2.387 |

The mean moves by a factor of 1.56 across the order's four thresholds.
The direction is not a finding — merging only lengthens units, and the
selftest asserts monotonicity — the size is. What the number describes
at t = 0 is the annotation's pause convention, which is upstream of
this repository.

## RMC_008 — G3, run

Per language on the analysed unit: median 1.36–2.71 s, mode (0.05 s
bins) 0.90–2.35 s, CV 0.42–0.63, right-tail ratio 1.46–2.64. On the
speech run with the pause excluded: median 0.77–1.67 s, CV 0.51–0.78,
right-tail ratio 2.10–3.41. The ratio exceeds 1 in 49 of 49 languages
on both quantities. By the order's own stated contrast — a long right
tail against a symmetric tight window — the distributions are of the
first shape in every language, more so on the speech run than on the
unit that includes its pause. This is a property of the file under the
stated statistics and is not a statement about what produces the shape.

## RMC_009 — the gaps that do not run

G4 asks for the word-level interval against the unit; the repository's
first script reads word rows from an external DoReCo path and writes
only the aggregated units, so the inner level is not in any file it
carries. G5's covariate joins on country, which the third script
obtains by geocoding coordinates; the table has coordinates and no
country, and geocoding is behind the allowlist. G1 and G6 are questions
about the paper's animal rows and their generators. G7's one number is
arithmetic: 1 / 2.020 s = 0.495 Hz.

## RMC_010 — the script's own comments

`04_plots_analysis_revision.R` states in comments a speech-run mean of
1.43 s and a pause mean of 0.83 s. Recomputed from the table: 1.430 and
0.827. A stated-vs-computed check on the upstream file, clean.

## RMC_011 — UNVERIFIED

No constant-organism row with a citation exists. Nothing in the
attached-gap results bears on the main table's hypotheses, and nothing
here asserts or denies any coupling; the order's scope note is honoured
and the instrument's render says so.
