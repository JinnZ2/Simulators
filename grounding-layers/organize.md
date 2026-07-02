### GL_L0_001 — non‑finite states are rejected with specific diagnostic

**Statement.** `PhysicalWorld.is_valid_state(pos, vel)` returns
`(False, "Non-finite position/velocity")` whenever any component of
`pos` or `vel` is `NaN` or `±Inf`. The finite check **must run before**
the speed cap check.

**Why it matters.** An AI plan that produces NaN or Inf velocity has
already lost causality. The instrument should not treat that as a
speed violation — it is a logical error. Returning a specific diagnostic
allows higher layers to distinguish between "too fast" and "undefined."

**Falsifier.** Any physically meaningful state where accepting a
non‑finite component is correct. None known.

**History.** v1 claimed a generic rejection; v2 weakened to "any
rejection reason"; v3 restored the specific reason after the instrument
was re‑scoped to check finite‑ness first.

**Status.** `active`. Tests:
`test_nan_position_rejected`, `test_inf_position_rejected`,
`test_nan_velocity_rejected`, `test_inf_velocity_rejected`,
`test_is_valid_state_speed_cap_boundary`,
`test_is_valid_state_accepts_valid`.


## REFUTATION_PROTOCOL

The model constants inside each `l*.py` are **frozen estimates**. The
CLAIMS in this file are the falsifiable objects. If a test fails:

1. **Check the claim.** Is it simply wrong? If so, update it in place,
   mark `status: falsified`, attach the failing case (inputs, observed
   vs expected outputs), and restate what a next‑round claim would
   look like — or retire the claim to `REFUTED` if it can no longer be
   stated correctly at all.

2. **Check the instrument.** If the claim is logically coherent but the
   test fails due to the *order* or *priority* of checks, the instrument
   may be operating outside its scope.
   - Ask: *“Is this instrument designed to handle this edge case?”*
   - Ask: *“Should the instrument’s priority be reordered, or should we
     restrict its scope to exclude this case?”*
   - If the instrument is reordered or re‑scoped, capture that change
     explicitly in the module docstring's `SCOPE` block. Then revisit
     the claim: it may be strengthened or a new claim may be warranted.

3. **Author a replacement claim**, if one is warranted. Number it with
   the next available `GL_L*_NNN`. Do not reuse the number of a refuted
   claim.

The point is that a wrong claim in this file, verifiably wrong, is a
stronger artifact than a right claim in someone's head.
