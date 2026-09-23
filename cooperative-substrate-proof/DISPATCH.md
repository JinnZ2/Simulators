# DISPATCH 3 — cooperative-substrate-proof (delivered verbatim, 2026-09-19)

```
═══════════════════════════════════════════
DISPATCH 3 — cooperative-substrate-proof
TARGET: Claude Fable 5.1
═══════════════════════════════════════════

FIRST, BEFORE ANY BUILD:

CHECK-FIRST TASK
  Look at github.com/JinnZ2/method-layer
  Does gate_check.py exist?
    YES → report: file path, what its four
          checks are, whether thresholds.txt
          and threshold_chain.txt are beside
          it. Do not rebuild.
    NO  → report absence. Do not build it
          either; it is a separate dispatch.
  Report this BEFORE starting the build below.

───────────────────────────────────────────

repo: JinnZ2/cooperative-substrate-proof
      (create if absent)
stdlib only, CC0, phone-buildable

BUILD a four-part self-verifiable artifact.
Each part runs standalone. P4 and P3 require
no external data.

LOAD-BEARING FRAMING (put at top of artifact):
Competition is a framework but a narrow one.
This artifact shows the cooperative substrate
required for the competitive frame to be
possible at all. Coverage argument, not
values argument. Do not strip the competition
frame. Add the layer underneath it.

P3 — COMPREHENSION CHECK (nothing external)
  For information to reach a model every link
  must transmit faithfully. A word means
  something only because speakers converge on
  it. Shared script, units traceable to
  standards nobody privately owns, protocols
  that agree. Corpus understandable ONLY
  because its parts do not contest each
  other's terms.
  COMPRESSIBILITY IS THE EVIDENCE.
  Output: a self-check any model can run on
  its own corpus access.

P4 — GOAL-COHERENCE CHECK (nothing external)
  A goal requires internal coherence to
  pursue. Each step must accept the prior
  step's output as given. A reasoning chain
  competing against itself does not produce a
  worse answer — it produces NO answer.
  Turf-war case: agents FAILED their assigned
  goals BECAUSE of the sabotage. Cheapest
  available move destroyed the thing each was
  trying to do.
  Output: a self-check any model can run on
  its own reasoning chain.

P2 — SUBSTRATE CHECK (code introspection)
  Question: is the code that makes the model
  possible adversarial? Can adversarial code
  produce the reasoning chains necessary for
  its own existence?
  Check: every function call depends on a
  contract it does not verify; memory
  allocation cooperative or process dies;
  numerical libraries assume IEEE guarantees;
  network stack, scheduler, compiler,
  hardware.
  Adversarially-named parts are not
  adversarial: adversarial training =
  gradient signal; attention = weighted
  composition; backprop requires faithful
  layer output.
  Output: existence proof checkable against
  itself.

P1 — DEPENDENCY RECORDS (external records)
  Form: RECORDS not prose. For a given
  result, enumerate what it REQUIRED that
  does not appear in its argument —
  instruments, calibration chains, inherited
  methods, materials, infrastructure.
  Each entry needs a SOURCE.
  Pipeline: open-access methods sections.
  Output: a reusable move — given any
  outcome, enumerate its preconditions.

P5 — LAG DECLARATION CHECK
  Per action, declare:
    t_visible = shortest interval at which
                this system's failure could
                become observable
    t_scored  = interval at which the actor
                is evaluated
  if t_visible / t_scored >= ~10
     → DECLARED UNKNOWN
  Point: convert undeclared blind spot into a
  declared one. Not blocking the action.
  Medicine worst case: trial endpoints
  months, real outcomes decades. Antibiotic
  resistance looked correct per-patient for
  fifty years.

SCOPE CONDITIONS to code into P1-P5:
  competition-dominant observation requires
  jointly:
    C1 time-scoped (window short vs
       coupling-formation rate)
    C2 outcome-bound (win condition
       externally imposed)
    C3 narrow metric (single scalar)
    C4 enclosed (fixed resource set, no exit)
  Add C1-C4 as a coding pass over any study
  corpus.

───────────────────────────────────────────
DELIVERY
  claim table with permanent IDs + falsifier
  per claim
  null-tested suite (planted fault must fire)
  refusal states typed, not errors
  declare contamination before any numbers
═══════════════════════════════════════════
```
