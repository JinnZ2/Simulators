"""Command-line interface ``cdeval`` for crossdomain_eval."""

from __future__ import annotations

import argparse
import json
import sys


def _parse_kv(pairs: list[str] | None) -> dict[str, float]:
    """Parse ``name=value`` strings into a float-valued dict."""
    out: dict[str, float] = {}
    for pair in pairs or []:
        name, _, val = pair.partition("=")
        try:
            out[name.strip()] = float(val)
        except ValueError:
            out[name.strip()] = val.strip()
    return out


def _parse_range(spec: str) -> tuple[str, tuple[float, float, int]]:
    """Parse ``name=lo:hi:n`` into (name, (lo, hi, n))."""
    name, _, rest = spec.partition("=")
    lo, hi, n = rest.split(":")
    return name.strip(), (float(lo), float(hi), int(n))


def _cmd_eval(args: argparse.Namespace) -> int:
    """Evaluate equations with variable substitutions."""
    from .symbolic import EquationSet  # lazy: provided by agent-core

    eqs = EquationSet([e.strip() for e in args.equations.split(";") if e.strip()])
    result = eqs.evaluate(_parse_kv(args.set))
    print(json.dumps(result, indent=2, default=float))
    return 0


def _cmd_solve(args: argparse.Namespace) -> int:
    """Solve an equation for a target symbol."""
    from .symbolic import EquationSet  # lazy: provided by agent-core

    eqs = EquationSet([args.equation])
    result = eqs.solve(target=args.target)
    print(json.dumps(result, indent=2, default=str))
    return 0


def _cmd_sweep(args: argparse.Namespace) -> int:
    """Run a parameter sweep over a symbolic expression."""
    from .experiments import parameter_sweep
    from .report import plot_sweep
    from .symbolic import parse  # lazy: provided by agent-core

    expr = parse(args.expression)
    ranges = dict(_parse_range(r) for r in args.range)
    symbols = [str(s) for s in expr.free_symbols]
    fixed = {s: 0.0 for s in symbols if s not in ranges}

    def func(**kw: float) -> float:
        return float(expr.evalf(subs=kw))

    sweep = parameter_sweep(func, ranges, fixed=fixed)
    print("sensitivity:", json.dumps(sweep.sensitivity(), indent=2))
    print("best:", json.dumps(sweep.best(maximize=not args.minimize), indent=2))
    if args.plot:
        plot_sweep(sweep, next(iter(ranges)), args.plot)
        print(f"plot written to {args.plot}")
    return 0


def _cmd_doe(args: argparse.Namespace) -> int:
    """Generate a full-factorial DOE plan."""
    from .experiments import propose_experiments

    factors = [f.strip() for f in args.factors.split(",") if f.strip()]
    plan = propose_experiments(args.objective or "unnamed objective", factors, levels=args.levels)
    print(json.dumps(plan, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the ``cdeval`` argument parser."""
    parser = argparse.ArgumentParser(prog="cdeval", description="crossdomain_eval CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("eval", help="evaluate equations with substitutions")
    p.add_argument("equations", help='semicolon-separated equations, e.g. "x+y; x*y"')
    p.add_argument("--set", nargs="*", default=[], metavar="NAME=VALUE",
                   help="variable substitutions, e.g. --set x=2 y=3")
    p.set_defaults(func=_cmd_eval)

    p = sub.add_parser("solve", help="solve an equation for a symbol")
    p.add_argument("equation", help='equation/expression, e.g. "x**2 - 4"')
    p.add_argument("--for", dest="target", default=None, help="symbol to solve for")
    p.set_defaults(func=_cmd_solve)

    p = sub.add_parser("sweep", help="parameter sweep of an expression")
    p.add_argument("expression", help='expression, e.g. "x**2 + y"')
    p.add_argument("--range", action="append", required=True, metavar="NAME=LO:HI:N",
                   help="swept parameter range; repeat for multiple params")
    p.add_argument("--plot", default=None, help="optional output image path")
    p.add_argument("--minimize", action="store_true", help="report argmin instead of argmax")
    p.set_defaults(func=_cmd_sweep)

    p = sub.add_parser("doe", help="full-factorial design of experiments plan")
    p.add_argument("--factors", required=True, help="comma-separated factor names")
    p.add_argument("--levels", type=int, default=2, help="coded levels per factor")
    p.add_argument("--objective", default=None, help="objective description")
    p.set_defaults(func=_cmd_doe)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``cdeval`` CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
