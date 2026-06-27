"""
forcing.py -- AMOC collapse as a control parameter, two formulations.

CC0. stdlib-only. Anti-freeze: nothing here returns a verdict. Everything
returns the *shape of the response surface* under a swept forcing, so the
caller sees where the gradient bends, where it oscillates, where it locks.

Two models, one interface (.state(F), .sweep(...), .is_bistable_region(...)):

  StommelBox   -- two-box thermohaline model (Stommel 1961 nondim form).
                  Freshwater flux F is the control parameter. Bistable:
                  thermal mode (overturning ON, q>0) vs haline mode
                  (overturning collapsed, q<0). Easy for non-substrate users
                  to read -- F in, flow q out, hysteresis visible.

  KramersWell  -- escape-rate dynamics over a tilted double-well. Mirrors
                  field_collapse.py so this drops into the JinnZ2 ecosystem.
                  Forcing tilts the well; escape rate r crosses the spinodal
                  when the barrier vanishes. Continuous with cascade work.

Pick by readability of audience, not by which is "right." They are two
instruments pointed at the same transition.

Units note: F (freshwater forcing) is nondimensional here. site.py is where
real sverdrups get mapped onto this axis, with the mapping declared, not
hidden. Do not read F as Sv without going through site.calibrate_forcing().
"""

import math
from dataclasses import dataclass, field
from typing import Callable, Optional


# ----------------------------------------------------------------------
# small stdlib RK4 so we carry no numpy dependency
# ----------------------------------------------------------------------
def rk4_step(f: Callable, t: float, y: list, h: float) -> list:
    k1 = f(t, y)
    k2 = f(t + h / 2, [yi + h / 2 * k1i for yi, k1i in zip(y, k1)])
    k3 = f(t + h / 2, [yi + h / 2 * k2i for yi, k2i in zip(y, k2)])
    k4 = f(t + h, [yi + h * k3i for yi, k3i in zip(y, k3)])
    return [yi + h / 6 * (a + 2 * b + 2 * c + d)
            for yi, a, b, c, d in zip(y, k1, k2, k3, k4)]


# ----------------------------------------------------------------------
# Model 1: Stommel two-box (audience: anyone)
# ----------------------------------------------------------------------
@dataclass
class StommelState:
    F: float            # freshwater forcing (nondim control parameter)
    dT: float           # equator-pole temperature contrast (nondim)
    dS: float           # equator-pole salinity contrast (nondim)
    q: float            # density-driven flow; >0 thermal mode, <0 haline mode
    mode: str           # "thermal_on" | "haline_collapsed" | "transitional"
    converged: bool


@dataclass
class StommelBox:
    """
    Nondimensional Stommel. Temperature restores fast to the atmosphere;
    salinity is driven by freshwater flux F and advected by the flow.

        q  = dT - dS                       (thermal minus haline density)
        dT' = (1 - dT)/eps - |q|*dT        (eps small: fast thermal restoring)
        dS' = F        - |q|*dS

    Thermal mode: dS low, q>0, vigorous overturning.
    Haline mode:  dS high, q<0, collapsed / reversed.
    Between the two saddle-node (spinodal) points the system is bistable:
    which state you land in depends on history -> hysteresis.
    """
    eps: float = 0.05          # thermal restoring speed (smaller = faster)
    dt: float = 0.01
    max_t: float = 4000.0
    tol: float = 1e-7

    def _rhs(self, F: float):
        def rhs(t, y):
            dT, dS = y
            q = dT - dS
            aq = abs(q)
            ddT = (1.0 - dT) / self.eps - aq * dT
            ddS = F - aq * dS
            return [ddT, ddS]
        return rhs

    def state(self, F: float, dT0: float = 1.0, dS0: float = 0.3) -> StommelState:
        """Integrate to equilibrium from a given start. Start matters: it
        selects which basin you fall into inside the bistable band."""
        rhs = self._rhs(F)
        y = [dT0, dS0]
        t = 0.0
        converged = False
        prev = None
        while t < self.max_t:
            y = rk4_step(rhs, t, y, self.dt)
            t += self.dt
            if prev is not None:
                if (abs(y[0] - prev[0]) < self.tol * self.dt and
                        abs(y[1] - prev[1]) < self.tol * self.dt):
                    converged = True
                    break
            prev = y[:]
        q = y[0] - y[1]
        if q > 0.05:
            mode = "thermal_on"
        elif q < -0.05:
            mode = "haline_collapsed"
        else:
            mode = "transitional"
        return StommelState(F=F, dT=y[0], dS=y[1], q=q, mode=mode,
                            converged=converged)

    def sweep(self, F_lo: float, F_hi: float, n: int = 60,
              direction: str = "up") -> list:
        """
        Quasi-static sweep of F, carrying state forward so hysteresis shows.
        direction="up": ramp F up (loading freshwater) -> catch the ON->collapse
                        spinodal.
        direction="down": ramp F down -> catch the collapse->ON spinodal.
        The two sweeps will NOT coincide if the system is bistable. That gap
        is the hysteresis loop -- the thing linear models throw away.
        """
        Fs = [F_lo + (F_hi - F_lo) * i / (n - 1) for i in range(n)]
        if direction == "down":
            Fs = list(reversed(Fs))
        out = []
        # seed: up-sweep starts in thermal mode, down-sweep starts collapsed.
        # Down-sweep seed sits just inside the haline basin (dS only modestly
        # above dT) so recovery is reachable as F falls, instead of being
        # pinned so deep it never returns inside the searched range.
        if direction == "up":
            dT0, dS0 = 1.0, 0.2
        else:
            dT0, dS0 = 0.8, 1.05
        for F in Fs:
            s = self.state(F, dT0=dT0, dS0=dS0)
            dT0, dS0 = s.dT, s.dS   # carry state -> hysteresis
            out.append(s)
        return out

    def hysteresis_band(self, F_lo: float, F_hi: float, n: int = 80) -> dict:
        """
        Map the bistable band by probing BOTH basins at each F (thermal seed
        and haline seed) and asking where two stable states coexist. This is
        more honest than a carried-state sweep, which can be poisoned once one
        branch collapses. Trajectory, not verdict: where coexistence ends is
        the spinodal; if never found in range, says so.
        """
        Fs = [F_lo + (F_hi - F_lo) * i / (n - 1) for i in range(n)]
        coexist = []
        thermal_only = []
        haline_only = []
        for F in Fs:
            th = self.state(F, dT0=1.0, dS0=0.1)
            ha = self.state(F, dT0=0.7, dS0=1.3)
            th_on = th.mode == "thermal_on"
            ha_off = ha.mode != "thermal_on"
            if th_on and ha_off:
                coexist.append(F)
            elif th_on and not ha_off:
                thermal_only.append(F)
            else:
                haline_only.append(F)
        spinodal_collapse = coexist[-1] if coexist else None   # ON loses stability above this
        spinodal_recovery = coexist[0] if coexist else None    # OFF loses stability below this
        return {
            "spinodal_recovery": spinodal_recovery,   # below: only thermal ON survives
            "spinodal_collapse": spinodal_collapse,   # above: only haline collapse survives
            "bistable": len(coexist) > 0,
            "bistable_band": (spinodal_recovery, spinodal_collapse),
            "searched_range": (F_lo, F_hi),
            "note": "Inside [recovery, collapse] both states are stable: which "
                    "one you are in depends on history. Cross spinodal_collapse "
                    "and there is no thermal branch left to fall back to.",
        }


# ----------------------------------------------------------------------
# Model 2: Kramers tilted double-well (audience: cascade/JinnZ2 continuity)
# ----------------------------------------------------------------------
@dataclass
class KramersState:
    F: float            # external forcing (tilt source)
    tilt: float         # h_ext applied to the well
    barrier_on_to_off: float   # delta-U out of the ON basin
    barrier_off_to_on: float
    escape_rate_on_to_off: float
    escape_rate_off_to_on: float
    spinodal: bool      # True if a basin barrier has vanished (no return)
    dominant: str       # which way the system is being driven


@dataclass
class KramersWell:
    """
    Potential  U(x) = x^4/4 - x^2/2 - h*x     (canonical tilted double-well).
    Wells near x=-1 (ON / overturning) and x=+1 (OFF / collapsed) when h=0.
    Forcing F maps to tilt h via forcing_gain. Noise amplitude D sets the
    Kramers escape rate r = (w0/2pi) * exp(-dU / D).

    Spinodal: as |h| grows the shallower barrier shrinks to zero. Past that,
    escape is not thermally activated noise any more -- it is deterministic,
    field-independent, self-driven. Same finding as field_collapse.py:
    above critical coupling the collapse no longer needs the field.
    """
    D: float = 0.06            # effective noise (mixing, internal variability)
    forcing_gain: float = 1.0  # F -> tilt h
    w0: float = 1.0            # attempt frequency prefactor

    def _wells_and_barrier(self, h: float):
        """Solve U'(x)=x^3 - x - h = 0 for the three roots (two minima, one
        max) when they exist. Returns (x_on, x_bar, x_off, exists)."""
        # depressed cubic x^3 + px + q = 0, p=-1, q=-h
        p, q = -1.0, -h
        disc = (q / 2) ** 2 + (p / 3) ** 3
        if disc > 0:
            # one real root -> barrier gone (spinodal passed)
            return (None, None, None, False)
        # three real roots via trig method
        r = math.sqrt(-(p ** 3) / 27)
        phi = math.acos(max(-1.0, min(1.0, -q / (2 * r))))
        m = 2 * math.sqrt(-p / 3)
        roots = sorted(
            m * math.cos((phi + 2 * math.pi * k) / 3) for k in range(3)
        )
        x_on, x_bar, x_off = roots[0], roots[1], roots[2]
        return (x_on, x_bar, x_off, True)

    def _U(self, x: float, h: float) -> float:
        return x ** 4 / 4 - x ** 2 / 2 - h * x

    def state(self, F: float) -> KramersState:
        h = self.forcing_gain * F
        x_on, x_bar, x_off, exists = self._wells_and_barrier(h)
        if not exists:
            # spinodal passed: one basin only, deterministic slide
            dominant = "collapse_to_off" if h > 0 else "drive_to_on"
            return KramersState(
                F=F, tilt=h,
                barrier_on_to_off=0.0, barrier_off_to_on=math.inf,
                escape_rate_on_to_off=math.inf, escape_rate_off_to_on=0.0,
                spinodal=True, dominant=dominant)
        U_on = self._U(x_on, h)
        U_bar = self._U(x_bar, h)
        U_off = self._U(x_off, h)
        dU_on = U_bar - U_on     # ON basin barrier
        dU_off = U_bar - U_off   # OFF basin barrier
        r_on = (self.w0 / (2 * math.pi)) * math.exp(-dU_on / self.D)
        r_off = (self.w0 / (2 * math.pi)) * math.exp(-dU_off / self.D)
        dominant = "collapse_to_off" if r_on > r_off else "hold_or_recover"
        return KramersState(
            F=F, tilt=h,
            barrier_on_to_off=dU_on, barrier_off_to_on=dU_off,
            escape_rate_on_to_off=r_on, escape_rate_off_to_on=r_off,
            spinodal=False, dominant=dominant)

    def sweep(self, F_lo: float, F_hi: float, n: int = 60) -> list:
        return [self.state(F_lo + (F_hi - F_lo) * i / (n - 1))
                for i in range(n)]

    def spinodal_forcing(self, F_lo: float = 0.0, F_hi: float = 1.0,
                         n: int = 200) -> Optional[float]:
        """First F in range where the ON basin barrier vanishes. None if not
        reached -- reported honestly, not silently assumed safe."""
        for i in range(n):
            F = F_lo + (F_hi - F_lo) * i / (n - 1)
            s = self.state(F)
            if s.spinodal or s.barrier_on_to_off <= 1e-6:
                return F
        return None


# ----------------------------------------------------------------------
# self-test
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("== StommelBox ==")
    box = StommelBox()
    band = box.hysteresis_band(0.0, 1.6, n=60)
    for k, v in band.items():
        print(f"  {k}: {v}")

    print("\n== KramersWell ==")
    well = KramersWell()
    sp = well.spinodal_forcing(0.0, 1.0, 200)
    print(f"  spinodal forcing (ON barrier -> 0): {sp}")
    for F in (0.0, 0.2, 0.38, 0.5):
        s = well.state(F)
        print(f"  F={F:.2f} barrier_on={s.barrier_on_to_off:.4f} "
              f"r_on={s.escape_rate_on_to_off:.3e} spinodal={s.spinodal}")
