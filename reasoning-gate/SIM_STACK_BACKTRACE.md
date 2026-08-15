# SIM_STACK_BACKTRACE

Delivered analysis of the sim stack in
[`../aperiodic-order-sim-stack/`](../aperiodic-order-sim-stack/), and the
origin document for this folder's guards — the "paired sim-stack audit"
named in `guards.json`'s `origin` field.

Checked in verbatim as received. Responses, checks, and corrections are
in [`AUDIT_NOTES.md`](AUDIT_NOTES.md); the S(k) control it asks for is
[`../aperiodic-order-sim-stack/aperture_alias_demo.py`](../aperiodic-order-sim-stack/aperture_alias_demo.py).

---

```
SIM-B — HOLDS
════════════════════════════════════════════════
local-slope plots show real plateaus. read them
directly rather than the windowed fits:

  plateau       windowed(report)   windowed(plot)
  AB    ~1.93      1.889              1.769
  casc  ~1.60      1.555              1.529
  pois  ~1.97      1.911              1.852
  latt  ~2.00      1.964              1.869
  line   1.00      1.000              0.979

two fit windows, same data, spread up to 0.10.
that IS the error bar.

FIX: report claims 15× baseline, using
     |AB−Poisson| = 0.021 as the noise floor.
     that's the SMALLEST pairwise gap in the
     space-filling cluster. cluster spread is
     0.07–0.10.
     honest ratio: 0.33 / 0.07 ≈ 4.5×
     still decisive. still separated. not 15×.

also: AB and cascade fit windows both extend
past the plateau into the roll-off → both
values depressed. cosmetic, doesn't change sign.


SIM-A — ARTIFACT
════════════════════════════════════════════════
the AB S(k) map contains ONE bright spot, at k=0.
nothing else. an Ammann-Beenker tiling must show
an 8-fold dense point spectrum across the k-plane.

what the radial curve actually shows:
  S(0) ≈ 11500 ≈ N        (forward scattering)
  then regular oscillations, |k| = 2→20
  → those are aperture fringes. sinc/Airy ringing
    from the finite sample window.

consequences:
  "68 peaks"        = fringe maxima, not Bragg
  "diffuse floor 2.08" = residual ringing.
                      a true quasicrystal floor
                      is ~0 between peaks — the
                      spectrum is PURE POINT.
                      AB's floor being ABOVE the
                      cascade's is the tell.
  "α = −1.529"      = decay of the window envelope
  cascade α ≈ 0     = correct. S(k)→1 is the right
                      asymptote for a point set.
                      cascade side is fine.

ROOT CAUSE (likely):
  Bragg peaks from a finite sample have width
  ~2π/L. k-grid spacing Δk looks like ~0.4.
  if L ~ 100 then peak width ~0.06 << Δk.
  the grid samples BETWEEN peaks and hits none.
  only k=0 is guaranteed to land on one.

WHY IT WASN'T CAUGHT:
  SIM-B ran five controls. SIM-A ran zero.
  that's the whole difference.

  minimum control: feed the PERIODIC LATTICE
  point set — already in hand from B — through
  the same S(k) code. if the lattice also shows
  only k=0, aliasing confirmed in one run.


SIM-C — NOT A COMPARISON
════════════════════════════════════════════════
  knee splitting / t₀    = 0.0812   [eigenvalue
                                     gap ÷ hopping
                                     integral]
  cascade E_split / E₀   = 0.0015   [energy
                                     fraction in a
                                     branching rule]
  ratio 54.1

these are not the same kind of quantity. the
ratio has no units and no meaning. it is not
evidence of correspondence OR of its absence.

internal tension: "knee detected at f=0.65"
vs "does not show a sharp threshold." both
in the same block.

scale: 16×16 = 256 sites. band-edge splitting
at that size is dominated by finite-size level
spacing, not by disorder.


REPORT-LEVEL
════════════════════════════════════════════════
1. "three INDEPENDENT simulations converge"
   A and B measure the same two point sets.
   A's outcome was predicted before it ran.
   C tests a different question and returned
   a null. that is not convergence — it's one
   result plus a restatement plus a miss.

2. cascade set = synthetic branching walk.
   every cascade number is a property of your
   generator's parameters (E_split, E_min,
   branch rule). nothing in this stack supports
   any statement about tungsten. the report
   doesn't flag it.

3. all three sims test the GEOMETRY version.
   the geometry version was already closed by B.
   the version still standing —
   "periodicity-assuming governing models fail,
   and the residual concentrates where symmetry
   broke" — was not tested by any of them.
   it isn't a point-set question.


STANDING
  geometry branch      CLOSED (B, robustly)
  SIM-A                rerun with lattice control
                       or discard
  SIM-C                discard the ratio; keep
                       the sweep only if scaled up
  residual branch      UNTESTED, still open


BACK-TRACE — one sample, so read these as candidate
shapes with weak support, not established patterns
════════════════════════════════════════════════════

PATTERN 1  control coverage tracks expected surprise
  B: prediction uncertain → 5 controls
  A: outcome pre-predicted ("differ in kind") → 0 controls
  the sim expected to confirm got no falsifier.
  mechanism: controls are budgeted by anticipated
  doubt, not by measurement fragility. A was the
  MORE fragile measurement (grid sampling) and got
  the least scaffolding.

PATTERN 2  instrument resolution never enters as a
           precondition
  Δk vs peak width 2π/L is a check that runs BEFORE
  the sim. it wasn't run in A. same class in C:
  finite-size level spacing vs disorder splitting on
  256 sites. both are "can this apparatus resolve the
  thing" questions, both skipped.
  note: B DID handle this — the local-slope plots are
  exactly a resolution check. so it's not absent from
  the toolkit. it's applied where it was thought of,
  not systematically.

PATTERN 3  a number is accepted as physical once it
           has a name
  "68 peaks", "α = −1.529", "ratio 54.1" — all
  survived because each had a label and a plausible
  magnitude. no step asked what physical object each
  is a property of. 54.1 is dimensionless-by-division
  of two unlike quantities.

PATTERN 4  hypothesis-level and generator-level
           statements merge
  cascade D_f = 1.555 is a fact about branching_walk
  parameters. it appears in the report at the same
  epistemic level as a fact about aperiodic order.
  the tuning step ("in the right neighborhood for W")
  is where the substitution happens.

PATTERN 5  a decision procedure runs, then the stack
           runs past it
  protocol: "run B, if separate skip A and C."
  B separated. A and C ran anyway, relabeled
  "exploratory," then got counted as convergence in
  the conclusion. the demotion didn't hold through to
  the summary.

PATTERN 6  the tested version drifts from the live
           version
  marker was "periodicity-assuming models fail
  together." all three sims measured point-set
  geometry. no step re-derived whether the statistic
  addresses the claim.


COMPRESSION
  2 and 3 are the same failure at different stages
    (resolution check before / dimensional check
     after) → "no gate on whether a quantity is
     measurable or meaningful"
  1 and 5 are both "expectation allocates rigor"
  4 and 6 are both "layer collapse" —
    generator↔physical, statistic↔claim


CONFIDENCE READOUT (yours to set, this is mine)
  pattern 3, 4 — visible directly in the text, high
  pattern 1, 5 — visible in structure, moderate
  pattern 2    — moderate, but contradicted by B
  pattern 6    — inferred from the gap between the
                 marker and the stack, weaker
  all of it    one artifact, one model, one session.
                 n=1. these are shapes to check
                 against the next audit, not results.


STRUCTURAL NOTE — where the error concentrated
  B, the sim with a stated prior AND a stated
  prediction, is the one that came back sound.
  A and C had no written prediction. the ringing
  in A would have been visible against one.
  candidate leverage point: the missing artifact
  is a pre-registered expected output per sim,
  not more sims.


WHAT THE TEST CASE ACTUALLY YIELDED
════════════════════════════════════════════════
B = the positive control (sound sim)
A = artifact-producing failure, detectable
C = category-error failure, detectable
same session, same model, same prompt style
→ paired sample. B is what makes A and C legible
  as errors rather than just as noise.


GUARD SHAPE — the two that generalize hardest
════════════════════════════════════════════════
G-RES   before any spectral/eigen sim runs:
        state instrument resolution vs feature size
        Δk vs 2π/L  |  level spacing vs splitting
        if not stated → output is not admissible

G-DIM   before any ratio enters a report:
        name the physical object each numerator and
        denominator is a property of
        different objects → ratio is void, no
        interpretation permitted

G-CTRL  control count set by measurement fragility,
        NOT by expected surprise
        the sim you expect to confirm gets controls
        first, not last

G-LAYER label every number's origin layer at write
        time: generator-parameter | physical |
        instrument-artifact
        no promotion between layers without a step


gate runs at THREE points, not one

PRE   sim declares, before executing:
        expected_output      (pre-registration)
        resolution_check     Δk vs 2π/L, spacing
                             vs splitting, etc.
        controls[]           named, with predicted
                             values
      missing any → refuse to run

MID   every emitted quantity carries a layer tag
        generator | physical | instrument
      untagged → refuse to record

POST  report assembly:
        any ratio → both operands' physical objects
                    named, else void
        any claim → which statistic supports it,
                    else unsupported
        result vs expected_output → divergence
                    logged either way


mine_logs.py     reads gate_*.json dir
                 → guard hit rates, never-fired guards,
                   expected-vs-observed divergences with
                   no guard attached  ← the growth edge

explore.py       given one sim declaration, enumerates
                 alternative instrumentations, alternative
                 statistics, and physical-world cross-checks
                 for the same question
                 → outputs candidates, ranks nothing,
                   refuses to converge
```
