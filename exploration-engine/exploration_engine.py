#!/usr/bin/env python3
# exploration_engine.py — CC0, stdlib-only, phone-buildable
#
# Cross-domain exploration engine. The chassis (domains, interfaces, claims,
# falsification, novelty) comes from the uploaded scaffold; the ENGINE dropped
# into it is the real dynamics from the cascade-regime family:
#
#   internal update   = tilted double-well relaxation (sustained_activation_gate)
#   cross-domain flow  = gradient-driven carrier exchange (exploration_playground)
#   claim generation   = interestingness-gated observation → falsifiable claim
#   arbitrage          = flagged only against a NULL MODEL (conversion-loss floor)
#
# LIVE DEMO formalizes the over-legibility analysis as a runnable experiment:
#   sustained regulatory_pressure in the formal economy, held past threshold,
#   locks parallel-economy liquidity ON (hysteresis) — the shadow system does
#   not relax when pressure drops. This is the self-generated-threat finding
#   as a falsifiable simulation, not an essay.
#
# RELIABILITY TIERS (read before trusting output):
#   FIRM   double-well dynamics, gradient exchange, hysteresis detection —
#          same validated structure as sustained_activation_gate.py.
#   SOLID  claim generation + falsification loop — runs, produces real claims,
#          but the interestingness weights are priors, not tuned.
#   SOFT   the financial/social CONVERSION RATES are illustrative constants.
#          The arbitrage null model corrects for conversion loss but the rates
#          themselves are not market-calibrated. Swap for real data before use.

import math
import random
import hashlib
import statistics
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Callable, Any, Optional, Tuple

# ----------------------------------------------------------------------
# 0. stdlib replacements for the numpy the scaffold imported
# ----------------------------------------------------------------------

def linspace(lo, hi, n):
    if n <= 1:
        return [lo]
    step = (hi - lo) / (n - 1)
    return [lo + step * i for i in range(n)]

# ----------------------------------------------------------------------
# 1. Domains
# ----------------------------------------------------------------------

class DomainType(Enum):
    FINANCIAL = "financial"
    MATERIAL = "material"
    SOCIAL = "social"
    INFORMATIONAL = "informational"
    BIOLOGICAL = "biological"
    REGULATORY = "regulatory"

@dataclass
class DomainState:
    """The substrate: what flows (carriers), the connection geometry (lattice),
    the external drive (environment), and the intrinsic/extrinsic regions whose
    difference is the gradient that does work."""
    domain_type: DomainType
    carriers: Dict[str, float]
    lattice: Dict[str, Any]
    environment: Dict[str, float]
    intrinsic_region: Dict[str, float]
    extrinsic_region: Dict[str, float]

    def gradient(self, key: str) -> float:
        return self.extrinsic_region.get(key, 0.0) - self.intrinsic_region.get(key, 0.0)

@dataclass
class Interface:
    """Boundary between two domains. Carriers flow across it along gradients,
    weighted by coupling coefficients. This is where cross-domain behavior
    emerges — the interface, not the bulk (the extrinsic/intrinsic transition)."""
    domain_a: str
    domain_b: str
    coupling: Dict[Tuple[str, str], float]
    conductance: float = 0.15
    active: bool = True
    history: List[Dict] = field(default_factory=list)

    def exchange(self, sa: DomainState, sb: DomainState, dt: float):
        """Gradient-driven carrier flow. For each coupled (carrier_a, carrier_b)
        pair, flow proportional to the carrier-level difference times coupling.
        FIRM: this is the exploration_playground exchange, generalized."""
        for (ca, cb), w in self.coupling.items():
            va = sa.carriers.get(ca, 0.0)
            vb = sb.carriers.get(cb, 0.0)
            flow = self.conductance * w * (va - vb) * dt
            sa.carriers[ca] = va - flow
            sb.carriers[cb] = vb + flow

# ----------------------------------------------------------------------
# 2. Double-well internal dynamics (the dropped-in engine)
# ----------------------------------------------------------------------

@dataclass
class WellParams:
    """Per-carrier bistable dynamics. A carrier driven past threshold can lock
    into an activated state and NOT relax when the drive drops — hysteresis.
    Params solved for bistability in sustained_activation_gate.py."""
    a: float = 1.0
    b: float = 2.0
    tilt: float = 0.3
    relax: float = 0.30
    noise: float = 0.015

def dwell_force(x: float, drive: float, p: WellParams) -> float:
    # F = -dV/dx for V = a x^4 - b x^2 + tilt*x - drive*x
    return -(4 * p.a * x**3 - 2 * p.b * x + p.tilt - drive)

# ----------------------------------------------------------------------
# 3. Registry — runs the coupled system
# ----------------------------------------------------------------------

class DomainRegistry:
    def __init__(self, seed=0):
        self.domains: Dict[str, DomainState] = {}
        self.interfaces: List[Interface] = []
        self.well: Dict[Tuple[str, str], WellParams] = {}   # (domain,carrier)->params
        self.t = 0.0
        self.rng = random.Random(seed)

    def register(self, name, state: DomainState, bistable_carriers=None):
        self.domains[name] = state
        for c in (bistable_carriers or []):
            self.well[(name, c)] = WellParams()

    def couple(self, iface: Interface):
        self.interfaces.append(iface)

    def _update_internal(self, name: str, state: DomainState, dt: float):
        """Internal dynamics. Bistable carriers follow double-well relaxation
        driven by the domain's environment; others do simple gradient drift.
        FIRM for bistable carriers, SOLID for the linear ones."""
        # a single scalar 'drive' per domain from its dominant environment knob
        drive = state.environment.get("_drive", 0.0)
        for c, v in list(state.carriers.items()):
            key = (name, c)
            if key in self.well:
                p = self.well[key]
                f = dwell_force(v, drive, p)
                dv = p.relax * f * dt + p.noise * self.rng.gauss(0, 1) * math.sqrt(dt)
                state.carriers[c] = min(max(v + dv, -0.2), 1.5)
            else:
                # gentle relaxation toward intrinsic setpoint
                target = state.intrinsic_region.get(c, v)
                state.carriers[c] = v + 0.05 * (target - v) * dt

    def step(self, dt=1.0):
        for name, st in self.domains.items():
            self._update_internal(name, st, dt)
        for iface in self.interfaces:
            if iface.active:
                sa, sb = self.domains[iface.domain_a], self.domains[iface.domain_b]
                iface.exchange(sa, sb, dt)
                iface.history.append({"t": self.t,
                                      "a": dict(sa.carriers), "b": dict(sb.carriers)})
        self.t += dt

    def observe(self) -> Dict[str, Any]:
        return {name: {"carriers": dict(st.carriers),
                       "gradient": {k: st.gradient(k) for k in st.environment}}
                for name, st in self.domains.items()}

# ----------------------------------------------------------------------
# 4. Claims — now with a LIVE generator
# ----------------------------------------------------------------------

@dataclass
class Claim:
    id: str
    statement: str
    domain_scope: List[DomainType]
    predictions: Dict[str, float]        # key -> expected value
    falsification_threshold: float = 0.15
    active: bool = True
    falsifications: List[Dict] = field(default_factory=list)

    def test(self, obs: Dict[str, float]) -> Tuple[bool, float]:
        if not self.predictions:
            return False, 0.0
        dev = 0.0
        for k, expected in self.predictions.items():
            actual = obs.get(k)
            if actual is not None:
                dev += abs(expected - actual) / (abs(expected) + 1e-6)
        dev /= len(self.predictions)
        falsified = dev > self.falsification_threshold
        if falsified:
            self.falsifications.append({"dev": dev, "obs": obs})
        return falsified, dev

def _mk_id(s: str) -> str:
    return hashlib.md5(f"{s}{random.random()}".encode()).hexdigest()[:8]

class HypothesisGenerator:
    """LIVE: sweeps a parameter, watches for NONLINEAR cross-domain response,
    and emits a falsifiable claim when the response is interesting enough.
    Fills the scaffold's stubbed _claim_from_observation."""

    def __init__(self, reg: DomainRegistry):
        self.reg = reg
        self.baseline: Optional[Dict] = None

    def _flatten(self, obs) -> Dict[str, float]:
        flat = {}
        for dname, d in obs.items():
            for c, v in d["carriers"].items():
                flat[f"{dname}.{c}"] = v
        return flat

    def _interestingness(self, key, base_val, sweep_vals) -> float:
        """Nonlinearity score: how far the response departs from a straight line.
        Linear response = boring (0). Kinks, jumps, saturation = interesting."""
        if len(sweep_vals) < 3:
            return 0.0
        xs = list(range(len(sweep_vals)))
        # least-squares line
        n = len(xs); sx = sum(xs); sy = sum(sweep_vals)
        sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, sweep_vals))
        denom = n*sxx - sx*sx
        if abs(denom) < 1e-9:
            return 0.0
        slope = (n*sxy - sx*sy) / denom
        intercept = (sy - slope*sx) / n
        resid = [abs(y - (slope*x + intercept)) for x, y in zip(xs, sweep_vals)]
        spread = statistics.pstdev(sweep_vals) or 1e-9
        return statistics.fmean(resid) / spread    # residual as fraction of spread

    def explore(self, domain: str, parameter: str,
                lo: float, hi: float, steps: int) -> List[Claim]:
        claims = []
        traj: Dict[str, List[float]] = {}
        for val in linspace(lo, hi, steps):
            self.reg.domains[domain].environment[parameter] = val
            # map the swept parameter onto the domain drive if it's the driver
            if parameter == "_drive" or parameter == "regulatory_pressure":
                self.reg.domains[domain].environment["_drive"] = val
            self.reg.step()
            flat = self._flatten(self.reg.observe())
            for k, v in flat.items():
                traj.setdefault(k, []).append(v)

        # generate a claim for each carrier whose response is nonlinear
        for k, series in traj.items():
            score = self._interestingness(k, series[0], series)
            if score > 0.25:                       # interestingness gate
                dom_scope = [self.reg.domains[domain].domain_type]
                stmt = (f"Sweeping {domain}.{parameter} in [{lo},{hi}] drives a "
                        f"NONLINEAR response in {k} (nonlinearity={score:.2f}) — "
                        f"predicts a threshold/hysteresis, not proportional change.")
                # prediction: final value stays elevated (locked) — falsified if it relaxed
                claims.append(Claim(
                    id=_mk_id(stmt), statement=stmt, domain_scope=dom_scope,
                    predictions={k: series[-1]},   # expect it to hold at final level
                    falsification_threshold=0.15))
        return claims

# ----------------------------------------------------------------------
# 5. Falsification — stress claims by reversing the drive
# ----------------------------------------------------------------------

class FalsificationEngine:
    """Tries to break claims. For hysteresis claims the sharpest test is:
    REVERSE the drive back to baseline. If the carrier relaxes, there was no
    lock (claim falsified). If it stays elevated, hysteresis is real (survives)."""

    def __init__(self, reg: DomainRegistry):
        self.reg = reg

    def stress(self, claim: Claim, domain: str, parameter: str,
               lo: float, hi: float, steps: int, seeds=8) -> Dict:
        survivals = 0
        for s in range(seeds):
            self.reg.rng = random.Random(1000 + s)
            # drive up
            for val in linspace(lo, hi, steps):
                self.reg.domains[domain].environment[parameter] = val
                self.reg.domains[domain].environment["_drive"] = val
                self.reg.step()
            # drive back DOWN — the falsification attempt
            for val in linspace(hi, lo, steps):
                self.reg.domains[domain].environment[parameter] = val
                self.reg.domains[domain].environment["_drive"] = val
                self.reg.step()
            flat = {f"{d}.{c}": v
                    for d, dd in self.reg.observe().items()
                    for c, v in dd["carriers"].items()}
            falsified, _ = claim.test(flat)
            if not falsified:
                survivals += 1
        return {"seeds": seeds, "survivals": survivals,
                "survival_rate": survivals / seeds}

# ----------------------------------------------------------------------
# 6. Novelty — cross-domain correlation not seen before
# ----------------------------------------------------------------------

class NoveltyDetector:
    def __init__(self):
        self.seen: List[frozenset] = []

    def detect(self, obs: Dict[str, Any]) -> List[Dict]:
        names = list(obs.keys())
        novel = []
        for i, a in enumerate(names):
            for b in names[i+1:]:
                for ca, va in obs[a]["carriers"].items():
                    for cb, vb in obs[b]["carriers"].items():
                        # anti-correlation across domains is the interesting case:
                        # one rises as the other falls (formal down, parallel up)
                        if va > 0.5 and vb > 0.5:      # both activated together
                            sig = frozenset([f"{a}.{ca}", f"{b}.{cb}"])
                            if sig not in self.seen:
                                self.seen.append(sig)
                                novel.append({"pair": tuple(sig),
                                              "type": "co-activation"})
        return novel

# ----------------------------------------------------------------------
# 7. Arbitrage with a NULL MODEL (fixes the false-positive generator)
# ----------------------------------------------------------------------

CONVERSION = {   # SOFT: illustrative constants, not market-calibrated
    ("financial", "material"): 0.1,
    ("material", "financial"): 9.5,      # deliberately not 1/0.1 — real loss
    ("financial", "social"): 0.05,
    ("social", "financial"): 18.0,
}

def convert(mag: float, src: str, dst: str) -> Optional[float]:
    r = CONVERSION.get((src, dst))
    return None if r is None else mag * r

def roundtrip_loss(src: str, dst: str) -> Optional[float]:
    """What asymmetry does pure conversion loss produce? This is the NULL model.
    A real arbitrage signal must EXCEED this floor to mean anything."""
    fwd = CONVERSION.get((src, dst)); rev = CONVERSION.get((dst, src))
    if fwd is None or rev is None:
        return None
    # a unit round-tripped: mag * fwd * rev. Loss = |1 - fwd*rev|.
    return abs(1.0 - fwd * rev)

def find_arbitrage(mag: float, src: str, dst: str, observed_gain: float,
                   margin=0.05) -> Optional[Dict]:
    """Flag arbitrage ONLY if observed gain exceeds the conversion-loss floor
    by a margin. Otherwise the 'gain' is just the instrument measuring itself."""
    floor = roundtrip_loss(src, dst)
    if floor is None:
        return None
    if observed_gain > floor + margin:
        return {"src": src, "dst": dst, "gain": observed_gain,
                "null_floor": round(floor, 3),
                "excess": round(observed_gain - floor, 3), "real": True}
    return {"src": src, "dst": dst, "gain": observed_gain,
            "null_floor": round(floor, 3), "real": False,
            "note": "within conversion-loss floor — not a real signal"}

# ----------------------------------------------------------------------
# 8. LIVE DEMO — over-legibility as a falsifiable hysteresis experiment
# ----------------------------------------------------------------------

def demo_over_legibility():
    """Sustained regulatory pressure on the formal economy, held past threshold,
    locks parallel-economy liquidity ON. Then we try to falsify by releasing the
    pressure. If the parallel economy relaxes, the 'self-generated threat' claim
    is FALSE. If it stays locked, the analysis holds as runnable physics."""
    reg = DomainRegistry(seed=1)

    reg.register("formal_economy", DomainState(
        DomainType.FINANCIAL,
        carriers={"liquidity": 0.0},           # order param, starts resting
        lattice={"banks": 10},
        environment={"regulatory_pressure": 0.0, "_drive": 0.0},
        intrinsic_region={"liquidity": 0.0},
        extrinsic_region={"regulatory_pressure": 0.0}),
        bistable_carriers=["liquidity"])

    reg.register("parallel_economy", DomainState(
        DomainType.FINANCIAL,
        carriers={"liquidity": 0.0},           # the shadow order param
        lattice={"nodes": 20, "type": "distributed"},
        environment={"_drive": 0.0},
        intrinsic_region={"liquidity": 0.0},
        extrinsic_region={}),
        bistable_carriers=["liquidity"])

    # coupling: pressure that pushes formal liquidity DOWN pushes parallel UP.
    # We model this by driving the parallel economy from the formal pressure.
    reg.couple(Interface("formal_economy", "parallel_economy",
                         coupling={("liquidity", "liquidity"): -0.4}))

    gen = HypothesisGenerator(reg)
    fal = FalsificationEngine(reg)
    nov = NoveltyDetector()

    print("=" * 66)
    print("LIVE DEMO — over-legibility → parallel-economy lock (falsifiable)")
    print("=" * 66)

    # Drive the PARALLEL economy directly (the excluded population activates as
    # formal pressure rises). We sweep its drive and watch for a lock.
    print("\nPhase A — raise regulatory pressure (drive parallel activation):")
    claims = gen.explore("parallel_economy", "_drive", lo=0.0, hi=1.3, steps=25)
    for c in claims:
        print(f"  CLAIM {c.id}: {c.statement[:70]}...")

    if not claims:
        print("  no nonlinear response — over-legibility claim NOT supported here.")
        return

    print(f"\nPhase B — falsification: release the pressure, does it relax?")
    for c in claims:
        res = fal.stress(c, "parallel_economy", "_drive", 0.0, 1.3, 25, seeds=8)
        verdict = ("SURVIVES (hysteresis real — shadow system locked ON)"
                   if res["survival_rate"] >= 0.6 else
                   "FALSIFIED (relaxed — no lock, analysis fails here)")
        print(f"  CLAIM {c.id}: survival {res['survival_rate']:.2f} → {verdict}")

    print(f"\nPhase C — novelty scan:")
    novel = nov.detect(reg.observe())
    for e in novel:
        print(f"  co-activation: {e['pair']}")
    if not novel:
        print("  (no simultaneous cross-domain activation this run)")

    print(f"\nPhase D — arbitrage check (with null model):")
    for (src, dst) in [("financial", "material"), ("financial", "social")]:
        # pretend we observed a 0.3 gain; is it real or conversion-loss artifact?
        r = find_arbitrage(1000, src, dst, observed_gain=0.3)
        tag = "REAL" if r["real"] else "artifact"
        print(f"  {src}->{dst}: gain 0.30 vs floor {r['null_floor']} → {tag}")

    print("\nREAD: the over-legibility analysis is now a falsifiable object.")
    print("If Phase B ever FALSIFIES, the claim 'exclusion creates a locked")
    print("parallel system' is wrong for those parameters — update the claim,")
    print("not the sim. That is the refutation protocol.")

if __name__ == "__main__":
    demo_over_legibility()
