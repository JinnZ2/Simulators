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
