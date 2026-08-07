# crossdomain-eval

Cross-domain scientific-analysis toolkit landed as two coordinated
drops. `PACKAGE_README.md` is the upstream package documentation
(quick-start, module overview, CLI). This file explains where the
folder sits in the repo, the two-variant reasoning module, and how
to run it.

## What's here

The `crossdomain_eval` Python package provides:

| Module | Purpose |
|---|---|
| `symbolic` | SymPy engine: parse, substitute, solve, differentiate, integrate, evaluate. |
| `numerical` | Root finding, ODE solving, optimization (NumPy / SciPy). |
| `reasoning` | Basic forward-chaining rule engine + confidence-tagged assumption tracker. |
| `reasoning_v2` | Stricter alternative: token-blocklist sandbox, ID-tracked assumptions with retract, `_fired` provenance in the derived facts. |
| `experiments` | Parameter sweeps, sensitivity, full-factorial DOE. |
| `report` | Markdown report generation + sweep plots. |
| `domains/physics` | Kinematics, energy, and other EquationSet helpers. |
| `domains/geometry` | Sphere-in-box packing density, TSP distance matrices. |
| `cli` | `cdeval` command-line interface (`eval`, `solve`, `sweep`, `doe`). |

## The two reasoning variants

The source drop arrived as two zips with a deliberate split. Both
are landed side-by-side because they encode different design choices
and neither is a drop-in replacement for the other:

### `reasoning.py` (default)
- Uses `eval()` under an explicit `{"__builtins__": {}}` namespace.
- `AssumptionTracker.add(...)` returns `None`; `check()` matches on
  a derived predicate name (first word) OR substring in the
  statement, case-insensitive.
- `RuleEngine.infer(facts)` returns derived facts only.
- Bare-expression conclusions get a derived key like `x_2` (from
  the expression text).
- 11 tests in `tests/test_reasoning.py` all green.

### `reasoning_v2.py` (stricter alternative)
- Uses `eval()` but pre-screens conditions and conclusions against a
  `_FORBIDDEN` regex blocklist (`__`, `import`, `open`, `exec`,
  `eval`, `globals`, `locals`) — rules containing those tokens
  raise at `add_rule` time rather than at inference time.
- `AssumptionTracker.add(...)` returns an integer `id`, supports
  `retract(target)` (marks inactive but keeps in audit trail),
  `check()` requires exact statement match and honours a
  confidence threshold (default 0.5).
- `RuleEngine.infer(facts)` returns derived facts with an extra
  `_fired` key holding the list of rule indices that fired.
- Bare-expression conclusions get keys like `conclusion_0`.
- 21 tests in `tests/test_reasoning_v2.py` all green.

Import whichever fits:

```python
from crossdomain_eval.reasoning import RuleEngine       # default
# or
from crossdomain_eval.reasoning_v2 import RuleEngine    # stricter
```

Neither variant uses the AST-based `safe_eval` + function-registry
+ missing-fact-policy design discussed in the accompanying
conversation. Both use guarded `eval()`; the strictness differs.
If a fully AST-sandboxed variant is wanted, that's a follow-up.

## Install

```bash
pip install -e .          # from crossdomain-eval/
```

Non-stdlib deps: `sympy`, `numpy`, `scipy`, `matplotlib` (pinned
in `pyproject.toml`). `pytest` is under the `dev` extra.

## Run

```bash
# Tests — 68 total (47 for the core package + 21 for reasoning_v2)
python -m pytest tests/ -q

# Examples
python examples/demo_symbolic.py
python examples/demo_experiment.py

# CLI
cdeval eval "F = m*a" --set m=80 a=9.81
cdeval solve "x**2 - 4" --for x
cdeval sweep "x**2 + y" --range x=0:5:50 --range y=0:3:30 --plot out.png
cdeval doe --factors temp,pressure,speed --levels 2
```

## Repo positioning

Non-stdlib package. Same exemption pattern as `energy/`,
`play-sims/`, `climate-modeling/`, and `relational/geometric_rag/`.
No `CLAIMS.md` / `REFUTATION_PROTOCOL` — this is scaffolding for
downstream simulators to use, not a claim-making artifact of its
own. If the reasoning engine ever gets wired into an audit, that
audit picks up the claim table.

Sibling utilities in the repo:

- `tools/validate_claim_table.py` — schema check for CLAIM_TABLE JSON.
- `tools/substrate_substitution.py` / `substrate_substitution_toolkit.py`
  — narrative-bias structural-substitution helpers.
- `relational/geometric_rag/` — numpy hypergraph-manifold RAG demo,
  another dependency-carrying module landed under its own folder.

## Provenance

Two source drops:

1. **OKComputer_Automating_Equation_Evaluation** — the complete
   package including `symbolic`, `numerical`, `experiments`,
   `report`, `cli`, `domains/`, and the default `reasoning.py`.
   Landed as the primary contents of this folder.
2. **OKComputer_Build_the_Reasoning_Portion** — a specialized
   rewrite of just the reasoning submodule with stricter
   sandboxing, ID-tracked assumptions, and provenance in the
   derived facts. Landed as `crossdomain_eval/reasoning_v2.py`
   with its own test file to preserve both approaches.

Both drops passed their own test suites cleanly before landing
(47 / 47 and 21 / 21). Verified again after landing that both suites
run green together in the same package (68 / 68).

CC0.
