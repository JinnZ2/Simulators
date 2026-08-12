# SPEC.md — crossdomain_eval

A Python toolkit for cross-domain scientific analysis: symbolic equation evaluation,
variable substitution, numerical analysis, rule-based reasoning, sensitivity analysis,
and experiment/design proposal generation.

## Target
- Python 3.11+, installable package `crossdomain_eval` + CLI `cdeval`
- Deps: sympy, numpy, scipy, matplotlib (all available in the environment)
- No network access required. Deterministic, well-tested.

## Repo layout
```
/mnt/agents/output/project/
├── SPEC.md (copy)
├── README.md
├── pyproject.toml
├── crossdomain_eval/
│   ├── __init__.py          # exports public API
│   ├── symbolic.py          # OWNER: agent-core
│   ├── numerical.py         # OWNER: agent-core
│   ├── reasoning.py         # OWNER: agent-exp
│   ├── experiments.py       # OWNER: agent-exp
│   ├── report.py            # OWNER: agent-exp
│   ├── cli.py               # OWNER: agent-exp
│   └── domains/
│       ├── __init__.py      # registry
│       ├── physics.py       # OWNER: agent-core
│       └── geometry.py      # OWNER: agent-core (packing/TSP-style hooks)
├── examples/
│   ├── demo_symbolic.py     # OWNER: agent-core
│   └── demo_experiment.py   # OWNER: agent-exp
└── tests/
    ├── test_symbolic.py     # OWNER: agent-core
    ├── test_numerical.py    # OWNER: agent-core
    ├── test_reasoning.py    # OWNER: agent-exp
    ├── test_experiments.py  # OWNER: agent-exp
    └── test_report.py       # OWNER: agent-exp
```

## Interface contracts (sacred)

### symbolic.py
```python
class EquationSet:
    def __init__(self, equations: list[str], symbols: list[str] | None = None): ...
    def substitute(self, values: dict[str, float | str]) -> "EquationSet": ...
    def solve(self, target: str | None = None) -> dict: ...
    def simplify(self) -> "EquationSet": ...
    def differentiate(self, wrt: str) -> "EquationSet": ...
    def integrate(self, wrt: str) -> "EquationSet": ...
    def evaluate(self, values: dict[str, float]) -> dict[str, float]: ...
    def variables(self) -> list[str]: ...
def parse(expr: str) -> "sp.Expr": ...
```

### numerical.py
```python
def root_find(f, bracket: tuple[float, float], **kw) -> float: ...
def solve_ode(rhs, y0: list[float], t_span: tuple[float, float], n: int = 1000) -> dict: ...
    # returns {"t": np.ndarray, "y": np.ndarray}
def optimize(f, x0: list[float], bounds=None, method: str = "auto") -> dict: ...
    # returns {"x": list, "fun": float, "success": bool}
```

### reasoning.py
```python
class AssumptionTracker:
    def add(self, statement: str, confidence: float = 1.0): ...
    def check(self, predicate_name: str) -> bool: ...
    def report(self) -> list[dict]: ...
class RuleEngine:
    def add_rule(self, condition: str, conclusion: str): ...
        # condition/conclusion are python-expr strings over a facts dict
    def infer(self, facts: dict) -> dict: ...
```

### experiments.py
```python
def parameter_sweep(func, param_ranges: dict[str, tuple[float, float, int]],
                    fixed: dict | None = None) -> "SweepResult": ...
class SweepResult:
    results: "np.ndarray"; params: dict
    def sensitivity(self) -> dict[str, float]: ...   # normalized effect sizes
    def best(self, maximize: bool = True) -> dict: ...
def propose_experiments(objective_desc: str, factors: list[str],
                        levels: int = 2) -> list[dict]:
    # full factorial DOE plan; each dict = one run's factor settings
```

### report.py
```python
def markdown_report(title: str, sections: list[dict], path: str) -> str: ...
    # sections: [{"heading": str, "text": str, "figure": path|None, "table": dict|None}]
def plot_sweep(sweep: "SweepResult", x_param: str, path: str) -> str: ...
```

### cli.py
Commands (argparse):
- `cdeval eval "eq1; eq2" --set x=2 y=3`
- `cdeval solve "x**2 - 4" --for x`
- `cdeval sweep "x**2+y" --range x=0:5:50 --range y=0:3:30 --plot out.png`
- `cdeval doe --factors temp,pressure,speed --levels 2`

### domains/physics.py
`kinematics(v0, a, t)`, `energy(m, v)`, helpers returning EquationSet.
### domains/geometry.py
`packing_density(sphere_r, box_dims)`, `tsp_distance_matrix(points)` → np.ndarray.

## Rules
- Every public function: docstring + type hints.
- Tests must pass: `python -m pytest tests/ -q`.
- No unilateral interface changes. Questions → report back, don't improvise.
- Work only in your assigned worktree/branch; commit when tests pass.
