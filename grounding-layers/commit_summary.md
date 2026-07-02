feat(biases): add institutional gatekeeping bias (GL_B_016)

- Added GL_B_016 to BIASES_REFERENCE.md with BIS=0.45
- Added _detect_institutional_gatekeeping to cultural_lens.py
- Added optional flag in safeguards.py (soft warning, not hard stop)
- Wired gatekeeping warnings into run_grounding_pipeline.py

This completes the bias registry for major structural biases.
