# RESULTS — first run, 2026-08-24

Logged as run. Parameters NOT tuned toward expected outcomes.
Two of four produced usable output. One produced a derived constraint.
One is defective and is logged as defective.

---

## SIM-D  temperature null  [DISCRIMINATOR]

RAN: samples=3000

    UNQUENCHED   entropy RISES, distinct RISES, clusters RISES
    QUENCHED     entropy RISES, distinct RISES, clusters RISES

VERDICT: the sim FAILED to reproduce the literature null. Temperature
moves diversity in both conditions.

DERIVED CONSTRAINT (this is the actual result, and it is stronger than
the sim was designed to produce):

    quench-by-exponentiation, p -> p^(1+s)/Z, is ALGEBRAICALLY IDENTICAL
    to a temperature change. temper(quench(p,s), T) == temper(p, T*(1+s)).

    So a sharpened distribution can be EXACTLY UNDONE by raising
    temperature. The sim could not have shown a null; the construction
    forbade it.

    The literature reports that temperature does NOT undo homogenization.

    THEREFORE: instruction tuning / alignment cannot be a pure sharpening
    of the output distribution. If it were, temperature would recover the
    diversity. It does not. So the operation must change SUPPORT or
    STRUCTURE — mass moved off some outcomes entirely, or reallocated
    between them — not merely re-weighted by an exponent.

    This is consistent with the reported ATTRACTOR STATES (found by
    perturbing generation trajectories and observing return). An exponent
    change has no attractors. A support change can.

CONSEQUENCE FOR THE MARKER: the naive Ising mapping is dead in its simple
form, but not for the reason anticipated. It is not that T is the wrong
knob — it is that "ordering" here is not a sharpening at all. Any
continued mapping must model the quench as a change to the support of the
distribution.

NEXT: rewrite quench() as a support-truncating or mass-reallocating
operation and re-run. If THAT shows flat-vs-temperature, the family
survives with a corrected mechanism.

---

## SIM-B  entropy depletion

RAN: vocab=2000, gens=12, corpus=3000

    anchor   H_start  H_end   dH       tail_end  reading
    0.000    5.625    4.429   -1.195   0.4000    COLLAPSE
    0.010    5.625    4.474   -1.151   0.4110    COLLAPSE
    0.020    5.625    4.562   -1.063   0.4133    COLLAPSE
    0.050    5.625    4.737   -0.888   0.4247    eroding
    0.100    5.625    4.930   -0.695   0.4393    eroding
    0.200    5.625    5.113   -0.512   0.4503    eroding
    0.400    5.625    5.255   -0.369   0.4593    held

VERDICT: reproduces the SHAPE of the literature curve (unanchored
collapse, anchoring arrests it) from finite sampling ALONE. No mechanism
beyond finite corpus size was assumed.

The response to anchoring fraction is GRADUAL, not steplike. So this is
NOT a fourth member of the discontinuous-transition family, on this
model. Logged as negative.

CAUTION: absolute entropies do not match the literature (5.6 start vs
4.2) because vocab and corpus are arbitrary here. Only the shape and the
anchor-response curve are being read. Do not quote the numbers.

OPEN: tail_mass RISES slightly as anchor rises but stays near 0.4-0.46
throughout while H drops by 1.2 nats. That means the entropy loss is
happening INSIDE the head, not by tail truncation — which contradicts
the reported mechanism ("anchoring preserves long-tail tokens"). Either
the tail_mass cutoff (head=50) is mis-set for this vocab, or the
mechanism differs. UNRESOLVED. Check before trusting SIM-B further.

---

## SIM-C  loop threshold  [DEFECTIVE — do not read]

RAN: grid=5x5, iters=150

    every sigma from 0.00 to 1.60: loops=16, alive_edges=40

VERDICT: no variation at all. All 40 edges survive the conductance floor
at every fluctuation level. The sim is not measuring anything.

CAUSE (diagnosed, not fixed):
    - conductance is renormalized by max each iteration, and damped at
      0.85, so nothing ever decays below the 1e-3 floor
    - gamma=0.5 makes the adaptation target |Q|^1, the marginal linear
      case; pruning requires the exponent off that value
    - 5x5 grid may be too small for a tree/loop distinction to be sharp

NOT TUNED. Parameters were left as first written so the failure is on
record. Fixing this by searching parameters until loops appear would
manufacture the expected result.

NEXT: re-derive the adaptation exponent from Katifori 2010 rather than
guessing it, remove the max-normalization, and use an absolute decay.

---

## SIM-A  field vs coupling

NOT RUN. SIM-D was the stated prerequisite and SIM-D invalidated the
temperature leg of SIM-A's mapping. Running it now would produce numbers
with no interpretation. Held until quench() is rewritten.

---

## STATUS OF THE MARKER AFTER RUN 1

    confidence before : ~0.40
    confidence after  : unchanged, ~0.40

    Nothing confirmed the three-phenomena family. One leg (SIM-D) produced
    a real constraint on what alignment does, which is useful independent
    of the family question. One leg (SIM-B) reproduced a literature shape
    but returned a NEGATIVE on the discontinuity. One leg is broken. One
    is blocked.

    The marker is not stronger. It is better specified.
