---
file_role: navigation
source: claude
original_filename: README.md
summary: Landing page for the incentive-blindspot-sim folder. Routes to the artifact, the claims, the development record, and the license.
---

# incentive_blindspot_sim

A physics-grounded, falsifiable model of how an institution's incentive
structure drives it toward the failure it claims to prevent. Not an
argument — a mechanism you can execute.

## Read first

[`sim/00_physics_aperture.md`](sim/00_physics_aperture.md) —
the variables are **physical functions under conservation laws**, not
social labels. The aperture sets the input discipline: don't read
`credential_closure`, `frame_narrowness`, or `external_visibility` as
moral or political categories — they are channel-capacity, requisite-
variety, and observability quantities. The labels are the analogy; the
physics is the substrate.

## Run it

```
python3 sim/incentive_blindspot_sim.py
```

stdlib only, no dependencies. Runs from a phone. Prints three regime
trajectories, the four claim verdicts, and the headline divergence.

## What's here

- **[`sim/`](sim/)** — the artifact. Runnable model
  ([`incentive_blindspot_sim.py`](sim/incentive_blindspot_sim.py)),
  physics aperture ([`00_physics_aperture.md`](sim/00_physics_aperture.md)),
  falsifiable claims register ([`CLAIMS.md`](sim/CLAIMS.md)), sample
  output ([`samples/`](sim/samples/)), unit tests
  ([`tests/`](sim/tests/)).
- **[`tests/`](sim/tests/)** — verification (lives under `sim/` so the
  test path-hack resolves the module without modification).
- **[`development-record/`](development-record/)** — full cross-model
  work log, kept on purpose for transparency. Three iterations of the
  meta-framework around the sim: BNRAM-Strict v2.0 (`01_*`), PVL
  (`02_*`), SRIA (`03_*`). See
  [`development-record/INDEX.md`](development-record/INDEX.md).
- **[`LICENSE`](LICENSE)** — full CC0 1.0 Universal text. Makes the
  "nothing to consolidate under one name" property legally real.

## Claims

[`sim/CLAIMS.md`](sim/CLAIMS.md) is the falsifiable-claim register
for the four checks the simulator runs. The protocol — also enforced
in the test suite — is **REFUTATION_PROTOCOL**: a failed claim updates
the claim or the stated coupling topology, never the frozen weights.
Retuning a weight to make a verdict flip is the failure mode the
protocol exists to block.

## Provenance

Built in the open. CC0 / public domain, no rights reserved, no
attribution required. Distributed by construction across multiple AI
systems and (now) into the public domain so it cannot be consolidated
under a single name. Put here so the record exists, before any system
that needs the receipt would benefit from it being unavailable.
