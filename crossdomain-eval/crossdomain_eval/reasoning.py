"""Rule-based reasoning and assumption tracking for crossdomain_eval."""

from __future__ import annotations

import re
from typing import Any


class AssumptionTracker:
    """Track named assumptions/statements with confidence values.

    Statements are stored with a predicate name derived from the statement
    text; predicates can be looked up with :meth:`check`.
    """

    def __init__(self) -> None:
        self._assumptions: list[dict[str, Any]] = []

    @staticmethod
    def _predicate(statement: str) -> str:
        """Derive a canonical predicate name from a statement string.

        The first word-character run is used, lowercased, so ``"Temp > 100"``
        yields predicate ``"temp"``.
        """
        m = re.search(r"[A-Za-z_][A-Za-z0-9_]*", statement)
        return m.group(0).lower() if m else statement.strip().lower()

    def add(self, statement: str, confidence: float = 1.0) -> None:
        """Record an assumption.

        Args:
            statement: Human-readable assumption, e.g. ``"temperature > 100"``.
            confidence: Confidence in [0, 1].
        """
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        self._assumptions.append(
            {
                "predicate": self._predicate(statement),
                "statement": statement,
                "confidence": float(confidence),
            }
        )

    def check(self, predicate_name: str) -> bool:
        """Return True if an assumption matching ``predicate_name`` exists.

        Matching is case-insensitive against both the derived predicate and
        a substring match on the statement text.
        """
        key = predicate_name.lower()
        for a in self._assumptions:
            if a["predicate"] == key or key in a["statement"].lower():
                return True
        return False

    def report(self) -> list[dict]:
        """Return all tracked assumptions as a list of dicts."""
        return [dict(a) for a in self._assumptions]


class RuleEngine:
    """Forward-chaining rule engine over a facts dictionary.

    Rules are added as (condition, conclusion) Python expression strings.
    Conditions are evaluated with :func:`eval` against the facts dict with
    builtins disabled. A conclusion may be either:

    - an assignment string ``"key = expression"`` which sets ``facts[key]``,
    - a bare expression whose value is stored under a derived key.

    :meth:`infer` applies rules repeatedly until a fixpoint is reached.
    """

    _ASSIGN_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=(?!=)")

    def __init__(self) -> None:
        self._rules: list[tuple[str, str]] = []

    def add_rule(self, condition: str, conclusion: str) -> None:
        """Add a rule.

        Args:
            condition: Python boolean expression over the facts dict,
                e.g. ``"temp > 100"``.
            conclusion: Assignment like ``"alert = True"`` or an expression
                evaluated and stored under a derived name.
        """
        self._rules.append((condition, conclusion))

    @staticmethod
    def _eval(expr: str, facts: dict) -> Any:
        """Safely evaluate an expression over facts with no builtins."""
        return eval(expr, {"__builtins__": {}}, dict(facts))  # noqa: S307

    def _apply(self, conclusion: str, facts: dict) -> bool:
        """Apply a conclusion to facts. Returns True if facts changed."""
        m = self._ASSIGN_RE.match(conclusion)
        if m:
            key = m.group(1)
            expr = conclusion[m.end():]
        else:
            key = re.sub(r"\W+", "_", conclusion).strip("_")
            expr = conclusion
        value = self._eval(expr, facts)
        if facts.get(key, object()) != value:
            facts[key] = value
            return True
        return False

    def infer(self, facts: dict) -> dict:
        """Apply rules repeatedly to fixpoint; return derived facts.

        The input ``facts`` dict is not mutated; a derived copy is returned.
        """
        derived = dict(facts)
        max_iterations = max(1, 10 * (len(self._rules) + 1) * (len(derived) + 10))
        for _ in range(max_iterations):
            changed = False
            for condition, conclusion in self._rules:
                try:
                    fired = bool(self._eval(condition, derived))
                except NameError:
                    continue  # missing facts -> rule cannot fire yet
                if fired:
                    try:
                        changed |= self._apply(conclusion, derived)
                    except NameError:
                        continue
            if not changed:
                break
        return derived
