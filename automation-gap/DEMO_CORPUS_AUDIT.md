# DEMO CORPUS AUDIT — 16 automation demos/deployments through the harness
### Run 2026-09-24. Corpus curated from documented reporting; method below.

**Sampling declaration (load-bearing):** this is a CURATED corpus, not a sample. Every rate
below is a property of these 16 records, not of "demos" in general. The corpus is itself
event-sampled: demos are published when impressive, so the population this corpus was drawn
from is already the flattering tail.

**Record discipline:** ABSENT means the record does not carry the information. ABSENT is a
property of the record and is a finding in itself — an audience cannot verify what was never
disclosed. No absence was filled by inference.

## The six checks

1. **teleop_disclosure_upfront** — autonomy status declared *at demo time*, not after being caught
2. **success_or_intervention_metrics** — completion rate / interventions-per-hour published
3. **repetitions_under_variation** — task repeated under changed conditions
4. **envelope_declared** — task/environment bounds stated by the presenter
5. **independent_evaluation** — any third party measured it
6. **sustained_runtime_evidence** — hours/days of operation, not a single take

## Results matrix

| Demo / deployment | teleop | metrics | variation | envelope | independent | sustained |
|---|---|---|---|---|---|---|
| Optimus @ 'We, Robot' (2024-10) | **FAIL** | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |
| Optimus kung fu (2025-10) | PASS | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |
| Optimus @ 'Autonomy Visualized' (2025-12) | **FAIL** | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |
| Optimus @ Tesla Diner (2025-07) | **FAIL** | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |
| Figure 02 @ BMW, 11 months | PASS | PASS | ABSENT | PASS | ABSENT | PASS |
| Figure 03 @ BMW sequencing | ABSENT | ABSENT | ABSENT | PASS | ABSENT | ABSENT |
| Digit @ GXO Spanx | PASS | PASS | ABSENT | PASS | ABSENT | PASS |
| Apollo @ Mercedes | ABSENT | ABSENT | ABSENT | PASS | ABSENT | ABSENT |
| Atlas @ CES 2026 stage | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |
| Hyundai 25–30k Atlas plan | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |
| 1X NEO home robot | PARTIAL | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT |
| World Humanoid Games 2025 | PASS | ABSENT | ABSENT | ABSENT | PASS | ABSENT |
| Aurora driverless launch | PASS | PASS | ABSENT | PASS | ABSENT | PASS |
| Stretch box-unloading fleet | PASS | PASS | ABSENT | PASS | ABSENT | PASS |
| Komatsu FrontRunner AHS | PASS | PASS | PASS | PASS | PASS | PASS |
| Ag-harvest field studies (77-study review) | PASS | PASS | PASS | ABSENT | PASS | ABSENT |

## Distribution (corpus property, declared frame)

| Check | PASS | PARTIAL | FAIL | ABSENT |
|---|---|---|---|---|
| teleop disclosed upfront | 8 | 1 | 3 | 4 |
| metrics published | 6 | — | — | 10 |
| repetitions under variation | 2 | — | — | 14 |
| envelope declared | 7 | — | — | 9 |
| independent evaluation | 3 | — | — | 13 |
| sustained runtime | 5 | — | — | 11 |

## Findings

**F1 — Exactly one record passes all six checks: the 20-year-old mining system.**
Komatsu FrontRunner AHS (private roads, decades in service, third-party documented) is the
only 6/6. Every humanoid record fails at least three. The most autonomous thing ever
deployed at scale is a truck on a private mine road — not anything with legs.

**F2 — The corpus splits into two failure classes, not one.**
*Demo class* (stage, hospitality, home): zero metrics, zero envelopes, teleop disclosed
late or never. All three outright teleop-disclosure FAILs are one vendor's, including an
event literally named "Autonomy Visualized" where the robot fell backward while reportedly
teleoperated. *Deployment class* (Figure 02, Digit, Aurora, Stretch): real metrics and
declared envelopes — but every metric is **vendor-self-measured** (independent evaluation:
0 of 4) and every deployment is **one task type** (variation: 0 of 4).

**F3 — The strongest ledgers are single-task by construction.**
Digit's 100,000 totes / 65,000 fleet hours and Figure's 90,000 parts / 1,250 hours are real,
SEC-adjacent numbers — for tote transfer and sheet-metal insertion respectively. The audit
cannot extend them one inch past the task that produced them. "General-purpose humanoid" is
a claim; the measured record is single-purpose machines, several of them genuinely good ones.

**F4 — The one fully independent observation in the corpus is the Games.**
The 2025 World Humanoid Robot Games (live, unedited, multi-vendor) is the only humanoid
record with independent evaluation — and it produced crashes, missed punches, and constant
staff intervention. Independent measurement and flattering outcome have not yet co-occurred
in this corpus.

**F5 — Plans are not deployments.** The largest numbers in the corpus (Hyundai's 25–30k
units/year, Tesla's 15k units) exist only in investor materials. The harness scored them
ABSENT on every check, which is the correct treatment: a forecast carries no observational
weight.

## New falsifiers

```
AUT-F5  Single-task confinement: every metric-carrying humanoid deployment
        is one task type (2026 corpus)
        Refutes if: any humanoid deployment publishes success/intervention
        metrics across >=3 distinct task types at one site, sustained
        >=6 months, by 2028
AUT-F6  Independence gap: 0 of 4 metric-carrying deployments third-party measured
        Refutes if: a customer (not vendor) publishes audited uptime,
        intervention rate, and cost-per-cycle for a humanoid deployment
        by 2028
```

## Cross-links

- F4 is the instrument-bias S1 shape: the demo corpus is event-sampled; the Games are the
  only record with a null baseline (everyone performed, not just the edited highlight).
- F2's deployment class matches the automation gap audit's shared-node conclusion: the
  envelope is real and the doers staff its edges.
- AUT-F1 (12% sim-to-real) is consistent with this corpus: no demo record carries evidence
  that would refute it.
