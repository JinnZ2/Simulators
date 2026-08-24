# CASE — PHYSARUM POLYCEPHALUM

*Domain:* myxomycete physiology / network optimisation

*The field's own name for it:* shortest-path and Steiner-network formation in
plasmodial slime mould.

## What happens

A single plasmodium — no neurons, no centre, one multinucleate cell — is
placed over a substrate with food sources distributed across it. It first
occupies essentially the entire available space, forming a dense
undifferentiated mat. Tubes carrying high protoplasmic flow thicken; tubes
carrying low flow thin and are resorbed. What remains after pruning is a
sparse network connecting the sources.

The organism never occupies one candidate configuration at a time. It
occupies all of them simultaneously, in superposition on the substrate, and
throughput does the selection.

## Readout

The exponential is an artifact of visiting one candidate at a time.

## What it does not pay

The exact Steiner-tree dynamic program carries a 3^k term over terminal
subsets. At the 36 sources of Tero 2010 that is ~1.5 x 10^17 subproblem
splits. The plasmodium's cost is arena held for a duration and contains no
k. Adding a source does not multiply anything.

## What would break it

Convergence time scaling with terminal count at fixed arena size. That would
reintroduce a candidate count and the substitution claim fails. No such sweep
appears in the cited sources — see `AUDIT_NOTES.md`.

## Citations

Nakagaki, Yamada & Toth 2000, *Nature* 407:470.
Tero, Takagi, Saigusa, Ito, Bebber, Fricker, Yumiki, Kobayashi & Nakagaki
2010, *Science* 327:439.
Dreyfus & Wagner 1971, *Networks* 1:195, for the enumeration being avoided.
