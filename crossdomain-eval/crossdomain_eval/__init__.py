"""crossdomain_eval: cross-domain scientific analysis toolkit."""

from crossdomain_eval.numerical import optimize, root_find, solve_ode
from crossdomain_eval.symbolic import EquationSet, parse
from crossdomain_eval.experiments import SweepResult, parameter_sweep, propose_experiments
from crossdomain_eval.reasoning import AssumptionTracker, RuleEngine
from crossdomain_eval.report import markdown_report, plot_sweep

__all__ = [
    "EquationSet",
    "parse",
    "root_find",
    "solve_ode",
    "optimize",
    "AssumptionTracker",
    "RuleEngine",
    "SweepResult",
    "parameter_sweep",
    "propose_experiments",
    "markdown_report",
    "plot_sweep",
]
