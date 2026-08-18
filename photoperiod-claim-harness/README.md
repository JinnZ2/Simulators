# photoperiod-claim-harness

CC0-1.0. stdlib only. One file. Runs on a phone.

```
python3 photoperiod_claim_harness.py run-all
python3 photoperiod_claim_harness.py claims
python3 photoperiod_claim_harness.py sweep S2
python3 photoperiod_claim_harness.py protocol
python3 photoperiod_claim_harness.py pending
python3 photoperiod_claim_harness.py log
```

## Reading protocol

This is a marker for a sensed shape that needs more exploration. It is not a
thesis and not a refutation of any publication. Test whether it fits, extend
it, or report where it breaks. A break is a measurement and goes in the claim
table.

Legibility is not confidence. The write-up may not match practice.

## The one hard rule

When a sim contradicts a claim: **update the claim, never retune the sim.**

A sim may only change through `MechanismEdit`, which requires a named physical
mechanism, an independent basis for it, and a prediction registered *before*
the run. The class refuses edits justified by outcome. Unrun candidates sit in
`PENDING_EDITS` rather than being quietly applied.

## Structure

```
CLAIM_TABLE   falsifiable predicates over sim output
  C1 -> S1    mass / denominator: is the reported signature diagnostic?
  C2 -> S2    can dark intervals raise Chl at EQUAL photon dose?
  C3 -> S2    is there a dark-interval crossover?
  C4 -> S3    can a reflectance index rise while true Chl falls?
  C5 -> S4    does channel count remove common-mode bias?

SIMS          declared mechanisms, no fitted parameters
  S1  volume / wall-density / water, four named mechanisms
  S2  Pchlide pool with FLU clamp + enzyme-saturated POR conversion
  S3  closed-loop controller maximising an index it can see
  S4  common-mode bias vs channel count

HARNESS       run -> provenance record -> residual router -> hypothesis block
              JSONL log carries file hash, params, status, reasoning
BENCH         each claim mapped to a physical measurement and its kit
```

Provenance never merges: `REPORTED`, `PHYSICS`, `SIM`, `BENCH`. `BENCH` is
empty until someone runs one.

## What the current run says

Not a verdict. A trajectory, at the parameters declared in the file.

- **C1 REFUTED.** 58 of 75 grid cells reproduce the reported side-effect
  signature (fresh mass held, wall density down, water fraction up, juice up).
  Across those cells, true energy-per-dry-gram spans about 4.9x. The reported
  metrics do not pin down the real efficiency. Dry mass is the missing
  measurement.
- **C2 REFUTED.** Continuous light wins at equal photon dose. The FLU clamp
  acts on *pool size*, so a full Pchlide pool slows its own synthesis; draining
  it continuously maximises flux. Pool-charging does not explain a dark-induced
  chlorophyll gain. Named unrun candidate: shade acclimation.
- **C3 REFUTED.** No crossover in this regime; dark is monotonically worse
  under C2's mechanism set.
- **C4 REFUTED.** Index and true chlorophyll moved the same direction here.
  Measurement artifact alone did not reproduce the signature.
- **C5 SUPPORTED.** 49 channels gave no error reduction against a shared bias.
  Independence lives in the calibration path, not in N.

Two of these came out against the direction the sims were built to explore.
Both stayed. That is the protocol working.

## Extending

Add a claim: append to `CLAIM_TABLE` with a predicate that can fail.
Add a mechanism: `MechanismEdit(sim_id, mechanism, basis, prediction, affects)`,
then `.settle(observed)`. Both write to the log.
Add a bench row: append to `BENCH` so the sim claim has a physical exit.
