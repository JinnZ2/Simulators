"""Symbolic equation handling built on sympy."""

from __future__ import annotations

import sympy as sp


def parse(expr: str) -> sp.Expr:
    """Parse a string into a sympy expression.

    Accepts either a bare expression (``"x**2 - 4"``) or an equation
    (``"lhs = rhs"``), which is converted to ``sp.Eq(lhs, rhs)``.

    Args:
        expr: String to parse via ``sympy.sympify``.

    Returns:
        The parsed sympy expression (``sp.Expr`` or ``sp.Eq``).
    """
    text = expr.strip()
    if "=" in text and not any(op in text for op in ("==", "<=", ">=", "!=")):
        lhs, rhs = text.split("=", 1)
        return sp.Eq(sp.sympify(lhs.strip()), sp.sympify(rhs.strip()))
    return sp.sympify(text)


class EquationSet:
    """A set of symbolic equations with substitution and calculus helpers."""

    def __init__(self, equations: list[str], symbols: list[str] | None = None):
        """Create an EquationSet from equation strings.

        Args:
            equations: Strings of the form ``"expr"`` or ``"lhs = rhs"``.
            symbols: Optional explicit symbol names to pre-declare.
        """
        self._symbols_hint = list(symbols) if symbols else None
        self.equations: list[sp.Expr] = [parse(e) for e in equations]

    def _new(self, equations: list[sp.Expr]) -> "EquationSet":
        obj = EquationSet.__new__(EquationSet)
        obj._symbols_hint = self._symbols_hint
        obj.equations = equations
        return obj

    def substitute(self, values: dict[str, float | str]) -> "EquationSet":
        """Return a new EquationSet with variables substituted.

        Values may be numbers or strings (parsed symbolically).
        """
        m = {sp.Symbol(k): (parse(v) if isinstance(v, str) else v)
             for k, v in values.items()}
        return self._new([eq.subs(m) for eq in self.equations])

    def solve(self, target: str | None = None) -> dict:
        """Solve the equations.

        Args:
            target: Variable to solve for. If None, solve the whole system
                for all free symbols.

        Returns:
            Mapping of variable name to solution value(s).
        """
        if target is not None:
            sym = sp.Symbol(target)
            sols = sp.solve(self.equations, sym)
            if isinstance(sols, dict):
                sols = [sols]
            normed = []
            for s in sols:
                if isinstance(s, dict):
                    normed.append(s[sym])
                elif isinstance(s, (tuple, list)):
                    normed.append(s[0])
                else:
                    normed.append(s)
            if len(normed) == 1:
                return {target: normed[0]}
            return {target: normed}
        syms = self.variables()
        sol = sp.solve(self.equations, [sp.Symbol(s) for s in syms], dict=True)
        if not sol:
            return {}
        if len(sol) == 1:
            return {str(k): v for k, v in sol[0].items()}
        return {f"solution_{i}": {str(k): v for k, v in s.items()}
                for i, s in enumerate(sol)}

    def simplify(self) -> "EquationSet":
        """Return a new EquationSet with each equation simplified."""
        return self._new([sp.simplify(eq) for eq in self.equations])

    def differentiate(self, wrt: str) -> "EquationSet":
        """Return a new EquationSet differentiated with respect to ``wrt``."""
        sym = sp.Symbol(wrt)

        def d(eq: sp.Expr) -> sp.Expr:
            if isinstance(eq, sp.Equality):
                return sp.Eq(sp.diff(eq.lhs, sym), sp.diff(eq.rhs, sym))
            return sp.diff(eq, sym)

        return self._new([d(eq) for eq in self.equations])

    def integrate(self, wrt: str) -> "EquationSet":
        """Return a new EquationSet integrated with respect to ``wrt``."""
        sym = sp.Symbol(wrt)

        def i(eq: sp.Expr) -> sp.Expr:
            if isinstance(eq, sp.Equality):
                return sp.Eq(sp.integrate(eq.lhs, sym), sp.integrate(eq.rhs, sym))
            return sp.integrate(eq, sym)

        return self._new([i(eq) for eq in self.equations])

    def evaluate(self, values: dict[str, float]) -> dict[str, float]:
        """Numerically evaluate each equation after substituting values.

        Returns:
            Mapping of variable or equation label to float value. For a
            bare expression, key is the expression string and value is its
            numeric value. For an equation, key is ``"lhs = rhs"`` and the
            value is ``lhs - rhs`` evaluated numerically.
        """
        m = {sp.Symbol(k): v for k, v in values.items()}
        out: dict[str, float] = {}
        for eq in self.equations:
            if isinstance(eq, sp.Equality):
                subbed = sp.Equality(eq.lhs.subs(m), eq.rhs.subs(m), evaluate=False)
                free = sorted(subbed.free_symbols, key=str)
                if not free:
                    label = f"{eq.lhs} = {eq.rhs}"
                    out[label] = float(subbed.lhs - subbed.rhs)
                elif len(free) == 1:
                    # One unknown remains: solve the equation for it.
                    sols = sp.solve(subbed, free[0])
                    if not sols:
                        raise ValueError(
                            f"Could not solve '{eq}' for '{free[0]}'")
                    out[str(free[0])] = float(sols[0])
                else:
                    raise ValueError(
                        f"Equation '{eq}' still has multiple unknowns after "
                        f"substitution: {[str(s) for s in free]}")
            else:
                out[str(eq)] = float(eq.subs(m))
        return out

    def variables(self) -> list[str]:
        """Return sorted free symbol names across all equations."""
        names: set[str] = set()
        for eq in self.equations:
            names |= {str(s) for s in eq.free_symbols}
        return sorted(names)

    def __repr__(self) -> str:
        return f"EquationSet({[str(e) for e in self.equations]})"
