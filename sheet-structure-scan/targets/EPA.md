# TARGETS — three EPA workbooks, pre-registered

Dated **2026-08-25**, before any of the three files was opened.
Runnable form: `targets/epa_check.py`. CC0.

---

## The targets, as handed over

| key | workbook | structure, as described |
|---|---|---|
| `local` | EPA Local GHG Inventory Tool | a live interactive workbook — sector calculators with real formula chains, community and government-operations modules |
| `efh` | EPA GHG Emission Factors Hub | almost entirely terminal constants by design; every factor a hardcoded number, with variance and provenance in a separate document |
| `simplified` | EPA Simplified GHG Emissions Calculator | smaller; a first run |

The Hub arrived with a standard attached: **if the scan does not light
that up, the scan is broken.** That is the right standard and it was not
yet a measurement, because *light up* had no value. §3 fixes one per
target per readout.

---

## 1. NOT RUN — the host is blocked

```
2026-08-25T15:14:12.787Z  connect_rejected  www.epa.gov:443
2026-08-25T15:14:13.079Z  connect_rejected  www.epa.gov:443
2026-08-25T15:14:13.354Z  connect_rejected  www.epa.gov:443
  gateway answered 403 to CONNECT (policy denial or upstream failure)
```

DNS resolves normally (`www.epa.gov` → `d32i4z0dxazdtp.cloudfront.net`,
eight AAAA records), so this is an egress policy denial and not a network
fault. The proxy README's instruction for a 403 is to report the blocked
host and not route around it, and that is what happened: three attempts,
one per target page, no retries, no alternate route.

**Nothing below is a reading of an EPA product.** Every number in
`epa_check.py --selftest` comes from two synthetic workbooks written here
to test whether the criterion can separate the two shapes at all.

---

## 2. THE PAIR IS THE TEST, NOT EITHER WORKBOOK

A Hub run alone cannot separate two hypotheses:

- the scan works, and the Hub is a flat table of terminal constants
- the scan reports every workbook as a flat table of terminal constants

They predict the same output. **The Local Tool is the discriminator.** If
a workbook of live sector calculators returns the same profile, the scan
is the thing being measured, and the Hub result carries nothing.

So `epa_check.py --check` scores one target and ends every report with
the sentence saying so. The instrument is not called until both arms are
in. The Simplified Calculator is a third point and is not the control.

---

## 3. PREDICTIONS

Frozen before any target file was opened. `patterns.json` was edited
earlier the same day — the loose generic parenthetical rule removed, and
energy and fuel units added — and that edit is recorded in its own
`_note` with its direction stated: **widening the unit list makes
`EFH-P3a` easier to satisfy, and no edit to that file can make the
variance or sample-size patterns fire.** So `EFH-P3b`/`P3c` — and the
differential between them and `P3a` — are the load-bearing part.

### `efh` — Emission Factors Hub

| check | readout | predicted | why |
|---|---|---|---|
| EFH-P1 | `derived_share` | < 0.05 | the stated design is hardcoded numbers |
| **EFH-P2** | `rank_zero_share` | **> 0.95** | a workbook of terminal constants has nothing downstream of anything, so `deps × ddepth` is zero almost everywhere and **the rank column carries no ordering.** This is the readout the target was handed over to test |
| EFH-P3a | `unit_present` | > 0.70 | an emission factor without a unit is not a factor, and the units are in the headers |
| EFH-P3b | `variance_present` | < 0.10 | the stated design puts variance in a separate document |
| EFH-P3c | `sample_present` | < 0.10 | same, for the sample size behind each factor |
| EFH-P4 | `listed_col_share` | < 0.10 | repeated headers across sheets all govern constants at depth zero, so they agree and are counted rather than listed |

### `local` — Local GHG Inventory Tool

| check | readout | predicted | why |
|---|---|---|---|
| LOC-P1 | `derived_share` | > 0.20 | live calculators |
| **LOC-P2** | `rank_zero_share` | **< 0.95** | the arm that decides whether EFH-P2 measured the Hub or measured the scan |
| LOC-P3 | `max_pdepth` | > 2 | sector calculators chain through intermediates |
| LOC-P4 | `listed_col_count` | > 0 | the same label carried by a community sheet and a government-operations sheet at different constructions is the case scan three was built for |

### `simplified` — no threshold registered

Deliberately. No structural description was given beyond its size, and a
threshold guessed from that is a number dressed as a prediction. The
profile is reported and nothing is scored. It is the first run.

### Reported and NOT predicted

`date_present`. The Hub is versioned by year and its provenance is
described as living in a separate document, so whether a vintage sits
inside a factor's neighborhood is exactly the open question — and
registering a threshold for it would be picking the answer. It prints.

---

## 4. THE CRITERION HAS BEEN NULL-TESTED, AND IT FOUND TWO DEFECTS

`--selftest` builds two synthetic workbooks — a flat two-sheet reference
table, and a three-sheet chain of calculators — and requires the
criterion to separate them. A criterion returning the same verdict for
both is not a measurement of either, and that is checkable without
leaving the room.

It does separate them: the flat shape holds 6 of 6 `efh` predictions and
fails `LOC-P1`/`LOC-P2`; the chain shape holds 4 of 4 `local` predictions
and fails `EFH-P1`/`EFH-P2`.

Building it turned up two defects, both of which would have produced a
false reading on the real Hub:

**(1) `EFH-P4` passed on an empty denominator.** A share needs its
denominator to exist. On a single-sheet workbook no label can appear
twice, `groups_ge2_col` is zero, and `listed_col_share < 0.10` was
satisfied by a result set with nothing in it — a predicate that returns a
pass on an absence, which this repository recorded as `PCH_001` in
another folder and reached again here. Fixed: shares carry a declared
denominator field and return `NOT_DETERMINABLE` when it is empty. Both
branches are pinned.

**(2) Scan three listed every shared header on a difference in TABLE
HEIGHT.** Two flat sheets carrying the same headers over twelve and nine
rows returned constructions `12c` and `9c`, which differ, so **five
column collisions were listed on a fixture where nothing collides** —
and the Emission Factors Hub is exactly that shape, many sheets sharing
headers over different numbers of rows. It would have lit up, with a rank
beside it, and read as a finding.

The delivered spec asks *whether* the cells are constants versus derived.
**Whether is a set.** The listing decision now takes the kind set
(`c` / `d` / `c+d`); the counts stay in the printed column, so nine
constants and one formula still reads differently from ten constants —
the distinction the composition was for. Recorded as `SSS_011`.

This is what the target was worth before it arrived.

---

## 5. ONE CONTINGENCY WORTH NAMING

If a target ships as legacy `.xls` (BIFF) rather than `.xlsx`/`.xlsm`,
`sheetmodel.read()` raises rather than guessing:

> no reader for .xls. The declared budget allows ONE spreadsheet reader
> beyond stdlib and it is unspent: install it and wire it here rather
> than widening this module.

That is the moment the one-reader slot gets spent, and it will have been
spent for a format the standard library cannot open rather than for
convenience — which is the test `SSS_001` names for itself.

---

## 6. HOW TO RUN IT

```
python3 targets/epa_check.py --predictions
python3 targets/epa_check.py --selftest
python3 targets/epa_check.py --check LocalGHGInventoryTool.xlsm --as local
python3 targets/epa_check.py --check GHGEmissionFactorsHub.xlsx   --as efh
python3 targets/epa_check.py --check SimplifiedGHGCalculator.xlsx --as simplified
```

Then the full tables:

```
python3 scans.py three GHGEmissionFactorsHub.xlsx
python3 scans.py two   GHGEmissionFactorsHub.xlsx --flags FLAGS.txt
```

`--check` chooses its own flag set — numeric constants that are not
labels — and prints that rule into the report. That is a **declared
sample, not scan one**: `SSS_003` measured what `--all` does to the
composition, and a stated sample rule is the honest middle. Scan two
proper still refuses to run without a flag list.
