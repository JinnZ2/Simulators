"""Rule-based reasoning utilities for crossdomain_eval.

OWNER: agent-exp

This module provides two complementary pieces:

- :class:`AssumptionTracker` — an audit trail for assumptions made during an
  analysis. Every assumption carries a confidence in [0, 1] and can be
  retracted (kept, but marked inactive) so downstream reports can show both
  what is currently believed and what was once believed.
- :class:`RuleEngine` — a small forward-chaining inference engine. Rules are
  ``(condition, conclusion)`` string pairs evaluated over a facts dict.
  ``infer`` applies rules to a fixpoint, so conclusions of earlier rules can
  trigger later ones.

Both classes are deliberately deterministic and dependency-free.
"""

from __future__ import annotations

import re
from typing import Any

__all__ = ["AssumptionTracker", "RuleEngine"]

# Names that must never be readable or writable inside rule evaluation.
_FORBIDDEN = re.compile(r"__|import|open|exec|eval|globals|locals")


class AssumptionTracker:
    """Track assumptions, their confidence, and their status.

    Parameters
    ----------
    None

    Notes
    -----
    ``check`` answers "do we currently hold this assumption?" — it returns
    ``True`` only if an assumption with exactly that statement exists, has
    not been retracted, and has confidence >= 0.5 (i.e. we hold it more
    likely than not).
    """

    #: confidence at or above which an assumption counts as "held"
    HELD_THRESHOLD = 0.5

    def __init__(self) -> None:
        self._assumptions: list[dict[str, Any]] = []
        self._next_id: int = 1

    def add(self, statement: str, confidence: float = 1.0) -> int:
        """Record an assumption.

        Parameters
        ----------
        statement:
            Human- and machine-readable statement of the assumption,
            e.g. ``"friction_is_negligible"``. Used verbatim by
            :meth:`check`, so keep naming consistent.
        confidence:
            Subjective confidence in [0, 1]. Defaults to 1.0 (certain).

        Returns
        -------
        int
            The id assigned to this assumption (stable, 1-based, increasing).

        Raises
        ------
        ValueError
            If ``statement`` is empty or ``confidence`` is outside [0, 1].
        """
        if not isinstance(statement, str) or not statement.strip():
            raise ValueError("statement must be a non-empty string")
        if not (0.0 <= float(confidence) <= 1.0):
            raise ValueError("confidence must be in [0, 1]")
        entry = {
            "id": self._next_id,
            "statement": statement.strip(),
            "confidence": float(confidence),
            "active": True,
        }
        self._assumptions.append(entry)
        self._next_id += 1
        return entry["id"]

    def check(self, predicate_name: str) -> bool:
        """Return True if ``predicate_name`` is a currently held assumption.

        An assumption counts as held when it is active and its confidence is
        at least :attr:`HELD_THRESHOLD`. Later duplicates shadow earlier ones
        (the most recently added matching entry wins).
        """
        for entry in reversed(self._assumptions):
            if entry["statement"] == predicate_name:
                return entry["active"] and entry["confidence"] >= self.HELD_THRESHOLD
        return False

    def retract(self, predicate_name: str) -> bool:
        """Mark the most recent matching assumption inactive.

        Returns True if a matching active assumption was found. Retraction
        preserves the audit trail — the entry stays in :meth:`report`.
        """
        for entry in reversed(self._assumptions):
            if entry["statement"] == predicate_name and entry["active"]:
                entry["active"] = False
                return True
        return False

    def confidence_of(self, predicate_name: str) -> float | None:
        """Return the confidence of the most recent matching assumption,
        or None if no such assumption was ever added."""
        for entry in reversed(self._assumptions):
            if entry["statement"] == predicate_name:
                return entry["confidence"]
        return None

    def report(self) -> list[dict]:
        """Return a copy of the full assumption log, oldest first.

        Each entry: ``{"id": int, "statement": str, "confidence": float,
        "active": bool}``.
        """
        return [dict(e) for e in self._assumptions]


class RuleEngine:
    """A deterministic forward-chaining rule engine over a facts dict.

    Rules are added as ``(condition, conclusion)`` string pairs:

    - ``condition`` — a Python boolean expression evaluated with the facts
      dict as local variables, e.g. ``"temp > 100 and pressure < 2"``.
    - ``conclusion`` — either an assignment ``"key = <expr>"`` (the expr is
      evaluated over current facts and stored under ``key``) or a bare
      expression, whose value is stored under ``conclusion_<n>``.

    :meth:`infer` iterates all rules to a fixpoint: a rule fires only when
    its condition is true and its conclusion would change the facts, so
    inference always terminates and is order-independent in result (though
    ``conclusion_<n>`` names reflect insertion order).

    Evaluation is sandboxed: no builtins, no dunders, no imports.
    """

    def __init__(self) -> None:
        self._rules: list[tuple[str, str]] = []

    def add_rule(self, condition: str, conclusion: str) -> None:
        """Register a rule.

        Parameters
        ----------
        condition:
            Python expression string over fact names; must evaluate truthy
            for the rule to fire.
        conclusion:
            ``"name = expr"`` assignment or a bare expression.

        Raises
        ------
        ValueError
            On empty strings, obvious sandbox violations, or a condition
            that does not compile.
        """
        for label, text in (("condition", condition), ("conclusion", conclusion)):
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"{label} must be a non-empty string")
            if _FORBIDDEN.search(text):
                raise ValueError(f"{label} contains forbidden tokens: {text!r}")
        try:
            compile(condition, "<condition>", "eval")
        except SyntaxError as exc:
            raise ValueError(f"condition is not a valid expression: {exc}") from exc
        # validate conclusion: assignment target must be a plain identifier
        target, _, expr = conclusion.partition("=")
        expr = expr.strip()
        if expr:
            if not target.strip().isidentifier():
                raise ValueError(f"conclusion target is not a valid name: {target!r}")
            try:
                compile(expr, "<conclusion>", "eval")
            except SyntaxError as exc:
                raise ValueError(f"conclusion expr is not valid: {exc}") from exc
        else:
            try:
                compile(conclusion, "<conclusion>", "eval")
            except SyntaxError as exc:
                raise ValueError(f"conclusion is not a valid expression: {exc}") from exc
        self._rules.append((condition.strip(), conclusion.strip()))

    @staticmethod
    def _eval(expr: str, facts: dict[str, Any]) -> Any:
        env = {k: v for k, v in facts.items() if isinstance(k, str) and k.isidentifier()}
        return eval(compile(expr, "<rule>", "eval"), {"__builtins__": {}}, env)

    @staticmethod
    def _apply(conclusion: str, idx: int, facts: dict[str, Any]) -> bool:
        """Evaluate one conclusion into facts. Returns True if facts changed."""
        target, _, expr = conclusion.partition("=")
        if expr.strip():
            name, rhs = target.strip(), expr.strip()
        else:
            name, rhs = f"conclusion_{idx}", conclusion
        # unknown names in rhs evaluate against current facts
        value = RuleEngine._eval(rhs, facts)
        if facts.get(name, _SENTINEL) != value:
            facts[name] = value
            return True
        return False

    def infer(self, facts: dict) -> dict:
        """Run forward chaining to a fixpoint and return derived facts.

        Parameters
        ----------
        facts:
            Initial facts; keys must be valid identifiers to be visible to
            rules. Not mutated — a new dict is returned.

        Returns
        -------
        dict
            A copy of ``facts`` augmented with every derived conclusion, plus
            a ``"_fired"`` key listing the indices of rules that fired at
            least once (in first-firing order).

        Notes
        -----
        A rule whose condition raises (e.g. a missing name) is treated as
        not firing. Missing names in a conclusion propagate as KeyError-like
        NameError — conclusions may only reference facts that are guaranteed
        present.
        """
        derived: dict[str, Any] = dict(facts)
        fired: list[int] = []
        changed = True
        while changed:
            changed = False
            for i, (cond, concl) in enumerate(self._rules):
                try:
                    if not self._eval(cond, derived):
                        continue
                except (NameError, KeyError, TypeError, AttributeError):
                    continue
                if self._apply(concl, i, derived):
                    if i not in fired:
                        fired.append(i)
                    changed = True
        derived["_fired"] = fired
        return derived


_SENTINEL = object()
