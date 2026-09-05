# RESULTS — steady-state reproduction, Huascarán CH4

Attaches to: MARKER_archive_siting_bias.md, earth-systems-physics
Source under reproduction: Lamantia et al., Nature 2026,
  doi 10.1038/s41586-026-10938-1; Zenodo 10.5281/zenodo.18657346
Opened: 2026-09-04

Split rule applied here: a finding that is DEMONSTRATED from the
published Methods folds into RESULTS. A finding that requires the
Zenodo code to separate stays OPEN. Two fold in, one stays out.

---

## R-1 — POLAR-ONLY BASELINE REPRODUCES

```
model      four-box steady state, rebuilt from published Methods
           (container had no network; no code from the archive used)
result     tropics source  163.1 Tg/yr   vs published 163
           attenuation A   0.774          vs published 0.765
status     REPRODUCED
```

This is what licenses R-2 and R-3 below. A discrepancy found by a model
that cannot reproduce the baseline is a discrepancy in the model.

---

## R-2 — UNITS LABEL IN METHODS IS WRONG (folded in)

```
as published   "transport exchange rates of 0.22/0.45/0.45 years"
read as TIMES  tropics -> 134 Tg/yr, and SH goes NEGATIVE
read as RATES  (1/yr; i.e. 4.5 yr and 2.2 yr) -> baseline reproduces
finding        the quantities are rates in 1/yr. The unit word is
               wrong; the numbers are right.
falsifier      any reading as times that reproduces 163 Tg/yr
status         DEMONSTRATED — reproduced from published values alone
```

Note the discriminator: the times-reading does not merely produce a
different answer, it produces a NEGATIVE source. That is a sign error,
not a calibration difference, so the units question is settled without
needing the archive.

### Script — units_test.py
```
input     the four-box steady state, both readings of 0.22/0.45/0.45
output    table: reading | tropics Tg/yr | SH Tg/yr | reproduces 163?
assert    times-reading yields SH < 0
assert    rate-reading yields tropics within 0.5 of 163
```

---

## R-3 — THE Tg COLUMN UNDERSTATES THE CONCENTRATION MOVE (folded in)

```
published    interpolated TN box 82 -> 88 Tg/yr with SCA  (+7%)
inversion    reproducing TN = 88 requires C_TN = 733 ppb
             — ABOVE both polar records, and 13 ppb under SCA
consequence  a +49 ppb concentration move appears in the table as
             +6 Tg/yr, because the 6-yr lifetime scales loss with
             concentration
reading      TN is not an interpolation between the poles under the
             +SCA run. The emission column compresses how far the
             neighbour box has to move.
falsifier    a C_TN at or between the polar records that yields
             TN = 88 under the published lifetime
status       DEMONSTRATED — inversion runs on published values
```

Bearing on the marker: this is the siting-bias shape appearing inside
the paper's own accounting. The unseen box moves further than the
reported quantity shows, because the reported quantity is downstream
of a loss term that scales with the thing being reported.

### Script — tn_inversion.py
```
input     published TN = 88 Tg/yr, tau = 6 yr, box structure as R-1
method    solve for C_TN
output    C_TN, its position relative to GISP2 / NEEM / Law Dome /
          WAIS / SCA, and dE/dC at that point
assert    C_TN falls outside the polar bracket
```

---

## OPEN — NOT FOLDED IN

```
FINDING 3   with C_TS = SCA and C_SH = WAIS, implied E_SH = -10.8
            against a hard-fixed +10 — a ~21 Tg/yr residual against
            a +50 Tg/yr headline. The paper reports SH uncertainty as
            +/-0% because the term is hard-capped.

why open    steady-state vs their transient run may absorb some or
            all of this. Not separable without the archived code.
            A residual that a known structural difference could
            produce is not yet a finding.

test        re-run the Zenodo model, transient, with SCA as a SOFT
            prior rather than prescribed. That run separates two
            things at once: the steady-state/transient question here,
            and the TS solved-vs-prescribed confound already logged
            in the marker.

status      OPEN, with a named test and a named blocker
```

Handling while open: R-3 may be cited; FINDING 3 may not be cited as
a discrepancy in the paper. It is a residual in a reduced model, and
the reduction is ours.

---

## WHAT THIS SECTION DOES NOT CLAIM

No position on the paper's headline result. The siting-bias conclusion
is not under attack here — R-2 and R-3 are both internal-consistency
findings, and R-3 in particular makes the siting effect look LARGER in
concentration space than the emission table shows.
