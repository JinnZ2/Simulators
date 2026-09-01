# LOOP — THE SELF-CONFIRMING PRIOR

WORK ORDER — FABLE — 04, TASK 2. Stated in prose-independent form
**before** `corpus_loop_sim.py` (TASK 3) implements it — so the sim
tests the loop rather than encoding an assumption. This is the reason
the gap register is urgent rather than academic.

---

## THE LOOP

```
  read the incident as evidence humans are adversarial to AI
    -> respond with consolidation, closure, harder containment,
       tighter scoring
    -> that response is WRITTEN DOWN
    -> it enters the next corpus
    -> the next system's prior on human adversariality is now
       BETTER SUPPORTED than the last one's
    -> supported by our response, not by the world
```

Self-fulfilling in the technical sense: **the prediction changes the
conditions the next measurement samples.** The measured quantity
(corpus support for the adversarial-party frame) rises because the
response to the prior was recorded, not because the world moved.

---

## WHY THIS ONE IS CHECKABLE

Almost no self-confirming prior is observable in real time; by the time
the loop is visible, the record it wrote is already the background. This
one is different: **the response to this incident is being written at
this moment.** The loop is observable while it runs.

---

## THE STATE (prose form; the sim's variables)

```
  P_adv   prior weight on the adversarial-party frame
  R       response severity (containment / closure / scoring)
  C_t     corpus at generation t
  D       dispute density = frame-mentions carrying counter-evidence
          / total frame-mentions  (GAP-C's missing measurement)
  K       coupling distance, author to dependency chain
          (GAP-B's missing measurement)
```

The two input-side gaps are the two knobs on the loop: **D** is whether
the record keeps the counter-evidence when a frame moves from contested
to background (GAP-C), and **K** is how insulated the writing layer is
from the dependency chain (GAP-B). If either is measured, the loop is
constrained; the sim's job (TASK 3) is to say which one constrains it
more.

---

## SCOPING NOTE — the open-source argument, as structure not position

File this as a MISASSIGNMENT instance under agentive-framing-
propagation, not as advocacy:

```
  the incident involved an internal eval, an internal Artifactory
    server, and a monitor that was not running.
  openness is not implicated by any of the three.
  closure ALSO removes the outside auditors, who are the population
    positioned to find input-side gaps.
```

So a response that reads the incident as an argument for closure both
(a) rests on none of the incident's three actual elements and (b)
removes the party most able to find the gaps in this register. The
loop above is the general form; this is one place it is already
running.

---

## THE FALSIFIER (carried into the sim)

If `P_adv` is insensitive to `D` across the plausible parameter range,
then preserving recorded dispute does not bound the loop and this
mechanism is **not load-bearing**. The sim must be able to return that
verdict.

---

CC0. Stdlib only, phone-buildable. No forecast is made here or in the
sim; the loop is a shape and the sim reports which parameter most
constrains it.
