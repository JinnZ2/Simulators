# FINDINGS — `datasets/mesa_sof.md`

The note is stored as delivered and is not edited. Computed by
`check_datasets.py`, which imports `sim-span/sim_span.py` rather than
modelling it. Sample run in `samples/check_datasets.sample.txt`.

The note proposes two real cohorts as the empirical answer to what
`sim-span/RESULTS.md` left open. Five readings, none of them a verdict on
the note.

---

## 1. It answers both halves of what RESULTS.md asked, and claims one

RESULTS.md left two items open, both quoted from the file at run time:

> in a study with polysomnography or actigraphy, both `true_sleep` and
> `frag` are measured separately. Fit the outcome on both.

> the fraction of respondents who answer a sleep-duration question with
> time in bed rather than time asleep. A validation sub-study against
> actigraphy would give it directly

One design answers both. The note claims the first. The second it
describes without naming — *"measured sleep, measured awakenings, and what
they said when asked"* **is** the validation sub-study `p` needs.

**CORRECTED by the follow-up note and by measurement.** This finding
originally read: *"the note says you can compute the span-versus-sleep gap
directly. That gives the gap, not the fraction. `p` is a three-way
comparison… Two-way against sleep alone gives a continuous gap and no
`p`."*

That is wrong. The two-way gap does give `p`, in its **slope**.
`E[gap | frag × wake_cost] = p × (frag × wake_cost)` exactly — a
span-reporter's gap *is* their WASO and a true-reporter's is zero, so the
mixture's conditional mean is `p` times the product. Measured in
`sim-span/three_column.py` across five levels: max error **0.0085**,
intercept at zero throughout.

The three-way classification would also work and is not needed. The
follow-up note's own test is the better route and it was already the
right one when this said otherwise.

## 2. The sim's two swept parameters are one PSG readout, and its shape is not

    sim   span = true_sleep + frag * wake_cost
    PSG   TIB  = TST + WASO + onset latency

So `frag × wake_cost` is **WASO**, and the sim's span excess is WASO plus
onset latency. Both are PSG readouts, which the note's instrument reports.
That was worth checking, because if the sim's outcome depended only on the
product then WASO alone would be the axis and the 360-cell grid was a 1-D
sweep over a directly measured quantity.

Measured, four equal-product pairs at two hours of WASO, `mono`, p = 1.0:

| frag | wake (min) | product (h) | measured excess (h) | vertex | U |
|---|---|---|---|---|---|
| 1.0 | 120 | 2.00 | 1.99 | 14.63 | yes |
| 2.0 | 60 | 2.00 | 1.99 | 13.46 | yes |
| 4.0 | 30 | 2.00 | 1.99 | 13.00 | yes |
| 8.0 | 15 | 2.00 | 1.98 | **12.84** | yes |

**The mean is the product exactly** (max error 0.02 h). **The shape is
not:** the manufactured minimum moves **1.79 h** across the four, and many
short awakenings push it *down* the axis, toward the window where a
published minimum sits. At one hour of WASO the four disagree on whether
there is a U at all.

So WASO alone is not sufficient and the awakening count is a second axis —
and the note's instrument reports both, which is more than the note claims
for it. It also means the sim can be **calibrated** rather than swept:
MESA fixes the operating point instead of leaving 360 cells open.

## 3. `parity` resolves sixteen times and not once in the note's sense

| token | bounded hits | in the note's sense |
|---|---|---|
| `G-SPAN` | 0 | — |
| `MESA` | 0 | — |
| `SOF` | 0 | — |
| `parity` | **14** | **0** |

Every repo use of `parity` is the **equality** sense — `parity()` as a
comparison function in the divergence log, *"what would count as parity"*
as equivalence. The note means the **obstetric** sense: number of
pregnancies. One word, two senses, and a resolver that counts occurrences
reports a reference as resolving sixteen times when it resolves zero.

`uninstrumented` case 021's sense substitution, and `nonidentity-census`
T1-3's `state` finding (nation-state vs steady state), third instance in
this tree. **It is a limit of this checker, not of the note.**

`G-SPAN` does not resolve; the folder is `sim-span/` and the module
SIM-SPAN. Recorded, not normalised — an entry is stored as delivered and
vocabulary is not harmonised across entries.

So the SOF half is a thread from outside this repo. Nothing here can say
what question it answers, and the note is already honest that the parity
field itself is unconfirmed.

## 4. A defect in this checker, committed three drops after it was recorded

The first version of `resolve()` was a bare substring scan. It returned
**`parity` 17, `SOF` 81, `MESA` 3** — matching inside *disparity* and
inside other words. Word-bounded it returns 16, 0, 0; with this audit's
own products excluded (see finding 7) it returns **14, 0, 0**.

That is `uninstrumented` `UNI_009`'s `lean` / "clean" defect, which this
repo recorded three drops ago and which this file then committed. The raw
counts are kept here beside the bounded ones.

Word boundaries fix substring bleed and do nothing about **sense**. Only
hand-reading the sixteen got finding 3's right number, which is
`nonidentity-census` T1-1 one level up — the instrument built to check
references decides by matching text, and matching text cannot read a word.

## 5. What is carried, and what is not the instrument for it

Carried from the note, unchecked: the sample size, the three instruments
on the same person, the age range and exam timing, SOF's composition and
its outcome data. The egress gate refuses the sources that would confirm
any of them — same status as `shape-spec-audit` `MS_004`. **Nothing above
rests on a dataset fact being right**; the readings are about the note's
fit to this repo and about the sim's own arithmetic.

`notes/study_watch.py` is **not** the instrument for these. It reads
`uninstrumented.ENTRIES`, and this is an operator note, not a register
entry. Filing it as one to make it watchable would be filing it under a
mechanism it does not claim.

## 6. The stated caveat reaches further than stated, in the note's favour

Stated: ages 45–84, no young cohort, no ageing clocks, mortality is the
outcome you get.

`sim_span.py` assumes `frag` and `true_sleep` are **independent** and
`RESULTS.md` flags that as *"probably wrong."* In a 45–84 cohort they are
near-certainly correlated. So MESA does not only test the finding — **it
measures the sim's own weakest assumption**, because both quantities are
recorded per person and their correlation is a number you get for free.

That makes it the hard case rather than a convenient one, which is the
right way round for a test that could refute. The age range is a
limitation on what the outcome can be and an *advantage* on what the
exposure can show, and the note prices only the first.

## 7. The checker measured its own previous run

Writing `MESA` into `CLAUDE.md` to describe finding 3 put `MESA` into the
tree. The next run reported it as resolving, and the selftest went red:

    FAIL: MESA or SOF now resolves; the note's cohorts have an
          antecedent and finding 2 must be restated

`uninstrumented` `UNI_010`'s self-reference loop — `scan.py` reading the
directory `scan_audit.py` writes into — arriving in `notes/`, and found the
same way: by running twice. Two consecutive runs disagreed before anything
about the note had changed.

The fix is an `EXCLUDE` list of seven paths, and it is **a hand-broken loop
rather than a fix**, stated here rather than left quietly true: anyone
grepping this tree for `MESA` still finds the commentary, so the reported
corpus is no longer the corpus on disk. The principled version compares
against the git tree as of the note's own commit, which is what *"does this
token have an antecedent"* actually means. Not built.

It also moved `parity` from 16 to 14, both bounded — the two lost were this
audit's own prose about `parity`.

**Two defects in one file, both previously recorded in this repo, both
committed anyway:** `UNI_009`'s substring bleed (finding 4) and `UNI_010`'s
loop (this one). Neither was caught by reading the code. The first was
caught by a hand-check of a suspicious count, the second by a selftest
assertion that happened to be pointed at the right variable.
