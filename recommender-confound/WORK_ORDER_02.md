WORK ORDER — Fable
CC0, stdlib-only, phone-buildable
=================================

TASK 1 — DENSE MULTI-SEED (do first)
------------------------------------
target: B) synthetic_catalog.py
run   : dense row only, both
        canonicality levels,
        N seeds (≥30), model held
        fixed exactly as seed 1

observation to test:
  seed 1 true rate
    dense/low  0.118
    dense/high 0.138
    Δ = 0.020  (17% relative)
  canonicality must NOT touch the
  true rate. sparse row showed
  Δ 0.002; dense showed 10x that.

out:
  mean, sd, CI on Δ per seed set
  verdict:
    Δ ~ 0 within noise
      → factorization holds,
        g × h × m stands as written
    Δ survives
      → CROSS-TERM. g × h × m is
        wrong. report which pair
        couples and the sign.

also print: whether sparse Δ 0.002
  is inside its own noise band.
  if sparse noise ≥ 0.02, the dense
  Δ was never anomalous and this
  closes with no cross-term.

TASK 2 — COLLISION CELL
-----------------------
target: B, generator side
finding: every measured ≥ true
  across all four corners. no
  deflation anywhere.
cause suspect: B may not generate
  the second error cell —
    fabricated title colliding
    with a real catalog entry
    → scored CORRECT
out:
  does B emit collisions? y/n
  if n: add a collision rate
    parameter, re-run 4 corners
  report measured − true SIGNED
    per corner
verdict: matcher can hide
  fabrication as well as invent it.
  current B under-states matcher
  damage if collisions absent.

TASK 3 — CANONICAL SELF-TEST (A)
--------------------------------
target: A) confound_probe.py
add   : pre-flight on any catalog.
  take the canonical subset, run
  the full matcher set.
  seed-1 basis: at high
  canonicality all matchers agreed
  to 3 decimals, both densities.
rule  : disagreement on canonical
  subset = matcher-set bug.
  ABORT before any catalog claim.
  → diagnoses the instrument
    without a ground-truth catalog.
  RC_008 unaffected; this is a
  bug gate, not a validation.

TASK 4 — FIXTURE PROMOTION
--------------------------
the kill-rule forms disagree on the
current fixture. keep it, name it,
document it as the boundary case
where ranking validity depends on
rule choice. both forms stay
printed. that disagreement is a
result, not a defect.

NOT IN THIS ORDER
-----------------
F repo creation — Kavik's call
G) preference_free_rank.py — specced,
   own repo, not started
protocol-over-information survey —
   verbatim, unbuilt
