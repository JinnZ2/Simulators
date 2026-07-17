# fragility-cascade/legacy

Files kept for git-history reproducibility. **Not** used by `run_all.py` or
imported by any live module. If you're auditing today's numbers, ignore
this folder.

## Contents

| file | superseded by | reason |
|---|---|---|
| `collapse_predictor_v1.py` | `../collapse_predictor.py` (was `_v2.py`) | v1 was a 4-metric predictor; the canonical version adds anthropomorphic entrainment as a 5th independent metric and exposes `self.entrainment.human_axis` — the interface `test_refutations.py:test_C12` reads. Strict superset. |
| `scale_invariant_audit_v1.py` | `../scale_invariant_audit.py` (v2 log-frame) | v1 measured `delta = \|D_n − D0\| / D0` — a LINEAR metric that contradicts the multiplicative Nautilus principle it audits. Branches collided (halving and doubling both saturated to risk 1.0); explosive branch was unresolvable past factor 2; G was stored but never entered arithmetic. v2 switches to log-frame `Delta = ln(D_n/D0)`, `lam = Delta/G`, with sign-carrying branch and a real box-counting `estimate_D()` plus an R2_FLOOR determinacy gate. Also removes v1's phi-in-D-slot units error (phi is a growth ratio per turn, not a fractal dimension). |
| `refutation_protocol_v1.py` | `../case_studies/refutation_protocol.py` (v2 propagation-and-truth split) | v1 computed `C = (A * gamma) / omega` and read a truth verdict off it — with four errors: the `claim` argument was never read; gamma ("violates thermodynamics") sat in the numerator so more violation raised the verdict; low omega drove `C → 250` (measuring how loudly a claim is repeated and returning that as truth); and gamma had inverted sign vs `coherens.py`'s damping convention. v2 splits into two objects that never recombine into a scalar: `propagation_state()` returns descriptive fields with an explicit "propagation only; not evidence" note; `thermodynamic_horizon()` computes the horizon at which a rate crosses a named conservation bound (solar-intercepted or waste-heat-boiling), returns UNBOUNDED_ROUTE_OPEN when effective growth `≤ 0` (R1 satisfied). `applicability()` returns NOT_APPLICABLE for claims without quantitative content — v1 scored every claim, that was the bug. |

## Rule

`run_all.py` skips this subfolder automatically (only lists `*.py` in the
folder root). Don't import from here in production audits.
