#!/usr/bin/env python3
# vector_field_explorer.py — CC0, stdlib-only, phone-buildable
#
# Exploratory sim for the interface-divergence idea: treat superconductor
# measurement channels as VECTORS (2D or 3D), hold them all simultaneously,
# and hunt for novel RELATIONAL structure BETWEEN them as parameters sweep.
#
# The premise (substrate-primary): the physics is not in the intrinsic layer
# alone or the extrinsic layer alone — it is in the DIVERGENCE between them,
# and in the angles between the measurement vectors. Standard instruments read
# scalar projections and lose the relational information. This reads the full
# vector field and flags where channels couple, rotate, phase-lock, or break
# symmetry.
#
# Channels are vectors, not scalars. A channel has magnitude AND direction.
# The novelty detector watches for ANGLE changes and cross-channel coupling,
# not just magnitude changes — that is the whole point.
#
# RELIABILITY TIERS:
#   FIRM   the vector algebra (rotation, divergence, phase-lock detection).
#   SOLID  the sweep/novelty/falsification loop — runs, produces real flags.
#   SOFT   the COUPLING constants are illustrative placeholders. Replace with
#          measured values from real superconductor data before any claim.
#          Every coupling is labeled with its confidence inline.

import math
import cmath
import statistics
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable

# ----------------------------------------------------------------------
# Vectors — 2D (magnitude, angle) and 3D (spherical). Unified interface.
# ----------------------------------------------------------------------

@dataclass
class Vec2:
    """2D vector as (magnitude, angle-radians). Angle is the load-bearing
    quantity — it carries the phase/orientation the scalar instruments drop."""
    mag: float
    ang: float

    def xy(self) -> Tuple[float, float]:
        return self.mag * math.cos(self.ang), self.mag * math.sin(self.ang)

    @staticmethod
    def from_xy(x: float, y: float) -> "Vec2":
        return Vec2(math.hypot(x, y), math.atan2(y, x))

    def rotated(self, dtheta: float) -> "Vec2":
        return Vec2(self.mag, self.ang + dtheta)

@dataclass
class Vec3:
    """3D vector in spherical (magnitude, theta=polar, phi=azimuth). For
    precession — the divergence vector that rotates as you move through a
    layered/tilted sample."""
    mag: float
    theta: float
    phi: float

    def xyz(self) -> Tuple[float, float, float]:
        st = math.sin(self.theta)
        return (self.mag * st * math.cos(self.phi),
                self.mag * st * math.sin(self.phi),
                self.mag * math.cos(self.theta))

    @staticmethod
    def from_xyz(x: float, y: float, z: float) -> "Vec3":
        r = math.sqrt(x*x + y*y + z*z)
        if r < 1e-12:
            return Vec3(0.0, 0.0, 0.0)
        return Vec3(r, math.acos(max(-1, min(1, z / r))), math.atan2(y, x))

# ----------------------------------------------------------------------
# Angle + divergence primitives (FIRM)
# ----------------------------------------------------------------------

def angle_between_2d(a: Vec2, b: Vec2) -> float:
    d = (a.ang - b.ang) % (2 * math.pi)
    return d if d <= math.pi else d - 2 * math.pi   # signed, in (-pi, pi]

def angle_between_3d(a: Vec3, b: Vec3) -> float:
    ax, ay, az = a.xyz(); bx, by, bz = b.xyz()
    na = math.sqrt(ax*ax+ay*ay+az*az); nb = math.sqrt(bx*bx+by*by+bz*bz)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    dot = (ax*bx + ay*by + az*bz) / (na * nb)
    return math.acos(max(-1, min(1, dot)))

def divergence_2d(intrinsic: Vec2, extrinsic: Vec2) -> Vec2:
    """The quantity the field ignores: the vector DIFFERENCE between the two
    layers. Its magnitude is the mismatch; its angle is the direction of
    disagreement. This is the third coordinate."""
    ix, iy = intrinsic.xy(); ex, ey = extrinsic.xy()
    return Vec2.from_xy(ex - ix, ey - iy)

def divergence_3d(intrinsic: Vec3, extrinsic: Vec3) -> Vec3:
    ix, iy, iz = intrinsic.xyz(); ex, ey, ez = extrinsic.xyz()
    return Vec3.from_xyz(ex - ix, ey - iy, ez - iz)

# ----------------------------------------------------------------------
# Channels — the measurement axes, each a vector
# ----------------------------------------------------------------------

class Dim(Enum):
    D2 = 2
    D3 = 3

@dataclass
class Channel:
    """A measurement axis carried as a vector. e.g. order-parameter phase,
    gap anisotropy, strain gradient, field response."""
    name: str
    dim: Dim
    vec2: Optional[Vec2] = None
    vec3: Optional[Vec3] = None

    def mag(self) -> float:
        return self.vec2.mag if self.dim is Dim.D2 else self.vec3.mag

# ----------------------------------------------------------------------
# Coupling — how channels drive each other. SOFT constants.
# ----------------------------------------------------------------------

@dataclass
class Coupling:
    """channel A's state drives channel B. `kind` selects the physics:
      'mag_to_mag'   : A's magnitude shifts B's magnitude
      'mag_to_angle' : A's magnitude rotates B (field tilts phase)
      'angle_to_angle': A's angle drags B's angle (co-rotation / phase-lock)
    strength is the SOFT placeholder — replace with measured coupling."""
    src: str
    dst: str
    kind: str
    strength: float
    confidence: str = "PLACEHOLDER"   # never EMPIRICAL until measured

# illustrative coupling set — the story these tell is a hypothesis to falsify
DEFAULT_COUPLINGS = [
    Coupling("strain", "gap", "mag_to_mag", -0.35, "PLACEHOLDER"),      # strain suppresses gap
    Coupling("field", "phase", "mag_to_angle", 0.8, "PLACEHOLDER"),     # field tilts phase
    Coupling("phase", "anisotropy", "angle_to_angle", 0.6, "PLACEHOLDER"), # phase drags anisotropy
    Coupling("gap", "anisotropy", "mag_to_mag", 0.4, "PLACEHOLDER"),
]

# ----------------------------------------------------------------------
# The measurement space
# ----------------------------------------------------------------------

class MeasurementSpace:
    def __init__(self, couplings=None):
        self.channels: Dict[str, Channel] = {}
        self.couplings: List[Coupling] = couplings or list(DEFAULT_COUPLINGS)
        self.params: Dict[str, float] = {}      # tunable environment
        self.t = 0.0

    def add(self, ch: Channel):
        self.channels[ch.name] = ch

    def set_param(self, k, v):
        self.params[k] = v

    def _apply_coupling(self, c: Coupling, dt: float):
        src = self.channels.get(c.src); dst = self.channels.get(c.dst)
        if src is None or dst is None:
            return
        s_mag = src.mag()
        if c.kind == "mag_to_mag":
            if dst.dim is Dim.D2:
                dst.vec2.mag = max(0.0, dst.vec2.mag + c.strength * s_mag * dt)
            else:
                dst.vec3.mag = max(0.0, dst.vec3.mag + c.strength * s_mag * dt)
        elif c.kind == "mag_to_angle":
            if dst.dim is Dim.D2:
                dst.vec2.ang += c.strength * s_mag * dt
            else:
                dst.vec3.phi += c.strength * s_mag * dt
        elif c.kind == "angle_to_angle":
            if src.dim is Dim.D2 and dst.dim is Dim.D2:
                # drag dst angle toward src angle
                da = angle_between_2d(src.vec2, dst.vec2)
                dst.vec2.ang += c.strength * da * dt
            elif src.dim is Dim.D3 and dst.dim is Dim.D3:
                dst.vec3.phi += c.strength * (src.vec3.phi - dst.vec3.phi) * dt
                dst.vec3.theta += c.strength * (src.vec3.theta - dst.vec3.theta) * dt

    def step(self, dt=1.0):
        for c in self.couplings:
            self._apply_coupling(c, dt)
        self.t += dt

    def snapshot(self) -> Dict[str, Dict]:
        out = {}
        for name, ch in self.channels.items():
            if ch.dim is Dim.D2:
                out[name] = {"mag": ch.vec2.mag, "ang": ch.vec2.ang}
            else:
                out[name] = {"mag": ch.vec3.mag, "theta": ch.vec3.theta,
                             "phi": ch.vec3.phi}
        return out

# ----------------------------------------------------------------------
# Relational events — the novelty the whole thing exists to find
# ----------------------------------------------------------------------

@dataclass
class RelationalEvent:
    kind: str          # PHASE_LOCK | DECOUPLE | SYMMETRY_BREAK | CO_ROTATE | SIGN_FLIP
    channels: Tuple[str, str]
    at_param: float
    detail: str

class RelationalDetector:
    """Watches pairs of channels across a sweep and flags relational structure.
    A lock only counts if it was DYNAMICALLY ACHIEVED — the pair must have been
    moving and then stopped. Guards against three artifacts that manufacture
    false positives:
      1. WARM-UP: the first `warmup` steps are ignored (startup transient).
      2. PRIOR MOTION: a pair must have shown real angle change before a
         'phase-lock' can be declared. Two idle channels are not locked.
      3. MAGNITUDE GATE: rotations driven by a near-zero-magnitude channel are
         noise; require the relevant magnitudes above `mag_floor`.
    Uses a history window so 'held constant' means constant across several
    steps, not one lucky small delta."""

    def __init__(self, warmup=3, window=3, mag_floor=0.1):
        self.warmup = warmup
        self.window = window
        self.mag_floor = mag_floor
        self.step_idx = 0
        self.diff_hist: Dict[Tuple[str, str], List[float]] = {}
        self.moved: Dict[Tuple[str, str], bool] = {}   # has this pair ever moved?
        self.locked: set = set()

    def _angle_diff(self, sa, sb, space) -> Optional[float]:
        ca, cb = space.channels[sa], space.channels[sb]
        if ca.dim is Dim.D2 and cb.dim is Dim.D2:
            return angle_between_2d(ca.vec2, cb.vec2)
        if ca.dim is Dim.D3 and cb.dim is Dim.D3:
            return angle_between_3d(ca.vec3, cb.vec3)
        return None

    def scan(self, space: MeasurementSpace, at_param: float,
             lock_tol=0.02, move_tol=0.03) -> List[RelationalEvent]:
        self.step_idx += 1
        events = []
        names = list(space.channels)
        for i, a in enumerate(names):
            for b in names[i+1:]:
                diff = self._angle_diff(a, b, space)
                if diff is None:
                    continue
                key = (a, b)
                hist = self.diff_hist.setdefault(key, [])
                hist.append(diff)
                if len(hist) > self.window + 1:
                    hist.pop(0)

                # WARM-UP guard: no verdicts during startup transient
                if self.step_idx <= self.warmup or len(hist) <= self.window:
                    continue

                # MAGNITUDE gate: both channels must carry real amplitude
                if space.channels[a].mag() < self.mag_floor or \
                   space.channels[b].mag() < self.mag_floor:
                    continue

                recent = hist[-(self.window+1):]
                deltas = [abs(recent[k+1] - recent[k]) for k in range(len(recent)-1)]
                max_delta = max(deltas)
                # PRIOR MOTION: mark the pair as having moved once it varies
                if max_delta >= move_tol:
                    self.moved[key] = True

                prev = recent[-2]
                # phase-lock: was moving, now held constant across the window
                if (self.moved.get(key) and max_delta < lock_tol
                        and key not in self.locked):
                    self.locked.add(key)
                    events.append(RelationalEvent(
                        "PHASE_LOCK", key, at_param,
                        f"Δangle settled at {diff:+.3f} rad after motion — "
                        f"dynamically phase-locked."))
                # decouple: a real lock started moving again
                elif max_delta >= lock_tol and key in self.locked:
                    self.locked.discard(key)
                    events.append(RelationalEvent(
                        "DECOUPLE", key, at_param,
                        f"locked pair separated (Δ resumed {max_delta:.3f})."))
                # sign flip: coherence inversion, only if pair has real motion
                if (self.moved.get(key) and prev * diff < 0
                        and abs(prev) > 0.08 and abs(diff) > 0.08):
                    events.append(RelationalEvent(
                        "SIGN_FLIP", key, at_param,
                        f"angle diff flipped {prev:+.2f}→{diff:+.2f} — "
                        f"coherence inversion (seal-band signature)."))
        return events

# ----------------------------------------------------------------------
# Explorer — sweep, watch all vectors, emit falsifiable predictions
# ----------------------------------------------------------------------

@dataclass
class CouplingClaim:
    pair: Tuple[str, str]
    predicted: str        # e.g. "phase-lock above tilt=0.6"
    at_param: float
    kind: str

def explore(space: MeasurementSpace, param: str, lo: float, hi: float,
            steps: int, drive_channel: str = None,
            drive_kind: str = "mag") -> Dict:
    """Sweep a parameter; the parameter drives one channel's magnitude (or a
    field angle). Watch ALL channels, log relational events, and turn the
    events into falsifiable coupling claims."""
    det = RelationalDetector()
    events: List[RelationalEvent] = []
    divergence_track: List[Tuple[float, float]] = []   # (param, |divergence|)

    step = (hi - lo) / (steps - 1) if steps > 1 else 0
    for i in range(steps):
        val = lo + step * i
        space.set_param(param, val)
        # inject the sweep into the driving channel
        if drive_channel and drive_channel in space.channels:
            ch = space.channels[drive_channel]
            if drive_kind == "mag":
                if ch.dim is Dim.D2: ch.vec2.mag = val
                else: ch.vec3.mag = val
            else:  # angle
                if ch.dim is Dim.D2: ch.vec2.ang = val
                else: ch.vec3.phi = val
        space.step()
        events.extend(det.scan(space, val))
        # track intrinsic/extrinsic divergence if both present
        if "intrinsic" in space.channels and "extrinsic" in space.channels:
            ci, ce = space.channels["intrinsic"], space.channels["extrinsic"]
            if ci.dim is Dim.D2:
                dv = divergence_2d(ci.vec2, ce.vec2)
                divergence_track.append((val, dv.mag))

    # events → falsifiable claims
    claims = []
    for e in events:
        claims.append(CouplingClaim(
            pair=e.channels, predicted=e.detail, at_param=e.at_param, kind=e.kind))
    return {"events": events, "claims": claims, "divergence": divergence_track}

# ----------------------------------------------------------------------
# DEMO — a 2D channel set and a 3D precession channel, swept together
# ----------------------------------------------------------------------

def demo():
    space = MeasurementSpace()
    # 2D channels: phase, anisotropy, gap, strain, field
    space.add(Channel("phase",      Dim.D2, vec2=Vec2(1.0, 0.0)))
    space.add(Channel("anisotropy", Dim.D2, vec2=Vec2(0.8, 0.5)))
    space.add(Channel("gap",        Dim.D2, vec2=Vec2(1.0, 0.0)))
    space.add(Channel("strain",     Dim.D2, vec2=Vec2(0.0, 0.3)))
    space.add(Channel("field",      Dim.D2, vec2=Vec2(0.0, 0.0)))
    # 3D divergence vector that precesses through the sample
    space.add(Channel("divergence3d", Dim.D3, vec3=Vec3(0.5, 0.4, 0.0)))

    print("=" * 66)
    print("VECTOR-FIELD EXPLORER — superconductor measurement space")
    print("channels held as vectors; watching angles & couplings, not scalars")
    print("=" * 66)

    print("\nSweep 1 — field magnitude 0→1.4 (field tilts phase, phase drags anisotropy)")
    r = explore(space, "field_mag", 0.0, 1.4, 30,
                drive_channel="field", drive_kind="mag")
    if r["events"]:
        for e in r["events"][:8]:
            print(f"  [{e.kind:12}] {e.channels[0]}×{e.channels[1]} "
                  f"@ {e.at_param:.2f}: {e.detail}")
    else:
        print("  no relational events — couplings too weak or sweep too short.")

    print(f"\n  relational events: {len(r['events'])}  "
          f"→ falsifiable claims: {len(r['claims'])}")

    print("\nSweep 2 — strain 0→1.0 (strain suppresses gap; watch gap-anisotropy)")
    space2 = MeasurementSpace()
    space2.add(Channel("gap",        Dim.D2, vec2=Vec2(1.0, 0.0)))
    space2.add(Channel("anisotropy", Dim.D2, vec2=Vec2(0.8, 0.6)))
    space2.add(Channel("strain",     Dim.D2, vec2=Vec2(0.0, 0.0)))
    r2 = explore(space2, "strain_mag", 0.0, 1.0, 25,
                 drive_channel="strain", drive_kind="mag")
    print(f"  events: {len(r2['events'])}")
    for e in r2["events"][:5]:
        print(f"  [{e.kind:12}] {e.channels[0]}×{e.channels[1]} @ {e.at_param:.2f}")

    print("\nFALSIFICATION FRAME:")
    print("  each relational event is a prediction: 'at this parameter, these")
    print("  two channels phase-lock / decouple / flip sign.' Measure it. If the")
    print("  real material does NOT show the predicted angle behavior, the")
    print("  COUPLING constant is wrong — update the coupling, not the sim.")
    print("  The SOFT couplings are placeholders; swap measured values in and")
    print("  the same engine yields real, testable predictions.")
    return r, r2

if __name__ == "__main__":
    demo()
