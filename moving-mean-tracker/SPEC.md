# SPEC (delivered verbatim, 2026-10-08)

The text below is the operator's spec as delivered. It is not edited.

```text
MOVING-MEAN TRACKER — spec (PROPOSED)

SCHEDULE   fixed interval (e.g. quarterly), declared up front;
           every run appended, never overwritten

SEGMENTS   declared before the first run, per domain:
           income/wealth band · region · connectivity tier ·
           occupation (desk vs hands-on) · access to AI tools
           segment definitions frozen; changes = new dated version

PER RUN, PER SEGMENT
           sample n (declared) with provenance per record:
             source · pull date · query · filters applied ·
             anything dropped as "noise" + rule that dropped it
           compute: mean · median · p10 · p90 · mean−median gap
           representation: segment share of sample vs share of
             population (named reference source + date)

TRACKED SERIES (the gauges)
  G1 mean−median gap over time        → tail pull on the reference
  G2 segment share vs population      → access-gate loop running
  G3 dropped-as-noise share by segment → cleaning as class filter
  G4 same metric in physical units vs dollars → token drift vs real

CANDIDATE DOMAINS (sources to confirm before use)
  income/wealth (distributional accounts) · adult literacy and
  skills surveys · training-text snapshots (filtered vs unfiltered)

RULES
  segments + metrics declared before run 1 · every dropped record
  logged with its rule · reruns compare like with like (same
  segment definitions) or say they don't
```
