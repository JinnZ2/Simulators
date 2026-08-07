"""Physics domain equation helpers."""

from __future__ import annotations

from crossdomain_eval.symbolic import EquationSet


def kinematics(v0: float | str = "v0", a: float | str = "a",
               t: float | str = "t") -> EquationSet:
    """Constant-acceleration kinematics equation set.

    Provides ``v = v0 + a*t`` and ``s = v0*t + a*t**2/2``.

    Args:
        v0: Initial velocity (number or symbol name).
        a: Acceleration (number or symbol name).
        t: Time (number or symbol name).

    Returns:
        An EquationSet for the kinematic relations.
    """
    return EquationSet([
        f"v = {v0} + {a}*{t}",
        f"s = {v0}*{t} + {a}*{t}**2/2",
    ])


def energy(m: float | str = "m", v: float | str = "v") -> EquationSet:
    """Energy equation set: kinetic and rest energy.

    Provides ``KE = m*v**2/2`` and ``PE = m*g*h``.

    Args:
        m: Mass (number or symbol name).
        v: Velocity (number or symbol name).

    Returns:
        An EquationSet for energy relations.
    """
    return EquationSet([
        f"KE = {m}*{v}**2/2",
        f"PE = {m}*g*h",
    ])
