# equivalence_field.py
# CC0. stdlib-only. phone-buildable.
# spine: claim_lineage.py
#
# Push comparison DOWN THE PYRAMID to intensive variables -- densities,
# per-capita and per-node ratios, gradients -- where hidden asymmetry
# surfaces. Two systems are equivalent when their intensive vectors match
# within tolerance, NOT when top-line extensive totals match. A billion
# people and three hundred million is an extensive count; what drives is
# the intensive ratio (space per person, capital per node, ...).
#
# SYMMETRY AS ODDNESS
#   gradient g(A,B) = v(A) - v(B) is ODD under actor exchange: g(B,A) = -g(A,B).
#   The physics is odd. So a consistent reading of that gradient must ALSO be
#   odd. A reading that treats the same gradient differently depending on which
#   actor holds the high side is NON-ODD -- and that break is exactly where the
#   smuggled asymmetry (propaganda) lives. The audit reports WHICH dimensions
#   fail oddness, i.e. where the actor-label is doing work the gradient is not.
#
# anti-freeze: emit() returns the gradient FIELD + the oddness audit, never a
# verdict about who is right.
# energy_english: fields are intensive measurements and potentials only; no
# moral labels, no intent, no interior-state overlay.

from dataclasses import dataclass, field
from typing import Callable
from claim_lineage import Lineage, Claim


# ---------------------------------------------------------------------------
# systems and the intensive/extensive split
# ---------------------------------------------------------------------------
@dataclass
class System:
    name: str
    intensive: dict[str, float] = field(default_factory=dict)  # ratios/densities


def intensive_from(extensive: float, normalizer: float) -> float:
    """Make an extensive total intensive: total / (the thing it is spread over).
    e.g. population / land_area -> density; capital / nodes -> capital_per_node."""
    if normalizer == 0:
        raise ValueError("normalizer is zero; intensive undefined")
    return extensive / normalizer


# ---------------------------------------------------------------------------
# gradient field  (dimensionless, symmetric-relative, odd under exchange)
# ---------------------------------------------------------------------------
def rel_gradient(a: float, b: float) -> float:
    """Symmetric relative difference in [-2, 2]. Odd: swap(a,b) negates it.
    Dimensionless so dimensions with different units are comparable."""
    scale = (abs(a) + abs(b)) / 2.0
    if scale == 0:
        return 0.0
    return (a - b) / scale


def gradient_field(A: System, B: System) -> dict[str, float]:
    """Per-dimension potential v(A)-v(B). Each entry is a driver: sign gives
    direction (high -> low), magnitude gives pressure toward flow."""
    dims = set(A.intensive) | set(B.intensive)
    return {d: rel_gradient(A.intensive.get(d, 0.0), B.intensive.get(d, 0.0))
            for d in dims}


def exposed_asymmetry(A: System, B: System, tol: float = 0.1) -> dict[str, float]:
    """Dimensions where the intensive vectors fail to match within tol.
    These are the places the 'it's the same' claim collapses."""
    g = gradient_field(A, B)
    return {d: v for d, v in g.items() if abs(v) > tol}


# ---------------------------------------------------------------------------
# symmetry test = oddness audit of a READING
# ---------------------------------------------------------------------------
Reading = Callable[[dict[str, float]], dict[str, float]]


def honest_reading(g: dict[str, float]) -> dict[str, float]:
    """pressure = the gradient itself. Odd by construction -> passes."""
    return dict(g)


def make_threat_reading() -> Reading:
    """A reading that counts a gradient as pressure ONLY when it runs against
    the reader (max(0, g) per dim). This is the propaganda shape: the same
    gradient reversed is scored zero. It is NON-ODD -> the audit catches it."""
    def r(g: dict[str, float]) -> dict[str, float]:
        return {d: max(0.0, v) for d, v in g.items()}
    return r


def oddness_audit(reading: Reading, A: System, B: System,
                  tol: float = 1e-9) -> dict:
    """Swap the actors, re-read, and check the reading is odd per dimension:
    reading(g(A,B)) == -reading(g(B,A)). Dimensions that fail are where the
    reading treats the two directions differently -- the smuggled asymmetry."""
    g_ab = gradient_field(A, B)
    g_ba = gradient_field(B, A)
    r_ab = reading(g_ab)
    r_ba = reading(g_ba)
    breaks = {}
    for d in set(r_ab) | set(r_ba):
        lhs = r_ab.get(d, 0.0)
        rhs = -r_ba.get(d, 0.0)
        if abs(lhs - rhs) > tol:
            breaks[d] = {"reading(A,B)": round(r_ab.get(d, 0.0), 4),
                         "-reading(B,A)": round(rhs, 4)}
    return {"odd": len(breaks) == 0, "breaks": breaks}


# ---------------------------------------------------------------------------
# emit  (gradient field, not a verdict)
# ---------------------------------------------------------------------------
def emit(A: System, B: System, reading: Reading = honest_reading,
         tol: float = 0.1) -> dict:
    g = gradient_field(A, B)
    return {
        "systems": (A.name, B.name),
        "gradient_field": {d: round(v, 4) for d, v in g.items()},
        "exposed_asymmetry": {d: round(v, 4)
                              for d, v in exposed_asymmetry(A, B, tol).items()},
        "oddness_audit": oddness_audit(reading, A, B),
        "note": "gradient field + oddness audit. no verdict. sign = direction "
                "of potential (high->low); magnitude = pressure toward flow. "
                "oddness breaks mark where a reading is actor-dependent.",
    }


# ---------------------------------------------------------------------------
# the engine's OWN claims, self-hosted in the lineage spine
# ---------------------------------------------------------------------------
def seed_claims() -> Lineage:
    L = Lineage()
    L.add_root(Claim(
        cid="E1",
        statement="equivalence is a match of INTENSIVE vectors, not extensive totals",
        variables=("intensive_vector",),
        prediction="two systems with matched top-line totals but mismatched "
                   "intensive vectors are judged non-equivalent",
        refuted_if="dependents treat extensive-matched systems as equivalent "
                   "while their intensive vectors diverge",
    ))
    L.add_root(Claim(
        cid="E2",
        statement="a consistent reading of a gradient is ODD under actor exchange",
        variables=("gradient", "actor_label"),
        prediction="a reading that fails oddness carries an actor-dependent term "
                   "locatable to specific dimensions",
        refuted_if="a reading fails oddness with no isolable actor-dependent term",
    ))
    L.add_root(Claim(
        cid="E3",
        statement="gradient magnitude predicts pressure toward flow",
        variables=("gradient",),
        prediction="larger intensive gradients precede larger flows "
                   "(migration, capital, force), other dims held",
        refuted_if="flow magnitude is uncorrelated with gradient magnitude "
                   "at fixed other dimensions",
    ))
    return L


# ---------------------------------------------------------------------------
# self-check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # extensive totals differ wildly; build intensive vectors and compare there
    X = System("X", intensive={
        "people_per_space": intensive_from(1_000_000_000, 9_000_000),   # ~111
        "capital_per_node": 3.0,
        "ownership_concentration": 0.7,
    })
    Y = System("Y", intensive={
        "people_per_space": intensive_from(300_000_000, 9_000_000),     # ~33
        "capital_per_node": 3.1,
        "ownership_concentration": 0.2,
    })

    print("== honest reading ==")
    out = emit(X, Y, reading=honest_reading)
    print("gradient_field:", out["gradient_field"])
    print("exposed_asymmetry:", out["exposed_asymmetry"])
    print("oddness:", out["oddness_audit"]["odd"])

    print("== threat reading (propaganda shape) ==")
    out2 = emit(X, Y, reading=make_threat_reading())
    print("oddness:", out2["oddness_audit"]["odd"])
    print("breaks (where actor-label does the work):",
          list(out2["oddness_audit"]["breaks"].keys()))

    L = seed_claims()
    print("seeded claims:", [c.cid for c in L.frontier()])
