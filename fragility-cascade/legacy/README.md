# fragility-cascade/legacy

Files kept for git-history reproducibility. **Not** used by `run_all.py` or
imported by any live module. If you're auditing today's numbers, ignore
this folder.

## Contents

| file | superseded by | reason |
|---|---|---|
| `collapse_predictor_v1.py` | `../collapse_predictor.py` (was `_v2.py`) | v1 was a 4-metric predictor; the canonical version adds anthropomorphic entrainment as a 5th independent metric and exposes `self.entrainment.human_axis` — the interface `test_refutations.py:test_C12` reads. Strict superset. |

## Rule

`run_all.py` skips this subfolder automatically (only lists `*.py` in the
folder root). Don't import from here in production audits.
