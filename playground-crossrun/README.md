# playground-crossrun

Status: STEP 1 of `WORK_ORDER.md` run. Steps 2 and 3 are not started (step 2 waits on
review of this report; step 3 waits on step 2). Neither playground's code is edited, and
`run_all.py` checks that at the end of every run. Every case is constructed by its own
playground; nothing here is a measurement of any physical system.

```text
study-aperture/experimental/playground  (Perplexity, merged, rev b9dbdef)
Simulators/relational-playground        (#257 draft, rev beac98b)
        |                                   |
        |  both ship a package named `playground` -> one process can load one of them
        v                                   v
 export_perplexity.py                 export_257.py          each runs inside its own playground,
   (cases captured on the way          (gate fixtures by      writes plain JSON to out/
    into each planted defect's          the gate's own seed,
    own gate: nothing retyped)          forest runs re-integrated)
        |                                   |
        +---------------> feed_into_257.py   feed_into_perplexity.py <---------------+
                          (the other side's public objects only; every translation
                           choice listed per row in `mapping`)
                                    |
                                    v
                              compare.py --> out/crossrun.json + STEP1_REPORT.md (generated)
                              axis map for #257 readings is THIS cross-run's, PROPOSED
```

Run: `python3 playground-crossrun/run_all.py` (about 50 s; `STUDY_APERTURE_PATH` points at a
study-aperture checkout, default `../study-aperture`). Tests:
`python3 -m unittest discover -s playground-crossrun/tests`.

## 1. Baseline (each playground's own checks, as-is)

```text
study-aperture  python3 -m playground.self_check
                guards 10/10 | planted defects 20/20 caught, 20/20 correctly classified
                controls 14/14 | 12 unit suites, 503 tests | COMBINED SELF-CHECK PASSED, exit 0
#257            python3 -m unittest discover -s tests
                43 tests, OK, exit 0
```

## 2. Disagreement table by code

138 cases: 78 study-aperture cases fed into #257, 60 #257 cases fed into study-aperture.
One code per case, with a precedence (ADAPTER > MISSED > NO_SLOT > MISCLASSIFIED > AGREE).
NO_SLOT outranks a reading comparison because a reading reached without the deciding concept
agrees or disagrees by accident; the `readings` column keeps what the readings did anyway.

```text
direction   ADAPTER  MISSED  NO_SLOT  MISCLASSIFIED  AGREE  total
P->257          4       3       59          0          12     78
257->P         19       1       30          0          10     60

NO_SLOT rows, readings anyway:  MISSED 39 | AGREE 7 | MISCLASSIFIED 2 | no reading 41
```

Zero rows code MISCLASSIFIED, and that is the shape of the result rather than an absence of
disagreement: every axis disagreement found sits on a concept #257 lacks, so it codes NO_SLOT
first. The two MISCLASSIFIED-under-NO_SLOT rows are the clearest:

```text
case                            study-aperture                        #257 (mapped)
model-conservation-violation    PHYSICAL failed  (DETERMINATION ok)   LEAK -> INCOMPLETE -> determination:failed
measured-imbalance-unresolved   PHYSICAL + INSTRUMENT indeterminate   LEAK -> INCOMPLETE -> determination:failed
deciding concept, absent in #257: declared_complete + value provenance at the closure gate
```

Per-case table, every row with its note: `STEP1_REPORT.md` section 2.

## 3. What the cross-run found, by where it sits

### In #257 (from study-aperture's cases)

```text
F1  ADAPTER  clean instrument UNTRUSTED  -- the gate's 'coef' plant scales a flux, so it is blind on
             any case whose required flux is zero. A static instrument has no start state in a
             dynamic-model gate; the adapter supplies one:
               y0 = -1  PASS (TP 1.00)     y0 = 0  MISSES (TP 0.83)     y0 = 1  MISSES (TP 0.83)
             The verdict on a correct instrument moves with a value nobody measured.
F2  MISSED   certify_tool divides by len(signals): a null-only harness, an empty ladder and an
             all-undetectable ladder raise ZeroDivisionError (3 cases). No record is produced.
             study-aperture reads each as INDETERMINATE / INSTRUMENT failed.
F3  AGREE    a wrong instrument, a blind one and a noisy one are all caught -- and #257 names the
             DETECTOR (CONSTANT_FIRES, CONSTANT_SILENT), not the instrument. The axis agrees only
             through the mapping.
F4  NO_SLOT  trust is keyed by model name; a model certified once reads TRUSTED in any system.
             study-aperture refuses both transfers it tests (diagnostics, calibration).
F5  NO_SLOT  13 of 15 measurand cases open a coincidence card, including all 8 that study-aperture
             VOIDs as different measurands: #257 reads equal numbers as agreement to explain.
F6  NO_SLOT  distribution-to-mean: interval [0, 4] contains both mean^2 = 1 and E[X^2] = 2; nothing
             flags the loss (12 of 14; 2 ADAPTER, weights unknown / zero mass).
F7  NO_SLOT  ABSENT_AT_SENSITIVITY(0.1) is accepted where the effect of interest is 0.01 and where
             the conditions do not match -- the value holds one number, no effect size, no scope.
```

### In study-aperture (from #257's cases)

```text
F8  NO_SLOT  forest run 9 port closes in both (misclosures recomputed bit-identically), and
             study-aperture reads all three clean runs DETERMINATION indeterminate:
             L0_INTERVENTION_REGISTRY_EMPTY. #257 records no registry. With every flux
             self-registered (circular, kept as a contrast arm) it reads ok.
F9  NO_SLOT  the planted leak lands on DETERMINATION failed (L0_ACCOUNTING_GAP) as stated and on
             PHYSICAL failed (L0_CONSERVATION_VIOLATION) when the ledger is declared complete.
             The leak IS a model defect by construction, so PHYSICAL is the right axis -- reached
             only under the circular arm. #257 reads INCOMPLETE either way.
F10 MISSED   an UNKNOWN with no exit stated is accepted (expiry_triggers = ()). #257 refuses it.
             The one case study-aperture misses.
F11 ADAPTER  all 12 percolation gate fixtures are refused by FiniteGraph (<= 32 nodes, <= 12 edges);
             the smallest #257 grid, 4x4, needs 16 nodes and up to 24 bonds. Site percolation with
             spread and spotting also has no slot in a static bond graph.
F12 AGREE    9 of 12 branching fixtures compute in the gated backend and match n0*R^n and the
             cumulative count exactly -- circular, since the plan's known answer IS #257's closed
             form. All 9 stay provisional (APP_UNRESOLVED): no #257 run carries applicability.
F13 ADAPTER  the other 3 hit two bounds that fail on two axes: founders > 4 reads outside-domain
             (determination ok, run blocked); population > 128 reads DETERMINATION failed
             (EQ_PLAN_OR_INPUT_BINDING). One kind of refusal, two axes.
F14 ADAPTER  Poisson die-out (unbounded support) and free-text expiry (typed triggers) cannot be
             entered without an interpretation the adapter does not make.
F15 NO_SLOT  21 coincidence cards, 3 claim tags, the one-change branch rule: no object.
```

### Agreements that hold (each carries a coincidence card, `STEP1_REPORT.md` section 3)

```text
continuity  5 of 5 cells agree (continuous / return-with-reconfiguration / drift-with-stable /
            discontinuous / indeterminate). PROVISIONAL, two causes standing:
              shared source  -- SPLIT BY LEVEL (ORIGIN_NOTE.md, operator statement, CARRIED):
                                concept level  possible shared cue (the s-a work order names a
                                               continuity layer)
                                split level    independent convergence -> anchor CANDIDATE
                                               (system-vs-configuration split is in SPEC_GPT.md,
                                               which the s-a builder did not receive)
              construction   -- the #257 system criterion was supplied by the adapter, so the
                                configuration axis carries the cleanest convergence
L0          balanced ledger passes in both; incomplete-ledger gap agrees on the surface only.
            shared constraint (closure arithmetic) + vocabulary echo (both call it 'L0')
absence     missing return observation -> NOT COMPARABLE / indeterminate; no sensitivity ->
            refused / indeterminate. Same refusal, different form (raise vs record).
observer    regimes undeclared -> #257 refuses the comparison; study-aperture reads the context
            UNKNOWN. This AGREE is on the single applicability OBSERVER coordinate. The regime
            partition itself is NOT scored: study-aperture observation/{passive,perturbative,
            strategic}.py are stubs. Names: 2 of 3 align; REACTIVITY (#257) vs PASSIVE (s-a) are
            different partitions, both recorded, not merged. Shared source UNDETERMINED.
```

## 4. Concept map

41 concepts, every location checked by the test suite (file exists, token present).

```text
present in both   18
VOID in #257      15   failure axes, axis statuses, intervention registry, declared-complete,
                       value provenance at L0, trust scope, detection limit, scoped absence,
                       stale reliance, reevaluation, two tracks, claim record, measurand identity,
                       denominator binding, distribution-to-mean loss
VOID in s-a        8   VOID budget with reason, FP/TP harness class, UNKNOWN refused without an
                       exit, one-change branch, claim tags, coincidence card, uncertainty
                       propagation (deliberately not done), pre-registration
```

Full table: `STEP1_REPORT.md` section 4; source `adapters/concept_map.py`.

## 5. Anything off

```text
O1  the axis map for #257 readings is this cross-run's (STEP1_REPORT.md section 5). Every AGREE and
    every MISCLASSIFIED across the axis boundary depends on it. #257 has one run status, so the map
    reads INCOMPLETE as DETERMINATION and UNTRUSTED as INSTRUMENT. Step 2 should decide it, not inherit it.
O2  the work order's NO_SLOT example undersells the gap: #257 has no failure axes at all, not just no
    instrument/determination split.
O3  #257 runs 6-8 originals are not filed (code void); only the run 9 port was fed.
O4  the pinned part1.json prints fluxes at 6 significant figures, too coarse for a 1e-9 closure test;
    the forest runs were re-integrated through #257's own runner (no file written) and the
    recomputed misclosures match the pinned ones exactly.
O5  study-aperture's cross-system classes were fed as its two transfer guards, not as five runs; the
    five constructed classes are bound to its own equation registry and have no #257 form.
O6  GAP_INSTRUMENT_CRASH / _UNRECOGNIZED_LABEL (step 3) occur in neither tree; F2 is the nearest
    thing in either playground to an instrument crash, and #257 records none.
O7  shared source: #257 files its brief, study-aperture's tree records none. ORIGIN_NOTE.md (operator
    statement, 2026-11-11) supplies it afterwards: the s-a builder got chat-side work orders only, not
    SPEC_GPT.md. Continuity cards now split by level; the observer card stays UNDETERMINED.
    Rule for future cross-builds: record each builder's input brief at build time.
```

## Layout

```text
WORK_ORDER.md            the order, verbatim
COMBINED_SPEC.md         STEP 2, CONFIRMED 2026-11-11, not built: axis mapping, gate order, provenance, Q&A log
ORIGIN_NOTE.md           builder input briefs (operator statement, verbatim) and what it moved
STEP1_REPORT.md          generated by adapters/compare.py; do not edit
run_all.py               baselines + both exports + both feeds + compare + untouched check
adapters/common.py       paths, JSON exchange, git checks (imports neither playground)
adapters/export_*.py     each side's own cases and readings
adapters/feed_into_*.py  the other side's cases through this side's public objects
adapters/compare.py      codes, coincidence cards, report (imports neither playground)
adapters/concept_map.py  concept -> location in each playground, or VOID
out/                     pinned JSON from the last run
tests/test_crossrun.py   code precedence, pinned findings F1-F13, concept-map resolution,
                         report regeneration, originals untouched
```

Stdlib only, parses under 3.9, CC0.
