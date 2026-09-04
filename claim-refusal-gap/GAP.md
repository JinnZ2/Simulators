# GAP: claim refusal is measured only where it is contested

CC0. No rights reserved.

Domain: insurance claim adjudication (auto liability/medical, health, homeowners)
Instrument class: accepted-side measurement — the refused side is either
uncounted or counted only on a self-selected sample.

---

## 0. ANCHOR OBSERVATION

Two series, same carriers, same decade, same filings.

| line | 2016 | 2025 |
|---|---|---|
| auto liability / medical, closed without payment | ~35% | 45% |
| auto collision / comprehensive, closed without payment | ~25% | ~25% |

Physical damage is the held-constant arm. Every line-neutral explanation
for the +10 (intake drift, digital claims rollout, fraud tooling,
reporting-definition change) predicts movement in both arms. Neither moved.

Source: WSJ analysis of NAIC Market Conduct Annual Statement filings, Aug 2026.
The ratio is NAIC's own scorecard Ratio 1. Regulators held the series
for the full decade; it was computed and published by a newspaper.

---

## 1. GAPS

### G-1 First-party / third-party split
CWP is published aggregated across 1P and 3P. The MCAS is filed on a
claimant/feature basis and covers both. The 3P claimant is not the
carrier's customer: no policy to cancel, no renewal to withhold, no
retention metric that degrades on refusal.
**Missing:** CWP disaggregated 1P vs 3P.
**Exists in:** raw MCAS state filings.
**Predicts:** 3P CWP drifts up faster than 1P. Tort states > no-fault states.
Partial corroboration: HI and CA drivers ~2x more likely than MI (no-fault)
to see a claim close unpaid.

### G-2 The uninsured-motorist estimator cannot separate two causes
`UM rate = UM claim frequency / BI claim frequency`
A claimant refused on the at-fault carrier's BI who then files on his own
UM/UIM raises the numerator and lowers the denominator. Refusal-driven
displacement and actual uninsured driving produce the identical reading.
A California DOI audit already listed "higher likelihood of filing a claim
and having it paid" on the UM side as an uncontrolled upward bias — written
before the liability CWP rate moved.
**Missing:** any term separating displacement from non-purchase.
**Note:** UIM (paid-short, not unpaid) rose faster than UM. BI frequency
rose over the same window, which should have pushed the ratio DOWN
mechanically. It rose anyway.

### G-3 Undocumented rebase inside the published series
Same year, different published value across table vintages, identical
footnote, no revision note:

| year | older vintage | newer vintage | delta |
|---|---|---|---|
| 2015 | 13.0 | 11.3 | -1.7 |
| 2017 | 13.1 | 11.6 | -1.5 |
| 2018 | 12.6 | 11.5 | -1.1 |
| 2019 | 12.6 | 11.1 | -1.5 |

All "record high" and "+N points since 2017" claims are computed across the
seam. On the older basis, 1993 (16.0%) exceeds 2023 (15.4%). If the newer
basis runs ~1.5 low, 2023 restated is ~17% and the record is larger than
claimed. Both readings live; the published tables do not permit a choice.
**Missing:** methodology note for the revision.

### G-4 Payment re-routed through litigation is not netted out
MCAS counts "lawsuits closed with consideration for the consumer" in a
separate field from "claims closed with payment." A claim refused at claim
stage and paid through suit need not appear as paid.
Litigation rose 10% -> 18% of claimants (2017-2022) against a ~10 point
CWP move. Same order of magnitude. Never subtracted.
**Missing:** carrier-level correlation of delta-CWP against
delta-lawsuits-closed-with-consideration.

### G-5 [PRIMARY] The refusal error rate is estimated from a <1% self-selected sample

| measure | value |
|---|---|
| NY external review, overturn rate | 46.7% (2019-2025) |
| NY trend | 38% (2019) -> 52.5% (2025) |
| NY home health care claims | 78.4% overturned |
| ACA internal appeal, overturn | ~44% |
| Medicare Advantage, all claims | 17% denied, 57% overturned |
| MA prior-auth, appealed | ~82% overturned |
| **appeal rate, ACA and PA** | **under 1%** |

Roughly half of the refusals that get checked were wrong. Under one percent
get checked. No instrument in any line samples the unchecked remainder.
The overturn rate rising while the appeal rate stays flat under 1% has no
benign reading: the decisions being reviewed got worse and the review
volume that would have registered it did not follow.

**Missing:** a random-sample audit of UNAPPEALED refusals in any line.
Everything published about wrongful-refusal rates is conditioned on
someone having contested.

### G-6 The pre-instrument regime has no reading, not even zero
Before compulsory insurance, settlement ran person-to-person, enforced by
license and registration suspension against an at-fault driver who did not
pay (still on the books in the WI Safety Responsibility Law). Direct
settlement generates no BI claim and no UM claim: both terms of the
estimator are zero. Wisconsin was the 49th state, June 2010; Illinois
finalized 1990; New Hampshire never.
Therefore the "uninsured motorist problem" appears in the data at the moment
the instrument is installed. There is no missing pre-1992 series to recover.
**Missing:** nothing recoverable. Recorded so nobody spends effort
reconstructing a series that cannot exist.

### G-7 No series exists for carrier-side noncompliance
Driver noncompliance is counted, penalized per instance, and enforced by
seizure of a state-granted privilege. Carrier refusal error is not counted,
carries no per-claim penalty, and the equivalent privilege — certificate of
authority to write in the state — is effectively never pulled over claims
practice. The overturn is the entire remedy and costs the carrier only the
amount already owed.
**Missing:** any published rate of carrier noncompliance comparable to the
uninsured-driver rate. The asymmetry is in enforcement, not in contract.

---

## 2. EXPERIMENT DESIGNS

### E-1 (closes G-5) Blind audit of unappealed refusals
- Sampling frame: one state DOI, closed-without-payment liability/medical
  files, one plan year.
- Draw a random sample stratified by carrier and coverage.
- Route each file to independent reviewers blind to carrier identity and
  to the original determination, applying the policy language only.
- Output: wrongful-refusal rate on the UNAPPEALED population.
- Contrast against the appealed-population overturn rate for the same
  carrier-year.
- Discriminates: is appeal selective on merit (unappealed rate << appealed
  rate) or on capacity (rates converge)? Convergence means the published
  overturn statistics understate total wrongful refusal by ~100x volume.

### E-2 (closes G-1) MCAS disaggregation
- Data request to participating state DOIs for CWP split 1P/3P by carrier.
- Regress CWP on: tort vs no-fault, UM/UIM mandate, minimum limits,
  carrier, year.
- Null: no 1P/3P differential after controls.

### E-3 (closes G-4) Litigation re-routing
- Carrier-year panel: delta-CWP against delta-lawsuits-closed-with-
  consideration-for-the-consumer, both from MCAS.
- Estimate the share of the +10 point CWP move that is payment channel
  substitution rather than refusal.
- Null: no correlation; the CWP move is entirely non-litigated.

### E-4 (bounds G-2 displacement) Health-side absorption
- Health plan claims with auto-accident etiology where no subrogation
  recovery was made (no settlement occurred).
- Trend against auto liability CWP by state and year.
- Estimates the magnitude of cost moved from auto to health, which appears
  in neither line's refusal statistics.

### E-5 (closes G-3) Series reconstruction
- Recompute the UM/BI ratio from raw carrier frequency data on one
  consistent basis across the full published span.
- Report the two vintages against the reconstruction.

---

## 3. STANDING SHAPE

The measured side is a SELECTED side. Confidence rises as coverage falls:

- accepted-side metrics improve as marginal risk exits
- refusal error is estimated only from contested cases
- the population that absorbs the cost silently is, by construction, the
  population that generates no record

Sibling markers: survivorship metrics in safety reporting (falling report
volume read as improved safety culture); surplus-lines displacement as the
shadow indicator for commercial declination.
