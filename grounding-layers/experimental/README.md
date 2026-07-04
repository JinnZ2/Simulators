# experimental/

Experimental instruments that attempt to calibrate the audit-grade
`grounding-layers/` pipeline against **human sensorimotor sensing**.

These are **not** part of the load-bearing L0-L5+Lε probabilistic
stack. They're peer instruments sitting alongside the audit-grade
pipeline, exploring what changes when you take human-in-the-loop
sensing as a first-class calibration source rather than a downstream
consumer.

## Framing

The audit-grade pipeline in `..` treats the AI as the primary
inspector: claims are scored under constraint-propagation math with
SCOPE-annotated category-error guards. That's one substrate.

These experimental instruments treat the **human sensorimotor read**
as a co-equal substrate. The idea being explored:

- Two processors read the same coupled system from different
  substrates (AI = outside, constraint math; human = inside, native
  harmonic read).
- Knowledge doesn't live in either read alone. It lives in the DELTA.
- Where the reads mismatch, the CLAIM updates. The human read is
  never retuned to match the model — same refutation-protocol pattern
  as the audit-grade side, but the direction of correction is
  explicitly named.

## Files

| file | what it does |
|---|---|
| [`field_compass.py`](field_compass.py) | ALIGNER (not translator). Takes a human sensorimotor `Read` and an AI cascade `Read` of the same system, points at their delta, names the lesson the AI has to learn (topology, early_broadcast, amplification, scalar_drift). |
| [`holistic_field_state.py`](holistic_field_state.py) | Lε ENTRY INSTRUMENT. Multi-channel operator-as-instrument read with confidence gating (`Trust.HIGH` / `BASELINE` / `GATED`), coupling graph, stress-field computation, shift-margin projection, verdict + refutation. |

## Status

- **CC0, stdlib-only, phone-buildable** — same portability constraints
  as the audit-grade side.
- **SCOPE annotations** on each module docstring (T | S | O | C) per
  `../SCOPE_TAXONOMY.md`.
- **No CLAIMS.md entries yet.** Behavior is illustrated via each
  file's `__main__` demo (truck front-axle, garden soil-plant-insect,
  refutation between predicted and measured). Once the calibration
  pattern is stable, these could be lifted to audit-grade with
  `GL_FC_*` and `GL_HFS_*` claim families.
- **Smoke tests** in `../tests/test_experimental_smoke.py` verify
  the demos run and produce the expected verdict shape.

## Not to be conflated with

- `../field_compass.py` — the DeepSeek pack's "probability field
  navigation for L5" module, which has the same filename but a
  different design. That one lives at the audit-grade level with its
  own callers; this one is experimental and unrelated.
- The audit-grade `entry.py` — the single-call `audit()` dispatcher.
  If you're an AI wanting to use the load-bearing pipeline, go there
  (see `../USAGE.md`). If you're exploring how to fold in human
  sensing, start here.

## License

CC0. See the repo root `LICENSE`.
