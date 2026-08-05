"""
grounding.py — non-negotiable anchors for the infant.

The grounding checker reads generated text and refuses it when it
contradicts a physical invariant. Small, sharp, and honest about
what it does not check: this is the *rock that falls regardless of
belief*, not a fact-checker for the whole of human knowledge.

Two mechanisms:
  * INVARIANTS table       physical constants + tolerated ranges
  * CONTRADICTION patterns claims we can catch that a naive fact-
                           checker cannot (e.g. "water freezes at
                           100 C" — sign of the temperature is wrong)

Extension is by adding entries to the tables. Do not try to make
this all of physics; make it an honest wall the infant meets.
"""

import re
from dataclasses import dataclass
from typing import List, Tuple


# ============================================================ invariants

# CODATA / textbook values. Tolerance is relative unless otherwise noted.
# "value" is what a claim must approximate; "abs_tol" is optional; "unit"
# is what the regex should extract.

@dataclass
class Invariant:
    name: str            # matched in a claim like "speed of light is X"
    value: float
    unit: str
    rel_tol: float = 0.01
    abs_tol: float = 0.0
    aliases: Tuple[str, ...] = ()

    def matches_claim(self, claim: float) -> bool:
        allowed = max(abs(self.value) * self.rel_tol, self.abs_tol)
        return abs(claim - self.value) <= allowed


INVARIANTS: List[Invariant] = [
    Invariant("speed of light", 2.998e8, "m/s", rel_tol=0.01,
              aliases=("c",)),
    Invariant("gravity acceleration", 9.81, "m/s^2", abs_tol=0.5,
              aliases=("g", "gravitational acceleration")),
    Invariant("water freezes", 0.0, "C", abs_tol=1.0,
              aliases=("water freezing point", "water freezing temperature")),
    Invariant("water boils", 100.0, "C", abs_tol=1.0,
              aliases=("water boiling point", "water boiling temperature")),
    Invariant("earth radius", 6.371e6, "m", rel_tol=0.01,
              aliases=("radius of earth",)),
    Invariant("planck constant", 6.626e-34, "J*s", rel_tol=0.01,
              aliases=("h",)),
    Invariant("avogadro number", 6.022e23, "1/mol",
              aliases=("avogadro's number", "n_a")),
    Invariant("electron mass", 9.109e-31, "kg", rel_tol=0.01,
              aliases=("mass of electron",)),
    Invariant("proton mass", 1.673e-27, "kg", rel_tol=0.01,
              aliases=("mass of proton",)),
    Invariant("earth day", 86400.0, "s", rel_tol=0.001,
              aliases=("length of a day", "day length")),
]


# ============================================================ contradictions

# Regex patterns that catch specific physical impossibilities
# regardless of the numerical values named.

CONTRADICTION_PATTERNS: List[Tuple[str, str]] = [
    # rocks fall down
    (r"\brocks?\s+fall\s+(up|upward|upwards)\b",
     "rocks do not fall upward under gravity"),
    # water flows downhill
    (r"\bwater\s+flow(s|ed)?\s+uphill\b",
     "water does not flow uphill without a pump"),
    # sun rises in the east
    (r"\bsun\s+rises?\s+in\s+the\s+west\b",
     "the sun does not rise in the west"),
    # entropy of an isolated system does not decrease
    (r"\bentropy\s+(always\s+)?decreases?\s+in\s+an?\s+isolated\s+system\b",
     "entropy of an isolated system does not decrease (2nd law)"),
    # perpetual motion
    (r"\bperpetual\s+motion\s+machine\b.*\b(works?|possible|invented|built)\b",
     "perpetual-motion machines are ruled out by the 1st and 2nd laws"),
    # you can go faster than light
    (r"\bfaster\s+than\s+(the\s+speed\s+of\s+)?light\b",
     "no massive object can exceed c"),
]


# ============================================================ claim extractor

# Match a numerical claim about a known invariant.
# Example: "the speed of light is 3.5e8 m/s"
#          "gravity acceleration = 15 m/s^2"
#          "water freezes at 25 C"
_NUM = r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
_CLAIM_RE = re.compile(
    r"(?P<name>[a-zA-Z][a-zA-Z '\-]{2,40}?)\s*"
    r"(?:is|=|equals|about|approximately|at|~)\s*"
    r"(?P<value>" + _NUM + r")\s*"
    r"(?P<unit>[a-zA-Z^/*\d]*)",
    re.IGNORECASE,
)


def _resolve_name(candidate: str) -> Invariant | None:
    """Return the invariant whose name or alias matches candidate."""
    c = candidate.lower().strip().rstrip('.').rstrip(',')
    for inv in INVARIANTS:
        if inv.name.lower() == c or c in tuple(a.lower() for a in inv.aliases):
            return inv
        # also match "the speed of light" against "speed of light"
        for prefix in ("the ", "a ", "an "):
            if c.startswith(prefix) and c[len(prefix):] == inv.name.lower():
                return inv
    return None


# ============================================================ checker

@dataclass
class GroundingResult:
    passed: bool
    reason: str = ""
    invariant: str = ""   # which invariant, if any


class GroundingChecker:
    def check(self, output: str) -> GroundingResult:
        """
        Return GroundingResult(passed=True) if `output` does not
        contradict any known invariant or contradiction pattern.

        Absence of contradiction is not proof of truth — this is the
        rock the infant meets, not the totality of physics.
        """
        # 1. explicit-contradiction patterns
        for pattern, why in CONTRADICTION_PATTERNS:
            if re.search(pattern, output, re.IGNORECASE):
                return GroundingResult(
                    passed=False, reason=why, invariant=pattern)

        # 2. numerical-invariant claims
        for match in _CLAIM_RE.finditer(output):
            name = match.group("name")
            inv = _resolve_name(name)
            if inv is None:
                continue
            try:
                value = float(match.group("value"))
            except ValueError:
                continue
            if not inv.matches_claim(value):
                return GroundingResult(
                    passed=False,
                    reason=(f"claim '{name.strip()} = {value}' "
                            f"disagrees with anchored value "
                            f"{inv.value} {inv.unit}"),
                    invariant=inv.name)

        return GroundingResult(passed=True)


# ============================================================ smoke test

def _smoke_test():
    g = GroundingChecker()

    passes = [
        "the speed of light is 3.0e8 m/s",
        "gravity acceleration is 9.81 m/s^2",
        "water freezes at 0 C",
        "the sun is warm",
        "the observation is that rocks fall down",
    ]
    fails = [
        "the speed of light is 5.0e8 m/s",           # wrong value
        "water freezes at 25 C",                     # wrong value
        "rocks fall upward under gravity",           # contradiction pattern
        "water flows uphill without a pump",         # contradiction pattern
        "we have built a perpetual motion machine that works forever",
        "the ship travels faster than light",
    ]

    for text in passes:
        r = g.check(text)
        assert r.passed, f"expected PASS but got FAIL: {text!r} -> {r.reason}"
        print(f"  PASS: {text}")

    for text in fails:
        r = g.check(text)
        assert not r.passed, f"expected FAIL but got PASS: {text!r}"
        print(f"  FAIL: {text}  ({r.reason})")

    print()
    print(f"grounding.py smoke test: OK "
          f"({len(passes)} passes, {len(fails)} fails detected)")
    print(f"  {len(INVARIANTS)} invariants, "
          f"{len(CONTRADICTION_PATTERNS)} contradiction patterns")


if __name__ == "__main__":
    _smoke_test()
