# crossdomain_eval

A Python toolkit for cross-domain analysis, scientific evaluation, complex design,
and experiment proposals. Automates equation evaluation, variable substitution,
symbolic/numerical analysis, rule-based reasoning, sensitivity analysis, and
design-of-experiments (DOE) planning.

## Install
```bash
pip install -e .          # from the project root
```

## Quick start

### Symbolic evaluation & substitution
```python
from crossdomain_eval import EquationSet

eqs = EquationSet(["F = m*a", "E = F*d"])
print(eqs.substitute({"m": 80, "a": 9.81, "d": 5}).evaluate({}))
print(eqs.solve("F"))
```

### Numerical analysis
```python
from crossdomain_eval import root_find, solve_ode, optimize
r = root_find(lambda x: x**3 - x - 2, (1, 2))
sol = solve_ode(lambda t, y: [-0.5*y[0]], [1.0], (0, 10))
```

### CLI
```bash
cdeval eval "F = m*a" --set m=80 a=9.81
cdeval solve "x**2 - 4" --for x
cdeval sweep "x**2 + y" --range x=0:5:50 --range y=0:3:30 --plot out.png
cdeval doe --factors temp,pressure,speed --levels 2
```

### Experiments & reasoning
```python
from crossdomain_eval.experiments import parameter_sweep, propose_experiments
from crossdomain_eval.reasoning import AssumptionTracker, RuleEngine

res = parameter_sweep(lambda p: p["x"]**2 + p["y"], {"x": (0, 5, 50), "y": (0, 3, 30)})
print(res.sensitivity())
print(propose_experiments("maximize yield", ["temp", "pressure"], levels=2))
```

## Modules
| Module | Purpose |
|---|---|
| `symbolic` | SymPy engine: parse, substitute, solve, differentiate, integrate, evaluate |
| `numerical` | Root finding, ODE solving, optimization (NumPy/SciPy) |
| `reasoning` | Assumption tracking + fixpoint rule-based inference |
| `experiments` | Parameter sweeps, sensitivity analysis, full-factorial DOE |
| `report` | Markdown reports + sweep plots |
| `domains/` | Domain adapters: physics, geometry (packing, TSP matrices) |
| `cli` | `cdeval` command-line interface |

## Examples
```bash
python examples/demo_symbolic.py
python examples/demo_experiment.py
```

## Tests
```bash
python -m pytest tests/ -q
```
