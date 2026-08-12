"""Numerical analysis helpers built on numpy and scipy."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from scipy import integrate, optimize as sp_optimize


def root_find(f: Callable[[float], float], bracket: tuple[float, float], **kw) -> float:
    """Find a root of ``f`` within ``bracket`` using Brent's method.

    Args:
        f: Scalar function with a sign change over the bracket.
        bracket: ``(a, b)`` interval containing the root.
        **kw: Extra keyword arguments forwarded to ``scipy.optimize.brentq``.

    Returns:
        The root as a float.
    """
    return float(sp_optimize.brentq(f, bracket[0], bracket[1], **kw))


def solve_ode(rhs: Callable[[float, np.ndarray], list[float]],
              y0: list[float], t_span: tuple[float, float],
              n: int = 1000) -> dict:
    """Integrate an ODE system with scipy's RK45 solver.

    Args:
        rhs: Right-hand side ``f(t, y) -> dy/dt``.
        y0: Initial state vector.
        t_span: ``(t_start, t_end)``.
        n: Number of output sample points.

    Returns:
        ``{"t": np.ndarray, "y": np.ndarray}`` where ``y`` has shape
        ``(len(y0), n)``.
    """
    t_eval = np.linspace(t_span[0], t_span[1], n)
    sol = integrate.solve_ivp(rhs, t_span, y0, t_eval=t_eval, method="RK45",
                              rtol=1e-9, atol=1e-12)
    return {"t": sol.t, "y": sol.y}


def optimize(f: Callable[[np.ndarray], float], x0: list[float],
             bounds: list[tuple[float, float]] | None = None,
             method: str = "auto") -> dict:
    """Minimize a scalar function.

    Args:
        f: Objective function over a numpy array.
        x0: Initial guess.
        bounds: Optional per-variable ``(low, high)`` bounds.
        method: ``"auto"`` (L-BFGS-B if bounds else BFGS), or any
            scipy ``minimize`` method name.

    Returns:
        ``{"x": list, "fun": float, "success": bool}``.
    """
    if method == "auto":
        method = "L-BFGS-B" if bounds else "BFGS"
    res = sp_optimize.minimize(f, np.asarray(x0, dtype=float),
                               bounds=bounds, method=method)
    return {"x": list(res.x), "fun": float(res.fun), "success": bool(res.success)}
