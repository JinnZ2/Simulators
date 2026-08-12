"""Demo: parse equations, substitute, solve, differentiate, evaluate."""

from crossdomain_eval import EquationSet, parse


def main() -> None:
    # Parse a bare expression and an equation
    expr = parse("x**2 - 4")
    eq = parse("y = m*x + b")
    print("parsed expression:", expr)
    print("parsed equation:  ", eq)

    # Build an EquationSet
    es = EquationSet(["y = m*x + b", "z = x**2 - 4"])
    print("\nequation set:", es)
    print("variables:", es.variables())

    # Substitute constants
    sub = es.substitute({"m": 2.0, "b": 1})
    print("\nafter substitute(m=2, b=1):", sub)

    # Evaluate numerically
    vals = sub.evaluate({"x": 3.0, "y": 7.0, "z": 5.0})
    print("evaluate(x=3, y=7, z=5):", vals)

    # Solve for x in y = 2x + 1
    sol = sub.equations[0]
    x_sol = EquationSet([str(sol)]).solve("x")
    print("\nsolve y = 2*x + 1 for x:", x_sol)

    # Solve a bare expression
    print("solve x**2 - 4 = 0 for x:", EquationSet(["x**2 - 4"]).solve("x"))

    # Differentiate
    deriv = es.differentiate("x")
    print("\nd/dx of equation set:", deriv)

    # Simplify
    simp = EquationSet(["x**2 + 2*x + 1 - (x + 1)**2"]).simplify()
    print("simplified:", simp)


if __name__ == "__main__":
    main()
